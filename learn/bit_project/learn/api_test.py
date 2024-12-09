import json
import requests
import unittest

'''
https://my.okx.com/docs-v5/zh/?python#overview-rest-authentication 接口文档
https://www.okx.com/zh-hans
实盘API交易地址如下：

REST：https://eea.okx.com
WebSocket公共频道：wss://wseea.okx.com:8443/ws/v5/public
WebSocket私有频道：wss://wseea.okx.com:8443/ws/v5/private
WebSocket业务频道：wss://wseea.okx.com:8443/ws/v5/business
'''


class TestOKXApi(unittest.TestCase):
    # def test_bit_connect_test(self):
    #     response = requests.get('https://my.okx.com/api/v5/account/config')
    #     data = json.loads(response.text)
    #     print(data)

    # 获取交易所的产品配置。 https://my.okx.com/docs-v5/zh/#public-data-rest-api-get-instruments
    '''
    {
    'code': '0',
    'data': [
        {
            'alias': '',
            'baseCcy': 'BTC', # 交易货币币种
            'category': '1',
            'ctMult': '',
            'ctType': '',
            'ctVal': '',
            'ctValCcy': '',
            'expTime': '',
            'instFamily': '',
            'instId': 'BTC-AUD', # 产品id
            'instType': 'SPOT', # 产品类型SPOT：币币
            'lever': '',
            'listTime': '1723771304000',
            'lotSz': '0.0000001', # 下单数量精度
            'maxIcebergSz': '99999999999.0000000000000000', # 冰山委托的单笔最大委托数量 大额的
            'maxLmtAmt': '20000000', # 限价单的单笔最大美元价值
            'maxLmtSz': '99999999999', # 限价单的单笔最大委托数量
            'maxMktAmt': '1000000', # 市价单的单笔最大美元价值
            'maxMktSz': '1000000', # 市价单的单笔最大委托数量
            'maxStopSz': '1000000', # 止盈止损市价委托的单笔最大委托数量
            'maxTriggerSz': '99999999999.0000000000000000', # 计划委托委托的单笔最大委托数量
            'maxTwapSz': '99999999999.0000000000000000', # 时间加权单的单笔最大委托数量
            'minSz': '0.0001', # 最小下单数量
            'optType': '',
            'quoteCcy': 'AUD', # 计价货币币种
            'ruleType': 'normal',
            'settleCcy': '',
            'state': 'live', # 产品状态
            'stk': '',
            'tickSz': '0.1', # 下单精度
            'uly': ''
        }
    ]
}
    '''

    def test_instruments_test(self):
        url = 'https://my.okx.com/api/v5/public/instruments?instType=SPOT'
        response = requests.request("GET", url)
        data = json.loads(response.text)
        print([i['instId'] for i in data['data'] if 'BTC' in i['instId']])
