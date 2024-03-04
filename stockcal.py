# stock calendar
from utils import *

class Calendar:

    def __init__(self) -> None:
        # NOTE: 目前是2024年到2014年
        self.calendar = pd.read_csv("storage/calendar.csv")
        '''
            exchange  cal_date  is_open pretrade_date
        0         SSE  20241231        1      20241230
        1         SSE  20241230        1      20241227
        2         SSE  20241229        0      20241227
        3         SSE  20241228        0      20241227
        4         SSE  20241227        1      20241226
        ···                                        ···
        '''
        
    def date_is_open(self, date: Union[str, Datetime]) -> bool:
        '''
        判断这一天a股赌场是否开门
        '''
        if type(date) is str:
            pass

        elif type(date) is Datetime:
            date = date.strftime(r"%Y%m%d")
            
        else:
            raise TypeError
            
        assert date in self.calendar["cal_date"].values.astype(str), str(date)

        return True if self.calendar[self.calendar["cal_date"].astype(str) == date]["is_open"].iloc[0] == 1 \
                    else False

    def pretrade_date(self, date: str) -> str:

        return date if self.date_is_open(date) \
                    else self.calendar[self.calendar["cal_date"].astype(str) == date]["pretrade_date"].iloc[0]

    def bestfit_trade_region(self, start: str, end: str) -> Tuple[str, str]:
        '''
        给定一个其实和结束区间, 剔除掉头尾的无效不交易区间 获得其中的交易区间
        '''
        # TODO: check start和end的重叠
        start_date = Datetime.strptime(start, r"%Y%m%d")
        end = end if self.date_is_open(end) else self.pretrade_date(end)

        while not self.date_is_open(start_date):
            start_date += timedelta(days=1)
        
        start = start_date.strftime(r"%Y%m%d")

        return (start, end)


    def bestfit_trade_list(self, start: str, end: str, ascending=True) -> List[str]:
        '''
        给定一个起始和结束区间, 返回其中的所有交易日的列表
        '''
        start_date = Datetime.strptime(start, r"%Y%m%d")
        end_date   = Datetime.strptime(end, r"%Y%m%d")

        res = []
        while start_date != end_date:

            if self.date_is_open(start_date):
                res.append(start_date.strftime(r"%Y%m%d"))

            start_date += timedelta(days=1)

        # 从start开始 本身就是升序了
        if not ascending:
            res.reverse()

        return res


calendar = Calendar()

if __name__ == "__main__":
    print(calendar.bestfit_trade_list("20240101", "20240304"))