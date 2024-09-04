import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader.data as pdr
import datetime as dt

'''
pd.to_datetime(["2017-12-25", "2017-12-31"])
GME 获取股票数据
gme.shift(n).下移一行
gme_small.rolling("2d").mean() 回看两天，不满的不算 （均线）
'''
def data_test():
    christmas_str = "2017-12-25"
    christmas = pd.to_datetime(christmas_str)
    print("The type of christmas is", type(christmas), christmas_str)
    for date in ["December 25, 2017", "Dec. 25, 2017",
                 "Monday, Dec. 25, 2017", "25 Dec. 2017", "25th Dec. 2017"]:
        print("pandas interprets {} as {}".format(date, pd.to_datetime(date)))
    christmas_amzn = "2017-12-25T00:00:00+ 00 :00"
    amzn_strftime = "%Y-%m-%dT%H:%M:%S+ 00 :00"
    pd.to_datetime(christmas_amzn, format=amzn_strftime)
    print(christmas_amzn)
    gme = pdr.DataReader("GME", "av-daily", start=dt.datetime(2013, 1, 2),
                         end=dt.datetime(2021, 11, 1),
                         api_key='N78MZQUK4ZCDUABU')
    print(gme.tail())
    gme.index = pd.to_datetime(gme.index)
    # print(gme.loc['2015'])
    print(gme.loc["August 2017"])
    gme_date_column = gme.reset_index()
    gme_date_column.head()
    gme_date_column["index"].dt.year.head()
    fig, ax = plt.subplots(figsize=(10, 4))
    gme["open"].plot(ax=ax, linestyle="--", alpha=0.8)
    gme.rolling("21d").max()["open"].plot(ax=ax, alpha=0.8, linewidth=3)
    ax.legend(["Original", "21 day max"])
    plt.show()

    gme_small = gme.head(6)
    print(gme_small.open.rolling("21d").apply(is_volatile))

def is_volatile(x):
    "Returns a 1 if the variance is greater than 1, otherwise returns 0"
    if x.var() > 1.0:
        return 1.0
    else:
        return 0.0

# BQ 季度 gme.resample("2BQS").agg(["min", "max"]) agg聚合函数
# 例如为了做出最佳决策，我们需要为每个月计算任何一天的收盘价减去该月第一天的开盘价的最大值。
if __name__ == '__main__':
    data_test()
