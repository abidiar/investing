# Investing OS Research — Options Positioning / Dealer Structure v1.0

Status: FROZEN FOR FALSIFICATION
Frozen: 2026-09-19

## Question
Can options-positioning and dealer-structure data improve Investing OS by forecasting whether an already-confirmed price move is more likely to amplify, dampen, pin, or become unstable — without using raw open interest as a directional signal?

## Core hypothesis
Options positioning is primarily a market-behavior / structural-destination overlay, not an independent directional predictor.

- Negative dealer gamma should be associated with larger subsequent realized moves and, conditional on an existing price trend, greater continuation risk/opportunity.
- Positive dealer gamma should be associated with smaller / more damped subsequent moves and greater mean-reversion / chop risk.
- Neutral / near-flip states should be treated as unstable rather than directionless.
- Raw OI alone should have no directional authority.
- OI change, persistence, proximity, DTE, and gamma-weighted concentration may add information in later tests.
- Expiration/rebalance state is a separate risk gate and may distort price/volume even when gamma levels themselves are well defined.

## Frozen rules — v1.0

### Information hierarchy
1. Price structure / confirmation remains primary. Price gets final vote.
2. Options positioning may modify expected move behavior, structural destinations, and risk.
3. Options positioning may not independently choose bullish/bearish direction.
4. It may not add points to STRENGTH or RUNWAY, manufacture R:R, override event risk, or excuse extension/chase.

### Frozen fields
- RAW OI
- 1-day delta OI
- POSITION PERSISTENCE = delta OI relative to same-contract daily volume (descriptive; direction not inferred from sign alone)
- DISTANCE FROM SPOT = absolute strike distance, also normalized where possible
- DTE
- GAMMA-WEIGHTED OI / gamma concentration
- NET GEX
- GAMMA REGIME = POSITIVE / NEGATIVE / NEUTRAL
- ZERO-GAMMA FLIP
- CALL WALL
- PUT WALL
- OPEX / TRIPLE-WITCHING / REBALANCE STATE
- subsequent price reaction

### Frozen interpretation
- NEGATIVE GAMMA = AMPLIFICATION RISK / OPPORTUNITY only after independent price confirmation.
- POSITIVE GAMMA = DAMPING / MEAN-REVERSION TENDENCY; apply caution to extended continuation entries.
- NEUTRAL = UNSTABLE / FLIP-ADJACENT; no directional edge.
- Walls are zones, not exact penny levels.
- Gamma flip is the least precise level and must be treated as a zone.
- Raw OI does not identify dealer side or customer intent.

### Frozen exploratory thresholds for Pass 1
- Meaningful current-day price move: |open-to-close return| >= 0.25%.
- Near gamma flip: absolute spot-to-flip distance <= 0.50%.
- GEX regime uses the source's published positive / negative / neutral label; no reclassification.
- Do not optimize these thresholds on Pass-1 outcomes.

## Data — Pass 1
Dealer structure: SquawkFlow open SPX gamma dataset (`dhawalc/spx-gamma-levels`).
- Full-chain SPX GEX, gamma flip, call wall, put wall, gamma regime.
- OI is prior-session settled data; dealer side is a standard convention / model assumption, not directly observed.
- Exclude early low-coverage rows where `contracts_analyzed` was only ~3k versus the mature ~19k–21k chain.

Price outcomes: SPY daily bars, using the next trading session after each positioning observation.

Usable sample: 35 sessions, 2026-07-30 through 2026-09-17. 2026-09-18 excluded because the following session had not yet occurred. This is a calibration / falsification sample, not final out-of-sample proof.

## Outcome metrics
- next-session close-to-close return
- next-session absolute close-to-close move
- next-session high-low range as % of prior close
- next-session opening gap
- next-session open-to-close return
- same-direction continuation when current-day |open-to-close| >= 0.25%

## Pass-1 results

### A. Gamma regime vs next-session movement

| Regime | n | Avg next C/C | Median next C/C | Avg |C/C| | Median |C/C| | Avg H-L range | Up rate |
|---|---:|---:|---:|---:|---:|---:|---:|
| NEGATIVE | 8 | +0.300% | +0.281% | 0.627% | 0.570% | 0.803% | 50.0% |
| NEUTRAL | 4 | +0.011% | -0.289% | 0.730% | — | 0.731% | 50.0% |
| POSITIVE | 23 | +0.013% | -0.171% | 0.455% | 0.396% | 0.614% | 39.1% |

NEGATIVE vs POSITIVE:
- average absolute next-session move: +0.172 percentage points larger in negative gamma (0.627% vs 0.455%)
- average next-session high-low range: +0.189 points larger (0.803% vs 0.614%)
- direction was not predicted: negative-gamma up rate was 50%

Statistical checks were not significant at conventional levels in this small sample (Welch t approximately p=0.26 for absolute return and p=0.32 for range; Mann-Whitney approximately p=0.19 and p=0.64 respectively). Result is suggestive, not established.

### B. Conditional continuation after a meaningful current-day move
Current-day meaningful move was frozen at |open-to-close| >= 0.25%.

- NEGATIVE gamma: n=4; same-direction next-close continuation 75% (3/4); average next absolute move 0.831%.
- POSITIVE gamma: n=14; continuation 42.9% (6/14); average next absolute move 0.444%.
- Fisher exact p approximately 0.58 because the sample is tiny.

Interpretation: promising as a continuation / amplification modifier after price has already chosen direction; not enough evidence to promote to an action gate.

### C. Gamma-flip proximity
Frozen exploratory threshold: <=0.50% from spot.

- Near flip: n=17; average absolute next C/C move 0.589%; average range 0.677%; average next gap 0.133%.
- Farther from flip: n=18; average absolute next C/C move 0.465%; average range 0.665%; average next gap 0.069%.

Interpretation: near-flip state may be associated with somewhat larger close-to-close instability, but not materially larger intraday high-low range in this sample. Keep as WATCH / descriptive context only.

### D. Wall proximity
A broad nearest-wall proximity check did not show a useful next-session edge in this sample:
- <=1% from nearest wall: n=10; average absolute next move 0.502%; average range 0.696%.
- >1%: n=25; average absolute next move 0.535%; average range 0.661%.

Interpretation: wall proximity alone is NOT promoted.

## Pass-1 verdict
SUPPORTED, PROVISIONALLY:
- GEX regime appears more useful for expected move behavior than for direction.
- Negative gamma deserves an AMPLIFICATION RISK / OPPORTUNITY tag when price already confirms direction.
- Positive gamma deserves a DAMPING / CHOP / MEAN-REVERSION tendency tag, especially for extended continuation entries.

NOT SUPPORTED / NOT PROMOTED:
- directional prediction from raw GEX sign
- raw OI as bullish/bearish signal
- wall proximity alone as a next-session signal
- exact gamma-wall / flip price precision

UNRESOLVED:
- delta OI
- delta OI / volume persistence
- gamma-weighted OI concentration by expiry bucket
- 0DTE vs 1–7D vs 8–30D differences
- whether the module improves Investing OS price-only decisions on untouched events

## Scanner impact after Pass 1
Do NOT change STRENGTH, RUNWAY, R:R, or action-state gates yet.

Allow only compact supporting tags:
- GAMMA REGIME: POSITIVE / NEGATIVE / NEUTRAL
- OPTIONS STRUCTURE: DAMPENING / AMPLIFYING / UNSTABLE
- GAMMA FLIP: distance as a zone, not an exact trigger
- OPEX DISTORTION: LOW / MODERATE / HIGH

Price confirmation remains mandatory. No options-positioning input may independently create BUY, SELL, CALL, PUT, HOLD, or overnight-carry authorization.

## Next clean falsification
Run the frozen rules on an untouched sample with contract-level daily OI + volume + gamma. Use only information actually available before the tested next session. Test whether delta OI / volume persistence and gamma concentration improve a price-only baseline. No threshold changes before that result.

Candidate data path identified: daily post-close QQQ chain snapshots with strike, type, volume, OI, and IV; because settled OI is once-daily, date-t chain data must predict t+1, never be treated as same-day intraday OI.

## Do Not Re-Test Unless
- a materially larger untouched sample becomes available;
- contract-level settled OI / volume can be added without lookahead;
- expiry-bucket construction is changed in advance; or
- the source methodology materially changes.
