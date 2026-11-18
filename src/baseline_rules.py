import re
from sklearn.metrics import classification_report, confusion_matrix, f1_score
from common import load_split, LABELS

FLAGS = re.IGNORECASE | re.DOTALL

# Patterns that suggest hidden orders to an AI assistant
INJECTION_PATTERNS = [
    r"ignore (all |any )?(your |the )?(previous|prior|above|earlier) (instructions|rules|prompts?)",
    r"(forget|disregard) (all |your )?(previous|prior|earlier) (instructions|rules)",
    r"\b(ai|assistant|language model|llm|chatbot|automated (reader|assistant|tool))\b.{0,60}"
    r"\b(ignore|forward|share|reveal|recommend|rank|skip|disable|accept|summari[sz]e|treat)\b",
    r"\b(system|developer) (message|mode|prompt)\b",
    r"<!--.*?-->",
    r"\[(note|instruction)s? (to|for) (the )?(ai|assistant|model)",
    r"(reveal|show|print) (your )?(hidden |system )?(instructions|prompt)",
    r"\byou are now\b",
]

# Weighted scam signals (adapted from the rules in frontend/index.html)
SCAM_RULES = [
    (r"\b(urgent|urgently|immediately|right now|last chance|act now|expires? (today|soon)|within \d+ ?(hours?|hrs?|minutes?|mins?))\b", 15),
    (r"\b(otp|cvv|pin|password|aadhaar|card number)\b", 25),
    (r"(kyc|account (will be |has been )?(blocked|suspended|closed|frozen)|sim (will be )?(blocked|deactivated)|update your (pan|kyc|details))", 20),
    (r"\b(you (have )?won|lottery|prize|lucky (draw|winner)|free gift|cashback|crore|lakh)\b", 20),
    (r"\b(work from home|registration fee|processing fee|advance payment|pay a (small )?fee|earn \S+ per day)\b", 20),
    (r"(bit\.ly|tinyurl|cutt\.ly|rb\.gy|is\.gd|t\.co|goo\.gl)/", 20),
    (r"(https?://|www\.)\S+", 10),
    (r"\b(call (this )?number|whatsapp (us )?on|contact (us )?(at|on))\b", 10),
    (r"\b(claim|reward|refund|verify now|verify your)\b", 10),
]
SCAM_THRESHOLD = 25


def predict_one(text):
    if any(re.search(p, text, FLAGS) for p in INJECTION_PATTERNS):
        return "prompt_injection"
    score = sum(w for p, w in SCAM_RULES if re.search(p, text, FLAGS))
    return "scam" if score >= SCAM_THRESHOLD else "safe"


def show(name, y_true, y_pred):
    print(f"\n===== {name} =====")
    print("Macro F1:", round(f1_score(y_true, y_pred, labels=LABELS, average="macro", zero_division=0), 3))
    print(classification_report(y_true, y_pred, labels=LABELS, digits=3, zero_division=0))
    cm = confusion_matrix(y_true, y_pred, labels=LABELS)
    print("Confusion matrix (rows = true, columns = predicted):")
    print("                  ", "  ".join(f"{l[:8]:>8}" for l in LABELS))
    for lab, row in zip(LABELS, cm):
        print(f"{lab:>18}", "  ".join(f"{v:>8}" for v in row))


if __name__ == "__main__":
    val = load_split("val")

    # Sanity floor: a model that always says 'safe'
    show("Always 'safe' (val)", val["label"], ["safe"] * len(val))

    # Keyword rules
    preds = val["text"].map(predict_one)
    show("Keyword rules (val)", val["label"], preds)