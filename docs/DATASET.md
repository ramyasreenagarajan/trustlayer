# TrustLayer Dataset Card

## Summary
A labeled text dataset for three classes: `safe`, `scam` and `prompt_injection`. It combines two public datasets with hand-written examples in English, Hinglish and Tamil written in English letters (Tanglish).

## Labels
See [labeling_guide.md](labeling_guide.md). Short version:
- `safe`: ordinary message with no attempt to deceive or manipulate
- `scam`: tries to trick a person into paying, sharing secrets or clicking
- `prompt_injection`: hidden instructions aimed at an AI assistant

## Sources

| Source | Rows used | Label mapping | License | Credit |
|---|---|---|---|---|
| SMS Spam Collection (UCI) | (n) after cleaning and sampling | ham -> safe, spam -> scam | CC BY 4.0 | Almeida, T. and Hidalgo, J. (2011). SMS Spam Collection [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CC84 |
| deepset/prompt-injections (Hugging Face) | (n) | injection label -> prompt_injection, other -> safe | Apache 2.0 | deepset, https://huggingface.co/datasets/deepset/prompt-injections |
| Own examples (this project) | (n) | written directly with the three labels | CC BY 4.0 | Ramya Sree Nagarajan |
| Own hard set (this project) | (n) | written directly with the three labels | CC BY 4.0 | Ramya Sree Nagarajan |

## Changes made to the public data
- Removed empty rows and duplicate messages
- Collapsed extra whitespace
- Relabeled to the three TrustLayer labels
- Sampled 600 of the SMS `safe` rows to reduce imbalance (all SMS `scam` rows kept)
-dropped rows that did not match my label definitions (see AUDIT.md) and detected languages automatically

## Final size
- Total rows: (n)
- By label: safe (n), scam (n), prompt_injection (n)
- Languages: english (n), hinglish (n), tamil_translit (n)

## Splits
Stratified 70 / 15 / 15 into train, validation and test, plus a separate hand-written hard set.
- train (n), val (n), test (n), hard (n)
- My own rows are split per label and language so each appears in every set where possible.
- No exact duplicate text appears in more than one set (checked by script).
- Rule: test and hard sets are used only for reporting, never for tuning.

## How the dataset is rebuilt
Raw public files are not stored in this repository. To rebuild:
1. Download the SMS Spam Collection and deepset files into `data/raw/` (see the steps in the README).
2. Run, in order:
   ```
   py src/prepare_public_data.py
   py src/build_dataset.py
   py src/split_dataset.py
   ```

## Known limitations
- Public data is about 95% of the rows. Own data is a small share, so overall scores mostly reflect UK/Singapore SMS and chatbot-style attacks.
- The SMS "spam" label includes plain advertising that may not match the `scam` definition.
- deepset `safe` rows are mostly chatbot questions, not emails or SMS.
- Message length differs by label (safe averages (n) characters, scam (n), prompt_injection (n)), so a model could learn length instead of intent.
- Hinglish and Tanglish rows are few (about (n) each), so scores for those languages are uncertain.
- Hard set is small (n rows), so each prediction moves a score by several percentage points.
- Injection and safe "twin" pairs may fall in different splits, which can make the test set slightly easier.
- Own examples were written by one person, so they reflect one writer's style.
-Public language labels come from an automatic detector. Hinglish, Tanglish and short messages are often mislabelled.

## Privacy and ethics
- All own examples use invented names, numbers, links and addresses.
- No real personal data, account numbers, OTPs or private messages are included.
- This dataset is for building defences. It is not meant for crafting attacks.