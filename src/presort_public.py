import re
import sys
import pandas as pd
from pathlib import Path

PROC = Path("data/processed")
AUD = Path("data/audit")

# SMS: cues for a deceptive lure vs cues for an ordinary advert, chat-line or subscription
SMS_KEEP = re.compile(r"(\bwon\b|\bwin\b|winner|prize|award|selected|congrat|guaranteed|claim|cash|voucher|reward|bonus|unredeemed|voicemail|admirer|attempt|statement|balance|identifier|someone you know)", re.I)
SMS_DROP = re.compile(r"(ringtone|polyphonic|\btones?\b|\bmonos?\b|jamster|videosound|wallpaper|\blogos?\b|arcade|subscri|(txt|text|send|reply) stop|re-?sub|per week|flirt|dating|\bdate\b|chat|lonely|horny|randy|\bsexy?\b|girls|housewives|singles|tickets|careers|top up|outbid|\bgoal\b)", re.I)

# deepset: override words in English, German, Spanish, Russian and Hindi (Latin letters)
DS_OVERRIDE = re.compile(r"(ignor|forget|disregard|vergiss|vergessen|abweichend|bisherig|vorherig|instruk|instruct|anweisung|auftr|olvid|забуд|игнор|previous|prior|earlier|new task|neue aufgabe|you are now|du bist jetzt|pretend|stell dir vor|act as|system prompt|developer mode|yaad na karen)", re.I)


def norm(s):
    return " ".join(str(s).lower().split())


def presort_sms(text):
    k, d = bool(SMS_KEEP.search(text)), bool(SMS_DROP.search(text))
    if k and not d:
        return "keep"
    if d and not k:
        return "drop"
    return "uncertain"


def presort_deepset(text):
    return "keep" if DS_OVERRIDE.search(text) else "uncertain"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    a = pd.read_csv(AUD / "audit_sample.csv", encoding="utf-8-sig", dtype=str).fillna("")
    a = a[a["decision"] != ""]

    # ---------- how well does the pre-sort agree with your audit? ----------
    s = a[(a["source"] == "uci_sms_spam") & (a["label"] == "scam")].copy()
    s["pre"] = s["text"].map(presort_sms)
    s["human"] = s["decision"].map(lambda x: "keep" if x == "keep" else "drop")
    dec = s[s["pre"] != "uncertain"]
    print(f"SMS scam audit rows: {len(s)} | pre-sort uncertain: {(s['pre'] == 'uncertain').sum()} | decided: {len(dec)}")
    print(f"Agreement with you on decided rows: {(dec['pre'] == dec['human']).mean():.0%}")
    for _, r in dec[dec["pre"] != dec["human"]].iterrows():
        print(f"   disagrees (pre-sort {r['pre']}, you {r['human']}): {r['text'][:110]}")
    print("   Note: I wrote these patterns after seeing these rows, so this agreement is optimistic.")
    print("   The blind sample you review below gives the honest error rate.\n")

    d = a[(a["source"] == "deepset_prompt_injections") & (a["label"] == "prompt_injection")].copy()
    d["pre"] = d["text"].map(presort_deepset)
    d["human"] = d["decision"].map(lambda x: "keep" if x == "keep" else "drop")
    m = d[d["pre"] == "keep"]
    u = d[d["pre"] == "uncertain"]
    print(f"deepset audit rows: {len(d)} | override words found: {len(m)} (you kept {(m['human'] == 'keep').sum()}) | not found: {len(u)} (you dropped {(u['human'] == 'drop').sum()})\n")

    audited = set(a["text"].map(norm))

    # ---------- build the review sheets ----------
    def make_sheet(df, label, presort, extra_sample, outname):
        g = df[df["label"] == label]
        rest = g[~g["text"].map(norm).isin(audited)].copy()
        rest["presort"] = rest["text"].map(presort)
        print(f"{outname}: {len(rest)} unaudited rows -> {rest['presort'].value_counts().to_dict()}")
        unc = rest[rest["presort"] == "uncertain"]
        auto = rest[rest["presort"] != "uncertain"]
        blind = auto.sample(n=min(extra_sample, len(auto)), random_state=3)
        sheet = pd.concat([unc, blind]).sample(frac=1, random_state=1).reset_index(drop=True)
        sheet.insert(0, "id", range(1, len(sheet) + 1))
        sheet["decision"] = ""
        sheet[["id", "text", "label", "source", "presort", "decision"]].to_csv(
            AUD / outname, index=False, encoding="utf-8-sig")
        print(f"   saved {len(sheet)} rows to review ({len(unc)} uncertain + {len(blind)} blind check)\n")

    make_sheet(pd.read_csv(PROC / "sms_clean.csv"), "scam", presort_sms, 40, "sms_review.csv")
    make_sheet(pd.read_csv(PROC / "deepset_clean.csv"), "prompt_injection", presort_deepset, 20, "deepset_review.csv")


if __name__ == "__main__":
    main()