from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Literal, Iterable, Optional
from zoneinfo import ZoneInfo
import math
import numpy as np
import pandas as pd

ET = ZoneInfo('America/New_York')

ATRMode = Literal['wilder', 'sma']
LineMode = Literal['pair', 'ols_refit']
ATRRefMode = Literal['local', 'breakout', 'mean_touches']

@dataclass(frozen=True)
class ReplicationProfile:
    """Only the mechanics that were not explicitly persisted are variable.

    ALL numeric Detector v1.2 thresholds remain frozen outside this profile.
    """
    name: str
    atr_mode: ATRMode = 'wilder'
    line_mode: LineMode = 'pair'
    touch_atr_ref: ATRRefMode = 'local'
    integrity_atr_ref: ATRRefMode = 'local'
    slope_atr_ref: ATRRefMode = 'breakout'

@dataclass
class LineCandidate:
    breakout_i: int
    breakout_time: pd.Timestamp
    first_touch_i: int
    third_touch_i: int
    touch_indices: tuple[int, ...]
    slope: float
    intercept: float
    action_line: float
    atr_breakout: float
    extension_atr: float
    mean_touch_error_atr: float
    history_bars: int

    @property
    def touches(self) -> int:
        return len(self.touch_indices)

@dataclass
class Event:
    breakout_i: int
    breakout_time: pd.Timestamp
    entry_time: Optional[pd.Timestamp]
    entry_price: Optional[float]
    action_line: float
    atr_breakout: float
    extension_atr: float
    touches: int
    first_touch_i: int
    third_touch_i: int
    touch_indices: tuple[int, ...]
    slope: float
    mean_touch_error_atr: float

PIVOT_SIDE = 2
MIN_TOUCHES = 3
MIN_TOUCH_BAR_GAP = 6
MIN_FIRST_THIRD_SESSIONS = 15
TOUCH_TOL_ATR = 0.25
MAX_SLOPE_ATR_PER_BAR = 0.25
INTEGRITY_CLOSE_ATR = 0.25
BREAKOUT_CLOSE_ATR = 0.10
FAMILY_BREAKOUT_BAR_GAP = 2
FAMILY_LINE_TOL_ATR = 0.25
TORI_EARLY_MAX_EXTENSION_ATR = 1.0


def _normalize_m30(df: pd.DataFrame) -> pd.DataFrame:
    need = {'time','open','high','low','close','volume'}
    missing = need - set(df.columns)
    if missing:
        raise ValueError(f'Missing columns: {sorted(missing)}')
    out = df.copy()
    out['time'] = pd.to_datetime(out['time'], utc=True)
    for c in ['open','high','low','close','volume']:
        out[c] = pd.to_numeric(out[c], errors='coerce')
    out = out.dropna(subset=['time','open','high','low','close']).sort_values('time').drop_duplicates('time')
    out['time_et'] = out['time'].dt.tz_convert(ET)
    return out.reset_index(drop=True)


def reconstruct_htf(m30: pd.DataFrame) -> pd.DataFrame:
    """Exact recovered construction: two RTH bars/session, 09:30-13:00 and 13:00-16:00 ET."""
    x = _normalize_m30(m30)
    rows = []
    for d, g in x.groupby(x['time_et'].dt.date, sort=True):
        g = g.sort_values('time_et')
        for label, sh, sm, eh, em in [
            ('AM',9,30,13,0),
            ('PM',13,0,16,0),
        ]:
            mins = g['time_et'].dt.hour*60 + g['time_et'].dt.minute
            lo = sh*60+sm; hi = eh*60+em
            z = g[(mins >= lo) & (mins < hi)]
            if z.empty:
                continue
            end_et = pd.Timestamp(f'{d} {eh:02d}:{em:02d}', tz=ET)
            rows.append({
                'session_date': d,
                'half': label,
                'time': end_et.tz_convert('UTC'),
                'open': float(z.iloc[0]['open']),
                'high': float(z['high'].max()),
                'low': float(z['low'].min()),
                'close': float(z.iloc[-1]['close']),
                'volume': float(z['volume'].fillna(0).sum()),
                'm30_count': int(len(z)),
            })
    h = pd.DataFrame(rows).sort_values('time').reset_index(drop=True)
    sessions = {d:i for i,d in enumerate(sorted(h['session_date'].unique()))}
    h['session_ord'] = h['session_date'].map(sessions).astype(int)
    return h


def add_atr(htf: pd.DataFrame, mode: ATRMode='wilder', period: int=14) -> pd.DataFrame:
    h = htf.copy()
    prev = h['close'].shift(1)
    tr = pd.concat([
        h['high']-h['low'],
        (h['high']-prev).abs(),
        (h['low']-prev).abs(),
    ], axis=1).max(axis=1)
    h['tr'] = tr
    if mode == 'sma':
        h['atr'] = tr.rolling(period, min_periods=period).mean()
    elif mode == 'wilder':
        atr = pd.Series(np.nan, index=h.index, dtype=float)
        if len(h) >= period:
            atr.iloc[period-1] = tr.iloc[:period].mean()
            for i in range(period, len(h)):
                atr.iloc[i] = (atr.iloc[i-1]*(period-1) + tr.iloc[i])/period
        h['atr'] = atr
    else:
        raise ValueError(mode)
    return h


def pivot_high_indices(h: pd.DataFrame) -> list[int]:
    highs = h['high'].to_numpy(float)
    out=[]
    for i in range(PIVOT_SIDE, len(h)-PIVOT_SIDE):
        if all(highs[i] > highs[j] for j in range(i-PIVOT_SIDE, i)) and all(highs[i] > highs[j] for j in range(i+1, i+PIVOT_SIDE+1)):
            out.append(i)
    return out


def _atr_ref(h: pd.DataFrame, mode: ATRRefMode, idx: int, breakout_i: int, touches: Iterable[int]) -> float:
    if mode == 'local':
        return float(h.at[idx,'atr'])
    if mode == 'breakout':
        return float(h.at[breakout_i,'atr'])
    vals = [float(h.at[j,'atr']) for j in touches if pd.notna(h.at[j,'atr'])]
    return float(np.mean(vals)) if vals else math.nan


def _fit_pair(i: int, j: int, h: pd.DataFrame) -> tuple[float,float]:
    yi=float(h.at[i,'high']); yj=float(h.at[j,'high'])
    slope=(yj-yi)/(j-i)
    return slope, yi-slope*i


def _fit_ols(idxs: list[int], h: pd.DataFrame) -> tuple[float,float]:
    x=np.asarray(idxs,dtype=float); y=h.loc[idxs,'high'].to_numpy(float)
    slope, intercept=np.polyfit(x,y,1)
    return float(slope),float(intercept)


def _touches_for_line(h: pd.DataFrame, pivots: list[int], slope: float, intercept: float,
                      breakout_i: int, profile: ReplicationProfile) -> tuple[list[int], list[float]]:
    prelim=[]; errs=[]
    for p in pivots:
        if p >= breakout_i: continue
        atr=_atr_ref(h, profile.touch_atr_ref, p, breakout_i, prelim or [p])
        if not np.isfinite(atr) or atr<=0: continue
        err=abs(float(h.at[p,'high'])-(slope*p+intercept))/atr
        if err <= TOUCH_TOL_ATR + 1e-12:
            prelim.append(p); errs.append(err)
    kept=[]; kept_err=[]
    for p,e in zip(prelim,errs):
        if not kept or p-kept[-1] >= MIN_TOUCH_BAR_GAP:
            kept.append(p); kept_err.append(e)
        elif e < kept_err[-1]:
            kept[-1]=p; kept_err[-1]=e
    return kept, kept_err


def _session_span_ok(h: pd.DataFrame, first: int, third: int) -> bool:
    return int(h.at[third,'session_ord']) - int(h.at[first,'session_ord']) >= MIN_FIRST_THIRD_SESSIONS


def _candidate_at_breakout(h: pd.DataFrame, confirmed_pivots: list[int], breakout_i: int,
                           profile: ReplicationProfile) -> list[LineCandidate]:
    if pd.isna(h.at[breakout_i,'atr']): return []
    atr_b=float(h.at[breakout_i,'atr'])
    if atr_b<=0: return []
    out=[]
    for a_pos in range(len(confirmed_pivots)):
        i=confirmed_pivots[a_pos]
        for b_pos in range(a_pos+1,len(confirmed_pivots)):
            j=confirmed_pivots[b_pos]
            if j-i < MIN_TOUCH_BAR_GAP: continue
            slope,intercept=_fit_pair(i,j,h)
            if slope >= 0: continue
            touches,errs=_touches_for_line(h,confirmed_pivots,slope,intercept,breakout_i,profile)
            if len(touches)<MIN_TOUCHES: continue
            if profile.line_mode=='ols_refit':
                slope,intercept=_fit_ols(touches,h)
                if slope>=0: continue
                touches,errs=_touches_for_line(h,confirmed_pivots,slope,intercept,breakout_i,profile)
                if len(touches)<MIN_TOUCHES: continue
            first,third=touches[0],touches[2]
            if not _session_span_ok(h,first,third): continue
            slope_ref=_atr_ref(h,profile.slope_atr_ref,breakout_i,breakout_i,touches)
            if not np.isfinite(slope_ref) or slope_ref<=0: continue
            if abs(slope)/slope_ref > MAX_SLOPE_ATR_PER_BAR + 1e-12: continue
            ok=True
            for q in range(first,breakout_i):
                ref=_atr_ref(h,profile.integrity_atr_ref,q,breakout_i,touches)
                if not np.isfinite(ref) or ref<=0: continue
                if float(h.at[q,'close']) > slope*q+intercept + INTEGRITY_CLOSE_ATR*ref + 1e-12:
                    ok=False; break
            if not ok: continue
            action=slope*breakout_i+intercept
            close=float(h.at[breakout_i,'close'])
            if close <= action + BREAKOUT_CLOSE_ATR*atr_b + 1e-12: continue
            ext=(close-action)/atr_b
            out.append(LineCandidate(
                breakout_i=breakout_i, breakout_time=h.at[breakout_i,'time'],
                first_touch_i=first, third_touch_i=third,
                touch_indices=tuple(touches), slope=slope, intercept=intercept,
                action_line=float(action), atr_breakout=atr_b, extension_atr=float(ext),
                mean_touch_error_atr=float(np.mean(errs)), history_bars=breakout_i-first,
            ))
    return out


def raw_candidates(htf: pd.DataFrame, profile: ReplicationProfile) -> tuple[pd.DataFrame,list[LineCandidate]]:
    h=add_atr(htf,profile.atr_mode)
    piv=pivot_high_indices(h)
    allc=[]
    for b in range(len(h)):
        confirmed=[p for p in piv if p+PIVOT_SIDE <= b]
        if len(confirmed)<MIN_TOUCHES: continue
        allc.extend(_candidate_at_breakout(h,confirmed,b,profile))
    return h,allc


def _canonical_family(cands: list[LineCandidate]) -> LineCandidate:
    return sorted(cands,key=lambda c:(-c.touches,-c.history_bars,c.mean_touch_error_atr,c.breakout_i))[0]


def dedupe_families(cands: list[LineCandidate]) -> list[LineCandidate]:
    if not cands: return []
    cands=sorted(cands,key=lambda c:(c.breakout_i,c.action_line))
    n=len(cands); parent=list(range(n))
    def find(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]]; x=parent[x]
        return x
    def union(a,b):
        ra,rb=find(a),find(b)
        if ra!=rb: parent[rb]=ra
    for a in range(n):
        for b in range(a+1,n):
            ca,cb=cands[a],cands[b]
            if cb.breakout_i-ca.breakout_i > FAMILY_BREAKOUT_BAR_GAP: break
            atr=max(1e-12,(ca.atr_breakout+cb.atr_breakout)/2)
            if abs(ca.action_line-cb.action_line) <= FAMILY_LINE_TOL_ATR*atr + 1e-12:
                union(a,b)
    groups={}
    for k,c in enumerate(cands): groups.setdefault(find(k),[]).append(c)
    return sorted((_canonical_family(v) for v in groups.values()),key=lambda c:c.breakout_i)


def apply_regime_lockout(families: list[LineCandidate]) -> list[LineCandidate]:
    if not families: return []
    accepted=[]
    last_break=None
    for c in sorted(families,key=lambda x:x.breakout_i):
        if last_break is None:
            accepted.append(c); last_break=c.breakout_i; continue
        new_touches=sum(1 for p in c.touch_indices if p>last_break)
        old_touches=sum(1 for p in c.touch_indices if p<=last_break)
        if new_touches>=2 and old_touches<=1:
            accepted.append(c); last_break=c.breakout_i
    return accepted


def map_entries(events: list[LineCandidate], h: pd.DataFrame, m30: pd.DataFrame) -> list[Event]:
    x=_normalize_m30(m30)
    out=[]
    for c in events:
        z=x[x['time'] >= c.breakout_time]
        row=z.iloc[0] if not z.empty else None
        out.append(Event(
            breakout_i=c.breakout_i,breakout_time=c.breakout_time,
            entry_time=None if row is None else row['time'],
            entry_price=None if row is None else float(row['open']),
            action_line=c.action_line,atr_breakout=c.atr_breakout,extension_atr=c.extension_atr,
            touches=c.touches,first_touch_i=c.first_touch_i,third_touch_i=c.third_touch_i,
            touch_indices=c.touch_indices,slope=c.slope,mean_touch_error_atr=c.mean_touch_error_atr,
        ))
    return out


def detect(m30: pd.DataFrame, profile: ReplicationProfile) -> tuple[pd.DataFrame,list[Event]]:
    base=reconstruct_htf(m30)
    h,c=raw_candidates(base,profile)
    fam=dedupe_families(c)
    locked=apply_regime_lockout(fam)
    return h,map_entries(locked,h,m30)


def tori_early(events: list[Event]) -> list[Event]:
    return [e for e in events if e.extension_atr <= TORI_EARLY_MAX_EXTENSION_ATR + 1e-12]


def coverage_audit(m30: pd.DataFrame) -> pd.DataFrame:
    h=reconstruct_htf(m30)
    p=h.pivot_table(index='session_date',columns='half',values='m30_count',aggfunc='first')
    p['normal_complete']=(p.get('AM')==7)&(p.get('PM')==6)
    return p.reset_index()


def profile_grid() -> list[ReplicationProfile]:
    profiles=[]
    k=0
    for atr in ['wilder','sma']:
        for line in ['pair','ols_refit']:
            for touch_ref in ['local','breakout']:
                for integrity_ref in ['local','breakout']:
                    for slope_ref in ['breakout','mean_touches']:
                        k+=1
                        profiles.append(ReplicationProfile(
                            name=f'P{k:02d}_{atr}_{line}_T{touch_ref}_I{integrity_ref}_S{slope_ref}',
                            atr_mode=atr,line_mode=line,touch_atr_ref=touch_ref,
                            integrity_atr_ref=integrity_ref,slope_atr_ref=slope_ref,
                        ))
    return profiles


def event_frame(events: list[Event]) -> pd.DataFrame:
    return pd.DataFrame([asdict(e) for e in events])

if __name__=='__main__':
    print(f'{len(profile_grid())} predeclared replication profiles')
