from datetime import date, datetime, timedelta

import baostock as bs
import pandas as pd





class BaoStockDataManager:
  def __init__(self):
    self.login_entity = bs

  def checkin(self):
    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)
    self.login_entity = bs
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
    k_data = self.login_entity.query_history_k_data_plus(stock_code, "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST",
                                                         start_date, end_date, frequency="d", adjustflag="2")
    #frequency：数据类型，默认为d，日k线；d=日k线、w=周、m=月、5=5分钟、15=15分钟、30=30分钟、60=60分钟k线数据，不区分大小写；
    #指数没有分钟线数据；周线每周最后一个交易日才可以获取，月线每月最后一个交易日才可以获取。
    # adjustflag：复权类型，默认不复权：3；1：后复权；2：前复权。已支持分钟线、日线、周线、月线前后复权。 BaoStock提供的是涨跌幅复权算法复权因子，
    # print('query_history_k_data_plus respond error_code:' + k_data.error_code)
    # print('query_history_k_data_plus respond  error_msg:' + k_data.error_msg)
    data_list = []
    while (k_data.error_code == '0') & k_data.next():
      # 获取一条记录，将记录合并在一起
      data_list.append(k_data.get_row_data())
    pd1 = pd.DataFrame(data_list, columns=k_data.fields)
    df = self.astypeKdata(pd1)
    return df

  def astypeKdata(self,df):
    df[['date']] = df[['date']].apply(pd.to_datetime,format='%Y-%m-%d', errors='coerce')
    df[['open','high','low','close','preclose','volume','amount','turn','pctChg','peTTM','pbMRQ','psTTM','pcfNcfTTM']] = df[['open','high','low','close','preclose','volume','amount','turn','pctChg','peTTM','pbMRQ','psTTM','pcfNcfTTM']].apply(pd.to_numeric, errors='coerce')
    # df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d',  errors='coerce')
    # df['open'] = pd.to_numeric(df['open'], errors='coerce')
    # df['high'] = pd.to_numeric(df['high'], errors='coerce')
    # df['low'] = pd.to_numeric(df['low'], errors='coerce')
    # df['close'] = pd.to_numeric(df['close'], errors='coerce')
    # df['preclose'] = pd.to_numeric(df['preclose'], errors='coerce')
    # df['volume'] = pd.to_numeric(df['volume'], errors='coerce')
    # df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    # df['turn'] = pd.to_numeric(df['turn'], errors='coerce')
    # df['pctChg'] = pd.to_numeric(df['pctChg'], errors='coerce')
    # df['peTTM'] = pd.to_numeric(df['peTTM'], errors='coerce')
    # df['pbMRQ'] = pd.to_numeric(df['pbMRQ'], errors='coerce')
    # df['psTTM'] = pd.to_numeric(df['psTTM'], errors='coerce')
    # df['pcfNcfTTM'] = pd.to_numeric(df['pcfNcfTTM'].values, errors='coerce')
    return df

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
  # print(bs.getStockIndustryInfo(''))
  print(bs.getHistoryKData('sh.600000', '2025-01-01', '2025-05-02'))
  bs.checkout()


  # employees = [('Stuti', 28, 'Varanasi', 20000), ('Saumya', 32, 'Delhi', 25000)]
  # df = pd.DataFrame(employees, columns=['Name', 'Age', 'City', 'Salary'])

  #### 结果集输出到csv文件 ####
  # result.to_csv("D:\\trade_datas.csv", encoding="gbk", index=False)
  # print(msg)
