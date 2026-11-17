import pandas as pd
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "data/own/scam_own.csv"
df = pd.read_csv(path)

print("Rows:", len(df))
print("Columns:", df.columns.tolist())
print("\nLabels:\n", df["label"].value_counts())
print("\nLanguages:\n", df["language"].value_counts())
print("\nDuplicate messages:", df["text"].duplicated().sum())
print("Empty messages:", df["text"].isna().sum())
print("\nShortest 3 messages:")
for t in df.loc[df["text"].str.len().nsmallest(3).index, "text"]:
    print("-", t)