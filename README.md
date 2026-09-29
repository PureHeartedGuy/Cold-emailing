# Cold outbound skill + self-improving eval loop

This repo turns Nick Saraev's *definitive guide to copywriting for outbound*
([video](https://www.youtube.com/watch?v=uSTGNHGFOAo)) into a Claude skill. It then gives
[karpathy/autoresearch](https://github.com/karpathy/autoresearch) a frozen, hard-to-game metric
so an agent can improve the skill overnight.

```
source/video-notes.md        timestamped study of the full 4h transcript (paraphrased)
scripts/get_transcript.py    downloads the exact transcript locally (not redistributed)
skill/cold-outbound/SKILL.md v0 skill: what the agent edits (autoresearch's train.py)
evals/                       frozen harness (autoresearch's prepare.py): never edited by the agent
  EVALS.md                   the metric, the reasoning behind it, and how to calibrate it
  cases/{dev,holdout}.jsonl  21 + 10 briefs incl. no-proof, fabrication-bait and safety cases
  cases/distractors.json     synthetic competitor emails for the inbox simulation
  checks.py                  deterministic gates
  run_eval.py                prints skill_score (higher is better)
  calibrate.py               correlates the proxy with your REAL reply rates
program.md                   the autoresearch loop instructions for this repo
```

## Quick start
```bash
pip install anthropic youtube-transcript-api
export ANTHROPIC_API_KEY=...
python scripts/get_transcript.py                                  # optional: exact transcript
python evals/run_eval.py --split dev --freeze-baseline            # score v0 and freeze it as the pairwise opponent
python evals/run_eval.py --split dev --reps 3                     # measure noise (σ)
```

Then point Claude Code (or any coding agent) at `program.md`, e.g.
"read program.md and kick off a new experiment, tag oct1", and let it loop.

## Use the skill itself
Copy `skill/cold-outbound/` into `~/.claude/skills/` (or your project's `.claude/skills/`).
Then ask for a cold email, DM, follow-up or roast. Always use the best-scoring version from the
`autoresearch/<tag>` branch.

## The one idea that makes this work
A strong model's v0 skill already scores well on naive "rate 1 to 10" judges, and an optimiser's
easiest path to a higher score is **inventing impressive proof**. So the metric is:

- **multiplicative gates**, including a fabrication audit;
- **binary rubric items**, which show exactly where the skill fails;
- **pairwise wins against frozen v0**, which can't saturate early;
- a **competitive inbox simulation**;
- a **holdout set** and a **noise-aware keep rule**;
- periodic **calibration against real reply rates**.

Details are in [`evals/EVALS.md`](evals/EVALS.md).
