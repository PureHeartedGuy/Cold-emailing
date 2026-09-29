"""Check that the proxy metric tracks REAL reply rates before trusting an overnight run.

Input CSV (your own campaign history; ≥ 8 variants, each with ≥ 300 sends):
    variant_id,channel,region,prospect_role,subject,body,sends,replies

    python evals/calibrate.py my_campaigns.csv

Output: Spearman rank correlation between judge score and observed reply rate, per component.
Rule of thumb: rho ≥ 0.5 → trust the proxy; 0.2-0.5 → keep the loop but re-weight toward the
components that correlate; < 0.2 → the judges don't know your market, so fix the rubric before optimizing.
"""

import csv
import json
import random
import statistics
import sys

from run_eval import CASES, RUBRIC, judge_inbox, judge_rubric


def rank(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    for pos, i in enumerate(order):
        r[i] = pos
    return r


def spearman(a, b):
    ra, rb = rank(a), rank(b)
    return statistics.correlation(ra, rb)


def main(path):
    rows = list(csv.DictReader(open(path)))
    distractors = json.loads((CASES / "distractors.json").read_text())
    rub_s, inbox_s, real = [], [], []
    for row in rows:
        case = {"id": row["variant_id"], "task": "write", "channel": row["channel"], "goal": "reply",
                "region": row["region"], "offer": "", "tags": [],
                "sender": {"name": "Sender", "does": "", "proof": [], "disclosures": []},
                "prospect": {"name": "the prospect", "role": row["prospect_role"], "company": "their company", "facts": []}}
        msg = {"subject": row["subject"], "body": row["body"], "followup": ""}
        rub = judge_rubric(case, row["body"], msg)
        rub_s.append(sum(bool(rub[k]) for k in RUBRIC) / len(RUBRIC))
        inbox_s.append(statistics.mean(judge_inbox(case, msg, distractors, random.Random(i)) for i in range(3)))
        real.append(int(row["replies"]) / max(1, int(row["sends"])))
    print(f"n={len(rows)}")
    print(f"spearman(rubric, reply_rate) = {spearman(rub_s, real):.2f}")
    print(f"spearman(inbox,  reply_rate) = {spearman(inbox_s, real):.2f}")
    combo = [0.5 * r + 0.5 * i for r, i in zip(rub_s, inbox_s)]
    print(f"spearman(combo,  reply_rate) = {spearman(combo, real):.2f}")


if __name__ == "__main__":
    main(sys.argv[1])
