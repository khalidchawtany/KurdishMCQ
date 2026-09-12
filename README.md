# KurdishMCQ — processing and quality-control scripts

Companion code for **KurdishMCQ: A multiple-choice question dataset for the Kurdish language (Sorani dialect)**.

- **Dataset (Mendeley Data, V2, CC BY 4.0):** https://doi.org/10.17632/z8z28jhszp.2
- **Data in Brief article:** (DOI to be added upon publication)
- **OCR training datasets (Hugging Face):**
  - initial synthetic dataset: https://huggingface.co/datasets/khalidchawtany/ckb_base_ocr_ds
  - improved dataset from verified questions: https://huggingface.co/datasets/khalidchawtany/ckb_improved_ocr_dataset
- **OCR fine-tuning:** performed with the [Unsloth](https://github.com/unslothai/unsloth) framework using its public
  [Gemma-3 (4B) notebook](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Gemma3_(4B).ipynb)
  with default hyperparameters, on the datasets above (base model `google/gemma-3-4b-pt`).

## Files

| File | Purpose |
|---|---|
| `dedup.py` | Duplicate removal used during dataset construction: exact match on the whitespace-trimmed (question, options, answer) signature. |
| `gemini_prompt.txt` | The exact instruction used for LLM post-processing of OCR output (spelling correction and question/option separation), as quoted in the article. |
| `audit_dataset.py` | Quality-control audit: blank fields, duplicated options (after Unicode/Kurdish letter-variant normalization), answer-key consistency, repeated stems, identical records. Writes a machine-readable report. |
| `make_figures.py` | Regenerates the article's answer-key and grade distribution figures (Figs. 1–2) from the published JSON. |
| `make_sunburst.py` | Regenerates the article's subject/category sunburst (Fig. 3) from the published JSON. |

## Reproducing the quality-control audit

```bash
python3 audit_dataset.py KurdishMCQ.json report.json
```

Expected result on V2 (17,221 records): no blank fields, no invalid keys, no identical records;
304 three-option records (empty `option D`, faithful to their sources); records flagged
`source_defect: true` are excluded from the duplicated-option check because their duplication is
printed in the original sources (see the dataset's quality-control report).
One record (`KMCQ-08418`) is reported as a duplicated-option item: this is a documented
normalization false positive — its options are "6ˣ" (superscript) and "6x", distinct in the source
and in the data, but collapsed by NFKC normalization.

## License

Code in this repository: MIT. The dataset itself is distributed under CC BY 4.0 via Mendeley Data.
