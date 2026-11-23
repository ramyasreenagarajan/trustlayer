import pandas as pd

PATH = "data/audit/audit_sample.csv"
d = pd.read_csv(PATH, encoding="utf-8-sig", dtype=str).fillna("")

# edit this list if you disagree with any change
CHANGES = {"4": "drop", "7": "drop", "11": "drop", "16": "drop",
           "21": "drop", "22": "drop", "23": "drop", "24": "keep"}

for row_id, decision in CHANGES.items():
    d.loc[d["id"] == row_id, "decision"] = decision

d.to_csv(PATH, index=False, encoding="utf-8-sig")

sms = d[(d["source"] == "uci_sms_spam") & (d["label"] == "scam")]
print(sms["decision"].replace("", "(not answered yet)").value_counts())