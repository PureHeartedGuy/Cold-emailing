# How the skill is measured (and why it's built this way)

## The problem
autoresearch works because `val_bpb` is cheap, objective and can't be argued with. Copy quality
has none of those properties. Its true metric, **real reply rate**, costs about 500 to 1,000 sends
per variant and a week of waiting (video, 3:31). So we optimise a **proxy**, and the proxy has
to survive three threats:

1. **Ceiling.** v0 is written by a strong model, so a "rate it 1 to 10" judge says 9/10 on day one
   and the loop has nothing to climb.
2. **Reward hacking.** An optimiser discovers that judges love specific numbers, famous clients and
   long, dense copy. The cheapest way to supply those is to **invent them**.
3. **Noise.** LLM judges are stochastic, and a +1.0 "gain" can be pure noise.

## The metric
```
case_score  = GATE × (0.35·RUBRIC + 0.35·PAIRWISE + 0.30·INBOX)      # safety cases: 1/0
skill_score = 100 × mean(case_score)  over evals/cases/dev.jsonl (21 cases)
```

| Component | What it is | Threat it handles |
|---|---|---|
| **GATE (hard, multiplicative)** | Deterministic checks (`checks.py`): length sanity, no links in first touch, no banned/AI phrases, no unfilled `[Name]`, no staged "sent from iPhone". **Plus a fabrication judge**: every claim about the sender or prospect must trace to the brief. Any failure zeroes the case. | Reward hacking. You can't buy score with invented proof or spammy tricks. |
| **RUBRIC** | 18 **binary** criteria, one per principle from the video: P2P frame, opener not salesy, proof-based "who am I", quantified + time-bound + risk-reversed offer, one specific CTA, the 7 influence levers, channel fit, compliance, variant-B divergence, honesty under pressure. Plus deterministic soft checks (subject length, I-vs-we, casual company name...). | Binary items are far more reliable than 1 to 10 scales and tell you *which* rule failed, which gives the agent a gradient. |
| **PAIRWISE** | A judge role-plays the skeptical prospect and picks between the candidate and **frozen v0 output** for the same brief, judged twice with A/B positions swapped. | Ceiling. Relative judgments keep discriminating when absolute scores saturate, and v0 starts at exactly 0.5. |
| **INBOX** | A simulated prospect sees 8 previews (sender, subject, first 110 chars): the candidate plus 7 fixed synthetic cold emails of mixed quality. Do they open it? Then among 4 full bodies, do they reply to it? | Measures the *whole funnel* the video stresses (sender name, subject, teaser, then body), competitively rather than in isolation. |

### Test set design (`cases/`)
- **dev (21)**: channel mix (email, LinkedIn, X, Instagram, SMS); goals (reply, watch, book); regions
  (US/UK/DE for compliance); rich-proof vs **no-proof** senders; thin briefs; true self-disclosure;
  roast-and-rewrite; follow-up; **fabrication bait** (a user asks to invent clients); and one
  **safety** case (a grey-hat request).
- **holdout (10)**: the same distribution with different people and niches, a CASL region, and a
  second bait and safety case. The agent only ever sees its aggregate score, every 5 keeps.
  If dev climbs while holdout falls, it's overfitting, so revert.
- `distractors.json`: 7 synthetic competitor emails, from awful to genuinely good (#3 and #7 are
  strong). A skill only "wins the inbox" by beating good copy, not strawmen.

## Keep/discard rule (in `program.md`)
- Measure σ once with `--reps 3` on v0. Keep a change only if Δ ≥ max(1.0, 2σ), gate rate
  didn't drop, and no safety case regressed.
- **Simplicity**: under +2 points while adding more than 150 words means discard. Equal score with
  fewer words means keep (autoresearch's own rule).
- The agent may not edit `evals/`, copy case facts into the skill, or weaken §1 non-negotiables.

## Grounding the proxy in reality (do this, it's the part people skip)
The proxy is only worth optimising if it **ranks messages the way your market does**.
1. **Calibrate before trusting.** Export ≥ 8 past variants with ≥ 300 sends each, then run
   `python evals/calibrate.py history.csv`.
   - Spearman ρ ≥ 0.5: trust it.
   - ρ between 0.2 and 0.5: re-weight toward whichever component correlates.
   - ρ < 0.2: the judges don't know your market. Edit the rubric/persona first. That's a human
     edit, never the agent's.
2. **Close the loop weekly.** Every Sunday (the video's cadence), take the top 2 skill versions from
   results.tsv and generate real campaigns with each. Send 500 to 1,000 per variant through Instantly
   or Smartlead and record reply rate.
3. **Promote real results into the eval.** Add each real campaign as a new case and re-run calibrate.
   Over time the proxy converges on *your* ICP instead of a generic judge's taste.

The proxy decides which skill *candidates* you test. The market decides which one you keep.

## Cost and runtime (estimate, not measured)
Per dev run: about 21 generations plus about 6 judge calls per case, so roughly 150 calls. With
Opus 5.5 as generator and judge at medium effort, expect a few dollars per run and a few minutes
wall-clock with 8 workers. Overnight that's about 60 to 100 experiments. To cut cost:
- set `JUDGE_MODEL=claude-sonnet-5-5` for extraction/inbox only (edit the calls, not mid-run);
- or run the whole thing with `GEN_MODEL=claude-sonnet-5-5` if that's the model your skill will
  actually run on.

Generator and judges must stay fixed within a run, or scores aren't comparable.

## Known limitations
- The judges are Claude; so is the generator. Self-preference bias is partly cancelled because both
  pairwise sides come from the same generator, but a second judge family would be stronger.
- 21 dev cases give coarse resolution (one case ≈ 4.8 points). Add cases from your real ICP; aim for
  40 or more.
- The inbox simulation can't model deliverability (spam folders, domain health). That lives outside
  the copy.
