from fastapi import FastAPI, Query
from typing import List
import db

app = FastAPI()

@app.get("/api/v1/hfq")
async def fetch(
    code: str = Query(..., title="Stock Code", description="Stock code for fetching data"),
    start_date: str = Query(..., title="Start Date", description="Start date for data fetching (YYYYMMDD)"),
    end_date: str = Query(..., title="End Date", description="End date for data fetching (YYYYMMDD)")
):
    try:
        data = db.fetch_or_query(code, start_date, end_date)
        if data is None:
            raise RuntimeError("TODO")
        return data.to_json()
    
    except Exception as e:
        # return {"error": str(e)}
        raise e

