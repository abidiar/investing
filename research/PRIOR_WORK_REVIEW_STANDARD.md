# Investing OS — Prior-Work Review Standard

Status: **MANDATORY PRE-EXPERIMENT STEP**
Effective: 2026-09-19

## Purpose
Before Investing OS spends time designing or running a new experiment, first determine whether the question has already been studied, what is already known, where the evidence conflicts, and what measurement problems are established.

This step exists to avoid duplicating solved work, rediscovering known failure modes, or designing a weaker version of a study that already exists.

## Required sequence
For every new research branch or materially new hypothesis:
1. **Define the question in plain language before searching.** Do not write outcome thresholds yet.
2. **Search prior work before freezing an experiment.** Search academic journals, working papers/preprints, exchange/operator research, regulatory/central-bank research, practitioner research, and reproducible open-source studies.
3. **Create a prior-work note** under `research/prior_work/` before the frozen protocol is written.
4. **Separate evidence by source quality:**
   - peer-reviewed / published academic research;
   - credible working papers / preprints;
   - exchanges, regulators, central banks, and data vendors;
   - practitioner/vendor claims;
   - open-source / community studies.
5. **Record disagreements and data limitations**, not just supportive findings.
6. **Identify what remains unresolved** and state why a new Investing OS test is still useful.
7. Only then write and commit the frozen protocol.

## Minimum contents of every prior-work note
- question / hypothesis family;
- search date;
- key sources and source class;
- what each source actually tested;
- data period, instrument, and horizon when known;
- main result;
- measurement method / sign convention / assumptions when relevant;
- contradictions or replication failures;
- direct implications for our design;
- what we should **not** bother retesting;
- what remains genuinely open;
- proposed new experiment only after the above.

## Design rules
- Existing literature may inform definitions, controls, robustness checks, and economic mechanism **before** our rules are frozen.
- Literature must not be used after our outcome results to justify changing a failed preregistered rule.
- If the exact question is already convincingly answered, default to **replication/incremental-utility testing** rather than pretending the question is novel.
- If existing studies conflict, freeze a design aimed at the source of disagreement: data source, sample period, market structure, sign convention, liquidity state, or horizon.
- Practitioner/vendor claims are hypotheses, not facts, unless independently validated.
- Public open interest must never be described as observed dealer inventory. Any dealer-side sign inferred from OI must be labeled as a model assumption.
- When the literature establishes a known moderator (for example liquidity), decide whether to include it **before** seeing our outcomes.

## Production rule
Prior-work review can improve a hypothesis, but it cannot authorize a scanner change. Production still requires our own frozen decision-level promotion gate when the change affects Investing OS behavior.

## Cross-chat rule
When a future chat says `next experiment`, `test this`, `backtest this`, or proposes a new scanner idea, the bootstrap sequence is now:
1. governance / status recovery;
2. **prior-work review**;
3. freeze protocol;
4. run test;
5. record results in both canonical systems.

No new clean experiment is complete if the prior-work step was skipped without an explicit reason documented in the protocol.
