from __future__ import annotations

import argparse
from datetime import datetime, timedelta, time
import os
from pathlib import Path
from zoneinfo import ZoneInfo
import pandas as pd

from webull.data.common.timespan import Timespan
from webull_client import WebullClient

ET=ZoneInfo('America/New_York')

PANELS={
    'calibration_h1_2025': {
        'tickers':['AAPL','AMZN','META','MSFT','NVDA'],
        'start':'2025-01-01','end':'2025-06-30',
    },
    'oos_h2_2024': {
        'tickers':['GOOGL','AMD','JPM','XOM','CAT'],
        'start':'2024-07-01','end':'2024-12-31',
    },
    'oos_partial_h1_2024': {
        'tickers':['AVGO','BAC','GS','CVX','SLB','UNH','LLY','WMT','COST','HD','CRM','ORCL','NOW','MU','QCOM','GE'],
        'start':'2024-02-27','end':'2024-06-30',
    },
}


def client_from_env():
    required=['WEBULL_APP_KEY','WEBULL_APP_SECRET']
    missing=[k for k in required if not os.environ.get(k)]
    if missing:
        raise RuntimeError('Missing environment variables: '+', '.join(missing))
    return WebullClient(
        app_key=os.environ['WEBULL_APP_KEY'],
        app_secret=os.environ['WEBULL_APP_SECRET'],
        access_token=os.environ.get('WEBULL_ACCESS_TOKEN') or None,
        region_id=os.environ.get('WEBULL_REGION_ID','us'),
        api_endpoint=os.environ.get('WEBULL_API_ENDPOINT','api.webull.com'),
        token_dir=os.environ.get('WEBULL_TOKEN_DIR','/tmp/webull-openapi-token'),
    )


def chunks(start_date: str,end_date: str,days: int=55):
    start=pd.Timestamp(start_date).date(); end=pd.Timestamp(end_date).date(); cur=start
    while cur<=end:
        nxt=min(cur+timedelta(days=days-1),end)
        yield cur,nxt
        cur=nxt+timedelta(days=1)


def fetch_window(client: WebullClient,symbol: str,d0,d1):
    start_et=datetime.combine(d0,time(9,30),tzinfo=ET)
    end_et=datetime.combine(d1,time(16,0),tzinfo=ET)
    payload=client._safe_call(
        f'M30 research bars for {symbol}',
        client._data_client.market_data.get_history_bar,
        symbol=symbol,
        category=client.category_for(symbol),
        timespan=Timespan.M30.name,
        count='1200',
        real_time_required=False,
        trading_sessions=['RTH'],
        start_time=int(start_et.timestamp()*1000),
        end_time=int(end_et.timestamp()*1000),
    )
    return client._normalize_single_bar_payload(payload,symbol,start_et,end_et)


def stage_symbol(client,symbol,start_date,end_date):
    rows=[]
    for d0,d1 in chunks(start_date,end_date):
        part=fetch_window(client,symbol,d0,d1)
        rows.extend(part)
        print(symbol,d0,d1,'bars',len(part))
    if not rows:
        raise RuntimeError(f'No bars returned for {symbol}')
    df=pd.DataFrame(rows)
    keep=['time','open','high','low','close','volume','trading_session']
    for col in keep:
        if col not in df.columns:
            df[col]=''
    df=df[keep].copy()
    df['time']=pd.to_datetime(df['time'],utc=True)
    df=df.sort_values('time').drop_duplicates('time')
    et=df['time'].dt.tz_convert(ET)
    lo=pd.Timestamp(start_date,tz=ET); hi=pd.Timestamp(end_date,tz=ET)+pd.Timedelta(days=1)
    df=df[(et>=lo)&(et<hi)].reset_index(drop=True)
    return df


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',default='research/data/tori_checksum')
    ap.add_argument('--panel',choices=['all']+list(PANELS),default='all')
    args=ap.parse_args()
    root=Path(args.out); root.mkdir(parents=True,exist_ok=True)
    client=client_from_env()
    names=list(PANELS) if args.panel=='all' else [args.panel]
    for name in names:
        spec=PANELS[name]; d=root/name; d.mkdir(parents=True,exist_ok=True)
        for symbol in spec['tickers']:
            df=stage_symbol(client,symbol,spec['start'],spec['end'])
            path=d/f'{symbol}.csv'; df.to_csv(path,index=False)
            print('wrote',path,'rows',len(df),df['time'].min(),df['time'].max())

if __name__=='__main__':
    main()
