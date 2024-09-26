import os
import re
from random import SystemRandom
from typing import Optional
from ddddocr import DdddOcr

from requests import Response, Session, get

from .const import _urls, _base_headers
from .utils import get_logger, emt_trade_encrypt

logger = get_logger(__name__)
_em_validate_key = ""
session = Session()
ocr = DdddOcr(show_ad=False)

def login(username: str = "", password: str = "", duration: int = 30) -> Optional[str]:
    """登录接口.

    :param str username: 用户名
    :param str password: 密码(明文)
    :param duration: 在线时长(分钟), defaults to 30
    :type duration: int, optional
    :return:
    """
    if not username:
        username = os.getenv("EM_USERNAME", "")
    if not password:
        password = os.getenv("EM_PASSWORD", "")
    random_num, code = _get_captcha_code()
    headers = _base_headers.copy()
    headers["X-Requested-With"] = "XMLHttpRequest"
    headers["Referer"] = "https://jywg.18.cn/Login?el=1&clear=&returl=%2fTrade%2fBuy"
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    url = _urls["login"]
    data = {
        "userId": username.strip(),
        "password": emt_trade_encrypt(password.strip()),
        "randNumber": random_num,
        "identifyCode": code,
        "duration": duration,
        "authCode": "",
        "type": "Z",
        "secInfo": "",
    }
    resp = session.post(url, headers=headers, data=data)
    _check_resp(resp)
    try:
        logger.info(f"login success for {resp.json()}")
        return _get_em_validate_key()
    except KeyError as e:
        logger.error(f"param data found exception:[{e}], [data={resp}]")


def _get_captcha_code():
    """get random number and captcha code."""
    cryptogen = SystemRandom()
    random_num = cryptogen.random()
    resp = get(f"{_urls['yzm']}{random_num}", headers=_base_headers, timeout=60)
    _check_resp(resp)
    code = ocr.classification(resp.content)
    if code:
        try:
            code = int(code)
        except Exception as e:
            logger.error(f"get_captcha_code found exception: {e}, ocr result={code}")
            return _get_captcha_code()
    return random_num, code


def _check_resp(resp: Response):
    if resp.status_code != 200:
        logger.error(f"request {resp.url} fail, code={resp.status_code}, response={resp.text}")
        raise


def _get_em_validate_key():
    """获取 em_validatekey"""
    url = "https://jywg.18.cn/Trade/Buy"
    resp = session.get(url, headers=_base_headers)
    _check_resp(resp)
    match_result = re.findall(r'id="em_validatekey" type="hidden" value="(.*?)"', resp.text)
    if match_result:
        _em_validatekey = match_result[0].strip()
        global _em_validate_key
        _em_validate_key = _em_validatekey
        return _em_validatekey



def query_funds_flow(size, start_time, end_time):
    """查询资金.

    :param int size: 请求的数据的条目数
    :param str start_time: 起始时间, 格式"%Y-%m-%d"
    :param str end_time: 起始时间, 格式"%Y-%m-%d"
    :return dict:
    """
    resp = _query_something("query_funds_flow", {"qqhs": size, "dwc": "", "st": start_time, "et": end_time})
    if resp:
        return resp.json()


def _query_something(tag: str, req_data: Optional[dict] = None) -> Optional[Response]:
    """通用查询函数

    :param tag: 请求类型
    :param req_data: 请求提交数据,可选
    :return:
    """
    if not _em_validate_key:
        validate_key = login()
    else:
        validate_key = _em_validate_key
    logger.info(validate_key)
    assert tag in _urls, f"{tag} not in url list"
    url = _urls[tag] + validate_key
    if req_data is None:
        req_data = {
            "qqhs": 100,
            "dwc": "",
        }
    headers = _base_headers.copy()
    headers["X-Requested-With"] = "XMLHttpRequest"
    logger.debug(f"(tag={tag}), (data={req_data}), (url={url})")
    resp = session.post(url, headers=headers, data=req_data)
    _check_resp(resp)
    return resp


def create_order(stock_code, trade_type, price: float, amount: int):
    """交易接口, 买入或卖出.

    :param str stock_code: 股票代码
    :param str trade_type: 交易方向,B for buy, S for sell
    # :param str market: 股票市场,HA 上海, SA  # "market": market, # 非必填
    :param float price: 股票价格
    :param int amount: 买入/卖出数量
    """
    req_data = {
        "stockCode": stock_code,
        "tradeType": trade_type,
        "zqmc": "",
        "price": price,
        "amount": amount,
    }
    # response = self.s.post(self._get_api_url('submit'), data={
    #     "stockCode": security,
    #     "price": price,
    #     "amount": amount,
    #     "zqmc": "unknown",
    #     "tradeType": entrust_bs
    # }).json()
    resp = _query_something("create_order", req_data=req_data)
    if resp:
        logger.info(resp.json())
        return resp.json()

'''
D:\oaTest\mdm\venv\Scripts\python.exe D:/oaTest/quant/learn/jywg_project/api/test_core_api.py
2024-09-26 10:15:53,052 learn.jywg_project.emtl.core login 49: INFO    : login success for {'Status': '-1', 'Return_Code': -1, 'Message': '请输入资金账号！', 'Khmc': None, 'Token': None, 'Session_Id': None, 'Date': None, 'Syspm1': None, 'Syspm2': None, 'Syspm3': None, 'Time': None, 'Radom_code': None, 'IsNeedRePwd': None}
2024-09-26 10:15:53,390 learn.jywg_project.emtl.core login 49: INFO    : login success for {'Message': '', 'Status': 0, 'Errcode': 0, 'Data': [{'khmc': '白阳', 'Date': '20240926', 'Time': '101553', 'Syspm1': '540340352219', 'Syspm2': '5403', 'Syspm3': '', 'Syspm_ex': '4'}]}
2024-09-26 10:15:53,442 learn.jywg_project.emtl.core _query_something 115: INFO    : 4c6790c3-ea20-4822-83e1-04a936d9a12f
4c6790c3-ea20-4822-83e1-04a936d9a12f
2024-09-26 10:15:53,504 learn.jywg_project.emtl.core _query_something 115: INFO    : 4c6790c3-ea20-4822-83e1-04a936d9a12f
{'Message': None, 'Status': 0, 'Data': [{'Fsrq': '20240925', 'Fssj': '145225', 'Zqdm': '000736', 'Zqmc': '中交地产', 'Ywsm': '证券买入', 'Cjsl': '100', 'Hbdm': 'RMB', 'Cjjg': '10.4000', 'Cjje': '1040.00', 'Sxf': '5.00', 'Jsxf': '4.93', 'Jygf': '0.00', 'Yhs': '0.00', 'Ghf': '0.00', 'Gfye': '100', 'Zjye': '71.00', 'Cjbh': '0102000061306526', 'Gddm': '0262481003', 'Htbh': '0401379516', 'Market': 'SA', 'Dwc': '', 'Qqhs': None, 'Fsje': '-1045.00', 'Qsrq': '20240925', 'Ywrq': '20240925', 'Cjsj': '14522569', 'Ywdm': '220000', 'Zjzh': '540340352219', 'Khxm': '白阳', 'Mmlb': '0B', 'Cjbs': '1', 'Qsf': '0.00', 'Qtfy': '0.00', 'Jsf': '0.00', 'Zgf': '0.00', 'Gpye': '100', 'Wtsl': '100', 'Wtjg': '10.4700', 'Fqf': '0', 'Wbyh': '2020', 'Wbyhmc': None, 'Wbzh': '', 'Yjyhs': '0.00', 'Yjghf': '0.01', 'Yjqsf': '0.00', 'Yjjygf': '0.00', 'Yjjsf': '0.04', 'Yjzgf': '0.02', 'Yjqtf': '0.00', 'Yjfxj': '0.00'}, {'Fsrq': '20240925', 'Fssj': '145106', 'Zqdm': '', 'Zqmc': '', 'Ywsm': '银行转证券', 'Cjsl': '0', 'Hbdm': 'RMB', 'Cjjg': '0.0000', 'Cjje': '0.00', 'Sxf': '0.00', 'Jsxf': '0.00', 'Jygf': '0.00', 'Yhs': '0.00', 'Ghf': '0.00', 'Gfye': '0', 'Zjye': '1116.00', 'Cjbh': '0', 'Gddm': '', 'Htbh': '', 'Market': '', 'Dwc': '', 'Qqhs': None, 'Fsje': '1100.00', 'Qsrq': '20240925', 'Ywrq': '20240925', 'Cjsj': '00000000', 'Ywdm': '160021', 'Zjzh': '540340352219', 'Khxm': '白阳', 'Mmlb': '', 'Cjbs': '0', 'Qsf': '0.00', 'Qtfy': '0.00', 'Jsf': '0.00', 'Zgf': '0.00', 'Gpye': '0', 'Wtsl': '0', 'Wtjg': '0.0000', 'Fqf': '0', 'Wbyh': '2020', 'Wbyhmc': None, 'Wbzh': '6214831004877269', 'Yjyhs': None, 'Yjghf': None, 'Yjqsf': None, 'Yjjygf': None, 'Yjjsf': None, 'Yjzgf': None, 'Yjqtf': None, 'Yjfxj': None}, {'Fsrq': '20240925', 'Fssj': '144408', 'Zqdm': '', 'Zqmc': '', 'Ywsm': '银行转证券', 'Cjsl': '0', 'Hbdm': 'RMB', 'Cjjg': '0.0000', 'Cjje': '0.00', 'Sxf': '0.00', 'Jsxf': '0.00', 'Jygf': '0.00', 'Yhs': '0.00', 'Ghf': '0.00', 'Gfye': '0', 'Zjye': '16.00', 'Cjbh': '0', 'Gddm': '', 'Htbh': '', 'Market': '', 'Dwc': '', 'Qqhs': None, 'Fsje': '5.00', 'Qsrq': '20240925', 'Ywrq': '20240925', 'Cjsj': '00000000', 'Ywdm': '160021', 'Zjzh': '540340352219', 'Khxm': '白阳', 'Mmlb': '', 'Cjbs': '0', 'Qsf': '0.00', 'Qtfy': '0.00', 'Jsf': '0.00', 'Zgf': '0.00', 'Gpye': '0', 'Wtsl': '0', 'Wtjg': '0.0000', 'Fqf': '0', 'Wbyh': '2020', 'Wbyhmc': None, 'Wbzh': '6214831004877269', 'Yjyhs': None, 'Yjghf': None, 'Yjqsf': None, 'Yjjygf': None, 'Yjjsf': None, 'Yjzgf': None, 'Yjqtf': None, 'Yjfxj': None}, {'Fsrq': '20240925', 'Fssj': '144013', 'Zqdm': '', 'Zqmc': '', 'Ywsm': '银行转证券', 'Cjsl': '0', 'Hbdm': 'RMB', 'Cjjg': '0.0000', 'Cjje': '0.00', 'Sxf': '0.00', 'Jsxf': '0.00', 'Jygf': '0.00', 'Yhs': '0.00', 'Ghf': '0.00', 'Gfye': '0', 'Zjye': '11.00', 'Cjbh': '0', 'Gddm': '', 'Htbh': '', 'Market': '', 'Dwc': '', 'Qqhs': None, 'Fsje': '10.00', 'Qsrq': '20240925', 'Ywrq': '20240925', 'Cjsj': '00000000', 'Ywdm': '160021', 'Zjzh': '540340352219', 'Khxm': '白阳', 'Mmlb': '', 'Cjbs': '0', 'Qsf': '0.00', 'Qtfy': '0.00', 'Jsf': '0.00', 'Zgf': '0.00', 'Gpye': '0', 'Wtsl': '0', 'Wtjg': '0.0000', 'Fqf': '0', 'Wbyh': '2020', 'Wbyhmc': None, 'Wbzh': '6214831004877269', 'Yjyhs': None, 'Yjghf': None, 'Yjqsf': None, 'Yjjygf': None, 'Yjjsf': None, 'Yjzgf': None, 'Yjqtf': None, 'Yjfxj': None}, {'Fsrq': '20240909', 'Fssj': '154838', 'Zqdm': '', 'Zqmc': '', 'Ywsm': '银行转证券', 'Cjsl': '0', 'Hbdm': 'RMB', 'Cjjg': '0.0000', 'Cjje': '0.00', 'Sxf': '0.00', 'Jsxf': '0.00', 'Jygf': '0.00', 'Yhs': '0.00', 'Ghf': '0.00', 'Gfye': '0', 'Zjye': '1.00', 'Cjbh': '0', 'Gddm': '', 'Htbh': '', 'Market': '', 'Dwc': '20240909|205364', 'Qqhs': None, 'Fsje': '1.00', 'Qsrq': '20240909', 'Ywrq': '20240909', 'Cjsj': '00000000', 'Ywdm': '160021', 'Zjzh': '540340352219', 'Khxm': '白阳', 'Mmlb': '', 'Cjbs': '0', 'Qsf': '0.00', 'Qtfy': '0.00', 'Jsf': '0.00', 'Zgf': '0.00', 'Gpye': '0', 'Wtsl': '0', 'Wtjg': '0.0000', 'Fqf': '1', 'Wbyh': '2020', 'Wbyhmc': None, 'Wbzh': '6214831004877269', 'Yjyhs': None, 'Yjghf': None, 'Yjqsf': None, 'Yjjygf': None, 'Yjjsf': None, 'Yjzgf': None, 'Yjqtf': None, 'Yjfxj': None}]}
2024-09-26 10:15:53,566 learn.jywg_project.emtl.core create_order 157: INFO    : {'Status': 0, 'Count': 1, 'Data': [{'Htxh': '0400479173', 'Wtbh': '479173'}], 'Errcode': 0}
'''