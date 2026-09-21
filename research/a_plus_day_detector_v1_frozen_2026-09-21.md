# A+ DAY DETECTOR v1.0 — FROZEN

Frozen: 2026-09-21
Objective: maximize directional precision and abstain aggressively. The detector is NOT designed to produce a trade every day.

## Output states
Exactly one state at each evaluation:
- A+ CALL — TRADE ALLOWED
- A+ PUT — TRADE ALLOWED
- WATCH / DEVELOPING — DO NOT TRADE YET
- NO TRADE

NO TRADE is the default. No setup is guaranteed; A+ means unusually strong evidence and favorable asymmetry.

## Core principle
A large move, gap, futures move, oil move, yield move, earnings beat/miss, Discord alert, or momentum reading cannot independently create A+.

Required causal chain:
MATERIAL NEW INFORMATION -> COHERENT REPRICING -> RTH PRICE ACCEPTANCE -> REMAINING RUNWAY.

Price gets the final vote.

## Hard gates — ALL required
1. MATERIAL DRIVER
A specific material catalyst/information shock must be identifiable and known by evaluation time. Examples: macro data surprise, central-bank/policy surprise, geopolitical shock/de-escalation, material earnings/guidance/read-through, thesis-changing company/sector information. A scheduled event that has not occurred does not count.

2. COHERENT TRANSMISSION
The assets that should react to the driver must actually do so. Use only relevant cross-assets: SPY/QQQ, Treasury yields, oil, VIX, dollar, sector ETFs, peers/leaders, futures and breadth. Do not require every asset to move. Contradictory behavior in the economically important channel blocks A+.

3. EQUITY / LEADERSHIP CONFIRMATION
The relevant index, sector and/or leaders must agree with the thesis. For broad macro A+ days, require credible broad-market participation or expanding breadth. For sector/thesis repricing, narrow breadth is permissible only when the recommended vehicle is explicitly confined to the sponsored sector/leader rather than presented as a broad SPY signal.

4. RTH PRICE ACCEPTANCE
Do not trade the narrative. After the open, price must accept the repricing on M5 structure. Relevant evidence includes VWAP hold/reclaim, accepted breakout/breakdown, constructive higher lows for calls/lower highs for puts, gap survival, failed countertrend repair, persistent RS, and stronger participation in thesis direction. If price rejects the thesis, classification is NO TRADE regardless of catalyst quality.

5. FRESH RUNWAY
At the actual executable trigger there must be a realistic structural destination with current R:R >= approximately 2:1, acceptable ADR/range consumption and no first-wave exhaustion/chase condition. A correct directional thesis with no remaining tradeable runway is NO TRADE.

6. EVENT / DISTORTION / EXECUTION VETO
No unresolved imminent binary event capable of invalidating the trade; account for FOMC/data releases, EIA when oil is the thesis, major scheduled announcements, quarterly expiration/rebalance distortion, closing-auction distortion, abnormal illiquidity, and option-quality problems. If using options, spread/liquidity/IV and realistic contract selection must be acceptable.

## A+ families currently admitted
### A. MACRO REPRICING
Material new macro/geopolitical information -> economically relevant cross-assets reprice coherently -> equities/leadership confirm -> RTH accepts -> runway remains.

Do NOT reduce this to mechanical rules such as oil down + yields down = calls or oil up + yields up = puts. Cause and market interpretation matter.

### B. THESIS-BREAK / THESIS-CONFIRMATION REPRICING
Material company/sector information directly changes or confirms a prevailing market thesis -> peers/sector provide independent confirmation -> opening repricing survives a test/pullback -> sponsorship/RS persists -> runway remains.

A large earnings gap alone is NOT sufficient. Do not chase first-wave extension.

### C. BEARISH FAILED REPAIR
Material negative repricing -> expected reflex bounce/reclaim attempt -> repair fails below important structure/VWAP -> sellers reassert -> downside is reaccepted -> sector/peers remain weak -> fresh downside runway remains.

Do not automatically buy puts into a large gap-down/panic open.

## Directional symmetry, execution asymmetry
Calls and puts are both allowed. However, negative gap events frequently produce reflex bounces, so bearish entries require particular attention to failed repair/reclaim rather than chasing the opening flush.

## State-based timing
Primary workflow:
- PREMARKET: identify A+ CANDIDATE only. No automatic trade.
- 09:50 ET: first actionable confirmation check if the opening test is already mature.
- 10:20 ET: continuation/reconfirmation check and catch setups whose acceptance developed more slowly.

Do not delay an already mature accepted setup merely to wait for 10:20, but do not lower confirmation requirements to enter earlier. Timing is state-based, not momentum-chasing.

## Automatic disqualifiers / NO TRADE
- No identifiable material information shock.
- Normal/mixed session.
- Cross-asset signals materially conflict in relevant channels.
- Price makes lower lows against a CALL thesis or higher highs against a PUT thesis without valid repair/acceptance.
- VWAP/key structure repeatedly fails in thesis direction.
- Relevant leadership/RS deteriorates or contradicts thesis.
- First wave is exhausted / destination largely consumed.
- Current realistic destination R:R < ~2:1.
- Imminent unresolved binary event.
- Triple-witching/rebalance distortion materially contaminates the signal.
- Options are not viable.
- Setup requires explaining away contradictory price action.

## Relationship to existing Investing OS
A+ DAY is a higher-level permission gate, not a replacement for stock selection.

If A+ is not active: WHAT I WOULD ACTUALLY BUY = NO TRADE for this selective workflow.

If A+ is active: existing scanners may select the best vehicle. Preserve hard STRENGTH >=4/5 AND RUNWAY >=4/5 independently, accepted M5 trigger, >=~2:1 current destination R:R, extension/ADR controls, sponsorship, event/macro risk, option quality, T1/reentry, quiet-leader preference, first-wave exhaustion penalty, independent universe rescan, cross-cluster rerank, emerging-cluster promotion, intra-cluster rotation/catch-up, delayed repricing, false-positive control and all NO TRADE rules.

A+ context never adds points to STRENGTH or RUNWAY and cannot rescue a failed stock-level setup.

## Triple witching / rebalance
Preserve standing distortion gate. Triple witching itself is not directional and contributes zero STRENGTH/RUNWAY. Post-OPEX acceptance/rejection remains research context only unless separately validated.

## 4D MR
Frozen 4D Mean-Reversion prior remains supporting context only and cannot create A+ or add STRENGTH/RUNWAY.

## External signals — CROM / Discord
Not part of v1 qualification. CROM/Gerald/Pulse/Alarm/Obizzy/etc. may be displayed as independent corroboration/candidate discovery but cannot promote WATCH/NO TRADE to A+. Their incremental value must be separately validated against A+ states before becoming a hard input.

## Research basis / falsifications preserved
- Late triple-witching direction -> next-session direction did not survive the long historical panel (33/64 = 51.6% in prior work); do not use as directional signal.
- Large earnings gaps alone are insufficient and often fade.
- Immediate gap continuation/chasing is not the target; controlled test + acceptance is preferable.
- Large negative earnings gaps often bounce; bearish execution should wait for failed repair/reacceptance lower.
- Oil/yield direction is context-dependent and cannot mechanically determine equity direction.
- Generic morning momentum is not sufficient; important information + coherent repricing + acceptance is the target.
- June 25, June 29, July 8 and July 17 were useful false-positive examples where strong narratives failed/vetoed confirmation.
- July 30 (MSFT/AI thesis repricing) is the clearest positive development example; July 31 provided supporting independent replication. Do not quote a live win probability from these small samples.

## Anti-overfitting rules
- Do not change these gates because a missed trade later worked.
- Do not use afternoon outcomes to classify a morning state.
- Do not promote a rule based on a tiny winning streak.
- Preserve NO TRADE as a successful outcome when evidence was insufficient.
- Origin/thesis labels must be preserved; do not relabel a failed setup after the fact.
- Historical hit rates are research statistics, never live probabilities without true OOS validation.

## Scheduled workflow specification
The live detector should run on U.S. trading days at:
1. 09:20 ET — PREMARKET CANDIDATE scan. Output CALL CANDIDATE / PUT CANDIDATE / NO A+ CANDIDATE. No trade permission.
2. 09:50 ET — ACTION CHECK. May output A+ CALL / A+ PUT only if every hard gate passes and an executable accepted M5 trigger with fresh runway exists; otherwise WATCH or NO TRADE.
3. 10:20 ET — CONFIRMATION / SECOND-CHANCE CHECK. Independently rescan and re-rank. May promote a developing setup only if all gates now pass. Do not chase a consumed first wave.

Each alert must include: state; origin/family; specific catalyst; causal transmission; SPY/QQQ state; relevant cross-assets; breadth/leadership; price-validation evidence; invalidation; remaining destination/runway; realistic R:R; event/distortion risks; best vehicle(s) only if stock-level gates pass; option viability if suggesting options; and a concise WHY NOW / WHY NOT.

The detector should notify on A+ CALL/A+ PUT. For NO TRADE, provide a concise status at scheduled checks rather than inventing an alternative trade.
