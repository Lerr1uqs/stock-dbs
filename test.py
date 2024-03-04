import sqlite3

import sys
import os
import pandas as pd
import tushare as ts

TOEKN_PATH = os.path.expanduser("~/.tushare.token")
with open(TOEKN_PATH, "r") as f:
    token = f.read().strip()
    ts.set_token(token)
    pro = ts.pro_api()

df: pd.DataFrame = ts.pro_bar(ts_code='000001.SZ', adj='hfq', start_date='20180101', end_date='20181011')

# ['ts_code', 'trade_date', 'open', 'high', 'low', 'close', 'pre_close', 'change', 'pct_chg', 'vol', 'amount']

df = df.rename(columns={
    'ts_code': 'code',
    'trade_date': 'date',
    'vol': "volume"
})[["date", "open", "high", "low", "close", "volume"]]

# Connect to SQLite database
conn = sqlite3.connect('db/squ-quantstock.db')
cursor = conn.cursor()

# Create a table (if not exists)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS day_level_hfq (
        date TEXT,
        open REAL,
        high REAL,
        low REAL,
        close REAL,
        volume INTEGER
    )
''')

# Insert data into SQLite table
data = [tuple(row) for row in df.values]
cursor.executemany('''
    INSERT INTO day_level_hfq (date, open, high, low, close, volume) 
    VALUES (?, ?, ?, ?, ?, ?)
''', data)

# Commit changes and close connection
conn.commit()
conn.close()