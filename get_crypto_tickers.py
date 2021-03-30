#!/usr/bin/env python3
import json
import urllib.request

import pandas as pd

endpoint = 'https://min-api.cryptocompare.com/data/all/coinlist'
with urllib.request.urlopen(endpoint) as url:
    data = json.loads(url.read().decode())

tickers = {}
for ticker, info in data['Data'].items():
    tickers[ticker] = info['CoinName']

df = pd.DataFrame.from_dict(tickers.items()).rename(columns={0: 'Ticker', 1: 'Coin Name'})
df.to_csv('data/crypto_tickers.csv', index=False)
print(df.head(10))
