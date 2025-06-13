
select a.domain_name ,a.code_name,c.code,c.date,c.close,c.pctChg
from hotcorestock  a
    inner join hotstockinfo b on a.hotstockinfo_id = b.id
    inner  join stockkdatainfo c on a.code = c.code and c.date = b.hot_date
where b.hot_date = '2025-06-12' order by b.id,a.code



selec * from hotstockinfo a where a.hot_date = '2025-06-13' order by a.id


select a.code_name,a.code,a.domain_name,b.*
from hotcorestock a
inner join stockbasic  b on a.code = b.code
inner join hotstockinfo c on a.hotstockinfo_id = c.id
         where c.hot_date = '2025-06-13' order by a.code;

select * from stockbasic


select min(calendar_date),max(calendar_date) from tradedate

select * from hotstockinfo a where a.hot_date = '2025-06-12'


select distinct hotstockinfo.hot_date from hotstockinfo

select *from hotstockinfo
