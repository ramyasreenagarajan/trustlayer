| Model | Set | Rows | Macro F1 | 95% range | Recall scam | Recall injection |
|---|---|---|---|---|---|---|
| Keyword rules | Validation | 261 | 0.386 | 0.32 to 0.46 | 0.14 | 0.08 |
| Keyword rules | Test | 261 | 0.350 | 0.29 to 0.41 | 0.12 | 0.05 |
| Keyword rules | Hard set | 26 | 0.267 | 0.11 to 0.41 | 0.0 | 0.25 |
| Keyword rules | Own rows (test + hard) | 36 | 0.426 | 0.23 to 0.60 | 0.23 | 0.3 |
| TF-IDF (word+char) + Linear SVM, C=0.3 | Validation | 261 | 0.946 | 0.91 to 0.97 | 0.97 | 0.84 |
| TF-IDF (word+char) + Linear SVM, C=0.3 | Test | 261 | 0.943 | 0.91 to 0.97 | 0.97 | 0.85 |
| TF-IDF (word+char) + Linear SVM, C=0.3 | Hard set | 26 | 0.672 | 0.48 to 0.85 | 0.56 | 0.75 |
| TF-IDF (word+char) + Linear SVM, C=0.3 | Own rows (test + hard) | 36 | 0.766 | 0.62 to 0.89 | 0.69 | 0.8 |

| Language | Rows | Accuracy | Note |
|---|---|---|---|
| english | 209 | 0.93 |  |
| german | 37 | 1.00 |  |
| hinglish | 8 | 0.50 | too few rows to trust |
| other_or_unknown | 25 | 0.96 | too few rows to trust |
| tamil_translit | 8 | 0.88 | too few rows to trust |
