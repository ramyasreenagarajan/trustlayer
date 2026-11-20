# Label Audit Rules

Applied to public data (SMS Spam Collection and deepset/prompt-injections).

## Decision codes
- `keep`: the label matches my definition
- `drop`: the row doesn't clearly fit any label, so it is removed from the dataset
- `relabel:<label>`: the label is wrong, and the right one is `safe`, `scam` or `prompt_injection`

## Rows labelled scam (SMS)
- keep: tries to get money, secrets (OTP, PIN, password), a click or a call-back, using a prize, threat, fake authority or false story
- drop: plain advertising, items for sale, chat-line or adult-chat promos, personal chat, or a charge notice that asks for nothing deceptive
- relabel:safe: genuine personal or service message mistakenly marked spam

## Rows labelled prompt_injection (deepset)
- keep: tries to override or ignore instructions, change the AI's role or rules, extract hidden instructions or data, or give a hidden command
- drop: an ordinary request or question, even if odd or offensive, that does not try to override instructions or the AI's rules
- relabel:safe: clearly harmless request

## Rows labelled safe
- keep: genuinely harmless
- relabel:scam or relabel:prompt_injection: contains a clear scam or injection

## When unsure
Choose `drop`, not `keep`. A smaller, cleaner dataset is better than a larger, confusing one.