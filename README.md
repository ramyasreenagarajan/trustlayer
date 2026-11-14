# TrustLayer

An open-source toolkit that helps protect people and AI assistants from scam messages and hidden prompt-injection attacks.

> **Status:** early development (Week 1 of 8). Setup, project structure and labeling guide are complete. Models are not trained yet.

## Why this project

- Scam messages (fake KYC updates, UPI refunds, job-fee offers) target people every day, often in mixed languages such as Hinglish and Tamil written in English letters.
- AI assistants now read emails, documents and web pages for us. Attackers can hide instructions inside that content, which is called prompt injection.
- Most student projects stop at classifying text. TrustLayer also looks at what an AI agent is about to do, and tests itself against attacks.

## Planned layers

| Layer | What it does | Planned |
|---|---|---|
| 1. Content scanner | Detects scam messages and prompt-injection text in English, Hinglish and Tamil | Weeks 2-5 |
| 2. Agent action guard | Checks whether an AI agent's action matches what the user asked | Weeks 6-7 |
| 3. Red-team loop | Generates attack variants to measure and improve robustness | Weeks 7-8 |

## Labels

- `safe`: ordinary message with no attempt to deceive or manipulate
- `scam`: tries to trick a person into paying, sharing secrets, or clicking
- `prompt_injection`: hidden instructions aimed at an AI assistant

See [docs/labeling_guide.md](docs/labeling_guide.md) for the full rules.

## Repository structure
````
data/        raw and processed datasets
notebooks/   experiments and analysis
src/         reusable Python code
api/         FastAPI backend
guard/       agent action guard
redteam/     attack generation and testing
frontend/    web interface
tests/       automated tests
models/      saved models
docs/        guides, brief and notes
````

## Tech stack

Python, scikit-learn, Hugging Face Transformers, FastAPI, HTML/CSS/JavaScript. All tools used are free.

## Roadmap

- [x] Project structure and environment
- [x] Labeling guide and seed examples
- [ ] Dataset collection and cleaning (Week 2)
- [ ] Baseline models and evaluation (Week 3)
- [ ] Transformer model and explainability (Week 4)
- [ ] API and web app (Week 5)
- [ ] Agent action guard (Weeks 6-7)
- [ ] Red-team loop and hardening (Weeks 7-8)

## Limitations

TrustLayer gives guidance, not guarantees. Detection can miss attacks or flag safe messages. Results, datasets and known weaknesses will be documented here as the project progresses.

## Privacy

Example messages in this repository are invented. Do not submit real personal data, account numbers or OTPs to this project.

## Author

Ramya Sree Nagarajan, MSc Artificial Intelligence, Royal Holloway, University of London.
[LinkedIn](https://www.linkedin.com/in/ramya-sree-nagarajan-619245345)

## License

MIT
````
````

Copy only what's inside the box. The outer fence is just for display. Your pasted text should begin with three backticks followed by `data/ raw and processed datasets`, and end with `MIT`.

## Check it

Press **`Ctrl+Shift+V`** to open the preview. You should see:
- A grey box listing the folders under "Repository structure"
- Headings for Tech stack, Roadmap, Limitations, Privacy, Author and License
- The roadmap as checkboxes, with the first two ticked

## One small fix

The first line of your file shows ```` ```markdown ```` at the top. That's just the code-box label from copying, and it shouldn't be in the file. If it's there, delete that line, and also delete any stray ```` ``` ```` at the very bottom. The file should begin with `# TrustLayer`.

When the preview looks right, move on to Part C (`docs/brief.md`).