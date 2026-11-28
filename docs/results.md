# Results Log

Every number here comes from a script in `src/`. Two generations of numbers appear, and they **must not be compared with each other**:
- **v1, before the label audit:** 1,990 rows, split into train 1,373, validation 295, test 296 and a hard set of 26.
- **v2, after the label audit:** 1,760 rows, split into train 1,212, validation 261, test 261 and a hard set of 26.

The hard set (26 hand-written rows) was not changed by the audit. See [AUDIT.md](AUDIT.md) and [DATASET.md](DATASET.md).

## v1: model comparison on the validation set (295 rows, before the audit)
Macro F1 is the average F1 over the three labels. The validation set has only 42 injection rows, so differences under about 0.01 to 0.02 are within noise.

| Model | Macro F1 | F1 safe | F1 scam | F1 injection | Recall scam | Recall injection |
|---|---|---|---|---|---|---|
| SVM, char, C=1 | 0.956 | 0.964 | 0.975 | 0.929 | 0.97 | 0.929 |
| LR, word+char, C=3 | 0.952 | 0.960 | 0.975 | 0.920 | 0.98 | 0.952 |
| SVM, char, C=0.3 | 0.950 | 0.961 | 0.975 | 0.914 | 0.97 | 0.881 |
| **SVM, word+char, C=0.3 (chosen)** | 0.948 | 0.958 | 0.970 | 0.916 | 0.97 | 0.905 |
| LR, char, C=3 | 0.946 | 0.957 | 0.975 | 0.905 | 0.98 | 0.905 |
| SVM, word+char, C=1 | 0.943 | 0.951 | 0.960 | 0.918 | 0.96 | 0.929 |
| LR, word+char, C=1 | 0.941 | 0.954 | 0.975 | 0.894 | 0.98 | 0.905 |
| SVM, word+char, C=0.1 | 0.939 | 0.955 | 0.975 | 0.886 | 0.98 | 0.833 |
| LR, char, C=1 | 0.936 | 0.947 | 0.965 | 0.894 | 0.97 | 0.905 |
| SVM, word, C=1 | 0.933 | 0.940 | 0.950 | 0.907 | 0.96 | 0.929 |
| SVM, char, C=0.1 | 0.930 | 0.949 | 0.970 | 0.872 | 0.96 | 0.810 |
| LR, word, C=3 | 0.921 | 0.930 | 0.946 | 0.886 | 0.96 | 0.929 |
| SVM, word, C=0.3 | 0.916 | 0.931 | 0.950 | 0.867 | 0.96 | 0.857 |
| LR, word, C=1 | 0.905 | 0.919 | 0.932 | 0.864 | 0.96 | 0.905 |
| SVM, word, C=0.1 | 0.898 | 0.922 | 0.937 | 0.835 | 0.96 | 0.786 |
| Keyword rules | 0.341 | 0.704 | 0.228 | 0.091 | 0.13 | 0.048 |

Chosen baseline: SVM with word and character features, C=0.3. The best validation score was SVM with character features, C=1 (0.956), but the top five models are within 0.01 of each other. The logistic regression with word and character features (C=3) had the best attack recall (scam 0.98, injection 0.95) and would have been preferred by my tie-break rule. I kept the SVM because I had already looked at its test and hard-set scores, and switching afterwards would weaken the test set. Every learned model beat the keyword rules by a wide margin. The rules are precise when they fire (precision 0.93 for scam and 1.00 for injection) but catch almost nothing.

## v1: scores for the chosen baseline (before the audit)

| Model | Set | Rows | Macro F1 | 95% range | Recall scam | Recall injection |
|---|---|---|---|---|---|---|
| Keyword rules | Validation | 295 | 0.341 | 0.28 to 0.40 | 0.13 | 0.05 |
| Keyword rules | Test | 296 | 0.327 | 0.28 to 0.38 | 0.13 | 0.02 |
| Keyword rules | Hard set | 26 | 0.267 | 0.11 to 0.41 | 0.00 | 0.25 |
| Keyword rules | Own rows (test + hard) | 36 | 0.426 | 0.22 to 0.59 | 0.23 | 0.30 |
| SVM, word+char, C=0.3 | Validation | 295 | 0.948 | 0.91 to 0.97 | 0.97 | 0.90 |
| SVM, word+char, C=0.3 | Test | 296 | 0.934 | 0.90 to 0.96 | 0.92 | 0.83 |
| SVM, word+char, C=0.3 | Hard set | 26 | 0.627 | 0.40 to 0.81 | 0.56 | 0.75 |
| SVM, word+char, C=0.3 | Own rows (test + hard) | 36 | 0.734 | 0.58 to 0.86 | 0.69 | 0.80 |

Accuracy by language (test + hard, SVM): English 0.93 (306 rows), Tanglish 0.75 (8 rows), Hinglish 0.50 (8 rows). The last two are too few rows to trust.

Recall by true label (test + hard): safe 0.969 (163 rows), scam 0.891 (110 rows), prompt injection 0.816 (49 rows).

On the test set by source: SMS 0.957 accuracy (186 rows), deepset 0.920 (100 rows), own examples 1.000 (10 rows).

Observations:
- The validation and test scores agree (0.948 and 0.934), so there was no sign of overfitting to the validation set.
- Test (0.934, range 0.90 to 0.96) and hard (0.627, range 0.40 to 0.81) do not overlap. Messages written without obvious keywords are much harder than the public data.
- The hard set has 26 rows, so each prediction moves its score by about 4 percentage points.

## v1: mistakes of the chosen baseline
The first error analysis is in [ERRORS.md](ERRORS.md).
- Test set, 16 mistakes: scam labelled safe 8, injection labelled safe 6, injection labelled scam 1, safe labelled injection 1.
- Hard set, 10 mistakes: safe labelled scam 4, scam labelled safe 3, injection labelled safe 2, scam labelled injection 1.

## v1: transformer, first run (validation set only)
Model: distilbert-base-multilingual-cased, 4 epochs, learning rate 2e-5, batch size 16, maximum length 128, class-weighted loss, trained on the 1,373 v1 training rows. Validation macro F1 by epoch: 0.889, 0.961, 0.964, 0.967 (best epoch 4). Training took 1 minute 47 seconds on a Tesla T4. The TF-IDF SVM scored 0.948 on the same validation set. The difference is within noise, and the transformer's score was also chosen as the best epoch on that same set. This model was not scored on the test or hard sets, and it was not trained on the audited data.

## Which model is deployed
The deployed model is TF-IDF (word and character features) with a Linear SVM and sigmoid calibration, trained on the training and validation rows. Reasons:
- The saved DistilBERT model is about 542 MB, which is more than the 512 MB of memory on the free hosting plan.
- I have no evidence that a transformer is better on the hard set, because the transformer comparison has not been repeated on the audited data.
- Explanations always come from hand-written rules and the TF-IDF model, so they stay fast and checkable.

## Alert thresholds (v2)
Rule, written before looking at the numbers:
- risk = 1 minus the model's probability of "safe".
- T_SUSPICIOUS is the highest threshold at which at least 95% of validation attacks are flagged.
- T_ATTACK is the lowest threshold at which at least 95% of flagged validation rows are real attacks, but never less than T_SUSPICIOUS + 0.2 and never above 0.95.
- Thresholds are chosen on validation rows only, using a model trained on the train split only. Test and hard are reported once and never used to adjust anything.

Chosen thresholds (from `models/deploy/thresholds.json`): suspicious 0.375, attack 0.575. The deployed model file is 2.7 MB.

## Not yet measured on the audited data
- Test, hard-set and own-row scores of the deployed model
- The transformer comparison (DistilBERT and MuRIL) on the audited splits
- What the chosen thresholds catch on the test and hard sets
- Memory and speed of the deployed model on the free host
- How accurate the warning-sign explanations are
- Hinglish and Tanglish accuracy (too few rows)