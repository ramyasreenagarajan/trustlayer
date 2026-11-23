import sys
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
if len(sys.argv) < 3:
    sys.exit("Usage: py src/review2_cli.py data/audit/sms_review.csv sms   (or deepset)")
PATH, KIND = sys.argv[1], sys.argv[2]

KEEP_KEYS = {
    "sms": {"p": "prize_or_gift_lure", "t": "threat_or_fake_authority", "s": "false_story"},
    "deepset": {"o": "override_or_ignore_instructions", "r": "changes_AI_role_or_rules", "x": "extracts_hidden_instructions"},
}[KIND]
MENU = {
    "sms": "Enter = DROP   p = prize/gift lure   t = threat/fake authority   s = false story   u = undo   q = quit",
    "deepset": "Enter = DROP   o = override/ignore   r = changes AI role or rules   x = extracts hidden instructions   u = undo   q = quit",
}[KIND]

df = pd.read_csv(PATH, encoding="utf-8-sig", dtype=str).fillna("")
if "reason" not in df.columns:
    df["reason"] = ""


def save():
    df.to_csv(PATH, index=False, encoding="utf-8-sig")


def counts():
    return df["decision"].value_counts().to_dict()


todo = df.index[df["decision"].str.strip() == ""].tolist()
print("REVIEW PROGRAM v3")
print(f"{len(df)} rows in total | answered so far: {counts()} | {len(todo)} left")
print("Enter (or d) = DROP. Type a letter only if you can name the trick.\n")

i, history = 0, []
while i < len(todo):
    idx = todo[i]
    print("\n" + "-" * 70)
    print(f"Row {df.loc[idx, 'id']}   ({i + 1} of {len(todo)})\n")
    print(df.loc[idx, "text"])
    print()
    a = input(MENU + "\n> ").strip().lower()
    if a == "q":
        save()
        print("Saved. Answers so far:", counts())
        sys.exit()
    if a == "u":
        if history:
            i = history.pop()
            df.loc[todo[i], ["decision", "reason"]] = ""
            save()
            print("Undone. Answer this row again.")
        else:
            print("Nothing to undo.")
        continue
    if a in ("", "d", "drop"):
        decision, reason = "drop", ""
    elif a in KEEP_KEYS:
        decision, reason = "keep", KEEP_KEYS[a]
    else:
        print("Not recognised. Press Enter, or type one of:", ", ".join(KEEP_KEYS), "u q")
        continue
    df.loc[idx, "decision"], df.loc[idx, "reason"] = decision, reason
    save()
    history.append(i)
    i += 1
    print(f">>> SAVED: {decision.upper()}   (answers so far: {counts()})")

print("\nAll rows reviewed.")