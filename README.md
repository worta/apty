[![arXiv](https://img.shields.io/badge/arXiv-2310.14863-b31b1b.svg)](https://arxiv.org/abs/2407.02302)
[![HuggingFace Datasets](https://img.shields.io/badge/🤗-Datasets-ffce1c.svg)](https://huggingface.co/datasets/worta/apty)

# APTY
Dataset from the paper "Towards Human Understanding of Paraphrase Types in ChatGPT" (https://arxiv.org/abs/2407.02302). It consists of two parts: The first part (APTY<sub>base</sub>) contains annotated paraphrases with specific atomic paraphrase types based on the ETPC dataset. The second part (APTY<sub>ranked</sub>) consists of human preferences ranking paraphrases with specific atomic paraphrase types.

The code to generate the paraphrase candidates can be found at https://github.com/worta/generate_apt_paraphrases. The generation uses ChatGPT. The dataset is also available at https://huggingface.co/datasets/worta/apty.


# Dataset
## APTY<sub>base</sub>

| Column Name            | Data Type        | Additional Info                    |
|------------------------|------------------|------------------------------------|
| annotator              | int64            | Id of annotator                    |
| apt                    | string           |  Atomic Paraphrase Type            |
| index                  | int64            | Can join with APTY-ranked paraphrases           |
| kind                   | int64            | Kind of generation                 |
| paraphrase-text        | string           | Text of paraphrase candidate                 |
| original               | string           | Base sentence                         |
| paraphrase_fixed       | string           | Paraphrase-text with generation artifacts removed (like "altered text:")      |
| paraphrase             | bool             | Semantically equivalent?      |
| applied-correctly      | bool             | Is the APT applied correctly?                         |
| failure_identical      | bool             | Failure reason: Identical sentences            |
| failure_otherchange    | bool             | Failure reason: Other APT applied                         |
| failure_nonsense       | bool             | Failure reason: Paraphrase is nonsense                         |
| failure_other          | bool             | Failure reason: Other reasons                          |
| correct_format         | bool             | Does the paraphrase contain undesired artifacts, see paraphrase_fixed                         |
| hard                   | bool             | Does the annotator judge the application of the APT as hard        |
| add_morph              | bool             | Additional change besides desired: Morph.                         |
| add_struct             | bool             | Additional change besides desired: Struct.                           |
| add_semantic           | bool             | Additional change besides desired: Semantic                         |
| add_others             | bool             | Additional change besides desired: Other                          |
| mistaken_morph         | bool             | Failure other APT applied: Morph.                         |
| mistaken_struct        | bool             | Failure other APT applied: Struct.                          |
| mistaken_semantic      | bool             | Failure other APT applied: Semantic                           |
| mistaken_other      | bool             | Failure other APT applied: Other                           |
| start                  | int          |  Start position of change (in paraphrase-text)   |
| end                    | int         |  End position of change (in paraphrase-text)    |
| marked_text            | string           |  Text of change                                 |
| golden_example         | bool             |  Is golden example (i.e. paraphrase was generated manually)                                  |

## APTY<sub>ranked</sub>
| Field Name             | Data Type        | Additional Info                    |
|------------------------|------------------|------------------------------------|
| meta.id                | int              | Id                                   |
| meta.annotators        | list of ints     | List of annotators rating this sentence      |
| meta.APT               | string           | Desired APT                                   |
| original               | string           | Original sentence                                   |
| chosen.id              | int              |  ID of paraphrase, can join with APTY_base  |
| chosen.text            | string           |  Text of preferred paraprhase                                  |
| chosen.ranks           | list of ints     |  Ranks given by annotators, in order                                  |
| rejected.id            | int              |  ID of paraphrase, can join with APTY_base                                  |
| rejected.text          | string           |  Text of non-preferred paraphrase                                  |
| rejected.ranks         | list of ints     |  Ranks given by annotators in order                                  |

# Citation
```bib
@misc{meier2024humanunderstandingparaphrasetypes,
      title={Towards Human Understanding of Paraphrase Types in ChatGPT}, 
      author={Dominik Meier and Jan Philip Wahle and Terry Ruas and Bela Gipp},
      year={2024},
      eprint={2407.02302},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2407.02302}, 
}
```
