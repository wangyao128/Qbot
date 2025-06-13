from sqlalchemy import create_engine, text
import pandas as pd


class DatabaseManager:
  def __init__(self, db_url=None):
    """
    初始化数据库连接引擎。

    :param db_url: 数据库连接 URL，如果未提供则使用默认本地数据库配置
    """
    # 阿里云数据库
    # engine_ts = create_engine(
    #     'mysql://wangyao128_xyz:WY!19850115xyz@rm-cn-uax3aay1g000x93o.rwlb.'
    #     'rds.aliyuncs.com:3306/stock_db?charset=utf8&use_unicode=1')
    if db_url is None:
      # 默认本地数据库配置
      db_url = 'mysql+pymysql://root:323121@127.0.0.1:3306/world?charset=utf8&use_unicode=1'
    self.engine = create_engine(db_url)

  def connect(self):
    """
    返回 SQLAlchemy 引擎对象。

    :return: SQLAlchemy 引擎
    """
    return self.engine.connect()

  def disconnect(self):
    """
    断开数据库连接并释放资源。
    """
    self.engine.dispose()

  def insert_data(self, tablename, data):
    """
    将 DataFrame 数据插入到指定表中。

    :param tablename: 表名 (str)
    :param data: 要插入的数据 (pandas.DataFrame)
    :return: 插入结果 (int or None)
    """
    return data.to_sql(tablename, self.engine, index=False, if_exists='append', chunksize=5000)

  def read_data(self, sql):
    """
    执行 SQL 查询并返回结果。

    :param sql: 查询语句 (str)
    :return: 查询结果 (pandas.DataFrame)
    """
    return pd.read_sql_query(sql, self.engine)

  def update_data(self, tablename, data):
    """
    将 DataFrame 数据更新到指定表中。

    :param tablename: 表名 (str)
    :param data: 要更新的数据 (pandas.DataFrame)
    :return: 更新结果 (int or None)
    """
    return data.to_sql(tablename, self.engine, index=False, if_exists='replace', chunksize=5000)


  def execute_sql(self, sql, params=None):
    """
    执行任意 SQL 语句（如增、删、改操作）。

    :param sql: SQL 语句 (str)
    :param params: 参数化查询参数 (tuple or dict, 可选)
    """
    with self.engine.connect() as conn:
      if params:
        conn.execute(text(sql), params)
      else:
        conn.execute(text(sql))

  def delete_data(self,table_name, condition):
    """
    从 MySQL 数据库中删除符合条件的数据。

    :param table_name: 要删除数据的表名
    :param condition: 删除条件，例如 "id = 1"
    :param engine: 数据库引擎
    :return: None
    """
    if not condition.strip():
      condition = '1=1'
    sql: str = f"DELETE FROM {table_name} WHERE {condition}"
    with self.engine.connect() as conn:
      conn.execute(text(sql))
      conn.commit()

  def bulk_delete_from_dataframe(self, dataframe, table_name, columns):
    """
    根据 DataFrame 批量删除数据。

    :param dataframe: 要删除的数据的 DataFrame
    :param table_name: 要删除数据的表名
    :param columns: 用于生成删除条件的列名列表
    :return: 被删除的记录的 ID 列表
    """
    # 生成删除条件的 SQL 语句
    values = []
    where_clause = " AND ".join([f"{column} = :{column}" for column in columns])

    for index, row in dataframe.iterrows():
      values.append((row[columns[0]]))  # 根据实际列名调整

    # 执行批量删除
    delete_ids = self.session.query(text(f"{table_name}.id")).filter(text(where_clause), *values).all()
    self.session.execute(text(f"DELETE FROM {table_name} WHERE {where_clause}"), values)
    self.session.commit()
    return delete_ids

if __name__ == '__main__':
  # 创建数据库管理器实例
  db_manager = DatabaseManager()
  engine_ts = db_manager.connect()

  # 查询示例
  sql = """SELECT * FROM tradedate LIMIT 20"""
  df = db_manager.read_data(sql)
  print(df)

  #### 删除数据库数据样例程序   ####
  # engine_ts = connectMysql()
  # deleteFromMysql("city", "id = 100", engine_ts)
  # print("数据删除成功")
