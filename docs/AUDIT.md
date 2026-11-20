# Label Audit

Date: (today)
Rules: [audit_rules.md](audit_rules.md)

I reviewed a random sample of 180 public rows against my own label definitions.

| Source | Label | Reviewed | Problem rate | 95% range |
|---|---|---|---|---|
| uci_sms_spam | scam | 60 | (n) | (n) to (n) |
| deepset_prompt_injections | prompt_injection | 60 | (n) | (n) to (n) |
| uci_sms_spam | safe | 30 | (n) | (n) to (n) |
| deepset_prompt_injections | safe | 30 | (n) | (n) to (n) |

What I found:
- (e.g. many SMS spam rows are advertising or chat-line promos, which are not scams under my definition)
- (e.g. many deepset injection rows are ordinary requests)

What I will do: (decision from Part G)