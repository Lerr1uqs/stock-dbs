import os
import tushare as ts

TOEKN_PATH = os.path.expanduser("~/.tushare.token")
with open(TOEKN_PATH, "r") as f:
    token = f.read().strip()
    ts.set_token(token)
    pro = ts.pro_api()

pro.moneyflow_hsgt(start_date='20240220', end_date='20240305')