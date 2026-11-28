# TrustLayer Dataset Card

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
| SMS Spam Collection (UCI) | 1030 | ham -> safe, spam -> scam | CC BY 4.0 | Almeida, T. and Hidalgo, J. (2011). SMS Spam Collection [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CC84 |
| deepset/prompt-injections (Hugging Face) | 642 | injection label -> prompt_injection, other -> safe | Apache 2.0 | deepset, https://huggingface.co/datasets/deepset/prompt-injections |
| Own examples (this project) | 62 | written directly with the three labels | CC BY 4.0 | Ramya Sree Nagarajan |
| Own hard set (this project) | 26 | written directly with the three labels | CC BY 4.0 | Ramya Sree Nagarajan |

## Changes made to the public data
- Removed empty rows and duplicate messages
- Collapsed extra whitespace
- Relabeled to the three TrustLayer labels
- Sampled up to 600 of the SMS `safe` rows to reduce imbalance
- Dropped rows that did not match my label definitions (see [AUDIT.md](AUDIT.md))
- Detected the language of every public row automatically

## Final size
- Total rows: 1760
- By label: safe 1027, scam 462, prompt_injection 271
- Languages: english 1308, german 252, other_or_unknown 170, hinglish 15, tamil_translit 15
- Average length in characters: safe 70, scam 136, prompt_injection 198

## Splits
Public rows were split 70 / 15 / 15 into train, validation and test, stratified by label. A separate hand-written hard set was kept out of the others.
- train 1212, validation 261, test 261, hard 26
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
- Public data makes up about 95% of the rows and my own examples about 5%, so overall scores mostly reflect UK and Singapore SMS and chatbot-style attacks.
- The SMS "spam" label includes advertising that does not match the `scam` definition. The audit removed many such rows, but some probably remain.
- deepset `safe` rows are mostly chatbot questions, not emails or SMS.
- Message length differs by label (average characters: safe 70, scam 136, prompt_injection 198), so a model could learn length instead of intent.
- Hinglish and Tanglish are scarce (15 and 15 rows in total), so no accuracy figure for either language is reliable.
- The hard set has 26 rows, so each prediction moves a score by several percentage points.
- Injection and safe "twin" pairs may fall in different splits, which can make the test set slightly easier.
- Own examples were written by one person, so they reflect one writer's style.
- Public language labels come from an automatic detector. Hinglish, Tanglish and short messages are often mislabelled.

## Privacy and ethics
- All own examples use invented names, numbers, links and addresses.
- No real personal data, account numbers, OTPs or private messages are included.
- This dataset is for building defences. It is not meant for crafting attacks.
