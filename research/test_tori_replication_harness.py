import pandas as pd
import sys
sys.path.insert(0,'.')
from tori_replication_harness import (
    reconstruct_htf, ReplicationProfile, raw_candidates,
    dedupe_families, apply_regime_lockout
)


def test_orcl_2024_06_06_htf_boundaries():
    rows=[
        ('2024-06-06T13:30:00Z',122.88,123.31,122.27,123.08,681770),
        ('2024-06-06T14:00:00Z',123.09,123.82,122.925,123.8102,434534),
        ('2024-06-06T14:30:00Z',123.78,123.925,123.55,123.68,527450),
        ('2024-06-06T15:00:00Z',123.68,123.84,123.66,123.75,411791),
        ('2024-06-06T15:30:00Z',123.75,124.03,123.73,123.95,377384),
        ('2024-06-06T16:00:00Z',123.955,123.97,123.69,123.79,340715),
        ('2024-06-06T16:30:00Z',123.785,123.86,123.58,123.85,226521),
        ('2024-06-06T17:00:00Z',123.88,123.9835,123.795,123.945,200672),
        ('2024-06-06T17:30:00Z',123.945,124.27,123.8695,124.24,289830),
        ('2024-06-06T18:00:00Z',124.24,124.25,123.51,123.61,343432),
        ('2024-06-06T18:30:00Z',123.6045,123.82,123.5,123.755,292432),
        ('2024-06-06T19:00:00Z',123.745,123.9425,123.63,123.69,379469),
        ('2024-06-06T19:30:00Z',123.68,123.86,123.26,123.5,1205790),
    ]
    df=pd.DataFrame(rows,columns=['time','open','high','low','close','volume'])
    h=reconstruct_htf(df)
    assert len(h)==2
    am=h.iloc[0]; pm=h.iloc[1]
    assert am['m30_count']==7 and pm['m30_count']==6
    assert (am['open'],am['high'],am['low'],am['close'])==(122.88,124.03,122.27,123.85)
    assert (pm['open'],pm['high'],pm['low'],pm['close'])==(123.88,124.27,123.26,123.50)


def test_synthetic_three_touch_breakout():
    n=70; rows=[]
    for i in range(n):
        d=pd.Timestamp('2024-01-02')+pd.tseries.offsets.BDay(i//2)
        half='AM' if i%2==0 else 'PM'
        line=101-.10*i
        high=line-.45; close=high-.4; low=close-.45; op=close-.05
        if i in [16,31,46]:
            high=line; close=line-.45; low=close-.45; op=close-.05
        if i==51:
            high=line+.35; close=line+.20; low=close-.6; op=close-.1
        rows.append(dict(session_date=d.date(),half=half,
            time=pd.Timestamp(d.date(),tz='America/New_York')+pd.Timedelta(hours=13 if half=='AM' else 16),
            open=op,high=high,low=low,close=close,volume=1000,
            m30_count=7 if half=='AM' else 6,session_ord=i//2))
    h=pd.DataFrame(rows)
    p=ReplicationProfile('synthetic')
    h2,c=raw_candidates(h,p)
    fam=dedupe_families(c)
    events=apply_regime_lockout(fam)
    assert len(events)==1
    e=events[0]
    assert e.breakout_i==51
    assert e.touch_indices[:3]==(16,31,46)
    assert e.extension_atr < 1.0

if __name__=='__main__':
    test_orcl_2024_06_06_htf_boundaries()
    test_synthetic_three_touch_breakout()
    print('OK: 2 tests passed')
