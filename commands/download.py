from utils import *
import os
import click
from datetime import datetime
import db
from tqdm.rich import tqdm
from warnings import simplefilter
simplefilter(action="ignore", category=FutureWarning)


@click.command()
@click.option("-s", "--start", type=str, help="开始时间")
@click.option("-e", "--end", type=str, help="结束时间")
def download_to_db(start, end):
    '''
    下载指定时间内的所有ts数据到db中去
    '''

    def is_valid_date(date_string) -> bool:
        try:
            datetime.strptime(date_string, r"%Y%m%d")
            return True
        except ValueError:
            return False
        
    assert is_valid_date(start), start
    assert is_valid_date(end), end
    
    for tick in tqdm(StocksManager.gen_code_list()):
        # 根据当前日期和时间生成文件名
        db.download_and_dump2db(tick, start_date=start, end_date=end)

if __name__ == "__main__":
    download_to_db()
