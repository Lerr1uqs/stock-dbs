from typing import List, TypeVar, Type, Generator, Tuple, Dict, Union, Optional, Callable
import pandas as pd
import numpy as np
from datetime import datetime as Datetime
from datetime import timedelta
import os 
import sys
import tushare as ts



TOEKN_PATH = os.path.expanduser("~/.tushare.token")
with open(TOEKN_PATH, "r") as f:
    token = f.read().strip()
    ts.set_token(token)
    pro = ts.pro_api()


# 加载ticks数据
import generic_data.sdmngr as sdmngr
from generic_data.sdmngr import StocksManager
StocksManager.load_from_storage()


# PYTHONPATH
current_path = os.getcwd()
sys.path.append(current_path)
print(current_path)
