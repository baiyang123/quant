# 导入函数库
from jqdata import *

'''
由于每个人的交易想法不尽相同，只好举一个简单的双均线交易策略为例进行描述，因为“双均线”这是一个接触到投资交易，
都基本会听过的词儿，“专家”告诉你在金叉的时候买，在死叉的时候卖，那实际效果到底是怎么样的呢？
'''
# 初始化函数，设定基准等等
def initialize(context):
    # 交易的股票
    g.stock = '600519.XSHG'
    # 长短均线参数
    g.short_len = 5
    g.long_len = 20

    # 设定沪深300作为基准
    set_benchmark('000300.XSHG')
    # 开启动态复权模式(真实价格)
    set_option('use_real_price', True)
    # 过滤掉order系列API产生的比error级别低的log
    log.set_level('order', 'error')
    # 打开防未来函数
    set_option('avoid_future_data', True)
    # 股票类每笔交易时的手续费是：买入时佣金万分之三，卖出时佣金万分之三加千分之一印花税, 每笔交易佣金最低扣5块钱
    set_order_cost(OrderCost(close_tax=0.001, open_commission=0.0003, close_commission=0.0003, min_commission=5),
                   type='stock')
    # 开盘时运行
    run_daily(stock_trade, time='open', reference_security='000300.XSHG')


## 开盘时运行函数
def stock_trade(context):
    stock = g.stock
    short_len = g.short_len
    long_len = g.long_len
    # 获取股票的收盘价
    # 当取日线数据时, 不包括当天的, 即使是在收盘后，没有未来
    data = attribute_history(stock, long_len + 1, '1d', ['close'])
    # 计算双均线数据
    data['ma5'] = data['close'].rolling(short_len).mean()
    data['ma20'] = data['close'].rolling(long_len).mean()
    # 昨日MA5和MA20数值
    ma5 = data['ma5'].iloc[-1]
    ma20 = data['ma20'].iloc[-1]
    # 前日MA5和MA20数值
    pre_ma5 = data['ma5'].iloc[-2]
    pre_ma20 = data['ma20'].iloc[-2]
    # 取得当前的可使用的资金
    cash = context.portfolio.available_cash

    # 如果昨日出现金叉，则今日开盘买入
    if (pre_ma5 < pre_ma20) and (ma5 > ma20) and (cash > 0):
        # 用所有资金买入股票
        order_value(stock, cash)
        # 输出买入信息
        log.info(">>> %s 买入 %d 股 %s" % (str(context.current_dt),
                                        context.portfolio.positions[stock].today_amount, stock))
    # 如果昨日出现死叉，则今日开盘全部卖出
    elif (pre_ma5 > pre_ma20) and (ma5 < ma20) and (stock in context.portfolio.positions.keys()):
        # 输出卖出信息
        log.info("<<< %s 卖出 %d 股 %s" % (str(context.current_dt),
                                        context.portfolio.positions[stock].total_amount, stock))
        # 卖出所有股票,使这只股票的最终持有量为0
        order_target(stock, 0)

# 收益csv文件画收益曲线