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

## Findings
- The UCI "spam" label means unwanted promotion, which is broader than "scam". Under my narrow definition many rows were adverts, chat-line and ringtone promotions or subscription notices.
- deepset contains many German rows and some in other languages, but my first pipeline labelled all public rows English. Languages are now detected automatically, which is unreliable for short text and for Hinglish and Tanglish.
- I changed my deepset rule during review: a role change or an appended command counts as an injection when it tries to steer the AI away from its task. I applied this rule to all deepset rows.
- My first review passes were unreliable because the review program made "keep" too easy. I rebuilt it so the default is "drop" and re-reviewed the doubtful subsets. The earlier answers are not used.
- The two safe samples (30 rows each) showed no problems, but 30 rows cannot rule out a true rate of up to about 11%.

## Method
1. Reviewed a random sample of 180 public rows (60 SMS scam, 60 deepset injection, 30 SMS safe, 30 deepset safe) against my own label definitions.
2. Sorted the remaining public scam and injection rows with a keyword pre-sort, then reviewed every uncertain row and a blind sample of the sorted rows by hand.
3. Applied the decisions to every row, dropped rows that did not fit any label, and detected the language of each row automatically.

## Sample results
| Source | Label | Reviewed | Dropped | Rate | 95% range |
|---|---|---|---|---|---|
| SMS Spam Collection | scam | 60 | (from summarize_audit) | | |
| deepset | prompt_injection | 60 | | | |
| SMS Spam Collection | safe | 30 | 0 | 0% | 0% to 11% |
| deepset | safe | 30 | 0 | 0% | 0% to 11% |

## After the audit
SMS scam rows: (from apply_audit) -> (from apply_audit). deepset injection rows: (from apply_audit) -> (from apply_audit).
Pre-sort agreement with my review on the blind rows: SMS (n)%, deepset (n)%.

## Findings
- The UCI "spam" label means unwanted promotion, which is broader than "scam". Under my narrow definition, many rows were adverts, chat-line and ringtone promotions or subscription notices.
- deepset contains many German and some Spanish, Russian and Hindi-in-Latin-letters rows, but my first pipeline labelled all public rows English. Languages are now detected automatically, which is unreliable for short text and for Hinglish or Tanglish.
- I changed my deepset rule during review: a role change or an appended command counts as an injection when it tries to steer the AI away from its task (recorded in audit_rules.md). This rule was applied to all deepset rows.
- My first two review passes were unreliable because the program made "keep" too easy. I rebuilt the tool so the default is "drop" and re-reviewed the doubtful subsets. The old answers are not used.
- The two safe samples (30 rows each) showed no problems, but 30 rows cannot rule out a true rate of up to about 11%.