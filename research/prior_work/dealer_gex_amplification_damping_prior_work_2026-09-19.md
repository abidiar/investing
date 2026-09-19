# Prior-Work Review — Signed / Modelled Dealer GEX Amplification vs Damping

Search date: **2026-09-19**
Status: **PRIOR-WORK REVIEW COMPLETE; EXPERIMENT NOT YET FROZEN**

## Question family
Can dealer gamma positioning, with direction supplied independently by price, help distinguish an **amplifying / momentum-prone** intraday environment from a **dampening / reversal-prone** environment?

This is distinct from the unsigned-gamma work. The question is about the **sign and inventory state** of the hedger/dealer book, not simply where theoretical gamma is concentrated.

## Bottom line from existing work
The broad economic mechanism is **not novel**. Multiple academic and institutional studies already support some version of:
- negative / short dealer gamma -> hedging in the direction of the underlying move -> greater momentum / amplification / volatility;
- positive / long dealer gamma -> hedging against the move -> more reversal / damping / lower volatility.

Therefore the next Investing OS study should **not** ask the weak question `does signed gamma matter at all?`.

The open questions for us are:
1. Can we measure dealer sign credibly with data we can actually obtain?
2. Does the relationship survive modern SPX/SPY/QQQ market structure, especially 0DTE?
3. Does it add decision value beyond price, volatility, liquidity, and trend state?
4. Is the effect useful as a **regime/amplitude modifier**, not as independent direction?

## Key prior work

### 1. Barbon & Buraschi — *Gamma Fragility* (working paper, 2020/2021)
Source class: academic working paper.

They document a link between aggregate dealer/hedger gamma imbalance and intraday momentum/reversal. Negative ex-ante gamma imbalance interacting with illiquidity is associated with intraday momentum; positive gamma with reversal. The effect is stronger in less-liquid underlyings and helps explain intraday volatility/autocorrelation and flash-crash behavior.

Important design implication: **liquidity is a preregistered moderator**, not an afterthought. A serious replication should either control for liquidity or explicitly interact gamma state with liquidity.

### 2. Baltussen, Da, Lammers & Martens — *Hedging demand and market intraday momentum*, Journal of Financial Economics (2021)
Source class: peer-reviewed academic research.

Across more than 60 futures markets, short-gamma hedging demand is linked to trading in the direction of price moves and to intraday momentum, especially late in the session. The work links a broad intraday-momentum phenomenon to gamma hedging demand from options and leveraged products.

Important design implication: the most defensible outcome is **intraday continuation/reversal after an independently observed price impulse**, not next-day directional forecasting.

### 3. Anderegg, Ulmann & Sornette — *The impact of option hedging on the spot market volatility*, Journal of International Money and Finance (2022)
Source class: peer-reviewed academic research.

They model and empirically estimate option-market-maker delta-hedging feedback in FX. Negative market-maker gamma increases spot volatility; positive gamma decreases it, at daily and intraday frequencies.

Important design implication: the gamma mechanism is plausibly cross-asset, but the strength of the effect depends on market liquidity and the size of hedge flow relative to the underlying market.

### 4. Dim, Eraker & Vilkov — *0DTEs: Trading, Gamma Risk and Volatility Propagation* (working paper, revised 2025)
Source class: academic working paper.

For S&P 500 0DTE options, market-maker inventory gamma is on average positive and is negatively related to future intraday volatility. Positive gamma is associated with stronger intraday reversal; negative gamma with momentum. Their evidence is presented as consistent with delta hedging rather than information-based trading.

Important design implication: modern 0DTE data directly supports the **damping vs amplification** framing, but not a directional forecast.

### 5. Adams, Fontaine & Ornthanalai — *The Market for 0DTE: The Role of Liquidity Providers in Volatility Attenuation* (working paper, revised 2025)
Source class: academic working paper / central-bank affiliated research.

Using 2019–2023 intraday option data and exogenous variation in expiration days, they find 0DTE market-maker intermediation lowers S&P 500 volatility on average. A key mechanism is that dealers absorb longer-dated customer positions that later become 0DTE; hedging those expiring positions generates futures order flow that dampens volatility.

A later combined paper by Adams, Dim, Eraker, Fontaine, Ornthanalai & Vilkov (2025/2026) similarly reports that 0DTE presence dampens volatility and that intraday variation in market-maker hedging needs predicts more order-flow reversal, lower momentum returns, and lower volatility.

Important design implication: do not focus only on same-day **0DTE trading volume**. Existing positions that age into 0DTE can matter more than same-day flow.

### 6. Cboe — *0DTEs Decoded: Positioning, Trends, and Market Impact* (2025)
Source class: exchange/operator research.

Cboe reports that customer 0DTE activity is highly balanced and estimates net market-maker gamma hedging from 0DTE activity at only about 0.2% of daily SPX liquidity at most.

Important design implication: a large gross 0DTE volume number does **not** imply large net hedge pressure. We need net positioning / inventory or a defensible proxy, plus a hedge-flow-to-liquidity normalization.

### 7. OptionMetrics practitioner research — gamma imbalance / DOOD
Source class: data-vendor practitioner research.

OptionMetrics has emphasized that aggregate GEX alone can be misleading because the same net gamma sign can arise from different call/put inventory compositions. Their DOOD framework combines signed option flow/delta information with GEX and finds materially different behavior for long-call, long-put, short-call and short-put dealer environments.

Important design implication: if possible, dealer-side sign should come from **signed trade/inventory information**, not a crude call-positive/put-negative OI rule alone. Composition may matter beyond net GEX.

### 8. Ni, Pearson & Poteshman — *Stock price clustering on option expiration dates*, Journal of Financial Economics (2005)
Source class: peer-reviewed academic research.

They find stock prices cluster at option strikes on expiration dates, with evidence that market-maker hedge rebalancing contributes.

### 9. Golez & Jackwerth — *Pinning in the S&P 500 Futures*, Journal of Financial Economics (2012)
Source class: peer-reviewed academic research.

They document expiration-day pinning/anti-pinning effects in S&P futures linked to hedge rebalancing and time decay.

### 10. Modern wall/pinning falsifications
Source class: recent preregistered / working-paper research.

A 2026 preregistered SPY study by Rees Popovici reports no reliable strike-local support/resistance, pinning, or volatility-dampening advantage of the largest GEX wall versus nearby high-GEX controls. A separate 2026 study of 2016–2025 expiration dynamics reports no modern pinning and argues the regime may have shifted from old expiration mechanics.

Important design implication: **do not make exact wall / strike-local pinning our next priority**. The stronger literature-backed question is market-wide regime behavior.

## Measurement problem: the main issue
Public open interest does not identify dealer inventory. Every open contract has a long and a short. Therefore:

**Preferred hierarchy**
1. observed dealer/customer inventory or exchange participant-class data;
2. signed trade-flow / buy-sell classification combined with Greeks;
3. a published inventory proxy validated against participant data;
4. OI-based dealer sign convention only as a clearly labelled model assumption.

Any OI-based GEX model must explicitly state the sign convention. Calls-positive / puts-negative (or the inverse) is an **inventory assumption**, not a Greek identity.

## What existing work tells us not to retest weakly
- Do not test `large GEX wall = automatic support/resistance/magnet` as the main hypothesis.
- Do not infer direction from GEX sign alone.
- Do not use raw OI as observed dealer position.
- Do not treat 0DTE gross volume as net hedging demand.
- Do not ignore liquidity: prior work repeatedly suggests hedge impact depends on the size of hedge demand relative to underlying liquidity.
- Do not pool positive and negative dealer gamma and only ask whether `more gamma` predicts range; that belongs to the already-completed unsigned-gamma branch.

## What remains genuinely useful for Investing OS
A good Investing OS replication should ask an **incremental decision question**:

> Given an independently confirmed price impulse, does a credible dealer-gamma state improve the forecast of **continuation vs reversal and realized excursion/volatility**, beyond price state, volatility state, and liquidity?

Candidate outcomes to freeze later:
- next 30/60/120-minute continuation return in the direction of the price impulse;
- reversal probability;
- MFE / MAE from the trigger;
- realized range after trigger;
- target-before-adverse-excursion if intraday bars permit exact ordering.

Candidate moderators that prior work says must be decided **before results**:
- liquidity / underlying dollar volume or bid-ask state;
- gamma exposure normalized by underlying liquidity;
- 0DTE vs non-0DTE contribution;
- possibly dealer inventory composition if signed flow permits it.

## Recommended next step
Before freezing the next outcome experiment, perform a **data-source and sign-method audit**. The experiment is only worth running if we can obtain a dealer-position measure stronger than the unsigned theoretical-gamma proxy we already exhausted.

Specifically, identify whether our accessible sources can provide:
- participant-class or customer/dealer trade direction;
- signed option volume / tick classification;
- historical dealer inventory proxy;
- SPX/SPXW rather than SPY-only chain coverage;
- 0DTE and longer-dated contributions separately;
- intraday underlying liquidity and price bars.

If only an OI call/put sign heuristic is available, treat that as a **proxy-method replication**, not as observed dealer gamma, and require stronger robustness against alternate sign conventions.

## References / starting points
- Barbon, A. & Buraschi, A. *Gamma Fragility*. SSRN 3725454.
- Baltussen, G., Da, Z., Lammers, S. & Martens, M. (2021). *Hedging demand and market intraday momentum*. Journal of Financial Economics 142(1), 377–403.
- Anderegg, B., Ulmann, F. & Sornette, D. (2022). *The impact of option hedging on the spot market volatility*. Journal of International Money and Finance 124, 102627.
- Dim, C., Eraker, B. & Vilkov, G. *0DTEs: Trading, Gamma Risk and Volatility Propagation*. SSRN 4692190.
- Adams, G., Fontaine, J.-S. & Ornthanalai, C. *The Market for 0DTE: The Role of Liquidity Providers in Volatility Attenuation*. SSRN 4881008.
- Adams, G., Dim, C., Eraker, B., Fontaine, J.-S., Ornthanalai, C. & Vilkov, G. *Do S&P500 Options Increase Market Volatility? Evidence from 0DTEs*. SSRN 5641974.
- Ni, S.X., Pearson, N.D. & Poteshman, A.M. (2005). *Stock price clustering on option expiration dates*. Journal of Financial Economics 78(1), 49–87.
- Golez, B. & Jackwerth, J.C. (2012). *Pinning in the S&P 500 futures*. Journal of Financial Economics 106(3), 566–585.
- Cboe (2025). *0DTEs Decoded: Positioning, Trends, and Market Impact*.
