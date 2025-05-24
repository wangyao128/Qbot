from prompt.data2mysql.DatabaseManager import DatabaseManager
from datetime import datetime, date, timedelta

class BaoStockDataSyncManager:
  def __init__(self):
    self.db_manager = DatabaseManager()

  def connect(self):
    return self.db_manager.connect()

  def disconnect(self):
    return self.db_manager.disconnect()



  def syncTradeDateInfo2DB(self):
    #### 同步交易日信息到数据库 ####
    db_manager = DatabaseManager()
    engine_ts = db_manager.connect()
    engine_baostock = self.checkin()

    if not engine_ts:
      return "数据库连接失败"
    if not engine_baostock:
      return "登陆失败"

    try:
      # 获取当前日期
      today = date.today()
      today_str = today.strftime('%Y-%m-%d')

      # 获取数据库中的最小和最大交易日期
      values = db_manager.read_data('SELECT MIN(calendar_date), MAX(calendar_date) FROM tradedate')
      if values.empty or values.iloc[0][0] is None and values.iloc[0][1] is None:
        start_date = '1990-01-01'
        end_date = today_str
      else:
        maxdate = values.iloc[0][1]
        next_day = datetime.strptime(maxdate, "%Y-%m-%d") + timedelta(days=1)
        start_date = next_day.strftime('%Y-%m-%d')
        end_date = today_str

      # 获取交易日信息
      result = self.getTradeDateInfo(start_date, end_date)
      # data_list = []
      # while (result.error_code == '0') & result.next():
      #   # 获取一条记录，将记录合并在一起
      #   data_list.append(result.get_row_data())
      # pd1 = pd.DataFrame(data_list, columns=result.fields)

      # result 是 baostock.data.resultset  中的ResultData 类型 其中 result.get_data() 返回的是一个pd.DataFrame()
      if result.empty:
        return "未获取到新的交易日信息"
      print(result.count())
      # 删除已有区间的数据（可选）
      # db_manager.delete_data('tradedate', f'calendar_date BETWEEN "{start_date}" AND "{end_date}"', engine_ts)

      # 插入新数据
      msg = db_manager.insert_data('tradedate', result)
      return msg

    except Exception as e:
      return f"同步交易日信息失败: {str(e)}"

    finally:
      db_manager.disconnect()
      self.checkout()

  def syncStockBasicInfo2DB(self):
    ####   同步股票信息到数据库 ####
    db_manager = DatabaseManager()
    engine_ts = db_manager.connect()
    engine_baostock = self.checkin()
    if not engine_ts:
      return "数据库连接失败"
    if not engine_baostock:
      return "登陆失败"
    try:
      result = self.getStockBasicInfo()
      if result.empty:
        return "未获取到新的股票基础信息"
      # 删除现有的股票基础信息
      db_manager.delete_data('stockbasic', '')
      # 插入最新的股票基础信息
      msg = db_manager.insert_data('stockbasic', result)
      return msg
    except Exception as e:
      return f"同步股票基础信息失败: {str(e)}"

    finally:
      db_manager.disconnect()
      self.checkout()

  def syncAllStock2DB(self, trade_date):
    #### 同步交易日所有股票列表到数据库 ####


  if __name__ == '__main__':
    bs = BaoStockDataManager()
    msg = bs.syncTradeDateInfo2DB()
    print(msg)
