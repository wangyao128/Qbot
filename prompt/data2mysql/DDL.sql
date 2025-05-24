#tradedate
CREATE TABLE TradeDate (
  calendar_date DATE NOT NULL COMMENT '交易日期',
  is_trading_day VARCHAR(1) NOT NULL COMMENT '是否交易日'
);
#stockbasicInfo
CREATE TABLE StockBasicInfo (
  code VARCHAR(10) NOT NULL COMMENT '证券代码',
  code_name VARCHAR(50) NOT NULL COMMENT '证券名称',
  ipoDate DATE COMMENT '上市日期',
  outDate DATE COMMENT '退市日期',
  type CHAR(1) COMMENT 'A股B股',
  status CHAR(1) COMMENT '上市状态'
);
#stockcode
CREATE TABLE stockcode (
  code VARCHAR(10) NOT NULL COMMENT '证券代码',
  tradeStatus VARCHAR(1) NOT NULL COMMENT '交易状态',
  code_name VARCHAR(50) NOT NULL COMMENT '证券名称'
);






