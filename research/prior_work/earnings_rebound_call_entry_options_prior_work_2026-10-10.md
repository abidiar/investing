# Prior-work review — post-earnings recovery call timing and option premium
Review date: 2026-10-10. Question: given quality-qualified sharp post-earnings selloffs, does delaying call entry or buying longer expiry yield economically survivable option performance after premium cost and volatility risk?

## Academic findings
- Truong, Corrado, Chen (2012), "The options market response to accounting earnings announcements," JIMFM: 1996–2008 US options, pre/post earnings implied vol. IV commonly drops across the announcement, with stronger transitory effects for nearer expiries. https://doi.org/10.1016/j.intfin.2012.01.006
- Fink (2021), review of 216 published PEAD papers and 8 working papers: price can drift *in the direction* of earnings surprises; recovery of a negative surprise is not automatic. https://doi.org/10.1016/j.jbef.2020.100446
- Chordia, Goyal, Sadka & Shivakumar (2009), Financial Analysts Journal: earnings-drift paper returns attenuate with liquidity and trading costs; transactions can consume much of a gross edge. https://business.columbia.edu/faculty/research/liquidity-and-post-earnings-announcement-drift
- Wang, Sarath & Rai, study of earnings IV change 1996–2022: approximately a quarter of firms experience rising rather than falling IV after earnings; assuming a universal one-way IV crush is invalid. https://www.researchwithrutgers.org/en/publications/options-market-implied-volatility-and-voluntary-disclosure-manage/

## Exchanges / data vendors / contract mechanics
- OCC: standard equity option generally controls 100 shares, American exercise, adjusted deliverables for splits and special events; simulated European call approximations are not exact equity option valuations. https://www.theocc.com/clearance-and-settlement/clearing/equity-options-product-specifications
- Massive contract OHLC endpoint returns *trade-derived* aggregate prices, NOT exchange-executable opening/closing NBBO. Historical per-contract option bars are available via connected Massive in a pilot; historical bid/ask endpoint /v3/quotes denied by current entitlement. https://massive.com/docs/rest/options/overview and https://www.massive.com/docs/rest/options/trades-quotes/quotes
- Alpaca official docs historical option market data start February 2024, free indicative quotes are not actual OPRA NBBO, and this connected Alpaca tool surface exposes only latest quotes and current snapshots, not historical options read methods. https://docs.alpaca.markets/us/docs/historical-option-data

## Prior Investing OS findings / conflicts
- 164 quality-qualified events, 92 original and 72 company-disjoint contemporary holdout, were previously outcome-inspected. Rising-lows and SMA confirmation had weak/inconsistent gross underlying edge; any new options modeling here is exploratory and must not claim fresh OOS replication.
- Missing data include historical quote spreads, actual contemporaneous IV and smile, open fills, strike listings/adjusted deliverables, dividend early exercise, and event-linked term structure. Historical trade bars alone cannot establish realizable premium ROI.

## Design consequences
- Distinguish ACTUAL option trade prints from THEORETICAL model-based pricing and EXECUTABLE bid/ask results; never blend them.
- Freeze one identical same-event entry comparison, include skipped signals, actual stock-path downside ordering, contract expiry risk and premium loss.
- Model 14/30/45/60/90 days only as hypothetical uniform initial DTE; apply multiple volatility assumptions and post-entry IV drift, spreads, and trade commission sensitivities without picking a favorable scenario post hoc.
- Independently match a modest fixed contract pilot for *observed option OHLC* and explicitly mark quote/fill omissions; any viable candidate requires prospectively recorded executable option quotes and independent event cohort.
- Do not re-test the old stock path/signal search with retuned triggers on the same 164 histories.