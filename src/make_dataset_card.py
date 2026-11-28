import sys
import pandas as pd
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
PROC = Path("data/processed")
sp = {n: pd.read_csv(PROC / f"{n}.csv") for n in ["train", "val", "test", "hard"]}
al = pd.concat(sp.values(), ignore_index=True)

total = len(al)
src = al["source"].astype(str)
n_sms = int((src == "uci_sms_spam").sum())
n_ds = int((src == "deepset_prompt_injections").sum())
n_own = int((src == "own").sum())
n_hard = int((src == "own_hard").sum())
pub_pct = round(100 * (n_sms + n_ds) / total)
own_pct = round(100 * (n_own + n_hard) / total)
lab = al["label"].value_counts()
lang = al["language"].value_counts()
length = al.groupby("label")["text"].apply(lambda s: round(s.str.len().mean()))
n_h, n_t = int(lang.get("hinglish", 0)), int(lang.get("tamil_translit", 0))
sizes = {k: len(v) for k, v in sp.items()}

card = f"""# TrustLayer Dataset Card

## Summary
A labeled text dataset for three classes: `safe`, `scam` and `prompt_injection`. It combines two public datasets, cleaned after a label audit ([AUDIT.md](AUDIT.md)), with hand-written examples in English, Hinglish and Tamil written in English letters (Tanglish).

## Labels
See [labeling_guide.md](labeling_guide.md). Short version:
- `safe`: ordinary message with no attempt to deceive or manipulate
- `scam`: tries to trick a person into paying, sharing secrets or clicking
- `prompt_injection`: hidden instructions aimed at an AI assistant

## Sources

| Source | Rows in the final dataset | Label mapping | License | Credit |
|---|---|---|---|---|
| SMS Spam Collection (UCI) | {n_sms} | ham -> safe, spam -> scam | CC BY 4.0 | Almeida, T. and Hidalgo, J. (2011). SMS Spam Collection [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CC84 |
| deepset/prompt-injections (Hugging Face) | {n_ds} | injection label -> prompt_injection, other -> safe | Apache 2.0 | deepset, https://huggingface.co/datasets/deepset/prompt-injections |
| Own examples (this project) | {n_own} | written directly with the three labels | CC BY 4.0 | Ramya Sree Nagarajan |
| Own hard set (this project) | {n_hard} | written directly with the three labels | CC BY 4.0 | Ramya Sree Nagarajan |

## Changes made to the public data
- Removed empty rows and duplicate messages
- Collapsed extra whitespace
- Relabeled to the three TrustLayer labels
- Sampled up to 600 of the SMS `safe` rows to reduce imbalance
- Dropped rows that did not match my label definitions (see [AUDIT.md](AUDIT.md))
- Detected the language of every public row automatically

## Final size
- Total rows: {total}
- By label: safe {int(lab.get("safe", 0))}, scam {int(lab.get("scam", 0))}, prompt_injection {int(lab.get("prompt_injection", 0))}
- Languages: english {int(lang.get("english", 0))}, german {int(lang.get("german", 0))}, other_or_unknown {int(lang.get("other_or_unknown", 0))}, hinglish {n_h}, tamil_translit {n_t}
- Average length in characters: safe {length.get("safe", 0)}, scam {length.get("scam", 0)}, prompt_injection {length.get("prompt_injection", 0)}

## Splits
Public rows were split 70 / 15 / 15 into train, validation and test, stratified by label. A separate hand-written hard set was kept out of the others.
- train {sizes["train"]}, validation {sizes["val"]}, test {sizes["test"]}, hard {sizes["hard"]}
- My own rows are split per label and language so each appears in every set where possible.
- No exact duplicate text appears in more than one set (checked by script).
- Rule: the test and hard sets are used only for reporting, never for tuning.

## How the dataset is built
Raw public files are not stored in this repository. The steps are:
1. Download the SMS Spam Collection and deepset files into `data/raw/`.
2. Run `py src/prepare_public_data.py` (cleans and relabels the public data).
3. Audit the public labels as described in [AUDIT.md](AUDIT.md). The review sheets are kept locally and are not published, so the exact dataset cannot be rebuilt from this repository alone.
4. Run `py src/apply_audit.py`, then `py src/build_dataset.py`, then `py src/split_dataset.py`.

## Known limitations
- Public data makes up about {pub_pct}% of the rows and my own examples about {own_pct}%, so overall scores mostly reflect UK and Singapore SMS and chatbot-style attacks.
- The SMS "spam" label includes advertising that does not match the `scam` definition. The audit removed many such rows, but some probably remain.
- deepset `safe` rows are mostly chatbot questions, not emails or SMS.
- Message length differs by label (average characters: safe {length.get("safe", 0)}, scam {length.get("scam", 0)}, prompt_injection {length.get("prompt_injection", 0)}), so a model could learn length instead of intent.
- Hinglish and Tanglish are scarce ({n_h} and {n_t} rows in total), so no accuracy figure for either language is reliable.
- The hard set has {n_hard} rows, so each prediction moves a score by several percentage points.
- Injection and safe "twin" pairs may fall in different splits, which can make the test set slightly easier.
- Own examples were written by one person, so they reflect one writer's style.
- Public language labels come from an automatic detector. Hinglish, Tanglish and short messages are often mislabelled.

## Privacy and ethics
- All own examples use invented names, numbers, links and addresses.
- No real personal data, account numbers, OTPs or private messages are included.
- This dataset is for building defences. It is not meant for crafting attacks.
"""

Path("docs/DATASET.md").write_text(card, encoding="utf-8")
print("Saved docs/DATASET.md")
print(f"total {total} | sms {n_sms} | deepset {n_ds} | own {n_own} | own_hard {n_hard}")
print("labels:", lab.to_dict())
print("languages:", lang.to_dict())
print("sizes:", sizes)
print("average length:", length.to_dict())