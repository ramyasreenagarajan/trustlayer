import sys
import pandas as pd
from common import load_split

sys.stdout.reconfigure(encoding="utf-8")
sets = {n: load_split(n) for n in ["train", "val", "test", "hard"]}
al = pd.concat([d.assign(split=n) for n, d in sets.items()], ignore_index=True)
al["origin"] = al["source"].astype(str).map(lambda s: "own" if s.startswith("own") else "public")

print("Total rows:", len(al), "| per split:", {n: len(d) for n, d in sets.items()})
print("\nBy label x split\n", pd.crosstab(al["label"], al["split"]).to_string())
print("\nBy label x origin\n", pd.crosstab(al["label"], al["origin"]).to_string())
print("\nBy source\n", al["source"].value_counts().to_string())
print("\nBy language x label\n", pd.crosstab(al["language"], al["label"]).to_string())
print("\nBy language x split (top 8 languages)\n",
      pd.crosstab(al["language"], al["split"]).sort_values("train", ascending=False).head(8).to_string())
print("\nAverage length in characters by label\n", al.groupby("label")["text"].apply(lambda s: round(s.str.len().mean())).to_string())