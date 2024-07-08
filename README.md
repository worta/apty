[![arXiv](https://img.shields.io/badge/arXiv-2310.14863-b31b1b.svg)](https://arxiv.org/abs/2407.02302)
[![HuggingFace Datasets](https://img.shields.io/badge/🤗-Datasets-ffce1c.svg)](https://huggingface.co/datasets/worta/apty)

# APTY
Dataset from the paper "Towards Human Understanding of Paraphrase Types in ChatGPT" (https://arxiv.org/abs/2407.02302). It consists of two parts: The first part (APTY<sub>base</sub>) contains annotated paraphrases with specific atomic paraphrase types based on the ETPC dataset. The second part (APTY<sub>ranked</sub>) consists of human preferences ranking paraphrases with specific atomic paraphrase types.

The code to generate the paraphrase candidates can be found at https://github.com/worta/generate_apt_paraphrases. The generation uses ChatGPT. The dataset is also available at https://huggingface.co/datasets/worta/apty.




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
