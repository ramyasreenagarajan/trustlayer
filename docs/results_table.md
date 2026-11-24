| Model | Set | Rows | Macro F1 | 95% range | Recall scam | Recall injection |
|---|---|---|---|---|---|---|
| Keyword rules | Validation | 295 | 0.341 | 0.28 to 0.40 | 0.13 | 0.05 |
| Keyword rules | Test | 296 | 0.327 | 0.28 to 0.38 | 0.13 | 0.02 |
| Keyword rules | Hard set | 26 | 0.267 | 0.11 to 0.41 | 0.0 | 0.25 |
| Keyword rules | Own rows (test + hard) | 36 | 0.426 | 0.22 to 0.59 | 0.23 | 0.3 |
| TF-IDF (word+char) + Linear SVM, C=0.3 | Validation | 295 | 0.948 | 0.91 to 0.97 | 0.97 | 0.9 |
| TF-IDF (word+char) + Linear SVM, C=0.3 | Test | 296 | 0.934 | 0.90 to 0.96 | 0.92 | 0.83 |
| TF-IDF (word+char) + Linear SVM, C=0.3 | Hard set | 26 | 0.627 | 0.40 to 0.81 | 0.56 | 0.75 |
| TF-IDF (word+char) + Linear SVM, C=0.3 | Own rows (test + hard) | 36 | 0.734 | 0.58 to 0.86 | 0.69 | 0.8 |

| Language | Rows | Accuracy | Note |
|---|---|---|---|
| english | 306 | 0.93 |  |
| hinglish | 8 | 0.50 | too few rows to trust |
| tamil_translit | 8 | 0.75 | too few rows to trust |

## Results (Week 4)

Measured on splits made after a label audit of the public data ([docs/AUDIT.md](docs/AUDIT.md)). All three models were trained on the same training split and scored on the same data. These numbers are not comparable with the earlier baseline in [docs/results_table_v1_before_audit.md](docs/results_table_v1_before_audit.md), which used different splits.

(paste the contents of docs/results_table.md here)

How to read this:
- **Test** is mostly public data, so it is the easiest set.
- **Hard set** (hand-written, often without obvious keywords) and **own rows** are the more realistic measures. They are small, so their 95% ranges are wide.
- Hinglish and Tanglish have too few rows to measure, so no model can be said to handle them.
- (write ONE sentence that matches your table, see the options below)

The API serves (model name), chosen by a rule written before the comparison ([docs/results.md](docs/results.md)).