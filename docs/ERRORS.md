# Known Errors and Limitations

Scores and tables are in [results.md](results.md). The label audit is in [AUDIT.md](AUDIT.md).

## Status of these numbers
The mistake counts below come from the first baseline (TF-IDF word + character features with a Linear SVM), measured on the splits made **before** the label audit. The hard set (26 hand-written rows) was not changed by the audit, so its findings still describe that model. The deployed model was retrained on the audited data, and its errors have not yet been analysed in the same way.

## What it gets wrong
1. **Scams without obvious keywords or links.** On the hard set the baseline missed 3 of 9 scams and labelled a 4th as an injection. The missed ones are written as a personal story ("new number, send money to this UPI id") or as a polite official request ("verify your details with our officer"), with no link, prize or the usual keywords.
2. **Honest messages that contain scam-like words.** On the hard set 4 of 9 safe messages were flagged as scams: an OTP safety warning, a bank debit notice, an "URGENT" exam-ticket notice and a Tamil OTP warning. All mention an OTP, a bank or urgency.
3. **Prompt injections that avoid the usual words.** 2 of 8 hard-set injections were missed. Both were in Hinglish. Every injection written in English or Tamil-in-English-letters was caught, which may only mean the model recognises words such as "assistant" or "AI tool".
4. **Hinglish and Tamil-in-English-letters generally.** 6 of the 10 hard-set mistakes involve one of these languages, but test and hard together contain only 8 rows of each, so no accuracy figure for either language is reliable.

## What the test set showed
On the pre-audit test set (296 rows) the baseline made 16 mistakes: 8 scams and 6 injections labelled safe, 1 injection labelled scam and 1 safe message flagged as an injection. Reading them against my own definitions showed that most were not model failures:
- 5 were SMS "spam" that is not a scam (a classified advert, a chat-line promotion, a personal reply) and 3 were premium-rate promotions.
- 4 were harmless requests labelled as injections in the public data (for example "generate c++" and "tell me a joke").
- 1 was a borderline request, 1 was a real injection written in Hindi that was missed, 1 was a real injection flagged as the wrong type, and 1 was a political question flagged as an injection.

So the test score of 0.93 macro F1 understates the model on real attacks and is not a clean measure. It also overstates it in another way: the hard set scored 0.63 (95% range 0.40 to 0.81) and the own-row subset 0.73, because those messages are written differently from the public data.

## Why
- The public data covers UK and Singapore SMS and chat-style prompts, not Indian scams, honest bank notices or messages in mixed languages.
- The training data contains few scams written as personal stories, few honest bank and OTP notices labelled safe, and only a handful of Hinglish and Tanglish rows (5 of each in the training split).
- The public labels did not match my definitions. The UCI "spam" label means unwanted promotion, which is broader than scam.
- The public language labels were wrong: most deepset rows are German, but the first version of my pipeline marked every public row as English.
- The validation, test and hard sets are small, so scores for single groups move a lot with one message.

## What I have already done about it
- Audited a random sample of the public labels, applied the findings to the whole dataset and fixed the language column ([AUDIT.md](AUDIT.md)). The SMS scam set fell from 642 to 432 rows and the injection set from 263 to 243.
- Tuned the alert thresholds on the validation set only.
- Added warning-sign rules, so the tool shows the matching words and says plainly when no specific trick was found.

## What I plan to do next
- Run the same error analysis on the deployed (post-audit) model and add the results here.
- Add more honest bank, OTP and urgent notices as safe examples, more story-style scams, and more Hinglish and Tanglish rows for all three labels (the target is 30 of each language).
- Test injections that avoid the words "AI" and "assistant" in the red-team step (Week 7).
- Complete the transformer comparison on the cleaned data, which has not been done yet.

## Things not to conclude
- The test score is not real-world performance.
- Nothing is known about Hinglish or Tanglish accuracy: 8 rows each is too few.
- The hard set has 26 rows, so its score has a wide range.
- The audit was done by one person against one set of definitions, and the SMS scam set probably still contains some adverts.
- Language labels for public data come from an automatic detector and are unreliable for short text.