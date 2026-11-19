import sys
import pandas as pd
from common import PROC

sys.stdout.reconfigure(encoding="utf-8")   # avoids errors on special characters in Windows

MAX_SHOWN = 40
frames = []

for name in ["test", "hard"]:
    path = PROC / f"errors_{name}.csv"
    if not path.exists():
        print(f"Missing {path}. Run: py src/final_eval.py")
        continue
    df = pd.read_csv(path)
    df.insert(0, "set", name)
    frames.append(df)

    print(f"\n==================== {name.upper()} set: {len(df)} mistakes ====================")
    if len(df) == 0:
        continue
    print("\nWhat was predicted instead (true -> predicted):")
    print(df.groupby(["label", "pred"]).size().sort_values(ascending=False).to_string())
    print("\nBy source:")
    print(df["source"].value_counts().to_string())
    print("\nBy language:")
    print(df["language"].value_counts().to_string())

    shown = df.sample(n=min(MAX_SHOWN, len(df)), random_state=1) if name == "test" else df
    print(f"\n--- {len(shown)} mistakes (true -> predicted) ---")
    for i, r in shown.reset_index(drop=True).iterrows():
        print(f"\n[{name} {i+1}] {r['label']} -> {r['pred']} | {r['language']} | {r['source']}")
        print("   ", str(r["text"])[:220])

# review sheet for your own notes (stays on your computer)
if frames:
    sheet = pd.concat(frames, ignore_index=True)
    sheet["cause"] = ""
    sheet["note"] = ""
    sheet.to_csv(PROC / "error_review.csv", index=False)
    print(f"\nSaved {len(sheet)} rows to data/processed/error_review.csv (fill in the 'cause' column)")