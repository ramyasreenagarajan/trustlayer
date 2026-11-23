import pandas as pd
from pathlib import Path

PROC = Path("data/processed")
OUT = Path("data/audit")
OUT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(PROC / "combined.csv")
pub = df[df["source"].isin(["uci_sms_spam", "deepset_prompt_injections"])]

# (source, label, how many rows to review)
PLAN = [
    ("uci_sms_spam", "scam", 60),
    ("deepset_prompt_injections", "prompt_injection", 60),
    ("uci_sms_spam", "safe", 30),
    ("deepset_prompt_injections", "safe", 30),
]

parts = []
for src, label, n in PLAN:
    d = pub[(pub["source"] == src) & (pub["label"] == label)]
    parts.append(d.sample(n=min(n, len(d)), random_state=7))

sheet = pd.concat(parts).reset_index(drop=True)
sheet.insert(0, "id", range(1, len(sheet) + 1))
sheet["decision"] = ""
sheet["note"] = ""
sheet.to_csv(OUT / "audit_sample.csv", index=False, encoding="utf-8-sig")
print(f"Saved {len(sheet)} rows to data/audit/audit_sample.csv")
print(sheet.groupby(["source", "label"]).size())