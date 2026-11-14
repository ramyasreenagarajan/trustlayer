# Project Brief: TrustLayer

## 1. Problem
Scam messages trick people, and hidden instructions in emails, web pages and documents can manipulate AI assistants that read them. Few free, open tools address both, especially for Indian-language and mixed-language content.

## 2. Users
- People who receive suspicious SMS, WhatsApp or email messages
- Developers building AI assistants or agents who want a simple safety check
- Students and researchers who want an open dataset and benchmark

## 3. Version 1 scope (what I will build)
- A labeled dataset of scam, prompt-injection and safe messages (English, Hinglish, Tamil in English letters)
- Baseline and transformer models with honest evaluation
- A FastAPI backend and a responsive web page
- An agent action guard (rule-based) with a demo
- An automated red-team script that tests the detector

## 4. Out of scope for now
- Voice, video and image scams
- Real-time monitoring of a user's inbox
- Handling real users' personal data
- Paid services or paid hosting

## 5. How I will measure success
- Precision, recall and F1 per label on a held-out test set
- Performance on a separate hard set of paraphrased and tricky examples
- Detection rate by attack type in the red-team tests
- Number of people who try the public demo, and the feedback they give

## 6. Risks and how I will handle them
| Risk | Plan |
|---|---|
| False alarms on genuine messages | Include borderline safe examples; report false-positive rate |
| Small or biased dataset | Document sources and limits; add my own local examples |
| Privacy of user messages | Don't store messages; invented data only in the repo |
| Free hosting may be slow or limited | Use a lightweight model; mention limits in the README |
| Overclaiming results | Report only measured numbers and state limitations |

## 7. Timeline
| Weeks | Focus |
|---|---|
| 1 | Setup, labels, README |
| 2 | Dataset |
| 3 | Baseline models |
| 4 | Transformer and explainability |
| 5 | API, web app, core launch |
| 6-7 | Agent action guard and red-team loop |
| 8 | Hardening, documentation, public launch |

## 8. Tools (all free)
Python, scikit-learn, Hugging Face, Google Colab, Kaggle, FastAPI, GitHub, GitHub Pages or Netlify, Hugging Face Spaces or Render.