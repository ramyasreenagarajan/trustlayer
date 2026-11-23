import sys
import pandas as pd
from pathlib import Path
from langdetect import detect, DetectorFactory

from presort_public import norm, presort_sms, presort_deepset

sys.stdout.reconfigure(encoding="utf-8")
DetectorFactory.seed = 0
PROC = Path("data/processed")
AUD = Path("data/audit")
LANGS = {"en": "english", "de": "german"}


def lang(t):
    if len(t) < 25:
        return "unknown"
    try:
        code = detect(t)
    except Exception:
        return "unknown"
    return LANGS.get(code, code)


def load_decisions(path):
    d = pd.read_csv(path, encoding="utf-8-sig", dtype=str).fillna("")
    missing = int((d["decision"].str.strip() == "").sum())
    if missing:
        raise SystemExit(f"{path.name}: {missing} rows have no decision yet. Finish that review first.")
    return {norm(t): x.strip().lower() for t, x in zip(d["text"], d["decision"])}


audit = load_decisions(AUD / "audit_sample.csv")
sms_rev = load_decisions(AUD / "sms_review.csv")
ds_rev = load_decisions(AUD / "deepset_review.csv")


def apply(df, presort, review, outname):
    rows, dropped, relabelled = [], 0, 0
    for t, label, source in zip(df["text"], df["label"], df["source"]):
        k = norm(t)
        if k in audit:
            dec = audit[k]
        elif label == "safe":
            dec = "keep"
        elif k in review:
            dec = review[k]
        else:
            dec = presort(t)
            if dec == "uncertain":
                raise SystemExit(f"Row not reviewed: {t[:80]}. Rerun presort_public.py and review again.")
        if dec == "drop":
            dropped += 1
            continue
        if dec.startswith("relabel:"):
            label = dec.split(":", 1)[1]
            relabelled += 1
        rows.append({"text": t, "label": label, "language": lang(t), "source": source})
    out = pd.DataFrame(rows).drop_duplicates(subset="text")
    out.to_csv(PROC / outname, index=False)
    print(f"\n{outname}: {len(df)} rows in, {dropped} dropped, {relabelled} relabelled, {len(out)} rows out")
    print("Before:", df["label"].value_counts().to_dict())
    print("After: ", out["label"].value_counts().to_dict())
    print("Languages detected:", out["language"].value_counts().head(8).to_dict())


apply(pd.read_csv(PROC / "sms_clean.csv"), presort_sms, sms_rev, "sms_audited.csv")
apply(pd.read_csv(PROC / "deepset_clean.csv"), presort_deepset, ds_rev, "deepset_audited.csv")