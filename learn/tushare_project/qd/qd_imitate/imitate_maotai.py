import traceback
from datetime import datetime, timedelta

from numpy import angle

from learn.tushare_project.model.qd_imitable_model import Qd_Imitable_Model
from learn.tushare_project.qd.maotai import work
import pandas as pd
import matplotlib.pyplot as plt


def Imitate_Maotai(qd_model):
    date_now = qd_model.start_date
    while int(start_date) <= int(date_now) <= int(end_date):
        work(int(date_now))
        date = datetime.strptime(str(date_now), '%Y%m%d').date()
        # date = datetime.strftime(str(date_now), '%Y%m%d')
        # 这里应该是下一个交易日，为了省事暂时做成第二天
        date_tomorrow = date + timedelta(days=1)
        date_now = date_tomorrow.strftime('%Y%m%d')
    from learn.tushare_project.qd.maotai import dataframe_maotai
    dataframe_maotai = dataframe_maotai.dropna()
    dataframe_maotai["cost"] = dataframe_maotai["cost"].astype(int)
    dataframe_maotai.set_index('nature_day', inplace=True)
    print(dataframe_maotai)
    # data_dict = {'销售额': [56, 10, 10, 1080, 120, 130, 20, 160]}
    # index_lst = ['华北1', '华北2', '西南1', '西北1', '西北2', '东北1', '东北2', '西南2']
    #
    # df = pd.DataFrame(data_dict, index=index_lst)

    dataframe_maotai.plot(kind='line')

    plt.title('收益曲线')
    plt.xlabel('nature_day')
    plt.ylabel('cost')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    # plt.figure(figsize=(100,10))
    plt.show()


def init_Imitate(**kwargs):
    qd_model = Qd_Imitable_Model(**kwargs)
    # qd_model.start_date = int(kwargs.start_date)
    # qd_model.end_date = int(kwargs.end_date)
    return qd_model


if __name__ == '__main__':
    # 日期加1   - timedelta(days=1)
    try:
        start_date = '20240731'
        end_date = '20240831'
        imitate_dict = {
            'start_date': start_date,
            'end_date': end_date
        }
        qd_model = init_Imitate(**imitate_dict)
        Imitate_Maotai(qd_model)
    except Exception as e:
        print('报警：{}'.format(traceback.format_exc()))

    # date = datetime.now()
    # dateint = int(datetime.now().strftime('%Y%m%d'))
    # i = 30
    # while i > 0:
    #     print(dateint)
    #     work(dateint)
    #     i -= 1
    #     date = date - timedelta(days=1)
    #     dateint = int(date.strftime('%Y%m%d'))
