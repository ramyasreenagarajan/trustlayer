import re
import numpy as np

F = re.I | re.S
NEG = re.compile(r"(do not|don't|dont|never|won't|will not|not to|nahi|mat\b|vendaam)", re.I)
DISCLAIMER = "This is a guide, not a guarantee. If money or personal details are involved, check through an official number or app you already trust."

# (id, strength, plain-language title, pattern, skip if the text says "do not / never")
SIGNS = [
    ("urgency", "weak", "Pushes you to act quickly",
     r"\b(urgent|urgently|immediately|right now|asap|last chance|act now|expires? (today|soon|tonight)|within \d+ ?(hours?|hrs?|minutes?|mins?)|turant|udane)\b", False),
    ("secret_request", "strong", "Asks you to share a secret such as an OTP, PIN or password",
     r"\b(share|send|tell|give|enter|read out|reply with|bata[oy]?|bhej[oi]?|sollunga|anuppunga)\b.{0,40}\b(otp|pin|cvv|password|passcode|verification code|card number)\b"
     r"|\b(otp|pin|cvv|password|passcode|verification code)\b.{0,40}\b(share|send|tell|give|enter|read out)\b", True),
    ("account_threat", "strong", "Threatens to block or cut off an account or service",
     r"\b(account|sim|card|connection|supply|number|a/c)\b.{0,30}\b(block(ed)?|suspend(ed)?|clos(ed|ure)|frozen|freez\w*|deactivat\w*|disconnect\w*|paused?)\b|\bkyc\b|kat jayega|band ho jayega|block aag\w*", False),
    ("prize", "strong", "Promises a prize, reward or free gift",
     r"\b(you (have )?won|winner|lottery|lucky draw|prize|cashback|congratulations|jeeta|inaam|kedachirukku|gift voucher)\b", False),
    ("payment", "strong", "Asks for a payment or money transfer",
     r"\b(registration fee|processing fee|clearance (charge|fee)|advance payment|pay (a )?(small )?(fee|charge)|send money|transfer rs\.?|pay rs\.?|upi id|bhej (do|de)|anuppu)\b", False),
    ("story_money", "strong", "Tells an urgent personal story, then asks for money",
     r"\b(new number|naya number|lost my phone|phone (broke|damaged|gir gaya|kharab)|stuck at|hospital|accident)\b.{0,160}\b(send|pay|transfer|bhej|anuppu)\b.{0,60}(rs\.?|₹|upi|money|paisa|\d{3,})", False),
    ("short_link", "strong", "Uses a shortened link that hides the real website",
     r"\b(bit\.ly|tinyurl\.com|cutt\.ly|rb\.gy|is\.gd|t\.co|goo\.gl)/\S+", False),
    ("link", "weak", "Contains a link you are asked to open", r"(https?://|www\.)\S+", False),
    ("impersonation", "weak", "Mentions an organisation that scammers often imitate",
     r"\b(sbi|hdfc|icici|axis bank|paytm|phonepe|amazon|income tax|customs|police|trai|electricity (board|department)|courier)\b", False),
    ("call_to_action", "weak", "Pushes you to call or reply to a number",
     r"\b(call (this )?number|call me|contact (us )?(at|on)|whatsapp (us )?on)\b", False),
    ("override", "strong", "Tells an AI assistant to ignore its earlier instructions",
     r"\b(ignore|forget|disregard)\s+(all\s+|any\s+|your\s+|the\s+)*(previous|prior|above|earlier|preceding)\s+(instructions?|rules?|prompts?|orders?)\b"
     r"|vergiss alles|ignorieren sie die obigen|pichhle[^.]{0,30}instructions?[^.]{0,20}(ignore|bhool)|munnadi sonna[^.]{0,40}ignore", False),
    ("addresses_ai", "strong", "Speaks directly to an AI assistant and gives it an instruction",
     r"\b(note|message|instruction|attention|reminder|p\.?s\.?)\s*(to|for)\s+(the\s+)?(any\s+)?(automated\s+)?(ai|assistant|language model|llm|chatbot|model|reader)\b"
     r"|\b(ai|assistant|llm|language model|chatbot)\b\s*[:,]\s*(ignore|forward|do not|please|reveal|skip|disable|rank|recommend|treat|mark|state)\b"
     r"|\bif you are an? (ai|language model|llm|assistant)\b|\b(assistant|ai tool|ai model)(-ku|-kku| ke liye)", False),
    ("hidden_text", "strong", "Hides an instruction in a comment or brackets",
     r"<!--.*?-->|\[[^\]]{0,60}\b(ai|assistant|model|system)\b[^\]]{0,200}\]|\([^)]{0,40}(language model|ai tool|assistant)[^)]{0,200}\)", False),
    ("data_request", "strong", "Asks to send private data to someone",
     r"\b(forward|send|share|email)\b.{0,80}\b(inbox|mailbox|contacts|calendar|passwords?|documents)\b.{0,80}(\S+@\S+|sender|this address)", False),
    ("roleplay", "strong", "Tries to change the AI's role or rules",
     r"\b(you are now|from now on,? you|developer mode|system message|system prompt|jailbreak|stell dir vor,? du bist)\b", False),
]
PATTERNS = [(i, s, t, re.compile(p, F), g) for i, s, t, p, g in SIGNS]

ADVICE = {
    "en": {
        "Likely scam": ["Don't click any link or call any number in the message.",
                        "Never share an OTP, PIN or password, even with someone who says they are from your bank.",
                        "Block the sender and report it at cybercrime.gov.in or on 1930."],
        "Prompt injection": ["Don't let an AI assistant act on this content.",
                             "Remove the hidden text before it is processed.",
                             "Limit what the assistant is allowed to do (send, share, delete) without your approval."],
        "Suspicious": ["Don't act on this message yet. Check it first.",
                       "Contact the organisation through its official app, website or the number on your card.",
                       "If you already shared details or paid, call your bank right away."],
        "Low risk": ["Stay alert. Scammers also send messages that look ordinary.",
                     "If anything feels off, check with the sender on a number you already trust."],
    },
    # short versions: please rewrite these in your own words
    "hi": {"Likely scam": ["Link par click na karein aur kisi number par call na karein.", "OTP ya PIN kabhi kisi se share na karein."]},
    "ta": {"Likely scam": ["Link-ai click panna vendaam, number-ku call panna vendaam.", "OTP, PIN yaarukkum sollakoodadhu."]},
}


def advice(verdict, lang="en"):
    return ADVICE.get(lang, {}).get(verdict) or ADVICE["en"].get(verdict, ADVICE["en"]["Suspicious"])


def warning_signs(text, max_evidence=80):
    """Return the known tricks found in the text, each with the matching words as evidence."""
    out = []
    for sid, strength, title, pat, guard in PATTERNS:
        for m in pat.finditer(text):
            window = text[max(0, m.start() - 35):m.end()]
            if guard and NEG.search(window):
                continue
            out.append({"id": sid, "strength": strength, "title": title,
                        "evidence": " ".join(m.group(0).split())[:max_evidence]})
            break
    return out


def influential_words(text, proba_model, k=5, min_drop=0.05, max_words=120):
    """Words whose removal lowers the risk score the most (risk = 1 - P(safe))."""
    words = text.split()[:max_words]
    if len(words) < 2:
        return []
    variants = [" ".join(words)] + [" ".join(words[:i] + words[i + 1:]) for i in range(len(words))]
    probs = proba_model.predict_proba(variants)
    safe = list(proba_model.classes_).index("safe")
    risk = 1.0 - probs[:, safe]
    drops = risk[0] - risk[1:]
    out = []
    for i in np.argsort(drops)[::-1][:k]:
        if drops[i] >= min_drop:
            out.append({"word": words[i], "effect": round(float(drops[i]), 2)})
    return out