from __future__ import annotations
import argparse, json
from pathlib import Path
import pandas as pd
from tori_replication_harness import detect, profile_grid


def load_panel(root: Path, names: list[str]) -> dict[str,pd.DataFrame]:
    out={}
    for t in names:
        p=root/f'{t}.csv'
        if not p.exists():
            raise FileNotFoundError(p)
        out[t]=pd.read_csv(p)
    return out


def event_date(e):
    return pd.Timestamp(e.breakout_time).tz_convert('America/New_York').date().isoformat()


def match_fp(events, fp):
    tol=float(fp.get('extension_rounding_tolerance',0.03))
    target=float(fp['extension_atr'])
    date=fp.get('date')
    candidates=[e for e in events if date is None or event_date(e)==date]
    return any(abs(float(e.extension_atr)-target)<=tol for e in candidates)


def evaluate_profile(profile, panels, manifest):
    all_events={}
    for sample, panel in panels.items():
        all_events[sample]={}
        for ticker,df in panel.items():
            _,ev=detect(df,profile)
            all_events[sample][ticker]=ev
    checks=[]
    cal=manifest['checksums']['calibration_h1_2025']
    got={t:len(all_events['calibration_h1_2025'][t]) for t in cal['universe_counts']}
    checks.append(('calibration_counts',got==cal['universe_counts']))
    h2=manifest['checksums']['oos_h2_2024']
    got2={t:len(all_events['oos_h2_2024'][t]) for t in h2['universe_counts']}
    checks.append(('h2_counts',got2==h2['universe_counts']))
    for fp in h2.get('known_event_fingerprint',[]):
        checks.append((f"h2_fp_{fp['ticker']}_{fp.get('date','any')}",match_fp(all_events['oos_h2_2024'][fp['ticker']],fp)))
    p=manifest['checksums']['oos_partial_h1_2024']
    total=sum(len(v) for v in all_events['oos_partial_h1_2024'].values())
    checks.append(('partial_h1_total',total==p['total']))
    for fp in p.get('known_retained_fingerprints',[]):
        checks.append((f"partial_fp_{fp['ticker']}_{fp['date']}",match_fp(all_events['oos_partial_h1_2024'][fp['ticker']],fp)))
    for fp in p.get('known_extension_rejections',[]):
        checks.append((f"partial_reject_ext_{fp['ticker']}_{fp['extension_atr']}",match_fp(all_events['oos_partial_h1_2024'][fp['ticker']],fp)))
    return {
        'profile': profile.name,
        'passed': all(x[1] for x in checks),
        'checks_passed': sum(x[1] for x in checks),
        'checks_total': len(checks),
        'failed_checks': [name for name,ok in checks if not ok],
        'calibration_counts': got,
        'h2_counts': got2,
        'partial_h1_total': total,
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--data-root',required=True)
    ap.add_argument('--manifest',default='tori_v1_2_checksum_manifest.json')
    ap.add_argument('--out',default='tori_checksum_results.csv')
    args=ap.parse_args()
    root=Path(args.data_root); manifest=json.load(open(args.manifest))
    panels={
        'calibration_h1_2025': load_panel(root/'calibration_h1_2025',list(manifest['checksums']['calibration_h1_2025']['universe_counts'])),
        'oos_h2_2024': load_panel(root/'oos_h2_2024',list(manifest['checksums']['oos_h2_2024']['universe_counts'])),
        'oos_partial_h1_2024': load_panel(root/'oos_partial_h1_2024',manifest['checksums']['oos_partial_h1_2024']['universe']),
    }
    rows=[]
    for p in profile_grid():
        r=evaluate_profile(p,panels,manifest); rows.append(r)
        print(p.name, f"{r['checks_passed']}/{r['checks_total']}", 'PASS' if r['passed'] else '')
    pd.DataFrame(rows).sort_values(['passed','checks_passed'],ascending=[False,False]).to_csv(args.out,index=False)
    print('wrote',args.out)

if __name__=='__main__': main()
