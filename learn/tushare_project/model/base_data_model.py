# coding: utf-8
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class StockBasic(Base):
    __tablename__ = 'stock_basic'
    __table_args__ = {'comment': '股票列表'}

    id = Column(Integer, primary_key=True)
    ts_code = Column(String(10), nullable=False, unique=True, comment='TS代码')
    symbol = Column(String(10), unique=True, comment='股票代码')
    name = Column(String(20), nullable=False, comment='股票名称')
    area = Column(String(20), comment='地域')
    industry = Column(String(20), comment='所属行业')
    market = Column(String(10), nullable=False, comment='市场类型（主板/创业板/科创板/CDR）')
    list_date = Column(String(20), nullable=False, comment='上市日期')