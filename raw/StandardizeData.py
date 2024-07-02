import json
import pandas as pd
import itertools

### Read fixed paraphrases (i.e. paraphrases without additional text like "Altered sentence:")
first_anno = pd.read_csv("annotation_sentence_fixed.csv",sep=";")

prompt_map = {2:"Zero-Shot",  1:"One-Shot",  0:"Few-Shot", 4:"CoT", 3:"Fine Tuned"}
paraphrases = {}
apt = {}
for _, row in first_anno.iterrows():
    paraphrases[row.Index] = row.Paraphrase
    apt[row.Index] = row.APT


#### First Phase

""" meta
id 106
annotator 5
generation
APT AdditionDeletion
Kind One-Shot
original They had . . .
paraphrase-text They had . . .
annotation
paraphrase True
applied-correctly True
correct-format True
hard False
failure
identical False
other False
nonsense False
otherchange False
additional
morph False
struct False
semantic False
other False
mistaken
morph False
struct False
semantic False
other False
marked-text
start 97
end 109
text additionally """

def get_choice(val, value_check = "Yes"):
    return val["choices"][0] == value_check

def get_choices_add(val):
    res = {}
    key_dict = {"Morpho- and Lexicon-based Changes":"morph","Structure-based Changes":"struct","Semantic-based Changes":"semantic","Others":"others"}
    for a in key_dict:
        if a in val["choices"]:
            res[key_dict[a]] = True
        else:
            res[key_dict[a]] = False
    return res

def get_choices_failure(val):
    res = {}
    key_dict = {"Identical sentences":"identical","otherchange":"otherchange","Nonsense":"nonsense","Other":"other"}
    for a in ["Identical sentences","otherchange","Nonsense","Other"]:
        if a in val["choices"]:
            res[key_dict[a]] = True
        else:
            res[key_dict[a]] = False
    return res

def parse_results(raw_res):
    summary = {}
    for r in raw_res:
        if "from_name" in r:
            match(r["from_name"]):
                case "APT":
                    summary["applied-correctly"] = get_choice(r["value"])
                case "Paraphrase":
                    summary["paraphrase"] = get_choice(r["value"])
                case "FailureReasons":
                    failure_res = get_choices_failure(r["value"])
                    for k in failure_res:
                        summary["failure_"+k] = failure_res[k]
                case "Additional":
                    add = get_choices_add(r["value"])
                    for k in add:
                        summary["add_"+k] = add[k]
                case "Group":
                    add = get_choices_add(r["value"])
                    for k in add:
                        summary["mistaken_"+k] = add[k]
                case "FormatCorrect":
                    summary["correct_format"] = get_choice(r["value"])
                case "Difficulty":
                    summary["hard"] = get_choice(r["value"],"Hard")
                case "type": ## Annotation where change happened
                    summary["start"]=r["value"]["start"]
                    summary["end"] = r["value"]["end"]
                    summary["marked_text"] = r["value"]["text"]
                case _:
                    raise ValueError(f"Failed parsing results: {r['from_name']} in {r}" )
        else:
            pass
    if not "add_morph" in summary:
        add = get_choices_add({"choices":{}})
        for k in add:
                    summary["add_"+k] = add[k]
    if not "mistaken_morph" in summary:
        add = get_choices_add({"choices":{}})
        for k in add:
                    summary["mistaken_"+k] = add[k]
    if not "failure_identical" in summary:
       add = get_choices_failure({"choices":{}})
       for k in add:
            summary["failure_"+k] = add[k] 

    return summary

def raw_to_dict(raw_annotation):
    results = parse_results(raw_annotation["annotations"][0]["result"]) 
    data = raw_annotation["data"]
    d = {
        "annotator" : data["Annotator"],
        "apt": data["APT"],
        #"id": raw_annotation["id"],
        "index": data["Index"],
        "kind" : data["Kind"],
        "paraphrase-text": data["Paraphrase"],
        "original": data["Original"],
        "paraphrase_fixed" : paraphrases[data["Index"]],
    }
    for k in results:
        d[k] = results[k]
    return d

annotation_json = {}
with open("result_first.json") as f:
    annotation_json = json.load(f)

annotation_list = []
for annotation_raw in annotation_json:
    anno_dict = raw_to_dict(annotation_raw)
    annotation_list.append(anno_dict)

df = pd.DataFrame(annotation_list)
df["golden_example"] = df["index"]>100000
df.to_csv("first_phase_out.csv",sep=";")

#### Second Phase
annotation_json = {}
with open("result_second.json") as f:
    annotation_json = json.load(f)
    

def get_places(ranked_list):
    places = {i:-1 for i in range(5)}
    ranking = 1
    for sub_list in ranked_list.values():
        for i in range(5):
            if str(i) in sub_list:
                places[i] = ranking
        if sub_list: #ignores empty list for ranking
            ranking +=1
    return places

data = {}
for task in annotation_json:
    annotation = task['annotations']
    id = task['data']['id'] #id of task, exists 5 times each (for the different annotators)
    ranked_list = annotation[0]['result'][0]['value']['ranker']
    annotator = task['data']['annotator']
    if not id in data:
        data[id] = {}
        data[id]["meta"] = {}
        data[id]["meta"]["id"] = id
        data[id]["meta"]["annotators"] = []
        data[id]["original"] = task['data']['original']
        data[id]["rankings"] = []
    places = get_places(ranked_list)
    data[id]["rankings"].append(places)
    data[id]["meta"]["annotators"].append(annotator)
    para_list = task['data']['List']
    #for para in para_list:
    #    paraphrases[id*10+para['id']] = para["body"]
    data[id]["paraphrase_prompts"] = [p['id'] for p in para_list]

        
# meta
## id 100
## annotators [8,7,11,12,14]
# original They had . . .
# pairwise
## chosen They had . . .
### ranks [1,1,2,3,1]
### id 106
## rejected Adding that . . .
### id 104
#### ranks [3,4,4,5,4]    
#

output = []

id = 0
# Pairwise comparison
for id in data:
    for (para_a,para_b) in itertools.combinations(data[id]["paraphrase_prompts"],2):
        one_pair={}
        one_pair["meta"] = {}
        one_pair["meta"]["id"] = id
        one_pair["meta"]["annotators"] = data[id]["meta"]["annotators"]
        one_pair["meta"]["APT"] = apt[id*10]  #corresponds to the FewShot entry which of course has the same APT as the other types
        one_pair["original"] = data[id]["original"]
        para_a_info = {
            "id" :para_a + id*10,
            "text":paraphrases[para_a + id*10],
            "ranks" : [r[para_a] for r in data[id]["rankings"]] 
        }
        para_b_info = {
            "id" :para_b + id*10,
            "text":paraphrases[para_b + id*10],
            "ranks" : [r[para_b] for r in data[id]["rankings"]] 
        }
        if sum(para_a_info["ranks"])<sum(para_b_info["ranks"]): #The comparison is the same as comparing mean rank as they have the same length
            one_pair["chosen"] = para_a_info
            one_pair["rejected"] = para_b_info
        else:
            one_pair["chosen"] = para_b_info
            one_pair["rejected"] = para_a_info
        output.append(one_pair)

with open("second_phase_out.json","w") as f:
    json.dump(output,f)