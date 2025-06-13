

import pandas as pd

from sqlalchemy.exc import DatabaseError

from prompt.baostockdata.BaoStockDataManager import BaoStockDataManager
from prompt.data2mysql.DatabaseManager import DatabaseManager
from datetime import datetime, date, timedelta

class BaoStockDataSyncManager:
  def __init__(self):
    self.db_manager = DatabaseManager()
    self.bs_data_manager = BaoStockDataManager()


  def connect(self):
    return self.db_manager.connect()

  def disconnect(self):
    return self.db_manager.disconnect()

  def checkin(self):
    #### 登陆系统 ####
    lg = self.bs_data_manager.checkin()
    # 显示登陆返回信息

  def checkout(self):
    lg = self.bs_data_manager.checkout()


  def syncTradeDateInfo2DB(self):
    #### 同步交易日信息到数据库 ####

    try:
      # 获取当前日期
      today = date.today()
      today_str = today.strftime('%Y-%m-%d')

      # 获取数据库中的最小和最大交易日期
      values = self.db_manager.read_data('SELECT MIN(calendar_date), MAX(calendar_date) FROM tradedate')
      if values.empty or values.iloc[0][0] is None and values.iloc[0][1] is None:
        start_date = '1990-01-01'
        end_date = today_str
      else:
        maxdate = values.iloc[0][1]
        next_day = datetime.strptime(maxdate, "%Y-%m-%d") + timedelta(days=1)
        start_date = next_day.strftime('%Y-%m-%d')
        end_date = today_str

      # 获取交易日信息
      result = self.bs_data_manager.getTradeDateInfo(start_date, end_date)
      # data_list = []
      # while (result.error_code == '0') & result.next():
      #   # 获取一条记录，将记录合并在一起
      #   data_list.append(result.get_row_data())
      # pd1 = pd.DataFrame(data_list, columns=result.fields)

      # result 是 baostockdata.data.resultset  中的ResultData 类型 其中 result.get_data() 返回的是一个pd.DataFrame()
      if result.empty:
        return "未获取到新的交易日信息"
      print("写入交易日的天数",result.count())
      # 删除已有区间的数据（可选）
      # db_manager.delete_data('tradedate', f'calendar_date BETWEEN "{start_date}" AND "{end_date}"', engine_ts)

      # 插入新数据
      msg = self.db_manager.insert_data('tradedate', result)
      return   f"同步交易日信息成功: 起始日：{start_date} 到 {end_date} 数量：{result.count()}"

    except Exception as e:
      return f"同步交易日信息失败: {str(e)}"


  def syncStockBasicInfo2DB(self):
    ####   同步股票信息到数据库 ####
    try:
      result = self.bs_data_manager.getStockBasicInfo()
      if result.empty:
        return "未获取到股票基础信息"
      # 删除现有的股票基础信息
      self.db_manager.delete_data('stockbasic', '1=1')
      # 插入最新的股票基础信息
      msg = self.db_manager.insert_data('stockbasic', result)
      return f"同步股票基础信息成功: {str(result.count())}"
    except Exception as e:
      return f"同步股票基础信息失败: {str(e)}"


  def syncAllStock2DB(self, trade_date):
    #### 同步交易日所有股票列表到数据库 ####
    today = date.today()
    today_str = today.strftime('%Y-%m-%d')
    if trade_date is None or trade_date == '':
      trade_date = today_str
    try:
      result = self.bs_data_manager.getAllStock(trade_date)
      if result.empty:
        return f"未获取到{trade_date}日的股票列表"
      # 删除已有的股票列表
      self.db_manager.delete_data('stockcode', f'date="{trade_date}"')
      # 增加一个日期列 并赋值日期
      result['date'] = trade_date
      # 插入新的股票列表
      msg = self.db_manager.insert_data('stockcode', result)
      return f"同步股票代码信息成功: {result.count()} 交易日期：{trade_date}"
    except Exception as e:
      return f"同步股票代码信息失败: {str(e)}"


  def syncHistoryKData2DB(self, start_date, end_date):
    #### 同步指定指定日期的所有股票K线数据到数据库 ####
    try:
      msglist =[]
      for row in self.db_manager.read_data('SELECT DISTINCT code FROM stockcode WHERE date = "%s" and tradeStatus = "0"' % end_date).itertuples():
        code = row.code
        result = self.bs_data_manager.getHistoryKData(code, start_date, end_date)
        if result.empty:
          msglist.append(f"未获取到{code}的{start_date}到{end_date}的K线数据")
        # 删除已有的K线数据
        self.db_manager.delete_data('stockkdatainfo', f'code="{code}" AND date BETWEEN "{start_date}" AND "{end_date}"')
        # 插入新的K线数据
        msg = self.db_manager.insert_data('stockkdatainfo', result)
        msglist.append(f"{code}的{start_date}到{end_date}的K线数据已写入数据库\n")
        print(f"{code}的{start_date}到{end_date}的K线数据已写入数据库\n")
      return msglist
    except Exception as e:
      return f"同步股票K线数据失败: {str(e)}"
    # finally:
      # self.disconnect()
      # self.checkout()

  def syncStockHistoryKData2DB(self,stock_code,start_date,end_date):
    #### 同步指定股票指定日期的K线数据到数据库 ####
    try:
      msglist =[]
      code = stock_code
      result = self.bs_data_manager.getHistoryKData(code, start_date, end_date)
      if result.empty:
          msglist.append(f"未获取到{code}的{start_date}到{end_date}的K线数据\n")
      # 删除已有的K线数据
      self.db_manager.delete_data('stockkdatainfo', f'code="{code}" AND date BETWEEN "{start_date}" AND "{end_date}"')
      # 插入新的K线数据
      msg = self.db_manager.insert_data('stockkdatainfo', result)
      msglist.append(f"{code}的{start_date}到{end_date}的K线数据已写入数据库\n")
      print(f"{code}的{start_date}到{end_date}的K线数据已写入数据库\n")
      return msglist
    except Exception as e:
      return f"同步股票K线数据失败: {str(e)}"
    # finally:
      # self.disconnect()
      # self.checkout()

if __name__ == '__main__':
  bssyncdata = BaoStockDataSyncManager()
  bssyncdata.checkin()
  bssyncdata.connect()
  # if not bssyncdata.db_manager.connect():
  #   raise DatabaseError("无法连接到数据库")
  # elif not bssyncdata.bs_data_manager.checkin():
  #   raise Exception("登陆失败")
  # message1 = bssyncdata.syncTradeDateInfo2DB()
  # print(message1)
  # message2 = bssyncdata.syncStockBasicInfo2DB()
  # print(message2)
  # message3 = bssyncdata.syncAllStock2DB('2025-05-28')
  message4 = bssyncdata.syncHistoryKData2DB('2024-01-01', '2025-05-28')
  bssyncdata.disconnect()
  bssyncdata.checkout()
  # print(message4)





    # msg = bs.syncTradeDateInfo2DB()
    # print(msg)
