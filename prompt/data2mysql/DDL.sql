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
drop table stockcode;
CREATE TABLE stockcode (
  date DATE NOT NULL COMMENT '交易所行情日期',
  code VARCHAR(10) NOT NULL COMMENT '证券代码',
  tradeStatus VARCHAR(1) NOT NULL COMMENT '交易状态',
  code_name VARCHAR(50) NOT NULL COMMENT '证券名称'
);

#sys_dict
CREATE TABLE `sys_dict` (
    `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键ID',
    `dict_type` varchar(100) NOT NULL COMMENT '字典类型',
    `dict_code` varchar(100) NOT NULL COMMENT '字典代码',
    `dict_name` varchar(200) NOT NULL COMMENT '字典名称',
    `dict_value` varchar(200) DEFAULT NULL COMMENT '字典值',
    `parent_id` bigint DEFAULT NULL COMMENT '父级ID',
    `sort_order` int DEFAULT 0 COMMENT '排序号',
    `is_enabled` tinyint(1) DEFAULT 1 COMMENT '是否启用(1:启用;0:禁用)',
    `remarks` varchar(500) DEFAULT NULL COMMENT '备注说明',
    `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `create_by` varchar(50) DEFAULT NULL COMMENT '创建人',
    `update_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `update_by` varchar(50) DEFAULT NULL COMMENT '更新人',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_type_code` (`dict_type`, `dict_code`),
    KEY `idx_type` (`dict_type`),
    KEY `idx_parent` (`parent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统数据字典表';


#hotstockinfo
drop table hotstockinfo;
CREATE TABLE hotstockinfo (
  id BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  hot_date DATE not null COMMENT '行情热点日期',
  domain_name VARCHAR(100) not null COMMENT '热点领域名称',
  hotspot_reson VARCHAR(100)   COMMENT '热点理由',
  market_performance TEXT   COMMENT '市场表现',
  driving_factors TEXT   COMMENT '驱动因素',
  create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='热点领域信息表';
ALTER TABLE hotstockinfo MODIFY COLUMN hotspot_reson VARCHAR(400);
ALTER TABLE hotstockinfo MODIFY COLUMN hotspot_reson VARCHAR(400) COMMENT '热点理由';
#hotcorestock
drop table hotcorestock;
CREATE TABLE hotcorestock (
  id BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  hotstockinfo_id BIGINT not null COMMENT '热点领域核心股票信息表主键ID',
  domain_name VARCHAR(100) not null COMMENT '热点领域名称',
  code  VARCHAR(10) not null COMMENT '证券代码',
  code_name VARCHAR(100) not null COMMENT '证券名称',
  recommend_type VARCHAR(20)   COMMENT '是否推荐买入',
  recommend_price VARCHAR(10)   COMMENT '推荐价格',
  recommend_reason VARCHAR(100)   COMMENT '推荐理由',
  create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='热点领域核心股票信息表';

ALTER TABLE hotcorestock MODIFY COLUMN recommend_reason VARCHAR(400) COMMENT '推荐理由';





