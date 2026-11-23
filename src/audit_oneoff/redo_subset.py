import os
import pandas as pd

S, D = "data/audit/sms_review.csv", "data/audit/deepset_review.csv"
if os.path.exists(S.replace(".csv", "_pass2.csv")):
    raise SystemExit("Backup already exists, so this was already run. Do NOT run it twice.")

s = pd.read_csv(S, encoding="utf-8-sig", dtype=str).fillna("")
d = pd.read_csv(D, encoding="utf-8-sig", dtype=str).fillna("")
s.to_csv(S.replace(".csv", "_pass2.csv"), index=False, encoding="utf-8-sig")
d.to_csv(D.replace(".csv", "_pass2.csv"), index=False, encoding="utf-8-sig")

m_s = (s["reason"] == "false_story") | ((s["presort"] != "uncertain") & (s["presort"] != s["decision"]))
m_d = d["decision"] == "drop"
s.loc[m_s, ["decision", "reason"]] = ""
d.loc[m_d, ["decision", "reason"]] = ""
s.to_csv(S, index=False, encoding="utf-8-sig")
d.to_csv(D, index=False, encoding="utf-8-sig")
print("SMS rows to redo:", int(m_s.sum()), "| deepset rows to redo:", int(m_d.sum()))