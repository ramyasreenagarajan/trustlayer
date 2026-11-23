import sys
import pandas as pd
from common import load_split
from explain import warning_signs

sys.stdout.reconfigure(encoding="utf-8")
df = pd.concat([load_split("test").assign(set="test"), load_split("hard").assign(set="hard")], ignore_index=True)
df["signs"] = df["text"].map(warning_signs)
df["strong"] = df["signs"].map(lambda s: [x["id"] for x in s if x["strength"] == "strong"])
df["has"] = df["strong"].map(len) > 0

print("Share of rows with at least one STRONG sign")
print(df.groupby(["set", "label"])["has"].agg(["mean", "size"]).round(2).to_string())

print("\nSAFE rows that got a strong sign (false signs):")
for _, r in df[(df.label == "safe") & df.has].head(15).iterrows():
    print(f"- {r['strong']} | {r['text'][:110]}")

print("\nSCAM / INJECTION rows with NO strong sign (missing signs):")
for _, r in df[(df.label != "safe") & ~df.has].sample(frac=1, random_state=1).head(15).iterrows():
    print(f"- {r['label']} | {r['text'][:110]}")

print("\n15 random flagged rows: does the evidence really show the trick?")
for _, r in df[df.has].sample(15, random_state=2).iterrows():
    ev = "; ".join(f"{s['id']}: \"{s['evidence']}\"" for s in r["signs"] if s["strength"] == "strong")
    print(f"- [{r['label']}] {ev}")