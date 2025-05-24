from datetime import date, datetime, timedelta

import baostock as baostock
import pandas as pd

# from prompt.data2mysql.DatabaseManager import DatabaseManager
# from pyfunds.backtest.xalpha.cons import today_obj


class BaoStockDataManager:
  def __init__(self):
    self.login_entity = None

  def checkin(self):
    #### 登陆系统 ####
    lg = baostock.login()
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)
    self.login_entity = baostock
    return lg

  def checkout(self):
    #### 登出系统 ####
    lg = self.login_entity.logout()
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)
    return lg

  def getTradeDateInfo(self, start_date, end_date):
    #### 获取交易日信息 ####
    trade_date_list = self.login_entity.query_trade_dates(start_date, end_date)
    print('query_trade_dates respond error_code:' + trade_date_list.error_code)
    print('query_trade_dates respond  error_msg:' + trade_date_list.error_msg)
    data_list = []
    while (trade_date_list.error_code == '0') & trade_date_list.next():
      # 获取一条记录，将记录合并在一起
      data_list.append(trade_date_list.get_row_data())
    pd1 = pd.DataFrame(data_list, columns=trade_date_list.fields)
    return pd1

  def getStockBasicInfo(self):
    #### 获取股票基础信息 ####
    stock_basic_info_list = self.login_entity.query_stock_basic()
    print('query_stock_basic respond error_code:' + stock_basic_info_list.error_code)
    print('query_stock_basic respond  error_msg:' + stock_basic_info_list.error_msg)
    data_list = []
    while (stock_basic_info_list.error_code == '0') & stock_basic_info_list.next():
      # 获取一条记录，将记录合并在一起
      data_list.append(stock_basic_info_list.get_row_data())
    pd1 = pd.DataFrame(data_list, columns=stock_basic_info_list.fields)
    return pd1

  # def deleteTradeDateInfo():
  ####  删除交易日信息 ####

  def getAllStock(self,trade_date):
    #### 获取指定交易日所有股票列表 ####
    stock_list = self.login_entity.query_all_stock(trade_date)
    data_list = []
    while (stock_list.error_code == '0') & stock_list.next():
      # 获取一条记录，将记录合并在一起
      data_list.append(stock_list.get_row_data())
    pd1 = pd.DataFrame(data_list, columns=stock_list.fields)
    return pd1

  def getHistoryKData(self,stock_code, start_date, end_date):
    #### 获取指定股票指定日期的K线数据 ####
    k_data = self.login_entity.query_history_k_data_plus(stock_code, "date,code,open,high,low,close,volume,amount,adjustflag",
                                                         start_date, end_date)
    print('query_history_k_data_plus respond error_code:' + k_data.error_code)
    print('query_history_k_data_plus respond  error_msg:' + k_data.error_msg)
    data_list = []
    while (k_data.error_code == '0') & k_data.next():
      # 获取一条记录，将记录合并在一起
      data_list.append(k_data.get_row_data())
    pd1 = pd.DataFrame(data_list, columns=k_data.fields)
    return pd1

  def getPerformanceExpressReportData(self,stock_code, start_date, end_date):
    #### 获取指定股票的季频公司业绩快报数据 ####
    #todo 获取指定股票指定日期的业绩数据
    performance_express_report_data = self.login_entity.query_performance_express_report(stock_code, start_date, end_date)
    print('query_performance_express_report respond error_code:' + performance_express_report_data.error_code)
    print('query_performance_express_report respond  error_msg:' + performance_express_report_data.error_msg)
    data_list = []
    while (performance_express_report_data.error_code == '0') & performance_express_report_data.next():
      # 获取一条记录，将记录合并在一起
      data_list.append(performance_express_report_data.get_row_data())
    pd1 = pd.DataFrame(data_list, columns=performance_express_report_data.fields)
    return pd1

  def getStockIndustryInfo(self, stock_code):
    #### 获取指定股票行业信息 ####
    stock_industry_info = self.login_entity.query_stock_industry(stock_code)
    print('query_stock_industry respond error_code:' + stock_industry_info.error_code)
    print('query_stock_industry respond  error_msg:' + stock_industry_info.error_msg)
    data_list = []
    while (stock_industry_info.error_code == '0') & stock_industry_info.next():
      # 获取一条记录，将记录合并在一起
      data_list.append(stock_industry_info.get_row_data())
    pd1 = pd.DataFrame(data_list, columns=stock_industry_info.fields)
    return pd1





if __name__ == '__main__':
  bs = BaoStockDataManager()
  bs.checkin()
  # print(bs.getTradeDateInfo('2025-01-01', '2025-05-02'))
  # print(bs.getStockBasicInfo())
  # print(bs.getAllStock('2025-05-23'))
  # print(bs.getHistoryKData('sh.600000', '2025-01-01', '2025-05-02'))
  # print(bs.getPerformanceExpressReportData('sh.600000', '2025-01-01', '2025-05-02'))
  print(bs.getStockIndustryInfo(''))
  bs.checkout()
  # msg = bs.syncTradeDateInfo2DB()
  # bs.checkin()
  # rs = bs.getTradeDateInfo('2025-01-01', '2025-05-02')
  # # print(msg)
  # #### 打印结果集 ####
  # data_list = []
  # while (rs.error_code == '0') & rs.next():
  #   # 获取一条记录，将记录合并在一起
  #   data_list.append(rs.get_row_data())
  # result = pd.DataFrame(data_list, columns=rs.fields)

  #### 结果集输出到csv文件 ####
  # result.to_csv("D:\\trade_datas.csv", encoding="gbk", index=False)
  # print(msg)
