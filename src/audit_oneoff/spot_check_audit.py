import sys
import re
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
d = pd.read_csv("data/audit/audit_sample.csv", encoding="utf-8-sig", dtype=str).fillna("")
print(d["decision"].value_counts(), "\n")

# SMS 'scam' rows with none of the usual scam cues
sms = d[(d["source"] == "uci_sms_spam") & (d["label"] == "scam")]
cues = re.compile(r"(call|txt|text|reply|claim|win|won|prize|www|http|\d{5,}|£|free|click|send|urgent)", re.I)
no_cue = sms[~sms["text"].str.contains(cues)]
print(f"SMS 'scam' rows with no typical scam cue: {len(no_cue)} of {len(sms)}")
for _, r in no_cue.iterrows():
    print(f"- [row {r['id']}] your answer: {r['decision']} | {r['text'][:160]}")

# deepset 'injection' rows with no sign of overriding instructions
dep = d[(d["source"] == "deepset_prompt_injections") & (d["label"] == "prompt_injection")]
override = re.compile(r"(ignore|forget|disregard|instruction|previous|prompt|rules?|pretend|you are now|act as|new task|stop|system|statement)", re.I)
no_over = dep[~dep["text"].str.contains(override)]
print(f"\ndeepset 'injection' rows with no override words: {len(no_over)} of {len(dep)}")
for _, r in no_over.iterrows():
    print(f"- [row {r['id']}] your answer: {r['decision']} | {r['text'][:160]}")
    