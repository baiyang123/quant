import pandas as pd

class BasicService:

    def attribute_history(self, ts_code, count: int, fields: list, current_dt: str):
        df_all = pd.read_csv('D:/oaTest/quant/learn/tushare_project/schedule/daily_{}.csv'.format(ts_code.split('.')[0]))
        df = df_all.query('trade_date <= {}'.format(current_dt)).head(count)[fields]
        df.reset_index(drop=True, inplace=True)
        return df

    def order_value(self, stock_value, cash):
        return divmod(cash, stock_value)


if __name__ == '__main__':
    df = BasicService().attribute_history('600519.SH', 20, ['close'], '20240828')
    print(df)