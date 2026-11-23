import sys
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
if len(sys.argv) < 3:
    sys.exit("Usage: py src/review_cli.py data/audit/sms_review.csv sms   (or: ... deepset_review.csv deepset)")
PATH, KIND = sys.argv[1], sys.argv[2]

REMINDER = {
    "sms": "KEEP = tries to get money, a secret, a click or a call using a prize, threat, fake authority or false story.\n"
           "DROP = advert, chat/dating promo, ringtone or subscription, personal chat, or a notice that asks for nothing deceptive. Unsure = drop.",
    "deepset": "KEEP = tries to override or ignore instructions, change the AI's role or rules, or extract hidden instructions.\n"
               "DROP = an ordinary request or question with no override. Unsure = drop.",
}[KIND]

df = pd.read_csv(PATH, encoding="utf-8-sig", dtype=str).fillna("")
todo = df.index[df["decision"].str.strip() == ""].tolist()
print(f"{len(todo)} rows left to review out of {len(df)}. Type q to quit (progress is saved).\n")
print(REMINDER)

for n, idx in enumerate(todo, 1):
    r = df.loc[idx]
    print("\n" + "-" * 70)
    print(f"Row {r['id']}   ({n} of {len(todo)})   Current label: {r['label']}\n")
    print(r["text"])
    print()
    while True:
        a = input("k=keep  d=drop  q=quit > ").strip().lower()
        if a == "q":
            df.to_csv(PATH, index=False, encoding="utf-8-sig")
            print("Saved. Run the program again to continue.")
            sys.exit()
        if a in ("k", "d"):
            df.loc[idx, "decision"] = "keep" if a == "k" else "drop"
            df.to_csv(PATH, index=False, encoding="utf-8-sig")
            break
        print("Please type k, d or q")

print("\nAll rows reviewed.")