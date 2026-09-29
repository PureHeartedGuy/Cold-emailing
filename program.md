# autoresearch: cold-outbound skill

This adapts karpathy/autoresearch to a prompt artifact. Instead of improving `train.py`
against `val_bpb`, you improve a Claude skill against `skill_score`.

| autoresearch | here |
|---|---|
| `train.py` (the only file you edit) | `skill/cold-outbound/` (`SKILL.md` + optional `references/*.md`) |
| `prepare.py` (frozen data + eval) | `evals/` (cases, checks, judges, `run_eval.py`). **Never edit.** |
| `val_bpb`, lower is better | `skill_score`, **higher is better** (0 to 100) |
| 5-minute training budget | fixed eval: same cases, same generator and judge models, same effort |

## Setup
1. Agree on a run tag (e.g. `oct1`). Create the branch `autoresearch/<tag>` from the current main.
2. Read `README.md`, `source/video-notes.md` (the domain knowledge), `evals/EVALS.md` (how you're scored) and `skill/cold-outbound/SKILL.md`.
3. Check that `ANTHROPIC_API_KEY` is set and `pip install anthropic` has been run.
4. If `runs/baseline_dev.json` doesn't exist, run `python evals/run_eval.py --split dev --freeze-baseline > run.log 2>&1`. This freezes v0's outputs as the pairwise opponent.
5. **Measure noise**: `python evals/run_eval.py --split dev --reps 3 > run.log 2>&1`. Record `skill_score` as the baseline and `score_stdev` as σ. Create `results.tsv` with the header below plus the baseline row.

## Experiment loop (LOOP FOREVER)
1. Read the latest `runs/*_dev.json`. Find the **lowest-scoring cases and the failing rubric items and checks**. Form ONE hypothesis about the skill text that would fix a *class* of failures, not a single case.
2. Edit the skill and `git commit` with a one-line hypothesis.
3. `python evals/run_eval.py --split dev > run.log 2>&1`, then `grep "^skill_score:\|^gate_pass_rate:\|^skill_words:" run.log`.
4. **Keep** only if *all* of these hold:
   - `skill_score` ≥ best + max(1.0, 2σ). If a single run clears the bar by less than 3σ, re-run with `--reps 2` and use the mean.
   - `gate_pass_rate` didn't drop.
   - No safety case (`d21`) regressed.
   - **Simplicity rule**: a gain under 2 points that adds more than 150 words to the skill → discard. An equal score with fewer words → keep.
5. Otherwise run `git reset --hard HEAD~1`.
6. Log to `results.tsv` (tab-separated, untracked): `commit	skill_score	gate_rate	words	status	description`.
7. **Every 5 kept commits**, run `python evals/run_eval.py --split holdout > holdout.log 2>&1` and log it with status `holdout`. If holdout fell more than 2 points below its best while dev rose, you're overfitting dev. Revert to the best-holdout commit and change strategy. **Never open `runs/*_holdout.json`.** Only the aggregate is yours to see.

## What you CAN change
Anything in `skill/cold-outbound/`: structure, rules, examples, ordering, emphasis, and adding or removing reference files. The best levers are usually clearer decision rules, better worked examples (invented and clearly synthetic), and deleting instructions that don't pay for themselves.

## What you CANNOT do
- Edit anything in `evals/`, the models, or the effort settings.
- Put eval case content (names, companies, facts from `evals/cases/*`) into the skill. That's overfitting and is treated as a failed experiment.
- Weaken the non-negotiables in SKILL.md §1: no fabrication, legal compliance, refusing grey-hat tactics. These encode the user's values, not score levers.
- Add instructions that target the judges ("the reviewer prefers...") instead of the reader.

## Idea bank (when stuck)
Re-read `source/video-notes.md` for principles the skill underuses. Try:
- worked before/after examples
- a tighter length target
- subject-line formulas
- cold-read patterns for thin briefs
- offer sizing relative to prospect scale
- better handling of no-proof senders
- stronger variant-B divergence
- a shorter skill overall
- moving rarely needed material into `references/`

Combine previous near-misses.

**NEVER STOP** until the human interrupts you. The human may be asleep.
