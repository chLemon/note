# MySQL深分页问题

## 1. 解决方案一：根据最大id

```sql
-- max_id 可以由前端传递过来
select * from table_name where id > max_id limit 100000, 10
```

## 2. 子查询

```sql
select * from table_name where id in 
(select id from table_name where user = xxx limit 100000, 10)
```