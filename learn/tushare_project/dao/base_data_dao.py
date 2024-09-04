from learn.tushare_project.model.base_data_model import StockBasic

# todo 大批量数据是删加还是新增修改，还是校验后新增修改
def add_stock_basic(session, stock_basic):
    session.add(stock_basic)
