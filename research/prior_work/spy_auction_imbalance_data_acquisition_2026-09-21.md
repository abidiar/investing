# SPY Auction-Imbalance Data Acquisition Review

Date: 2026-09-21
Status: **DATA-PATH REVIEW COMPLETE / AUTHENTICATED DATABENTO PILOT REQUIRED NEXT**

## Objective
Identify the cheapest clean path to historical NYSE Arca closing-auction imbalance data for SPY, with paired quantity and imbalance fields sufficient to test whether the post-August-2024 closing-auction regime differs mechanically from the prior regime.

## Free NYSE path

NYSE publishes free sample files for TAQ NYSE Arca Order Imbalances. The current public sample directory exposes full exchange-wide files for 2026-04-01 and 2026-04-02.

The public NYSE TAQ specification confirms that Arca imbalance messages include the fields needed for the mechanism test:
- SourceTime
- Symbol
- ReferencePrice
- PairedQty
- TotalImbalanceQty
- MarketImbalanceQty
- AuctionTime
- AuctionType
- ImbalanceSide

The NYSE historical product page states that TAQ NYSE Arca Order Imbalances are available historically from 2012-01-30 onward.

Conclusion: the free sample files validate the schema and file class, but do not supply the quarterly-expiration dates needed for the research panel.

## Databento path

Dataset:
- `ARCX.PILLAR`
- Venue: NYSE Arca
- Historical coverage begins 2018-05-01, with historical schema availability varying by schema.

Relevant schema:
- `imbalance`

Databento's normalized Arca imbalance fields include:
- `ref_price`
- `ind_match_price`
- `paired_qty`
- `total_imbalance_qty`
- `market_imbalance_qty`
- `auction_type`
- `side`
- `auction_status`
- `freeze_status`
- `significant_imbalance`
- collars and additional venue-specific auction fields

Databento explicitly documents SPY on NYSE Arca in its auction-imbalance example, using `ARCX.PILLAR` + `imbalance`.

Historical data is available usage-based with no subscription required. Databento advertises new-user historical credits and exposes authenticated metadata methods to estimate request cost before downloading:
- `Historical.metadata.get_record_count(...)`
- `Historical.metadata.get_billable_size(...)`
- `Historical.metadata.get_cost(...)`

Exact request-level cost cannot be obtained from the public web pages alone because Databento's cost estimator requires an authenticated API key/account.

## Clean pilot

Do not download the full expiration panel before freezing the mechanism metric.

Pilot dates are chosen for structure validation only, not based on outcomes:
- 2023-09-15 — ordinary pre-change quarterly expiration
- 2024-06-21 — last quarterly expiration before the August-2024 auction change and a known miss in the price-only rule
- 2024-09-20 — first quarterly expiration after the August-2024 change
- 2025-03-21 — post-change quarterly expiration

Pilot request:
- dataset: `ARCX.PILLAR`
- symbol: `SPY`
- schema: `imbalance`
- time window per date: 15:30:00 ET through 16:00:01 ET
- output: DBN or CSV
- include only closing-auction records (`auction_type == 'C'`)

Before retrieval, call `get_cost` for each pilot window and record the estimated total.

## Candidate mechanics to inspect during pilot

The pilot is for field behavior and measurement reliability only. Do not test outcome separation yet.

Potential variables:
1. Paired-quantity growth from first closing-auction message to final pre-close message.
2. Absolute imbalance / paired quantity ratio.
3. Imbalance-side persistence vs side flips.
4. Indicative-match-price displacement from reference price.
5. Convergence of indicative match price toward the final close.
6. Timing of major jumps in paired quantity.
7. Significant-imbalance flag behavior where historically available.
8. Final auction imbalance relative to earlier 15:50/15:55 states.

After inspecting the pilot, freeze a small set of mechanically interpretable regime metrics before retrieving the remaining quarterly-expiration events.

## Current blocker

No Databento connector/plugin is available in the current tool environment. Databento's authenticated Historical API requires the user's own account/API key. Do not request that the user paste an API key into chat.

The next operation requires the user to authenticate with Databento outside the chat and either:
- make the narrowly scoped pilot download and provide the resulting file, or
- make the authenticated cost-estimate/API result available through a connected environment.

## Decision
- Do not buy NYSE TAQ yet.
- Do not subscribe to Webull LV2 for this historical experiment.
- Databento historical ARCX.PILLAR imbalance data is the preferred route.
- Freeze measurement logic only after a four-date pilot confirms consistent field behavior.
