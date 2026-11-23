import sys
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
PATH = "data/audit/audit_sample.csv"

df = pd.read_csv(PATH, encoding="utf-8-sig", dtype=str).fillna("")
CODES = {"k": "keep", "d": "drop", "s": "relabel:safe",
         "c": "relabel:scam", "i": "relabel:prompt_injection"}

todo = df.index[df["decision"].str.strip() == ""].tolist()
print(f"{len(todo)} rows left to review out of {len(df)}. Type q to quit (progress is saved).")

for n, idx in enumerate(todo, 1):
    r = df.loc[idx]
    print("\n" + "-" * 70)
    print(f"Row {r['id']}   ({n} of {len(todo)})   Current label: {r['label']}   Source: {r['source']}")
    print()
    print(r["text"])
    print()
    while True:
        a = input("k=keep  d=drop  s=relabel safe  c=relabel scam  i=relabel injection  q=quit > ").strip().lower()
        if a == "q":
            df.to_csv(PATH, index=False, encoding="utf-8-sig")
            print("Saved. Run the program again to continue.")
            sys.exit()
        if a in CODES:
            df.loc[idx, "decision"] = CODES[a]
            df.to_csv(PATH, index=False, encoding="utf-8-sig")
            break
        print("Please type one of: k  d  s  c  i  q")

print("\nAll rows reviewed. Now run: py src/summarize_audit.py")