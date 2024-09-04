# 导入函数库
from learn.tushare_project.service.basic_service import *
from datetime import datetime, timedelta
import pandas as pd

'''
由于每个人的交易想法不尽相同，只好举一个简单的双均线交易策略为例进行描述，因为“双均线”这是一个接触到投资交易，
都基本会听过的词儿，“专家”告诉你在金叉的时候买，在死叉的时候卖，那实际效果到底是怎么样的呢？
'''
cash = 1000000
stock_num = 0
balance = 1000000
cost = 0
dataframe_maotai = pd.DataFrame(columns=['nature_day', 'cost'],index=[0])
income = 0


# 初始化函数，设定基准等等
class Maotai():

    def __init__(self, date=''):
        # 交易的股票
        self.stock = '600519.XSHG'
        # 长短均线参数
        self.short_len = 5
        self.long_len = 20
        self.date = date

        # # 设定沪深300作为基准
        # set_benchmark('000300.XSHG')
        # # 开启动态复权模式(真实价格)
        # set_option('use_real_price', True)
        # # 过滤掉order系列API产生的比error级别低的log
        # log.set_level('order', 'error')
        # # 打开防未来函数
        # set_option('avoid_future_data', True)
        # # 股票类每笔交易时的手续费是：买入时佣金万分之三，卖出时佣金万分之三加千分之一印花税, 每笔交易佣金最低扣5块钱
        # set_order_cost(OrderCost(close_tax=0.001, open_commission=0.0003, close_commission=0.0003, min_commission=5),
        #                type='stock')
        # # 开盘时运行
        # run_daily(stock_trade, time='open', reference_security='000300.XSHG')

    ## 开盘时运行函数
    def stock_trade(self):
        current_dt = self.date
        stock = self.stock
        short_len = self.short_len
        long_len = self.long_len
        # 获取股票的收盘价
        # 当取日线数据时, 不包括当天的, 即使是在收盘后，没有未来
        BasicService()
        data = BasicService().attribute_history(stock, long_len + 1, ['trade_date', 'close'], current_dt - 1)
        # ascending true 升序 inplace true 直接替换原来的数据，返回none
        data.sort_values(by='trade_date', ascending=True, inplace=True)
        # 计算双均线数据
        data['ma5'] = data['close'].rolling(short_len).mean()
        data['ma20'] = data['close'].rolling(long_len).mean()
        # 昨日MA5和MA20数值
        # loc接受标签名，iloc接受索引 loc[行,列]
        ma5 = data['ma5'].iloc[-1]
        ma20 = data['ma20'].iloc[-1]
        # 前日MA5和MA20数值
        pre_ma5 = data['ma5'].iloc[-2]
        pre_ma20 = data['ma20'].iloc[-2]
        # print(data)
        # print(ma5,ma20,pre_ma5,pre_ma20)
        # 取得当前的可使用的资金
        # cash = context.portfolio.available_cash
        global stock_num, balance, cost, cash, income, dataframe_maotai
        # 如果昨日出现金叉，则今日开盘买入
        if (pre_ma5 < pre_ma20) and (ma5 > ma20) and (cash > data.iloc[-1]['close']):
            print(">>> %s 买入 " % (str(current_dt)))
            # 用所有资金买入股票
            res = BasicService().order_value(data.iloc[-1]['close'], cash)
            stock_num = stock_num + int(res[0])
            balance = int(res[1])
            cost = data.iloc[-1]['close']
            print('买入：{}股，余额：{}元'.format(stock_num, balance))
            balance_now = balance + stock_num * data.iloc[-1]['close']
            income = balance_now - cash
            # 构建df todo
            df_new = pd.DataFrame({'nature_day':current_dt, 'cost':income},index=[0])
            dataframe_maotai=pd.concat([dataframe_maotai,df_new],axis=0,ignore_index=True)
            # 输出买入信息
            # log.info(">>> %s 买入 %d 股 %s" % (str(context.current_dt),
            # context.portfolio.positions[stock].today_amount, stock))
        # 如果昨日出现死叉，则今日开盘全部卖出
        # elif (pre_ma5 > pre_ma20) and (ma5 < ma20) and (stock in context.portfolio.positions.keys()):
        # 输出卖出信息
        # log.info("<<< %s 卖出 %d 股 %s" % (str(context.current_dt),
        # context.portfolio.positions[stock].total_amount, stock))
        # 卖出所有股票,使这只股票的最终持有量为0
        # order_target(stock, 0)
        elif (pre_ma5 > pre_ma20) and (ma5 < ma20):
            print(">>> %s 卖出 " % (str(current_dt)))
            # 暂且设定第二天开盘价等于前一天收盘价，按理应该取第二天开盘价
            balance = balance + stock_num * data.iloc[-1]['close']
            stock_num = 0
            income = balance - cash
            print('卖出全部持仓，余额为:{},本次收益为:{}'.format(balance, income))
            # todo
            df_new = pd.DataFrame({'nature_day': current_dt, 'cost': income},index=[0])
            dataframe_maotai=pd.concat([dataframe_maotai, df_new], axis=0, ignore_index=True)

        else:
            balance_now = balance + stock_num * data.iloc[-1]['close']
            income = balance_now - cash
            print(">>>无操作{}, 当前收益为{}".format(str(current_dt), income))
            # todo
            df_new = pd.DataFrame({'nature_day': current_dt, 'cost': income},index=[0])
            dataframe_maotai=pd.concat([dataframe_maotai,df_new],axis=0,ignore_index=True)
    # 收益csv文件画收益曲线


def work(date=''):
    Maotai(date).stock_trade()


if __name__ == '__main__':
    # 日期加1   - timedelta(days=1)
    date = datetime.now()
    dateint = int(datetime.now().strftime('%Y%m%d'))
    i = 30
    while i > 0:
        print(dateint)
        work(dateint)
        i -= 1
        date = date - timedelta(days=1)
        dateint = int(date.strftime('%Y%m%d'))
