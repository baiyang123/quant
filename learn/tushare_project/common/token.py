import time

import tushare as ts

token = '5c704de5a065340a7fd9b1763638b25f3f1b5cf3ae8f231f20ec4053'


def get_token_expire():
    pro = init_pro()
    df = pro.user(token=token)
    print(df)


def init_pro():
    return ts.pro_api(token)


def trade_cal_test():
    pro = init_pro()
    df = pro.trade_cal(exchange='SSE', is_open='1',
                       start_date='20200101',
                       end_date='20200401',
                       fields='cal_date')
    for date in df['cal_date'].values:
        df = get_daily(trade_date=date)
        print(df)
        break


# 三次重试机制
def get_daily(ts_code='', trade_date='', start_date='', end_date=''):
    for _ in range(3):
        try:
            if trade_date:
                df = init_pro().daily(ts_code=ts_code, trade_date=trade_date)
            else:
                df = init_pro().daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        except:
            time.sleep(1)
        else:
            return df


if __name__ == '__main__':
    get_token_expire()
