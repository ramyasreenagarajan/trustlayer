import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
README, TABLE, TRAIN = Path("README.md"), Path("docs/results_table.md"), Path("data/processed/train.csv")

text = README.read_text(encoding="utf-8")
table = TABLE.read_text(encoding="utf-8").strip()
fresh = TABLE.stat().st_mtime >= TRAIN.stat().st_mtime
when = ("on the current splits, made after the label audit" if fresh
        else "on the older splits, made before the label audit, so they cannot be compared with newer numbers")

if "(your model name)" not in text and "(paste the contents of docs/results_table.md here)" not in text:
    sys.exit("Nothing to replace: the placeholder lines are already gone.")

text = text.replace("(your model name)", "TF-IDF (word + character features) with a Linear SVM, C=0.3")
text = text.replace("Scores come from `src/make_results_table.py`.",
                    f"Scores come from `src/make_results_table.py`, measured {when}.")
text = text.replace("(paste the contents of docs/results_table.md here)", table)
README.write_text(text, encoding="utf-8")

print(f"The table was measured {when}.")
print("First lines of the table that were inserted:")
print("\n".join(table.splitlines()[:4]))