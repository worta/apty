[![arXiv](https://img.shields.io/badge/arXiv-2310.14863-b31b1b.svg)](https://arxiv.org/abs/2407.02302)
[![HuggingFace Datasets](https://img.shields.io/badge/🤗-Datasets-ffce1c.svg)](https://huggingface.co/datasets/worta/apty)

# APTY
Dataset from the paper "Towards Human Understanding of Paraphrase Types in ChatGPT" (https://arxiv.org/abs/2407.02302). It consists of two parts: The first part (APTY<sub>base</sub>) contains annotated paraphrases with specific atomic paraphrase types based on the ETPC dataset. The second part (APTY<sub>ranked</sub>) consists of human preferences ranking paraphrases with specific atomic paraphrase types.

The code to generate the paraphrase candidates can be found at https://github.com/worta/generate_apt_paraphrases. The generation uses ChatGPT. The dataset is also available at https://huggingface.co/datasets/worta/apty.


# Dataset
APTY<sub>base</sub>

| Column Name            | Data Type        | Additional Info                    |
|------------------------|------------------|------------------------------------|
| annotator              | int64            |                                    |
| apt                    | string           |  Atomic Paraphrase Type            |
| index                  | int64            |                                    |
| kind                   | int64            |                                    |
| paraphrase-text        | string           |                                   |
| original               | string           |                          |
| paraphrase_fixed       | string           | Paraphrase-text with generation artificats removed (like "altered text:")      |
| paraphrase             | bool             | Semantically equivalent?      |
| applied-correctly      | bool             |                          |
| failure_identical      | bool             |                           |
| failure_otherchange    | bool             |                          |
| failure_nonsense       | bool             |                          |
| failure_other          | bool             |                           |
| correct_format         | bool             |                          |
| hard                   | bool             |                          |
| add_morph              | bool             |                          |
| add_struct             | bool             |                          |
| add_semantic           | bool             |                          |
| add_others             | bool             |                          |
| mistaken_morph         | bool             |                          |
| mistaken_struct        | bool             |                           |
| mistaken_semantic      | bool             |                           |
| start                  | float64          |  Start position of change (in paraphrase-text)   |
| end                    | float64          |  End position of change (in paraphrase-text)    |
| marked_text            | string           |  Text of change                                 |
| golden_example         | bool             |  Is golden example (i.e. paraphrase was generated manually)                                  |

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
