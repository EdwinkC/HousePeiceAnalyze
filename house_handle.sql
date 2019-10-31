select id from house group by name, date having COUNT(date)>1;
# 去重 删除重复的id小的项
delete from house where id in (select * from 
	(select id from house group by name, date having COUNT(date)>1) table1);

select * from house order by name, date; 
# 找出10年数据全的城市
select name, COUNT(*) from house group by name having COUNT(*)>9;
# 找出10年数据全的城市的2019年的数据
select name, price, date from house where name in (select * from (
	select name from house group by name having COUNT(*)>9) table1) and date = '2019';
	
select name, price, date from house where date = '2017';
