from datetime import datetime
from learn.tushare_project.qd import maotai

def OneStockQD(date=''):
    maotai.work(date)

if __name__ == '__main__':
    # 模仿从某一条一直到最后
    OneStockQD()