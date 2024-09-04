import tushare as ts
from learn.tushare_project.common import token
from datetime import datetime


class basedata():

    def __init__(self):
        self.pro = token.init_pro()

    def stock_basic(self):
        pro = self.pro
        df = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date,market')
        return df

    def daily(self, ts_code, start_date, end_date):
        pro = self.pro
        if not ts_code:
            raise Exception("no ts_code")

        # datetime.strptime(start_date, '%Y%m%d')
        # datetime.strptime(end_date, '%Y%m%d')

        df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        return df

if __name__ == '__main__':
    df = basedata().daily('600519.SH', '', '')
    print(df)