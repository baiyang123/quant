'''
能够使用字符串方法来清理以字符串形式出现的数据
能够删除丢失的数据
使用清理方法准备和分析真实数据集

清理数据 我们准备了这些内容
清理数据
字符串方法
类型转换
缺失数据
案例分析
an class="nolink">附录：.str方法的执行效率
练习

astype 类型转换
df.isnull().any(axis=0)
axis=0 表示列；axis=1 表示行
.str 效率很高
contract join 等拼接
'''

import numpy as np
import pandas as pd
import matplotlib as plt


def data_clean_test():
    df = pd.DataFrame({"numbers": ["#23", "#24", "#18", "#14", "#12", "#10", "#35"],
                       "nums": ["23", "24", "18", "14", np.nan, "XYZ", "35"],
                       "colors": ["green", "red", "yellow", "orange", "purple", "blue", "pink"],
                       "other_column": [0, 1, 0, 2, 1, 0, 2]})
    df["numbers_str"] = df["numbers"].str.replace("#", "")
    df["colors"] = df["colors"].str.capitalize()  # 转化大写
    df["numbers_numeric"] = pd.to_numeric(df["numbers_str"])
    df["numbers_numeric"] = df["numbers_numeric"].astype(float)
    print(df, '\n', df.dtypes)
    df.dropna() # 忽略整行
    df.fillna(value=100) # 预测填值
    # bfill()函数用于向后填充缺失值，即用后面的非缺失值来填充当前的缺失值；ffill()函数用于向前填充缺失值，即用前面的非缺失值来填充当前的缺失值。
    df.fillna(method="bfill")



if __name__ == '__main__':
    data_clean_test()