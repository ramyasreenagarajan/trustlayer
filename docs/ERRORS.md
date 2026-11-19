# Known Errors and Limitations (baseline model)

# Known Errors and Limitations (baseline model)

Model: TF-IDF (word+char) + Linear SVM, C=0.3. Scores are in [results.md](results.md).

## Test set (296 rows, 16 mistakes)
- Most mistakes come from labels in the public data that do not match this project's definitions, not from the model.
- 8 were SMS "spam" labelled scam: 5 are not scams under my definition (a classified ad, a chat-line promo, a personal reply) and 3 are premium-rate promos.
- 5 were deepset "injection" rows that are harmless prompts (for example "generate c++" or "tell me a joke").
- 1 real injection written in Hindi with Latin letters was missed, 1 real injection was flagged as a scam, and 1 political question was flagged as an injection.
- Conclusion: the test score (macro F1 0.93) understates the model on real attacks and is not a clean measure.

## Hard set (26 rows, 10 mistakes, clean labels)
- 4 of 9 honest safe messages were flagged as scams. All 4 mention OTP, PIN, a bank or "URGENT". The training data has few honest bank-style notices.
- 3 of 9 scams were missed. They were written as a personal story or a polite official request, with no links or keywords.
- 6 of 10 mistakes involve Hinglish or Tanglish, but each language has only 8 rows in test and hard combined, so this is not a measured rate.
- Both missed injections were Hinglish. All English and Tanglish injections were caught, possibly because they contain words like "assistant" or "AI tool".

## What I plan to do about it
- Add more honest bank, OTP and urgent-notice messages as safe examples (Week 4).
- Add more story-style scams and more Hinglish and Tanglish rows for every label (Week 4).
- Audit a random sample of the public data labels with a written rule, and rescore all models on the same data (Week 4).
- Test injections that avoid the words "AI" and "assistant" (Week 7).
- Tune the alert threshold on the validation set (Week 5).

## Things not to conclude
- Do not read the test score as real-world performance.
- The language column for public data is assumed to be English, which is not always true.
- Results for Hinglish and Tanglish rest on 8 rows each.
- The hard set has 26 rows, so its score has a wide range (0.40 to 0.81).

## What it gets wrong
1. (Pattern 1, with a count and an example, e.g. "Scams without links or keywords are often labeled safe (n of m hard-set scams).")
2. (Pattern 2)
3. (Pattern 3)

## Why
- (Cause 1, e.g. "The training data has few scams written as personal stories.")
- (Cause 2)

## What I plan to do about it
- (Fix 1 and when)
- (Fix 2 and when)

## Things not to conclude
- Scores on the public test set are higher than on my own rows, so they overstate real-world performance.
- Hinglish and Tanglish results are based on very few rows and are uncertain.