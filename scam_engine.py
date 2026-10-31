"""Rule-based message checker. No AI or internet needed, so it always works."""
import re

# (name, pattern, why it is a warning sign, what to do)
RULES = [
    ("Asks for a secret code or password",
     r"\b(otp|pin|password|cvv|one[- ]time|verification code|cnic)\b",
     "Real banks never ask for your PIN, password or code in a message.",
     "Never share it. Not even with someone who says they work at the bank."),
    ("Tries to scare or rush you",
     r"\b(urgent|immediately|within \d+ ?(hours?|minutes?)|last chance|suspended|blocked|expire[sd]?|final warning|act now)\b",
     "Scammers rush you so you do not stop and think.",
     "Take a breath. Real offices can wait 10 minutes while you check."),
    ("Promises a prize or free money",
     r"\b(won|winner|prize|lottery|jackpot|bonus|reward|bisp|cash grant|free gift)\b",
     "If you did not enter a contest, you cannot win one.",
     "Ignore it. Free money messages are almost always tricks."),
    ("Has a link you are told to click",
     r"(https?://|www\.|bit\.ly|tinyurl|\.xyz|\.top|\.click|click here|tap here)",
     "Links in messages can lead to fake websites that steal your details.",
     "Do not click. Open the real app yourself, or call the number on your card."),
    ("Asks you to send money",
     r"\b(send money|transfer|easypaisa|jazzcash|western union|gift ?card|load|advance fee|processing fee)\b",
     "Asking for money first is the biggest scam sign.",
     "Never send money to someone you only know by message."),
    ("Pretends to be someone you trust",
     r"\b(nadra|fbr|state bank|sbp|police|fia|customs|courier|bank officer|your son|your daughter|new number)\b",
     "Scammers copy the names of banks, offices and even your family.",
     "Hang up and call the real number yourself, or call your family member on the old number."),
    ("Asks you to install an app",
     r"\b(anydesk|teamviewer|install|download the app|apk)\b",
     "These apps let a stranger see and control your phone.",
     "Never install an app because a message or caller asked you to."),
    ("Asks you to keep it secret",
     r"\b(do not tell|don't tell|keep this secret|confidential|tell no one)\b",
     "Scammers do not want you to ask your family for help.",
     "Always show the message to someone you trust first."),
]

def analyze(text: str):
    """Return (level, findings). level is 'safe-looking', 'careful' or 'danger'."""
    found = []
    low = (text or "").lower()
    for name, pattern, why, todo in RULES:
        if re.search(pattern, low):
            found.append({"name": name, "why": why, "todo": todo})
    n = len(found)
    level = "danger" if n >= 3 else "careful" if n >= 1 else "safe-looking"
    return level, found

# Practice messages for the quiz: (message, is_scam, explanation)
QUIZ = [
    ("URGENT: Your bank account will be blocked in 2 hours. Click http://bit.ly/xk29 and enter your PIN.", True,
     "Rush + link + asks for PIN. Three red flags."),
    ("Hi Ammi, this is Ali. I am at the shop, my phone broke. This is my new number. Please send Rs 5000 on Easypaisa, do not tell Abbu.", True,
     "New number, money request and secrecy. Call Ali on his OLD number first."),
    ("Your parcel is ready. Please collect it from our office tomorrow. Call 111-xxx-xxx to confirm.", False,
     "No rush, no money, no link. Still, call the courier's official number if unsure."),
    ("Congratulations! You won Rs 50,000 in the BISP lucky draw. Send a Rs 500 processing fee to claim.", True,
     "You cannot win a draw you did not enter, and real prizes never ask for a fee."),
    ("Reminder: your doctor appointment is tomorrow at 5 PM. Reply YES to confirm.", False,
     "Normal reminder. It asks for nothing secret and no money."),
    ("This is FBR. Download AnyDesk so our officer can fix your tax file. Tell no one.", True,
     "Offices never ask you to install remote-control apps or keep things secret."),
]

RULES_OF_THUMB = [
    "STOP: Do not reply or click right away.",
    "THINK: Is it rushing me? Is it asking for money or a code?",
    "CHECK: Call the real number, or ask my family.",
    "A bank will NEVER ask for my PIN or password.",
    "If unsure, do nothing. Nothing bad happens if I wait.",
]
