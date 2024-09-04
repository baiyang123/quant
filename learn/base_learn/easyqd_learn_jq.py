# 克隆自聚宽文章：https://www.joinquant.com/post/3910
# 标题：【量化课堂】因子研究系列之三 -- 技术因子
# 作者：JoinQuant量化课堂

# 多因子选股模型
# 先导入所需要的程序包

import datetime
import numpy as np
import pandas as pd
import time
from jqdata import *
from pandas import Series, DataFrame

'''
================================================================================
总体回测前
================================================================================
'''


# 总体回测前要做的事情
def initialize(context):
    set_params()  # 1 设置策参数
    set_variables()  # 2 设置中间变量
    set_backtest()  # 3 设置回测条件


# 1 设置策略参数
def set_params():
    # 单因子测试时g.factor不应为空
    g.factor = 'MTM3'  # 当前回测的单因子
    g.shift = 21  # 设置一个观测天数（天数）
    g.precent = 0.05  # 持仓占可选股票池比例
    g.index = '000001.XSHG'  # 定义股票池，上交所股票
    # 设定选取sort_rank： True 为最大，False 为最小
    g.sort_rank = False
    # 多因子合并称DataFrame，单因子测试时可以把无用部分删除提升回测速度
    # 定义因子以及排序方式，默认False方式为降序排列，原值越大sort_rank排序越小
    g.factors = {'MTM1': False, 'MTM3': False,
                 'MTM6': False, 'MTM12': False,
                 'TR': False, 'TRC': False,
                 'VAR': False, 'VARC': False,
                 'FLUC': False
                 }


'''
000001.XSHG
上证指数
1991-07-15
SZZS
全部上市A股和B股
000002.XSHG
A股指数
1992-02-21
AGZS
全部上证A股
000003.XSHG
B股指数
1992-08-17
BGZS
全部上市B股
'''


# 2 设置中间变量
def set_variables():
    g.feasible_stocks = []  # 当前可交易股票池
    g.if_trade = False  # 当天是否交易
    g.num_stocks = 0  # 设置持仓股票数目


# 3 设置回测条件
def set_backtest():
    set_benchmark('000001.XSHG')  # 设置为基准
    set_option('use_real_price', True)  # 用真实价格交易
    log.set_level('order', 'error')  # 设置报错等级


'''
================================================================================
每天开盘前
================================================================================
'''


# 每天开盘前要做的事情
def before_trading_start(context):
    # 获得当前日期
    day = context.current_dt.day
    # 获得前一个交易日日期
    yesterday = context.previous_date
    # 调仓日期为上一个交易日后的一个交易日
    rebalance_day = shift_trading_day(yesterday, 1)
    # 如果上一个交易日与下一个交易日月份不同开始交易
    if yesterday.month != rebalance_day.month:
        # 获取调整为day == rebalance_day.day更好？
        if yesterday.day > rebalance_day.day:
            g.if_trade = True
            # 5 设置可行股票池：获得当前开盘的股票池并剔除当前或者计算样本期间停牌的股票
            g.feasible_stocks = set_feasible_stocks(get_index_stocks(g.index), g.shift, context)
            # 6 设置手续费与手续费
            set_slip_fee(context)
            # 购买股票为可行股票池对应比例股票
            g.num_stocks = int(len(g.feasible_stocks) * g.precent)


# 4
# 某一日的前shift个交易日日期 
# 输入：date为datetime.date对象(是一个date，而不是datetime)；shift为int类型
# 输出：datetime.date对象(是一个date，而不是datetime)
def shift_trading_day(date, shift):
    # 获取所有的交易日，返回一个包含所有交易日的 list,元素值为 datetime.date 类型.
    tradingday = get_all_trade_days()
    # 得到date之后shift天那一天在列表中的行标号 返回一个数
    shiftday_index = list(tradingday).index(date) + shift
    # 根据行号返回该日日期 为datetime.date类型
    return tradingday[shiftday_index]


# 5
# 设置可行股票池
# 过滤掉当日停牌的股票,且筛选出前days天未停牌股票
# 输入：stock_list为list类型,样本天数days为int类型，context（见API）
# 输出：list=g.feasible_stocks
def set_feasible_stocks(stock_list, days, context):
    # 得到是否停牌信息的dataframe，停牌的1，未停牌得0
    suspened_info_df = get_price(list(stock_list),
                                 start_date=context.current_dt,
                                 end_date=context.current_dt,
                                 frequency='daily',
                                 fields='paused'
                                 )['paused'].T
    # 过滤停牌股票 返回dataframe
    unsuspened_index = suspened_info_df.iloc[:, 0] < 1
    # 得到当日未停牌股票的代码list:
    unsuspened_stocks = suspened_info_df[unsuspened_index].index
    # 进一步，筛选出前days天未曾停牌的股票list:
    feasible_stocks = []
    current_data = get_current_data()
    for stock in unsuspened_stocks:
        if sum(attribute_history(stock,
                                 days,
                                 unit='1d',
                                 fields=('paused'),
                                 skip_paused=False
                                 )
               )[0] == 0:
            feasible_stocks.append(stock)
    return feasible_stocks


# 6 根据不同的时间段设置滑点与手续费
def set_slip_fee(context):
    # 将滑点设置为0
    set_slippage(FixedSlippage(0))
    # 根据不同的时间段设置手续费
    dt = context.current_dt

    if dt > datetime.datetime(2013, 1, 1):
        set_commission(PerTrade(buy_cost=0.0003,
                                sell_cost=0.0013,
                                min_cost=5))

    elif dt > datetime.datetime(2011, 1, 1):
        set_commission(PerTrade(buy_cost=0.001,
                                sell_cost=0.002,
                                min_cost=5))

    elif dt > datetime.datetime(2009, 1, 1):
        set_commission(PerTrade(buy_cost=0.002,
                                sell_cost=0.003,
                                min_cost=5))

    else:
        set_commission(PerTrade(buy_cost=0.003,
                                sell_cost=0.004,
                                min_cost=5))


'''
================================================================================
每天交易时
================================================================================
'''


def handle_data(context, data):
    # 如果为交易日
    if g.if_trade == True:
        # 8 获得买入卖出信号，输入context，输出股票列表list
        # 字典中对应默认值为false holding_list筛选为true，则选出因子得分最大的
        holding_list = get_stocks(g.feasible_stocks,
                                  context,
                                  g.factors,
                                  asc=g.sort_rank,
                                  factor_name=g.factor)
        # 9 重新调整仓位，输入context,使用信号结果holding_list
        rebalance(context, holding_list)
    g.if_trade = False


# 7 获得因子信息
# stocks_list调用g.feasible_stocks factors调用字典g.factors
# 输出所有对应数据和对应排名，DataFrame
def get_factors(stocks_list, context, factors):
    # 从可行股票池中生成股票代码列表
    df_all_raw = pd.DataFrame(stocks_list)
    # 修改index为股票代码
    df_all_raw['code'] = df_all_raw[0]
    df_all_raw.index = df_all_raw['code']
    # 格式调整，没有一步到位中间有些东西还在摸索，简洁和效率的一个权衡
    del df_all_raw[0]
    stocks_list300 = list(df_all_raw.index)
    # 每一个指标量都合并到一个dataframe里
    for key, value in g.factors.items():
        # 构建一个新的字符串，名字叫做 'get_df_'+ 'key'
        tmp = 'get_df' + '_' + key
        # 声明字符串是个方程
        aa = globals()[tmp](stocks_list, context, value)
        # 合并处理
        df_all_raw = pd.concat([df_all_raw, aa], axis=1)
    # 删除code列
    del df_all_raw['code']
    # 对于新生成的股票代码取list
    stocks_list_more = list(df_all_raw.index)
    # 可能在计算过程中并如的股票剔除
    for stock in stocks_list_more[:]:
        if stock not in stocks_list300:
            df_all_raw.drop(stock)
    return df_all_raw


# 8获得调仓信号
# 原始数据重提取因子打分排名
def get_stocks(stocks_list, context, factors, asc, factor_name):
    # 7获取原始数据
    df_all_raw1 = get_factors(stocks_list, context, factors)
    # 根据factor生成列名
    score = factor_name + '_' + 'sorted_rank'
    try:
        stocks = list(df_all_raw1.sort(score, ascending=asc).index)
    except AttributeError:
        stocks = list(df_all_raw1.sort_values(score, ascending=asc).index)
    return stocks


# 9交易调仓
# 依本策略的买入信号，得到应该买的股票列表
# 借用买入信号结果，不需额外输入
# 输入：context（见API）
def rebalance(context, holding_list):
    # 每只股票购买金额
    every_stock = context.portfolio.portfolio_value / g.num_stocks
    # 空仓只有买入操作
    if len(list(context.portfolio.positions.keys())) == 0:
        # 原设定重scort始于回报率相关打分计算，回报率是升序排列
        for stock_to_buy in list(holding_list)[0:g.num_stocks]:
            order_target_value(stock_to_buy, every_stock)
    else:
        # 不是空仓先卖出持有但是不在购买名单中的股票
        for stock_to_sell in list(context.portfolio.positions.keys()):
            if stock_to_sell not in list(holding_list)[0:g.num_stocks]:
                order_target_value(stock_to_sell, 0)
        # 因order函数调整为顺序调整，为防止先行调仓股票由于后行调仓股票占金额过大不能一次调整到位，这里运行两次以解决这个问题
        for stock_to_buy in list(holding_list)[0:g.num_stocks]:
            order_target_value(stock_to_buy, every_stock)
        for stock_to_buy in list(holding_list)[0:g.num_stocks]:
            order_target_value(stock_to_buy, every_stock)


# 因子数据处理函数单独编号，与系列文章中对应
# 20MTM1
# 一个月动能，输入stock_list, context, asc = True/False
# 输出：dataframe，index为code
def get_df_MTM1(stock_list, context, asc):
    # 上个交易日日期
    yest = context.previous_date
    # 一个shift前的交易日日期
    days_1shift_before = shift_trading_day(yest, shift=-21)
    # 获得上个交易日收盘价
    df_price_info = get_price(list(stock_list),
                              start_date=yest,
                              end_date=yest,
                              frequency='daily',
                              fields='close')['close'].T
    # 1个月前收盘价信息
    df_price_info_1shift = get_price(list(stock_list),
                                     start_date=days_1shift_before,
                                     end_date=days_1shift_before,
                                     frequency='daily',
                                     fields='close')['close'].T
    # 1月的收益率,Series
    Series_mtm1 = (df_price_info.ix[:, yest]
                   - df_price_info_1shift.ix[:, days_1shift_before]
                   ) / df_price_info_1shift.ix[:, days_1shift_before]
    # 生成dataframe格式
    df_MTM1 = pd.DataFrame({'MTM1': Series_mtm1})
    # 删除NaN
    df_MTM1 = df_MTM1[pd.notnull(df_MTM1['MTM1'])]
    # 排序给出排序打分，MTM1
    df_MTM1['MTM1_sorted_rank'] = df_MTM1['MTM1'].rank(ascending=asc, method='dense')
    return df_MTM1


# 21MTM3
# 三个月动能，输入stock_list, context, asc = True/False
# 输出：dataframe，index为code
def get_df_MTM3(stock_list, context, asc):
    # 上个交易日日期
    yest = context.previous_date
    # 3个shift前的交易日日期
    days_3shift_before = shift_trading_day(yest, shift=-63)
    # 获得上个交易日收盘价
    df_price_info = get_price(list(stock_list),
                              start_date=yest,
                              end_date=yest,
                              frequency='daily',
                              fields='close')['close'].T
    # 1个月前收盘价信息
    df_price_info_3shift = get_price(list(stock_list),
                                     start_date=days_3shift_before,
                                     end_date=days_3shift_before,
                                     frequency='daily',
                                     fields='close')['close'].T
    # 3个月的收益率,Series
    Series_mtm3 = (df_price_info.ix[:, yest]
                   - df_price_info_3shift.ix[:, days_3shift_before]
                   ) / df_price_info_3shift.ix[:, days_3shift_before]
    # 生成dataframe格式
    df_MTM3 = pd.DataFrame({'MTM3': Series_mtm3})
    # 删除NaN
    df_MTM3 = df_MTM3[pd.notnull(df_MTM3['MTM3'])]
    # 排序给出排序打分，MTM3
    df_MTM3['MTM3_sorted_rank'] = df_MTM3['MTM3'].rank(ascending=asc, method='dense')
    return df_MTM3


# 22MTM6
# 六个月动能，输入stock_list, context, asc = True/False
# 输出：dataframe，index为code
def get_df_MTM6(stock_list, context, asc):
    # 获得上一个交易日日期
    yest = context.previous_date
    # 一个shift前的交易日日期
    days_6shift_before = shift_trading_day(yest, shift=-125)
    # 获得上个交易日收盘价
    df_price_info = get_price(list(stock_list),
                              start_date=yest,
                              end_date=yest,
                              frequency='daily',
                              fields='close')['close'].T
    # 6个月前收盘价信息
    df_price_info_6shift = get_price(list(stock_list),
                                     start_date=days_6shift_before,
                                     end_date=days_6shift_before,
                                     frequency='daily',
                                     fields='close')['close'].T
    # MTM6六月动量,Series
    Series_mtm6 = (df_price_info.ix[:, yest]
                   - df_price_info_6shift.ix[:, days_6shift_before]
                   ) / df_price_info_6shift.ix[:, days_6shift_before]
    # 生成dataframe格式
    df_MTM6 = pd.DataFrame({'MTM6': Series_mtm6})
    # 删除NaN
    df_MTM6 = df_MTM6[pd.notnull(df_MTM6['MTM6'])]
    # 排序给出排序打分，MTM6
    df_MTM6['MTM6_sorted_rank'] = df_MTM6['MTM6'].rank(ascending=asc, method='dense')
    return df_MTM6


# 23MTM12
# 十二个月动能，输入stock_list, context, asc = True/False
# 输出：dataframe，index为code
def get_df_MTM12(stock_list, context, asc):
    # 上个交易日日期
    yest = context.previous_date
    # 一个shift前的交易日日期
    days_12shift_before = shift_trading_day(yest, shift=-250)
    # 获得上个交易日收盘价
    df_price_info = get_price(list(stock_list),
                              start_date=yest,
                              end_date=yest,
                              frequency='daily',
                              fields='close')['close'].T
    # 12个月前收盘价信息
    df_price_info_12shift = get_price(list(stock_list),
                                      start_date=days_12shift_before,
                                      end_date=days_12shift_before,
                                      frequency='daily',
                                      fields='close')['close'].T
    # MTM12月动量,Series
    Series_mtm12 = (df_price_info.ix[:, yest]
                    - df_price_info_12shift.ix[:, days_12shift_before]
                    ) / df_price_info_12shift.ix[:, days_12shift_before]
    # 生成dataframe格式
    df_MTM12 = pd.DataFrame({'MTM12': Series_mtm12})
    # 删除NaN
    df_MTM12 = df_MTM12[pd.notnull(df_MTM12['MTM12'])]
    # 排序给出排序打分，MTM12
    df_MTM12['MTM12_sorted_rank'] = df_MTM12['MTM12'].rank(ascending=asc, method='dense')
    return df_MTM12


# 24TR
# 得到一个dataframe：包含股票代码、换手率(%)TR和TR_sorted_rank
# 默认date = context.previous_date,使用默认值，避免未来函数，不建议修改
def get_df_TR(stock_list, context, asc):
    # 获取价格数据,当前到21天前一共22行，与之前get_price不同，没有使用转置，行为股票代码
    # 列为日期，上边为较早最后为较晚
    df_volume_info_between_1shift = get_price(list(stock_list),
                                              count=22,
                                              end_date=context.previous_date,
                                              frequency='daily',
                                              fields='volume')['volume'].T
    # 换手量加总
    df_volume_info_between_1shift['VOLUME'] = df_volume_info_between_1shift.sum(axis=1, skipna=True)
    # 获得换手率(%)turnover_ratio
    df_TR = get_fundamentals(query(valuation.code, valuation.circulating_cap
                                   ).filter(valuation.code.in_(stock_list)), context.previous_date)
    # 删除nan
    df_TR = df_TR.dropna()
    # 使用股票代码作为index
    df_TR.index = df_TR.code
    # 生成TR
    df_TR['TR'] = df_volume_info_between_1shift['VOLUME'] / (df_TR['circulating_cap'] * 10000)
    # 删除无用数据
    del df_TR['code']
    del df_TR['circulating_cap']
    # 生成排名序数
    df_TR['TR_sorted_rank'] = df_TR['TR'].rank(ascending=asc, method='dense')
    return df_TR


# 25TRC
# 得到一个dataframe：包含股票代码、净资产收益率TR变动turnover_ratio_change(TRC)和TRC_sorted_rank
def get_df_TRC(stock_list, context, asc):
    # 一个shift前的交易日日期
    days_1shift_before = shift_trading_day(context.previous_date, shift=-21)
    # 获取价格数据,当前到21天前一共22行，与之前get_price不同，没有使用转置，行为股票代码
    # 列为日期，上边为较早最后为较晚
    df_volume_info_between_1shift = get_price(list(stock_list),
                                              count=22,
                                              end_date=days_1shift_before,
                                              frequency='daily',
                                              fields='volume')['volume'].T
    # 换手量加总
    df_volume_info_between_1shift['VOLUME'] = df_volume_info_between_1shift.sum(axis=1, skipna=True)
    # 获得换手率(%)turnover_ratio
    df_TRC = get_fundamentals(query(valuation.code, valuation.circulating_cap
                                    ).filter(valuation.code.in_(stock_list)), days_1shift_before)
    # 删除nan
    df_TRC = df_TRC.dropna()
    # 使用股票代码作为index
    df_TRC.index = df_TRC.code
    # 生成TR
    df_TRC['tr'] = df_volume_info_between_1shift['VOLUME'] / (df_TRC['circulating_cap'] * 10000)
    # 获取TR
    df_TR = get_df_TR(stock_list, context, False)
    # 使用TR为当期数据，turnover为上一个shift数据
    df_TRC['TR'] = df_TR['TR']
    # 计算变化量,TR为上个月，tr为上上月
    df_TRC['TRC'] = df_TRC['tr'] - df_TRC['TR']
    # 删除nan
    df_TRC = df_TRC.dropna()
    # 生成排名序数
    df_TRC['TRC_sorted_rank'] = df_TRC['TRC'].rank(ascending=asc, method='dense')
    # 删除无用数据
    del df_TRC['code']
    del df_TRC['circulating_cap']
    return df_TRC


# 26VAR
# 波动，股票收盘价方差
# 一个月内收盘价，dataframe，index为code
def get_df_VAR(stock_list, context, asc):
    # 获取价格数据,当前到21天前一共22行，与之前get_price不同，没有使用转置，行为股票代码
    # 列为日期，上边为较早最后为较晚
    df_price_info_between_1shift = get_price(list(stock_list),
                                             count=22,
                                             end_date=context.previous_date,
                                             frequency='daily',
                                             fields='close')['close']
    # 生成一个空得列
    x = []
    # 计算日回报率为前一天收盘价/当天收盘价 - 1
    for i in range(0, 21):
        x.append(df_price_info_between_1shift.iloc[i + 1]
                 / df_price_info_between_1shift.iloc[i] - 1)
    # 进行转置
    df_VAR_info = pd.DataFrame(x).T
    # 生成方差
    df_VAR_info['VAR'] = df_VAR_info.var(axis=1, skipna=True)
    # 生成新的DataFrame
    df_VAR = pd.DataFrame(df_VAR_info['VAR'])
    # 删除nan
    df_VAR = df_VAR.dropna()
    # 排序给出排序打分，MTM6
    df_VAR['VAR_sorted_rank'] = df_VAR['VAR'].rank(ascending=asc, method='dense')
    return df_VAR


# 27VARC
# 波动率变动
def get_df_VARC(stock_list, context, asc):
    # 一个shift前的交易日日期
    days_1shift_before = shift_trading_day(context.previous_date, shift=-21)
    # VAR当期值（上个月）获取, 排序没关系，这里随便假设
    df_VARC = get_df_VAR(stock_list, context, True)
    df_price_info_between_2shift = get_price(list(stock_list),
                                             count=22,
                                             end_date=days_1shift_before,
                                             frequency='daily',
                                             fields='close')['close']
    # 生成一个空得列
    x = []
    # 计算日回报率为前一天收盘价/当天收盘价 - 1
    for i in range(0, 21):
        x.append(df_price_info_between_2shift.iloc[i + 1]
                 / df_price_info_between_2shift.iloc[i] - 1)
    # 进行转置
    df_VAR_info = pd.DataFrame(x).T
    # 生成方差
    df_VAR_info['VAR'] = df_VAR_info.var(axis=1, skipna=True)
    # 生成新的DataFrame,VAR大写为上个月得，var小写为上上月
    df_VARC['var'] = pd.DataFrame(df_VAR_info['VAR'])
    # VAR_change VARC
    df_VARC['VARC'] = df_VARC['var'] - df_VARC['VAR']
    # 删除nan
    df_VARC = df_VARC.dropna()
    # 排序给出排序打分
    df_VARC['VARC_sorted_rank'] = df_VARC['VARC'].rank(ascending=asc, method='dense')
    del df_VARC['VAR']
    del df_VARC['VAR_sorted_rank']
    return df_VARC


# 28FLUC
# 震荡指标=[(前月最高价-最低价)/(前月月初股价+月末股价)] fluctuations
def get_df_FLUC(stock_list, context, asc):
    # 上个交易日日期
    yest = context.previous_date
    # 一个shift前的交易日日期
    days_1shift_before = shift_trading_day(yest, shift=-21)
    # 获得收盘价信息
    df_price_info_between_1shift = get_price(list(stock_list),
                                             start_date=days_1shift_before,
                                             end_date=yest,
                                             frequency='daily',
                                             fields='close')['close'].T
    # 根据给出的公式进行计算
    Series_aa = ((df_price_info_between_1shift.max(axis=1, skipna=True)
                  - df_price_info_between_1shift.min(axis=1, skipna=True)) /
                 (df_price_info_between_1shift.ix[:, 0]
                  - df_price_info_between_1shift.ix[:, -1]))
    # 获得股票代码作为index
    Series_aa.index = df_price_info_between_1shift.index
    # 生成datafram格式
    df_FLUC = pd.DataFrame(Series_aa)
    # 定义变量名称
    df_FLUC['FLUC'] = pd.DataFrame(Series_aa)
    # 删除nan
    df_FLUC = df_FLUC.dropna()
    del df_FLUC[0]
    # 生成排序数据
    df_FLUC['FLUC_sorted_rank'] = df_FLUC['FLUC'].rank(ascending=asc, method='dense')
    return df_FLUC


'''
================================================================================
每天收盘后
================================================================================
'''


# 每日收盘后要做的事情（本策略中不需要）
def after_trading_end(context):
    return