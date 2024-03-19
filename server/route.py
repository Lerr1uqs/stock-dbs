from fastapi import FastAPI, Query
from typing import List
import db
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

