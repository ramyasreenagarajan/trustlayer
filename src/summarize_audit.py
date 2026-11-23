import pandas as pd

df = pd.read_csv("data/audit/audit_sample.csv", encoding="utf-8-sig", dtype=str)
df["decision"] = df["decision"].fillna("").astype(str).str.strip().str.lower()

empty = (df["decision"] == "").sum()
if empty:
    print(f"WARNING: {empty} rows have no decision yet. Fill them in first.\n")
df = df[df["decision"] != ""]


def wilson(k, n, z=1.96):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / denom
    return centre - half, centre + half


rows = []
for (src, label), g in df.groupby(["source", "label"]):
    n = len(g)
    keep = (g["decision"] == "keep").sum()
    drop = (g["decision"] == "drop").sum()
    relabel = g["decision"].str.startswith("relabel").sum()
    bad = drop + relabel
    lo, hi = wilson(bad, n)
    rows.append({"source": src, "label": label, "reviewed": n, "keep": keep, "drop": drop,
                 "relabel": relabel, "problem_rate": round(bad / n, 2),
                 "range_low": round(lo, 2), "range_high": round(hi, 2)})

print(pd.DataFrame(rows).to_string(index=False))
print("\nRelabel targets:")
print(df[df["decision"].str.startswith("relabel")]["decision"].value_counts().to_string())