import sys
import pandas as pd
from presort_public import presort_sms, presort_deepset

sys.stdout.reconfigure(encoding="utf-8")
a = pd.read_csv("data/audit/audit_sample.csv", encoding="utf-8-sig", dtype=str).fillna("")
a["human"] = a["decision"].map(lambda x: "keep" if x == "keep" else "drop")

for name, src, label, fn in [("SMS scam", "uci_sms_spam", "scam", presort_sms),
                             ("deepset injection", "deepset_prompt_injections", "prompt_injection", presort_deepset)]:
    g = a[(a["source"] == src) & (a["label"] == label)].copy()
    g["pre"] = g["text"].map(fn)
    dec = g[g["pre"] != "uncertain"]
    print(f"\n{name}: {len(g)} rows | pre-sort decided {len(dec)} | agreement with your audit: {(dec['pre'] == dec['human']).mean():.0%}")
    for _, r in dec[dec["pre"] != dec["human"]].iterrows():
        print(f"   pre-sort {r['pre']}, you {r['human']}: {r['text'][:110]}")
print("\nNote: I wrote the patterns after seeing these rows, so this figure is optimistic.")