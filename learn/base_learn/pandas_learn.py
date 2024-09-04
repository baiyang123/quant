import pandas as pd
import matplotlib.pyplot as plt

'''
方法.head和.tail显示行分别位于系列的开头和结尾（通常默认是五行）。
Series
DataFrames
.corr 相关系数
dtypes 类型
pandas 已经有了一些最常用的聚合。

例如：

均值 ( mean)
方差 ( var)
标准偏差 ( std)
最小 ( min)
中位数 ( median)
最大值 ( max)
ETC…
'''


def series():
    values = [5.6, 5.3, 4.3, 4.2, 5.8, 5.3, 4.6, 7.8, 9.1, 8., 5.7]
    years = list(range(1995, 2017, 2))
    unemp = pd.Series(data=values, index=years, name="Unemployment")
    print(unemp.loc[[1995, 2005, 2015]])
    ax = unemp.plot()
    plt.show()


def dataFrames():
    years = list(range(1995, 2017, 2))
    data = {
        "NorthEast": [5.9, 5.6, 4.4, 3.8, 5.8, 4.9, 4.3, 7.1, 8.3, 7.9, 5.7],
        "MidWest": [4.5, 4.3, 3.6, 4., 5.7, 5.7, 4.9, 8.1, 8.7, 7.4, 5.1],
        "South": [5.3, 5.2, 4.2, 4., 5.7, 5.2, 4.3, 7.6, 9.1, 7.4, 5.5],
        "West": [6.6, 6., 5.2, 4.6, 6.5, 5.5, 4.5, 8.6, 10.7, 8.5, 6.1],
        "National": [5.6, 5.3, 4.3, 4.2, 5.8, 5.3, 4.6, 7.8, 9.1, 8., 5.7]
    }

    unemp_region = pd.DataFrame(data, index=years)
    unemp_region["UnweightedMean"] = (unemp_region["NorthEast"] +
                                      unemp_region["MidWest"] +
                                      unemp_region["South"] +
                                      unemp_region["West"]) / 4
    unemp_region.loc[1995, "UnweightedMean"] = 0.0
    names = {"NorthEast": "NE",
             "MidWest": "MW",
             "South": "S",
             "West": "W"}
    unemp_region.rename(columns=names, inplace=True)
    print(unemp_region)
    # unemp_region.plot()
    # plt.show()


'''
如上所示，聚合的默认值是聚合每一列。

但是，通过使用axis关键字参数，您也可以按行进行聚合。

size.var(axis=1).head()
编写一个 Python 函数，它接受一个 Series 并输出一个新的 Series。
将我们的新函数作为参数传递给apply方法（或者，transform方法）。
size_small.loc[[True, True, True, False, False], [True, False, False, False, False, True, True]]
big_Autos = size_small["Autos"] > size_small["Banks"] 
size_small.loc[big_Autos]
.isin .any .all
any当至少一个输入为 True 时返回 True，all而仅当所有输入为 True时返回 True。
'''
def pandas():
    url = "https://raw.githubusercontent.com/amoreira2/Lectures/main/assets/data/49_Industry_Portfolios.CSV"
    industret_raw = pd.read_csv(url, parse_dates=["Date"])
    # print(industret_raw.head())
    size_all = (
        industret_raw
            .reset_index()
            .pivot_table(index="Date", columns="industry", values="size")
    )
    industries = [
        "Autos", "Banks", "Meals", "Softw",
        "Smoke", "Telcm", "Mines"
    ]
    size = size_all[industries]
    size.tail()
    size.agg([min, max, 'mean', 'std'])
    # print(size.agg([min, max, 'mean', 'std']))
    print(size.head().value_counts())
    size.agg([min, max, 'mean', 'std']).plot(figsize=(8, 6), logy=True)
    # plt.show()


if __name__ == '__main__':
    pandas()
