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
