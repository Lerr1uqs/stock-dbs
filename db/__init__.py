import sqlite3

import sys
import os
import pandas as pd
import tushare as ts
from utils import *
from stockcal import calendar
from loguru import logger

TOEKN_PATH = os.path.expanduser("~/.tushare.token")
with open(TOEKN_PATH, "r") as f:
    token = f.read().strip()
    ts.set_token(token)
    pro = ts.pro_api()

conn = sqlite3.connect('db/squ-quantstock.db')

# cursor = conn.cursor()
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS day_level_hfq (
#         code TEXT,
#         date TEXT,
#         open REAL,
#         high REAL,
#         low REAL,
#         close REAL,
#         volume INTEGER
#     )
# ''')
# conn.commit()
# conn.close() # TODO: 关闭数据库连接在合适位置



# 标准化的columns
STD_COLUMNS = ["code", "date", "open", "high", "low", "close", "volume"]

def query_from_tushare(ts_code: str, start_date: str, end_date: str, adj: str) -> Optional[pd.DataFrame]:
    '''
    ts_code:    000001.SZ
    start_date: 20180101
    end_date:   20181011
    adj:        hfq
    '''

    df: pd.DataFrame = ts.pro_bar(
        ts_code    = ts_code, 
        adj        = adj, 
        start_date = start_date, 
        end_date   = end_date
    )

    if df is None or df.empty:
        logger.warning("ts.pro_bar return a None")
        return None

    df = df.rename(columns={
        'ts_code': 'code',
        'trade_date': 'date',
        'vol': "volume"
    })[STD_COLUMNS]

    df = df.sort_values("date", key=lambda x: pd.to_datetime(x, format=r"%Y%m%d"), ascending=True)

    return df


def dump_to_database(df: pd.DataFrame, adj: str) -> None:

    # TODO:
    assert all(a == b for (a, b) in zip(df.columns, STD_COLUMNS)), f"{df.columns} != {STD_COLUMNS}"

    # Connect to SQLite database
    # cursor is an object that allows you to execute SQL queries on the database.
    cursor = conn.cursor()

    # Create a table (if not exists)
    # TEMP: day_level_hfq
    table = f"day_level_{adj}"

    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table} (
            code TEXT,
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
    cursor.executemany(f'''
        INSERT INTO {table} (code, date, open, high, low, close, volume) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', data)

    # Commit changes and close connection
    conn.commit()

# TODO: 交易日期范围 + 数据库中的数据不足
def fetch_from_database(ts_code: str, start_date: str, end_date: str, adj: str) -> Optional[pd.DataFrame]:
    # Connect to SQLite database
    cursor = conn.cursor()

    table = f"day_level_{adj}"
    
    # Execute a query to fetch data from the database
    cursor.execute(f'''
        SELECT * FROM {table} 
        WHERE code = ? AND date BETWEEN ? AND ?
    ''', (ts_code, start_date, end_date))

    # Fetch the results
    data = cursor.fetchall()

    # Convert the results to a DataFrame
    return pd.DataFrame(data, columns=STD_COLUMNS) \
        if data \
        else None 
    
def fetch_or_query(ts_code: str, start_date: str, end_date: str, adj: str) -> Optional[pd.DataFrame]:
    '''
    对外提供的数据库接口, 向数据库查询数据, 如果数据不存在会自动从tushare去获取
    ts_code:    000001.SZ
    start_date: 20180101
    end_date:   20181011
    adj:        hfq
    '''
    # Check if data already exists in the database for the specified date range
    df = fetch_from_database(ts_code, start_date, end_date, adj)
    # 数据已有
    if df is not None and not df.empty:
        # 并且无缺失
        # TODO: check
        if set(df["date"].astype(str)) == set(calendar.bestfit_trade_list(start_date, end_date)):
            # 期间的所有交易日都涉及到了
            return df
    

    # 数据不存在 从tushare拿
    df = query_from_tushare(ts_code, start_date, end_date, adj)
    
    if df is None or df.empty:
        logger.debug("return a None")
        return None

    # Dump data to SQLite database
    dump_to_database(df, adj)

    return df


def download_and_dump2db(ts_code: str, start_date: str, end_date: str, adj: str) -> None:
    '''
    下载数据 保存到本地中去
    '''
    df = query_from_tushare(ts_code, start_date, end_date, adj)
    
    if df is None or df.empty:
        logger.debug("return a None")
        raise RuntimeError
    
    dump_to_database(df, adj)
