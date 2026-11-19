# Results Log

## Week 3, Day 1: baselines on the validation set
| Model | Macro F1 | safe F1 | scam F1 | injection F1 | Notes |
|---|---|---|---|---|---|
| Always 'safe' | (n) | (n) | 0 | 0 | Floor |
| Keyword rules | (n) | (n) | (n) | (n) | (what stood out) |

## Week 3, Day 2: TF-IDF + Logistic Regression (validation set)

| Setting | Macro F1 (val) |
|---|---|
| word, C=0.3 | (n) |
| word, C=1 | (n) |
| word, C=3 | (n) |
| word, C=10 | (n) |
| char, C=0.3 | (n) |
| char, C=1 | (n) |
| char, C=3 | (n) |
| char, C=10 | (n) |

Best: (kind, C), macro F1 (n)
Per label F1: safe (n), scam (n), prompt_injection (n)

Observations:
- Compared with the keyword rules (macro F1 n): (better/worse and why)
- Weakest label: (label), because (reason)
- Top features look like: (meaningful words / source fingerprints, give examples)

## Week 3, Day 3: model comparison (validation set)

| Model | Macro F1 | F1 safe | F1 scam | F1 injection | Recall scam | Recall injection |
|---|---|---|---|---|---|---|
| rules | (n) | (n) | (n) | (n) | (n) | (n) |
| (best SVM) | (n) | (n) | (n) | (n) | (n) | (n) |
| (best LR) | (n) | (n) | (n) | (n) | (n) | (n) |

Chosen baseline: (model name) because (reason: score, recall, simplicity).
Notes: (what surprised you; whether differences are bigger than noise)

## Week 3, Day 4: final scores (chosen model: (name))

| Set | Rows | Macro F1 | 95% range |
|---|---|---|---|
| Validation | (n) | (n) | - |
| Test | (n) | (n) | (n) to (n) |
| Hard | (n) | (n) | (n) to (n) |
| Own rows only (test + hard) | (n) | (n) | (n) to (n) |

Recall by true label (test + hard): safe (n), scam (n), prompt_injection (n)

By language: english (n rows, accuracy n), hinglish (n rows, accuracy n), tamil_translit (n rows, accuracy n)

Observations:
- Gap between test and hard: (n points), meaning (your interpretation)
- Model is weakest on: (label / language / source)
- Languages with too few rows to measure: (list)
- No changes were made to the model after seeing these scores: (yes / describe)

## Week 3, Day 5: error analysis

Mistakes reviewed: (n) from the test set, (n) from the hard set.

| Cause | Test | Hard | Example number |
|---|---|---|---|
| label_noise | (n) | (n) | (e.g. test 3) |
| no_keywords | (n) | (n) | |
| disguised | (n) | (n) | |
| language | (n) | (n) | |
| style_fingerprint | (n) | (n) | |
| scam_words_honest | (n) | (n) | |
| ambiguous | (n) | (n) | |
| other | (n) | (n) | |

Most common wrong prediction (true -> predicted): (e.g. scam -> safe, n times)
Most dangerous misses (attacks labeled safe): (n); examples: (short descriptions)