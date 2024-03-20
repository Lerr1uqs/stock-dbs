from fastapi import FastAPI, Query, Body
from typing import List
import db
from utils import *
import pandas as pd

app = FastAPI()

@app.get("/api/v1/fetch")
async def fetch(
    code: str = Query(..., title="Stock Code", description="Stock code for fetching data"),
    start_date: str = Query(..., title="Start Date", description="Start date for data fetching (YYYYMMDD)"),
    end_date: str = Query(..., title="End Date", description="End date for data fetching (YYYYMMDD)"),
    adj: str = Query(..., title="Adjustment", description="Adjustment for price(qfq/hfq)")
):
    try:
        data = db.fetch_or_query(code, start_date, end_date, adj)
        if data is None:
            raise RuntimeError("TODO")

        data: pd.DataFrame = data.sort_index()

        # 注意这里不能用to_json 否则就被二次解析了 客户端就要eval两次
        return data
    
    except Exception as e:
        # return {"error": str(e)}
        raise e

@app.post("/api/v1/fetch_codes")
async def fetch_codes(
    codes: List[str] = Body(..., embed=True, title="Stock Codes", description="Stock codes for fetching data"),
    start_date: str = Body(..., title="Start Date", description="Start date for data fetching (YYYYMMDD)"),
    end_date: str = Body(..., title="End Date", description="End date for data fetching (YYYYMMDD)"),
    adj: str = Body(..., title="Adjustment", description="Adjustment for price(qfq/hfq)")
):
    try:
        print(codes, start_date, end_date, adj)
        data = db.fetch_from_database(codes, start_date, end_date, adj)
        if data is None:
            raise RuntimeError("data is None")

        return data
    
    except Exception as e:
        # return {"error": str(e)}
        raise e

@app.get("/api/v1/codes")
async def get_all_codes():
    try:
        codes = StocksManager.gen_code_list()
        if codes is None:
            raise RuntimeError("TODO")

        # 注意这里不能用to_json 否则就被二次解析了 客户端就要eval两次
        return codes
    
    except Exception as e:
        # return {"error": str(e)}
        raise e

