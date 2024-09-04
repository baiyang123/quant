import pandas as pd
import matplotlib.pyplot as plt

'''
数据处理
世界银行的世界发展指标数据
自动对齐
层次索引 切片索引
我们应该如何选择索引?
每一列都应该有一个变量。
每行都应该有一个观察值。
'''
def index():
    url = "https://raw.githubusercontent.com/amoreira2/Lectures/main/assets/data/wdi_data.csv"
    df = pd.read_csv(url)
    # df.info()
    df_small = df.head(5)
    df_year = df.set_index(["year"])
    df_year.loc[df_year["country"] == "United States", "GDP"].loc[2010]
    wdi = df.set_index(["country", "year"])
    # print(wdi.loc[("United States", 2010), "GDP"])
    # print(wdi.loc[(["United States","Canada"],[2010,2011]),'GDP'])
    # print(wdi.loc[["United States", "Canada"]])
    # print(wdi.sort_index() .loc[pd.IndexSlice[:, [2005, 2007, 2009]], :])
    print(wdi.T.loc[:, (["United States", "Canada"], [2008,2010])])
    print(wdi.shape)
    # df.plot()
    # plt.show()

def time_index():
    pass


if __name__ == '__main__':
    index()