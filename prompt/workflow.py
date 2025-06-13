

from prompt.KimiAPI import KimiAPI
from prompt.baostockdata.BaoStockDataSyncManager import BaoStockDataSyncManager
from prompt.data2mysql.DatabaseManager import DatabaseManager
import baostock as bs


class  workflow:
  def __init__(self):
    self.db_manager = DatabaseManager()
    self.kimiAPI = KimiAPI()
    self.bssyncdata = BaoStockDataSyncManager()
  def begin(self):
    # 0 完成数据库的连接与baostock的登录
    self.bssyncdata.connect()
    self.bssyncdata.bs_data_manager.checkin()
    self.db_manager.connect()
    #每日工作前初始化相应数据
    # 1 更新数据库中所有交易日期信息
    log = self.bssyncdata.syncTradeDateInfo2DB()
    print(log)
    # 2 更新数据库中所有股票基础信息
    log = self.bssyncdata.syncStockBasicInfo2DB()
    print(log)
    #  3 更新今日所有股票列表
    log = self.bssyncdata.syncAllStock2DB('')
    print(log)

    return True

  def end(self):
    self.db_manager.disconnect()
    self.bssyncdata.disconnect()
    self.bssyncdata.checkout()

if __name__ == "__main__":

    #初始化准备
    workflow = workflow()
    workflow.begin()
    #每天同步热点数据入数据库
    content = {"date": "2025-06-13", "role": "专业的股票分析师","sync_time":"16：00"}
    json_str = workflow.kimiAPI.getKimistockAnalysis(content)
    FLG = workflow.kimiAPI.syncKimistockAnalysis2DB(json_str,content)

    #获取到热点股票数据代码
    workflow.db_manager.connect()
    hotcorestock = workflow.db_manager.read_data('''select a.code,a.code_name,a.domain_name
                                           from hotcorestock a inner join hotstockinfo b on a.hotstockinfo_id = b.id
                                           where b.hot_date = '
                                        '''
                                        +  content["date"]
                                        +  "'")

    #同步热点数据中每个股票的K线数据入数据库
    for index, row in hotcorestock.iterrows():
        message = workflow.bssyncdata.syncStockHistoryKData2DB(row["code"], '1900-01-01',content["date"])
        print(message)

    #结束
    workflow.end()

    # 每天下午 四点钟同步会比较好
    # data = json.loads(json_str)
    # df = pd.json_normalize(json_str)
    # print(data)
    # 每日最新数据更新时间：
    # 当前交易日17: 30，完成日K线数据入库；
    # 当前交易日18: 00，完成复权因子数据入库；
    # 第二自然日11: 00，完成分钟K线数据入库；
    # 第二自然日1: 30，完成前交易日“其它财务报告数据”入库；
    # 周六17: 30，完成周线数据入库；
