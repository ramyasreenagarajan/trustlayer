## Dataset review (Week 2, Day 2)
- SMS spam sample: X of 20 are scams, Y of 20 are ordinary advertising. Decision: (keep as scam / note as a limitation).
- deepset: label 1 = injection confirmed.
- Some deepset rows are not in English: (yes/no).

## Combined dataset (Week 2, Day 5)
- Final rows: (number)
- By label: safe (n), scam (n), prompt_injection (n)
- Own rows: scam (n), prompt_injection (n), safe (n)
- Languages in each label: (comment)
- Problems found: (for example: too few Tamil safe rows; deepset safe rows are mostly chatbot questions)
- Decisions: kept SMS safe sample at 600; will handle imbalance with class weights in Week 3

## Dataset split (Week 2, Day 6)
- Split: 70/15/15 stratified by label, plus a separate hard set (n rows)
- Hard set written by hand: scams without keywords, disguised words, injections without "ignore previous instructions", safe messages with scam words
- No exact duplicates across sets (checked by script)
- Known limitation: injection/safe "twin" pairs may fall in different sets, which can make the test set slightly easier
- Rule: test and hard sets are used only for final scores, never for tuning