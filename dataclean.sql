# 删除重复异常数据
delete from newdata where id in (select * from 
	(select id from newdata group by name, date having COUNT(date)>1) table1);
delete from newdata where name = '普洱';
delete from newdata where name = '黔西南';	
delete from newdata where price < 1000;

select name, COUNT(*) from newdata group by name having COUNT(*)>9;