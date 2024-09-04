import requests
import tushare as ts
import pandas as pd
import json


'''
20240724
https://tushare.pro/document/1?doc_id=40
http restful 采用post方式，通过json body传入接口参数，请求地址为http://api.tushare.pro
curl -X POST -d '{"api_name": "trade_cal", "token": "xxxxxxxx", "params": {"exchange":"", "start_date":"20180901", "end_date":"20181001", "is_open":"0"}, "fields": "exchange,cal_date,is_open,pretrade_date"}' http://api.tushare.pro
{
    "request_id":"af1a9100498311ef9225d00d1a2e4f8b",
    "code":0,
    "msg":"",
    "data":{
        "fields":[
                "ts_code",
                "trade_date",
                "open",
                "high",
                "low",
                "close",
                "pre_close",
                "change",
                "pct_chg",
                "vol",
                "amount"
        ],
        "items":[
        [
                "000001.SZ",
                "20240723",
                10.25,
                10.33,
                10.16,
                10.18,
                10.23,
                -0.05,
                -0.4888,
                1020153.63,
                1046994.471
        ]
        ],
        "has_more":false
        }
}
'''

if __name__ == '__main__':
    print("tushare版本号{}".format(ts.__version__))
    # pro = ts.pro_api('5c704de5a065340a7fd9b1763638b25f3f1b5cf3ae8f231f20ec4053')
    # print("000001历史数据:{}".format(ts.get_hist_data('000001')))
    url = 'http://api.tushare.pro'
    headers = {}
    param = {"api_name": "daily",
             "token": "5c704de5a065340a7fd9b1763638b25f3f1b5cf3ae8f231f20ec4053",
             "params": {'ts_code': '000001.SZ,600000.SH',
                        'start_date':'20240723',
                        'end_date':'20240723'
                        },
             "fields": ["ts_code",
                        "trade_date",
                        "open",
                        "high",
                        "low",
                        "close",
                        "pre_close",
                        "change",
                        "pct_chg",
                        "vol",
                        "amount"]}
    resp = requests.request('POST', url, json=param, headers=headers)
    r = json.loads(resp.text)
    print(r)
    data = r.get('data').get('items')
    fields = r.get('data').get('fields')
    d = pd.DataFrame(data)
    d.columns = fields
    print(d)