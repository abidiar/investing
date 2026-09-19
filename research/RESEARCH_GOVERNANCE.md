# Investing OS Research Governance

Status: **CANONICAL OPERATING RULE**
Effective: 2026-09-19

## Purpose
This file defines how Investing OS research must be handled across chats, tools, notebooks, GitHub work, Google Drive work, and scanner-development sessions. The goal is to prevent duplicated experiments, hindsight tuning, lost findings, scanner drift, and unnecessary re-discovery of work already done elsewhere.

## Source-of-truth hierarchy
1. **GitHub reproducible scientific record** — `abidiar/investing/research/`
   - prior-work reviews: `research/prior_work/`
   - frozen protocols: `research/*.md`
   - executable tests: `research/run_*.py`
   - reproducible outputs: `research/results/`
   - topic status/index files such as `research/options_positioning_research_status.md`
2. **Google Doc human-readable canonical ledger** — `Investing OS Research Ledger — Canonical`
   - document ID: `1MxHv5HPlr1Ab9A8cb3diPUtBJv6fWgNZwhhrw72zAus`
   - this is the cross-chat summary and handoff document.
3. **Investing OS Intelligence Engine Google Sheet** — live implementation/runtime record, not the scientific source of truth.
   - spreadsheet ID: `14lTnD-on91I4F5E5FAQ8-39zTRv2GzBjyd1b4_uCzjc`

When records disagree, the frozen GitHub protocol + committed result files control the scientific verdict. The Google Doc should be brought back into sync immediately.

## Mandatory workflow for every research experiment
Before starting any Investing OS experiment in any chat or work session:
1. Read this governance file.
2. Read the relevant topic status/index file and the Google Doc canonical ledger.
3. Check **Do Not Re-Test Unless** sections before proposing another test.
4. **Run a prior-work review before freezing the experiment.** Follow `research/PRIOR_WORK_REVIEW_STANDARD.md`. Search academic research, working papers, exchange/regulatory/operator research, practitioner/vendor research, and reproducible open-source work. Record the review under `research/prior_work/`.
5. State what is already known, what conflicts, what measurement problems are established, what should not be retested weakly, and what genuinely remains open.
6. Write and commit a frozen protocol **before** looking at outcome results. The protocol must state hypothesis, data/sample, exact definitions, thresholds, controls, outcomes, robustness tests, promotion gates, and what may not be changed after results.
7. Run the exact frozen test. Do not alter rules because the result is inconvenient.
8. Save reproducible code and machine-readable outputs in GitHub.
9. Save a readable result summary with one explicit verdict: SUPPORTED / CONDITIONAL / RESEARCH-ONLY / FAILED / FAILED REPLICATION / NOT SUPPORTED, or another predeclared status.
10. Update the relevant master status/index file, including failed and falsified ideas.
11. Update the Google Doc canonical ledger with the result, production implication, and next clean falsification.
12. Only after steps 1–11 may a finding be considered for scanner/runtime changes.

## Prior-work discipline
- The prior-work stage happens **before** protocol freezing, not after outcomes are known.
- Existing literature may improve our definitions, controls, data choices, moderators, and falsification design.
- If the exact question is already convincingly answered, default to **replication or incremental-utility testing**, not rediscovery.
- If prior studies conflict, freeze a test aimed at the disagreement: data source, sample, market structure, sign convention, liquidity, horizon, or measurement method.
- Practitioner/vendor claims are hypothesis-generating unless independently validated.
- A literature result cannot rescue a failed Investing OS promotion gate after the fact.

## Scanner-change discipline
A research finding may affect production only if its frozen promotion standard passes. A statistically interesting relationship is not enough. Any production change must state:
- exactly what scanner field/rule changes;
- whether direction, Strength, Runway, R:R, action state, target, chase filter, option selection, or overnight logic changes;
- the evidence and frozen gate that authorized the change;
- rollback criteria.

If a result is research-only, it must not silently leak into production logic.

## Anti-moving-goalpost rules
- No threshold tuning after viewing outcomes unless a brand-new exploratory study is explicitly labeled as such and later retested on untouched data.
- No reclassifying failed promotion gates after the fact.
- No dropping bad years/instruments/events because they hurt the result unless exclusion was preregistered.
- No using Day-T+1/future information as a Day-T feature.
- No treating missing data as favorable evidence.
- Independent replication should use a non-overlapping period, different instrument, different provider, or materially independent sample whenever possible.

## Required experiment record
Every frozen experiment should preserve:
- experiment ID/name and date frozen;
- prior-work review path and date;
- research question and economic mechanism;
- what prior work already established and what remains open;
- baseline/control model;
- treatment/overlay model;
- dataset/provider and known limitations;
- sample period and universe;
- exact feature definitions;
- exact outcome definitions;
- thresholds and gates;
- primary/secondary/robustness tests;
- results with sample sizes;
- verdict;
- production implication;
- Do Not Re-Test Unless condition;
- next clean falsification.

## Standing production principles
- **Price gets final vote.**
- Supporting research overlays cannot manufacture direction, Strength, Runway, or R:R unless a frozen production promotion specifically authorizes it.
- Options positioning/OI/gamma is context-only unless and until a particular decision rule passes its preregistered promotion gate.
- Quarterly expiration / rebalance risk must be surfaced prominently and cannot be ignored when evaluating late-day structure or fresh directional options.
- Failed ideas remain documented; they are not erased.

## Cross-chat bootstrap rule
If a future chat says `continue Investing OS research`, `next clean experiment`, `scanner research`, `test this`, `backtest this`, or otherwise resumes this project, first recover the current state from:
1. `research/RESEARCH_GOVERNANCE.md`
2. the relevant topic status file(s)
3. the Google Doc `Investing OS Research Ledger — Canonical`
4. the latest prior-work review relevant to the question, or create one if the branch is new
5. the latest frozen protocol/result files relevant to the question.

Do not rely on conversational memory alone when these artifacts are available.

## Update obligation
Every completed clean experiment must update both:
- the GitHub topic status/index; and
- the Google Doc canonical ledger.

Every new research branch must also have a prior-work review before the first frozen outcome test.

This dual-update rule and prior-work requirement are part of the experiment completion criteria, not optional documentation work.
