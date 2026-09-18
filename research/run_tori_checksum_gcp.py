from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import pandas as pd

NEEDED_ENV = [
    'WEBULL_APP_KEY','WEBULL_APP_SECRET','WEBULL_ACCESS_TOKEN',
    'WEBULL_REGION_ID','WEBULL_API_ENDPOINT','WEBULL_TOKEN_DIR'
]


def run(cmd, *, env=None, capture=False, check=True):
    kwargs={'check':check,'text':True,'env':env}
    if capture:
        kwargs.update(stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return subprocess.run(cmd,**kwargs)


def cloud_run_env(project:str,region:str,service:str)->dict[str,str]:
    raw=run([
        'gcloud','run','services','describe',service,
        '--project',project,'--region',region,'--format=json'
    ],capture=True).stdout
    svc=json.loads(raw)
    containers=(svc.get('spec',{}).get('template',{}).get('spec',{}).get('containers') or [])
    if not containers:
        raise RuntimeError('Cloud Run service has no container spec')
    entries=containers[0].get('env') or []
    out={}
    for item in entries:
        name=item.get('name')
        if name not in NEEDED_ENV:
            continue
        if 'value' in item:
            out[name]=str(item['value'])
            continue
        ref=(item.get('valueFrom') or {}).get('secretKeyRef') or {}
        secret=ref.get('name'); version=ref.get('key') or 'latest'
        if secret:
            val=run([
                'gcloud','secrets','versions','access',str(version),
                '--secret',str(secret),'--project',project
            ],capture=True).stdout.rstrip('\n')
            out[name]=val
    return out


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--project',required=True)
    ap.add_argument('--region',default='us-east4')
    ap.add_argument('--service',default='investing-os-post-open')
    ap.add_argument('--push-results',action='store_true')
    args=ap.parse_args()

    root=Path(__file__).resolve().parents[1]
    env=os.environ.copy()
    recovered=cloud_run_env(args.project,args.region,args.service)
    env.update(recovered)
    missing=[k for k in ['WEBULL_APP_KEY','WEBULL_APP_SECRET'] if not env.get(k)]
    if missing:
        raise RuntimeError('Could not recover required Webull configuration from Cloud Run: '+', '.join(missing))
    print('Recovered credentialed Webull runtime configuration without printing secret values.')

    data_root=root/'research'/'data'/'tori_checksum'
    results_dir=root/'research'/'results'; results_dir.mkdir(parents=True,exist_ok=True)
    results_csv=results_dir/'tori_checksum_results.csv'

    # Old samples only. H2-2023 is deliberately not staged until checksum passes.
    run([sys.executable,str(root/'research'/'stage_tori_webull.py'),'--out',str(data_root),'--panel','all'],env=env)
    run([
        sys.executable,str(root/'research'/'run_tori_checksum.py'),
        '--data-root',str(data_root),
        '--manifest',str(root/'research'/'tori_v1_2_checksum_manifest.json'),
        '--out',str(results_csv)
    ],env=env)

    df=pd.read_csv(results_csv)
    passed=df[df['passed'].astype(str).str.lower().isin(['true','1'])]
    best=df.sort_values(['passed','checks_passed'],ascending=[False,False]).head(10)
    summary={
        'protocol':'TORI-DETECTOR-v1.2-REPLICATION-CHECKSUM-v1',
        'profiles_tested':int(len(df)),
        'exact_pass_profiles':passed['profile'].tolist(),
        'exact_pass_count':int(len(passed)),
        'top_profiles':best[['profile','checks_passed','checks_total','failed_checks']].to_dict(orient='records'),
        'h2_2023_touched':False,
    }
    summary_path=results_dir/'tori_checksum_summary.json'
    summary_path.write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))

    if args.push_results:
        run(['git','-C',str(root),'add',str(results_csv.relative_to(root)),str(summary_path.relative_to(root))])
        status=run(['git','-C',str(root),'status','--porcelain'],capture=True).stdout.strip()
        if status:
            run(['git','-C',str(root),'commit','-m','Record Tori v1.2 structural replication checksum'])
            run(['git','-C',str(root),'push','origin','research/tori-v1-2-replication'])
            print('Pushed checksum results to research/tori-v1-2-replication.')
        else:
            print('No checksum result changes to commit.')

if __name__=='__main__':
    main()
