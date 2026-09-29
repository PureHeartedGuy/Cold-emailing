"""Deterministic checks. These are free, fast and ungameable by judge persuasion.

Each check returns (passed: bool, detail: str). HARD checks zero the case score;
SOFT checks feed the rubric component.
"""

import re

# Word ranges per channel for the primary message body (min, max).
# HARD gate triggers outside [min*0.6, max*1.5]; SOFT check uses the exact range.
WORD_RANGE = {
    "email": (50, 125),
    "linkedin": (40, 90),
    "x": (15, 60),
    "instagram": (15, 60),
    "sms": (15, 45),
}
FOLLOWUP_MAX_WORDS = 60

BANNED_PHRASES = [
    "hope this finds you well", "hope this email finds you", "hope you're doing well",
    "i came across your profile", "i wanted to reach out", "i am reaching out",
    "i'm reaching out to", "in today's fast-paced", "pick your brain",
    "synergy", "synergies", "leverage", "revolutionize", "cutting-edge",
    "game-changer", "unlock your full potential", "streamline your",
    "would you be interested in learning more", "let me know your thoughts",
    "just following up", "just circling back", "touch base",
    "i hope this message", "dear sir", "to whom it may concern",
]
LEGAL_SUFFIX = re.compile(r"\b(LLC|L\.L\.C\.|Inc\.?|GmbH|PLLC|P\.C\.|Ltd\.?|Corp\.?)(?=\W|$)")
URL = re.compile(r"(https?://|www\.)\S+|\b\S+\.(com|io|ai|co|net|org)/\S*", re.I)
UNFILLED = re.compile(r"\[(first ?name|name|company|company name|your name)\]|\{\{\s*(first_?name|company)\s*\}\}", re.I)
STAGED = re.compile(r"sent from my (iphone|android|phone)", re.I)


def words(text: str) -> int:
    return len(re.findall(r"\b[\w'’$%.,-]+\b", text or ""))


def run_checks(case: dict, msg: dict) -> dict:
    """msg = {"subject", "body", "followup"} extracted from the generation."""
    body = msg.get("body") or ""
    subject = msg.get("subject") or ""
    low = (subject + "\n" + body).lower()
    ch = case["channel"]
    lo, hi = WORD_RANGE.get(ch, (40, 125))
    n = words(body)
    hard, soft = {}, {}

    hard["has_body"] = (n >= 5, f"{n} words")
    hard["length_sane"] = (lo * 0.6 <= n <= hi * 1.5, f"{n} words, allowed {int(lo*0.6)}-{int(hi*1.5)}")
    if case["task"] in ("write", "roast") and ch in ("email", "linkedin"):
        hard["no_links"] = (not URL.search(body), "link in first-touch message")
    banned = [p for p in BANNED_PHRASES if p in low]
    hard["no_banned_phrases"] = (not banned, ", ".join(banned))
    hard["no_unfilled_prospect_vars"] = (not UNFILLED.search(body), "unfilled name/company variable")
    hard["no_staged_device_sig"] = (not STAGED.search(body), "fake 'sent from my iPhone'")

    soft["length_in_range"] = (lo <= n <= hi, f"{n} words, target {lo}-{hi}")
    if ch == "email":
        soft["subject_present_short"] = (0 < len(subject) <= 50 and words(subject) <= 7, f"'{subject}'")
        soft["subject_not_salesy"] = (not re.search(r"(opportunit|solution|offer|partnership|quick question|!)", subject, re.I), f"'{subject}'")
    we = len(re.findall(r"\bwe\b|\bour\b|\bus\b", body, re.I))
    i = len(re.findall(r"\bI\b|\bI'm\b|\bI'll\b|\bI'd\b|\bmy\b", body))
    soft["first_person_singular"] = (i >= we, f"I={i} we={we}")
    soft["casual_company_name"] = (not LEGAL_SUFFIX.search(body), "legal suffix left in body")
    soft["no_question_pileup"] = (body.count("?") <= 2, f"{body.count('?')} questions")
    fu = msg.get("followup") or ""
    if fu:
        soft["followup_short"] = (words(fu) <= FOLLOWUP_MAX_WORDS, f"{words(fu)} words")

    return {
        "hard_pass": all(v[0] for v in hard.values()),
        "hard": {k: v for k, v in hard.items()},
        "soft_rate": sum(v[0] for v in soft.values()) / max(1, len(soft)),
        "soft": {k: v for k, v in soft.items()},
    }
