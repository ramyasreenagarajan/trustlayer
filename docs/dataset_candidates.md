# Dataset Candidates

| Name | Link | License | Rows | Labels | Notes |
|---|---|---|---|---|---|
| SMS Spam Collection | archive.ics.uci.edu (dataset 228) | CC BY 4.0 | 5,574 (5,160 after removing duplicates) | ham / spam | English; mostly UK and Singapore messages; credit Almeida and Gomez Hidalgo (2011) |
| deepset/prompt-injections | huggingface.co/datasets/deepset/prompt-injections | Apache 2.0 | 662 | 0 / 1 | Small; mostly classic injections; label 1 = prompt injection (confirm after reading examples) |

## Limits to mention in the README
- Public SMS data does not cover Indian scams or Hinglish and Tamil text, so my own examples fill that gap.
- The SMS "spam" label also includes plain advertising, which may not match my scam definition.
- deepset "safe" rows are mostly chatbot questions, not emails or SMS messages.
