# Label Audit

Rules: [audit_rules.md](audit_rules.md).

## Method
1. I reviewed a random sample of 180 public rows (60 SMS scam, 60 deepset injection, 30 SMS safe, 30 deepset safe) against my own label definitions.
2. I sorted the remaining public scam and injection rows with a keyword pre-sort, then reviewed the uncertain rows and a blind sample of the sorted rows by hand.
3. I applied the decisions to every row, dropped rows that did not fit any label, and detected each row's language automatically.

## Sample results
| Source | Label | Reviewed | Dropped | Rate | 95% range |
|---|---|---|---|---|---|
| SMS Spam Collection | scam | 60 | 28 | 47% | 35% to 59% |
| deepset | prompt_injection | 60 | 6 | 10% | 5% to 20% |
| SMS Spam Collection | safe | 30 | 0 | 0% | 0% to 11% |
| deepset | safe | 30 | 0 | 0% | 0% to 11% |

## Whole dataset after the audit
- SMS scam rows: 642 reduced to 432 (210 dropped, 33%).
- deepset injection rows: 263 reduced to 243 (20 dropped, 8%).
- The whole-set SMS rate (33%) is lower than the sample rate (47%), so some adverts, chat-line promotions or ringtone notices are probably still labelled scam.
- After combining with my own examples and splitting, the dataset has 1,760 rows: train 1,212, validation 261, test 261 and a separate hard set of 26.

## Checking the pre-sort
The keyword pre-sort was compared with my careful audit decisions on the 60 audited deepset injection rows: it made a decision on 38 of them and agreed with me on all 38. I wrote those patterns after seeing the same rows, so this figure is optimistic and is not an independent accuracy measure.

## Findings
- The UCI "spam" label means unwanted promotion, which is broader than "scam". Under my narrow definition many rows were adverts, chat-line and ringtone promotions or subscription notices.
- deepset contains many German rows and some in other languages, but my first pipeline labelled all public rows English. Languages are now detected automatically (training split: 902 English, 184 German, 116 other or unknown, 5 Hinglish, 5 Tanglish). Detection is unreliable for short text and for Hinglish and Tanglish.
- I changed my deepset rule during review: a role change or an appended command counts as an injection when it tries to steer the AI away from its task (recorded in audit_rules.md). I applied this rule to all deepset rows.
- My first review passes were unreliable because the review program made "keep" too easy. I rebuilt it so the default is "drop" and re-reviewed the doubtful subsets. The earlier answers are not used.
- The two safe samples (30 rows each) showed no problems, but 30 rows cannot rule out a true rate of up to about 11%.