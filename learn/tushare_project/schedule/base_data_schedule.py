import tushare
import numpy as np
import pandas as pd
import matplotlib as plt
from learn.tushare_project.api.basedata import basedata
from datetime import datetime
import os

'''
大数据量先落文件再读文件，多线程分批分页处理
    或使用LOAD DATA INFILE：对于大量数据的快速导入，可以使用MySQL的LOAD DATA INFILE语句，它通常比INSERT语句更快。
    插入缓存设置，临时删除索引
    import random

print( random.randint(1,10) )        # 产生 1 到 10 的一个整数型随机数  
print( random.random() )             # 产生 0 到 1 之间的随机浮点数
print( random.uniform(1.1,5.4) )     # 产生  1.1 到 5.4 之间的随机浮点数，区间可以不是整数
print( random.choice('tomorrow') )   # 从序列中随机选取一个元素
print( random.randrange(1,100,2) )   # 生成从1到100的间隔为2的随机整数
'''


class base_data_load():

    def stock_basic_load(self):
        df = basedata().stock_basic()
        date = datetime.now().strftime('%Y-%m-%d')
        df.to_csv('stock_basic_{}.csv'.format(date), index=False)

    '''
    # 定义文件路径
    directory = '/path/to/csv/files'
    
    # 获取目录下所有CSV文件
    all_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.csv')]
    
    # 将所有文件合并成一个DataFrame
    df_list = [pd.read_csv(file) for file in all_files]
    # 遍历主目录下的每个子文件夹
    for folder_name in os.listdir(main_directory):
        folder_path = os.path.join(main_directory, folder_name)
        if os.path.isdir(folder_path):
            # 获取子文件夹中的所有文件
            for file_name in os.listdir(folder_path):
                if file_name.endswith('.csv'):
                    file_path = os.path.join(folder_path, file_name)
                    df = pd.read_csv(file_path)
                    df['folder'] = folder_name  # 添加一列标记数据来源
                    df_list.append(df)
    '''
    # https://blog.csdn.net/a13407142317/article/details/141232312
    # mr以最新的为准所有公司
    def stock_basic_save(self):
        # 改成读取目录下所有stock_basic_文件，最新的和上一批mr后落库，如果只有一个文件则直接落库
        df = pd.read_csv('stock_basic.csv')
        date = datetime.now().strftime('%Y-%m-%d')
        df_new = pd.read_csv('stock_basic_{}.csv'.format('2024-08-27'))

        merged_df = df.merge(df_new, how='right')
        print(merged_df)
        # merged_df.to_csv('stock_basic_mr.csv'.format(date), index=False)
        '''
        获取之后进行数据清洗
        如果我们要删除包含空字段的行，可以使用 dropna() 方法，语法格式如下：

        DataFrame.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
        参数说明：
        
        axis：默认为 0，表示逢空值剔除整行，如果设置参数 axis＝1 表示逢空值去掉整列。
        how：默认为 'any' 如果一行（或一列）里任何一个数据有出现 NA 就去掉整行，如果设置 how='all' 一行（或列）都是 NA 才去掉这整行。
        thresh：设置需要多少非空值的数据才可以保留下来的。
        subset：设置想要检查的列。如果是多个列，可以使用列名的 list 作为参数。
        inplace：如果设置 True，将计算得到的值直接覆盖之前的值并返回 None，修改的是源数据。
        median()  中位数
        mode() 方法计算列的众数
        df['PID'].fillna(df["ST_NUM"].mean(), inplace = True) 用聚合函数替代na
        df.fillna(method='ffill')
        '''
        # 必须一样大才能对比，所以compare不太实用，要先mr
        # print(df.compare(df_new))
        # 数据清洗
        for i in merged_df.columns:
            x = merged_df[i].mode().values[0]
            merged_df[i].fillna(x, inplace=True)
        # df.fillna(method='bfill', inplace=True)
        print(merged_df)
        merged_df.to_csv('stock_basic.csv'.format(date), index=False)


    def daily(self, ts_code, start_date='', end_date=''):
        df = basedata().daily(ts_code, start_date, end_date)
        code = ts_code.split('.')[0]
        if os.path.exists('daily_{}.csv'.format(code)):
            df_old = pd.read_csv('daily_{}.csv'.format(code))
            df_old['trade_date'] = df_old['trade_date'].astype(object)
            df = df_old.merge(df, how='right')
        df.to_csv('daily_{}.csv'.format(code), index=False)





class base_data_schedule():

    def stock_basic_schedule(self):
        pass


if __name__ == '__main__':
    # base_data_load().stock_basic_load()
    base_data_load().daily('600519.SH')
