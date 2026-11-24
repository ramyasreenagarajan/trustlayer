# Progress Log

## Week 1
- Set up tools, repo, Python environment, and API test
- Defined three labels and wrote a labeling guide
- Wrote README and project brief
- Challenges: (write what was hard, e.g. Git setup, virtual environment)
- What I learned: (write 2-3 things)
- Next: build the dataset (Week 2)

## Week 3
- Built a keyword-rules baseline and trained TF-IDF + logistic regression and linear SVM models
- Chose the final baseline on the validation set only; scored on test, hard set and own rows once
- Read and tagged model mistakes; documented limitations in docs/ERRORS.md
- Saved the model and wrote a predict() function with tests
- Problems: (for example: split script was incomplete; wrong file names; version conflict on GitHub)
- What I learned: (2-3 sentences: for example, why accuracy misleads, why the hard set matters)
- Next: transformer model and readable explanations (Week 4)

## Week 4
- Audited public labels against my own definitions and found the "spam" and "injection" labels did not match; rebuilt the data with a written rule
- Fixed the language column with automatic detection
- Trained DistilBERT and MuRIL on Colab and compared them with the TF-IDF baseline on the same final splits
- Added warning signs, influential words and advice, with tests
- Problems: the first review passes were unreliable (one-key "keep"); saving failed silently in one version of the review tool; the language column had been wrong
- What I learned: (2-3 sentences in your own words)
- Next: FastAPI backend, thresholds tuned on validation data, free deployment (Week 5)