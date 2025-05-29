> 本笔记参考以下资料整理：
>
> [Java基础+进阶](https://www.bilibili.com/video/BV1uJ411k7wy)
>
> [【黑马程序员】2020最新MySQL高级教程（求职面试必备）【源码+笔记】](https://www.bilibili.com/video/BV1UQ4y1P7Xr?p=1)
>
> [MySQL Documentation](https://dev.mysql.com/doc/)
>
> 《MySQL必知必会》（《MySQL Crash Course》）Ben Forta9
>

# MySQL基础

# 1 数据库基础

## 1.1 数据库的一些概念

### 1.1.1 数据库

数据库（database，DB）：保存有组织的数据的容器（通常是一个文件或一组文件）。

数据库软件（DBMS）：人们经常用“数据库”一词来指代“数据库软件”，这是不对的。

可以把数据库理解成一个文件柜。

### 1.1.2 表和模式

表（table）：某种特定类型数据的结构化清单。

表名：同一个数据库下的表名应该唯一。

模式（schema）：关于数据库和表的布局及特性的信息。

可以把表理解成文件柜里的一个文件。

### 1.1.3 列和数据类型

列（column）：表中的一个字段，

数据类型（datatype）：所允许的数据类型，每一列都有相应的数据类型。

### 1.1.4 行

行（row）：表中的一个记录。

记录（record）：与行同义，从技术上来说，行是正确的术语。

### 1.1.5 主键

主键（primary key）：一列（或一组列），可以唯一区别表中的每个行。

应该保证表中有主键。

+ 主键的条件：
  1. 任意两行的主键值都不同；
  2. 每行都有主键值，不允许为NULL。

主键通常定义在表的一列上，但是也可以定义在多个列上，保证列值的组合唯一即可。

+ 对于主键，最好：
  1. 不更新主键列的值
  2. 不重用主键列的值
  3. 不在主键列使用可能会更改的值

## 1.2 SQL

SQL，结构化查询语言（Structured Query Language），一种专门用来与数据库通信的语言。

优点：
  1. 所有数据库几乎都可以用
  2. 简单易学
  3. 灵活好用

但是不同DBMS的SQL还是会有一些区别，本笔记的SQL是专门针对MySQL的。

# 2 MySQL数据库软件

## 2.1 MySQL简介

DBMS分为2类，一类是基于共享文件系统的DBMS，主要用于桌面用途；另一类为基于客户机-服务器的DBMS，如MySQL。

**服务器**部分负责所有的数据访问和处理，部署的计算机称为数据库服务器；请求都是来自于**客户机**，与用户打交道。

## 2.2 安装与卸载

版本：6.x开始收费

+ 我司使用的MySQL版本为：ver. 5.6.26-log。

配置的时候如果有哪一个不是勾，就得删了重装

控制台：`mysql -uroot -p[password]`查看是否安装成功

+ 卸载流程：
  1. 找到MySQL的安装路径
  2. 找到my.ini文件，从里面找到datadir
  3. 控制面板卸载MySQL
  4. 删掉datadir那个路径最高的MySQL文件夹

## 2.3 配置

计算机——右键——管理——服务和应用程序——可以查看服务
cmd——> services.msc也可以打开服务

（管理员cmd）

```shell
net start mysql  # 开启服务
net stop mysql  # 关闭服务
```

## 2.4 登录与退出

MySQL安装好后，自带一个命令行程序：mysql。

cmd：

```shell
# 登录
mysql -uroot -p[password]
mysql -h[ip] -uroot -p[password] -P[port]
mysql --host=[ip] --user=root --password=[password]
```

```sql
mysql> #语句必须以;或\g结束

# 退出
exit
quit

# 帮助
help
\h
help select
help show
...
```

## 2.5 MySQL目录结构

+ my.ini 配置文件

+ 数据目录
  每个文件夹：一个数据库
  `.frm`文件：表
  数据记录

## 2.6 图形化工具

### 2.6.1 客户端图形化工具：SQLYog

12.0.9-0
破解码：
姓名：cr173
序列号：
8d8120df-a5c3-4989-8f47-5afc79c56e7c
59adfdfe-bcb0-4762-8267-d7fccf16beda
ec38d297-0543-4679-b098-4baadf91f983

### 2.6.2 客户端图形化工具：DataGrip

公司用的，JetBrains家的

### 2.6.3 IDEA

IDEA有内置

### 2.6.3 服务器管理MySQL Administrator

可以管理用户权限等。必须单独在官网下载。

# 3 SQL

Structured Query Language：结构化查询语言

所有关系型数据库都可以用SQL操作，而每种数据库方式里不一样的地方称为“方言”。

## 3.1 SQL通用语法

1. 可以单行或多行书写，分号结尾，多个空格会被视为一个空格。
2. 不区分大小写，但是关键字建议大写
3. 注释有3种：

```sql
-- 单行注释【这个必须有空格】

# 单行注释【这个可以没有空格】

/* 多行注释 */	
```

## 3.2 MySQL数据类型

数据类型的作用：

1. 限制数据类型
2. 更有效的存储
3. 不同类型的数据排序规则不同

### 3.2.1 串数据类型

定长串：长度固定，不允许更多，存储空间与指定的相同，效率更高，如CHAR。

变长串：长度可变，有的有最大定长，只保存数据，节约空间，无法索引，如TEXT。

串值必须在引号内（通常单引号更好）。

不进行计算的数字也应该存储为串，如邮编、电话等。

```sql
CHAR
1~255个字符的定长串。长度必须创建时指定，否则默认为CHAR(1)

ENUM
接受最多64K个串组成的一个预定义集合的某个串

LONGTEXT
最大长度为4GB的TEXT

MEDIUMTEXT
最大长度为16K的TEXT

SET
接受最多64K个串组成的一个预定义集合的零个或多个串

TEXT
最大长度为64K的变长文本

TINYTEXT
最大长度为255字节的TEXT

VARCHAR
长度可变，最大65535个字符，创建时指定为VARCHAR(n)，则存储0到n个字符的变长串
```

SET和ENUM是在定义的时候预先指定一个集合，如：`('a','b','c')`，则插入的时候只能是这个集合的子集

CHAR和VARCHAR括号内的值为字符的长度

NCHAR或NVARCHAR（National character）是使用了预定义字符集的，MySQL使用的是utf8。

MySQL默认的utf8是3个字节的utf8mb3，4个字节时要使用utf8mb4。

### 3.2.2 字符集和校对顺序

+ 字符集：字母和符号的集合
+ 编码：字符集成员的二进制表示
+ 校对：字符之间如何比较

字符集一般是在服务器、数据库、表级进行指定，通常是在表级指定。

```sql
show character set     -- 显示支持的所有字符集
show collation         -- 显示支持的所有校对        -- 后缀_cs：区分大小写      -- 后缀_ci：不区分大小写
                           
show variables like 'character%'       -- 查看当前使用的字符集
show variables like 'collation%'       -- 查看当前使用的校对
```

+ 创建表的时候指定字符集和校对

```sql
create table table_name(
    ...
) default character set hebrew
  collate hebrew_general_ci0;
```

1. 如果两者都指定，则使用指定值
2. 如果只指定了字符集，则使用此字符集机器默认的校对（`show character set`可以查看）
3. 都不指定，使用数据库默认的

+ 还支持对某一列指定

+ 还可以在`select`的`order by`等子句里通过关键字`collate`指定校对，实现临时对大小写进行区分（或不区分）的排序、分组等。

### 3.2.3 数值数据类型

取值范围越大，需要的存储空间越多

除了`BIT`和`BOOLEAN`外，都可以有符号或无符号，由`UNSIGNED`关键字控制

数值不要带引号

MySQL没有专门存储货币的数据类型，一般情况下用`DECIMAL(8,2)`，也可以直接用整数

```sql
BIT
位字段，1~64位，版本5之前等价于TINYINT

BIGINT
8个字节64位整数

BOOLEAN/BOOL
布尔

DECIMAL/DEC
精度可变浮点型，DEC(M,D)，M为总位数，D为小数位，字节数为M>D?M+2:D+2

DOUBLE
8字节双精度浮点数，DOUBLE(M,D)

FLOAT
4字节单精度浮点数

INT
4字节整数

MEDIUMINT
3字节整数

REAL
4字节浮点数，和FLOAT不一样

SAMLLINT
2字节整数

TINYINT
1字节整数
```

### 3.2.4 日期和时间数据类型

```sql
DATE
格式为YYYY-MM-DD，1000-01-01~9999-12-31

DATETIME
DATE+TIME

TIMESTAMP
功能与DATETIME相同，但范围较小，如果不赋值或赋值为NULL，则使用当前系统时间自动赋值

TIME
HH:MM:SS

YEAR
2位数字表示1970~2069，4位数字表示1901~2155
```

### 3.2.5 二进制数据类型

二进制数据类型可以存储任何数据，如图片、多媒体等。

```sql
BLOG
64KB

MEDIUMBLOG
16MB

LONGBLOG
4GB

TINYBLOG
255字节
```

## 3.3 SQL语句的分类

1. **DDL**（Data Definition Language），数据定义语言
   操作数据库、表

2. **DML**（Manipulation）操作
   增删改表中的数据

3. **DQL**（Query）查询
   查询表中的数据

4. **DCL**（Control）控制
   授权

## 3.4 DDL：操作数据库、表

### 3.4.1 操作数据库

**1. Create：创建**

```sql
create database 数据库名称;  -- 创建数据库
create database if not exists 数据库名称;  -- 判断不存在再创建：
create database 数据库名称 character set 字符集名;  -- 指定字符集：
```

**2. Retrieve：查询**

```sql
show databases;  -- 查询所有数据库的名称
show create database 数据库名;  -- 查看某个数据库的字符集（编码），本意是查询某个数据库的创建语句
```

**3. Update：修改**

```sql
alter database 数据库名称 character set 字符集名;  -- 修改数据库的字符集。utf8，没有中间的横杠.
```

**4. Delete：删除**

```sql
drop database 数据库名称;  -- 删除数据库
drop database if exists 数据库名称;  -- 判断存在再删除
```

**5. 使用数据库**

```sql
select database();  -- 查询当前正在使用的数据库名称
use 数据库名称;  -- 使用数据库
```

### 3.4.2 操作表

**1. 创建**

```sql
create table 表名(
    列名1 数据类型1,
    列名2 数据类型2,
    ...
    列名n 数据类型n     -- 注意：最后一列不要加逗号
);

create table 表名 if not exists(
		...
);  -- 判断不存在再创建：

create table 表名(
    ...
    number int not null default 0,  -- 设置非空，默认值为1
    primary key(列1, 列2)   -- 在创建表的时候指定主键的一种方式
)ENGINE=InnoDb;  -- 在创建表的时候指定引擎

create table 新表 like 源表;  -- 复制

rename table 新表名 to 旧表名,
						 新表名2 to 旧表名2;   -- 对表重命名
```

**2. 查询**

```sql
show tables;  -- 查询某个数据库中所有的表名称
show create table 表名; -- 查看创建表的SQL语句
show columns from 表名; -- 查询表结构，列的详细信息
desc 表名;  -- 与show columns from 相同
```

**3. 修改**

谨慎使用，无法撤销，应该先备份数据。

```sql
alter table 表名 rename to 新的表名;  -- 修改表名
alter table 表名 character set utf8;  -- 修改表的字符集
alter table 表名 add 列名 数据类型;  -- 添加一列
alter table 表名 add 列名 数据类型 comment '注释' after 位置列名;  -- 添加一列
alter table 表名 change 原列名 新列名 新类型;  -- 修改列名和类型
alter table 表名 modify 列名 新类型;  -- 只修改类型
alter table 表名 drop column 列名;  -- 删除列
```

**4. 删除**

```sql
drop table 表名;
drop table if exists 表名;
```

## 3.4 DML：增删改表中数据

**1. 添加数据**

```sql
insert into 表名(列名1, 列名2, ..., 列名n) values(值1, 值2, ..., 值n);

insert into 表名(列名1, 列名2, ..., 列名n) values(值1, 值2, ..., 值n),(值1, 值2, ..., 值n),(值1, 值2, ..., 值n);  -- 同时插入多行

insert into 表A(列名1, 列名2, ..., 列名n) select (列1, 列2, ..., 列n) from 表B;    -- select出的第一列插入到insert into 表的第一列中，以此类推，select出的列名不重要
```

注意：

1. 列名和值要一一对应
2. 如果表名后没有指定列名，则默认给所有列添加值
3. 除了数字类型和NULL，其他类型需要使用引号（单双均可）引起来
4. 在值前面加上N表示用预定义字符集，MySQL是utf8

**3.4.2 删除数据**

```sql
delete from 表名 where 条件;
```

注意：

+ 如果不加where，会删除表中所有的记录。
+ 但是该操作会重复执行很多次（一条记录一次），如果希望清空表，用

```sql
truncate table 表名;    -- 实际上会删除原来的表并重新创建一个表
```

**3.4.3 修改数据**

```sql
update 表名 set 列名1 = 值1, 列名2 = 值2, ... [where 条件];
```

注意：如果不加条件，会修改所有值。

`ignore`关键字：`update`语句在更新多行的时候，如果某一行更新失败了，那么整条语句就会被取消，回滚。可以用`ignore`关键字在即使发生了错误的情况下也继续更新。`update ignore table set ...`

## 3.5 DQL：查询表中的记录

```sql
select * from 表名;  -- 查询表中所有的数据
```

注意：

1. 查询出的语句在未使用`order by`排序时，每次显示的顺序可能不同；关系数据库设计理论认为，**如果不明确规定“排序顺序”**
   **，则不应该假定检索出的数据的顺序有意义。**
2. 通配符`*`返回的列顺序一般是列在表定义中出现的顺序，表模式的变化（列的添加或删除）可能会导致顺序的变化。

### 3.5.1 语法

```sql
select
    字段列表
from
    表名列表
where
    条件列表
group by
    分组列表
having
    分组之后的条件
order by
    排序
limit
    分页限定
```

子句（clause）的相对顺序不能错，不然会报错。

### 3.5.2 基础查询

1. 多个字段的查询

```sql
select 字段名1, 字段名2, ... from 表名;
```

注意：如果查询所有字段，则可以用`*`来替代字段列表

2. **去除重复**：`distinct`关键字。注意该关键字**应用于所有列**而不仅是前置它的列。

3. 计算列
   一般可以使用四则运算计算一些列的值，如果有`null`参与，结果都为`null`。

```sql
ifnull(表达式1,表达式2);
```

表达式1为可能会出现null的字段，判断是否有null的字段名。如果字段为null，会替换为表达式2的值

4. 起别名：`as`关键字，`as`也可以省略，用`空格`

### 3.5.3 条件查询

where子句后跟条件，称为搜索条件（search criteria）或过滤条件（filter condition）。

运算符：

```sql
> < <= >= = <>  -- 【不等于有2种<>或!=，等于只有一个等号】

BETWEEN ... AND  -- 选取介于两个值之间的数据范围，包括开始值和结束值

IN(元素1，元素2，元素3)

IS NULL  -- NULL不能用等于和不等于判断，当其他语句过滤时不匹配时并不会返回NULL，必须要用 IS NULL 获取
IS NOT NULL

and或&&，推荐and，下同
or或||  -- 与and混合使用时，要加小括号
not或！ -- 只对IN、BETWEEN AND、EXISTS有效，如：NOT IN (1,2)  

LIKE  -- 模糊查询，配合占位符一起使用。若无占位符，效果等同=。   LIKE此时在官方文档里叫做predicate，谓词
	_  -- 通配符，单个任意字符
	%  -- 通配符，多个任意字符，不可匹配NULL	
```

数据也可以在应用层过滤，但是：

1. 数据库对数据过滤有优化，效率会高于应用层；
2. 会发送多余的数据，浪费网路带宽。

#### 3.5.3.1 正则表达式

MySQL只支持部分正则表达式，同时在匹配的时候只要部分满足就会返回，例如`select * from t where name regexp 'J' `，那么名字中有`J`的都会被返回

```sql
REGEXP -- 正则表达式

select 'hello' regexp '[0-9]';  -- 正则表达式测试，可以不需要数据库，返回0表示没有匹配，返回1表示匹配

  .      -- 匹配单个字符
  |      -- 或
  []     -- [123]相当于[1|2|3]，匹配单个字符，为1或2或3
  [0-9]  -- 范围匹配，如[1-3]，[a-z]
  ^      -- 非，如[^123]，匹配123以外的单个字符
  \\     -- 转义符号，如\\.为.   用2个\的原因：MySQL会解释一个，正则表达式库会解释另一个
  
# 字符类 character class
  [:alnum:]    -- 任意字母和数字  [a-zA-Z0-9]
  [:alpha:]    -- 任意字符  [a-zA-Z]
  [:blank:]    -- 空格和制表  [\\t]
  [:cntrl:]    -- ACSII控制字符  ASCII0到31和127
  [:digit:]    -- 任意数字  [0-9]
  [:graph:]    -- 与[[:print:]]相同，但不包括空格
  [:lower:]    -- 任意小写字母  [a-z]
  [:print:]    -- 任意可打印字符
  [:punct:]    -- 既不在[:alnum:]又不在[:cntrl:]中的任意字符
  [:space:]    -- 包括空格在内的任意空白字符  [\\f\\n\\r\\t\\v
  [:upper:]    -- 任意大写字母  [A-Z]
  [:xdight:]   -- 任意十六进制数字  [a-fA-F0-9]
  
# 重复元字符
  *      -- 0或多个匹配
  +      -- 1或多个匹配
  ?      -- 0或1个匹配，相当于{0,1}
  {n}    -- 指定数目的匹配
  {n,}   -- 不少于指定数目的匹配
  {n,m}  -- 匹配数目的范围，m不超过255
  
# 定位符 anchor
  ^        -- 文本的开始
  $        -- 文本的结尾，regexp ^expression$ 和 like expression 效果相同
  [[:<:]]  -- 词的开始
  [[:>;]]  -- 词的结尾
```

### 3.5.4 排序查询

```sql
order by 子句

即：
order by 排序字段1 排序方式1， 排序字段2 排序方式2...

排序方式：
  ASC：升序，默认
  DESC：降序，只是应用到直接位于其前面的列，多列降序需要给每个列后面加上DESC
```

注意：
如果有多个排序条件，则当前面的条件值一样时，才会判断第二个条件。

### 3.5.5 聚合函数

aggregate function

将一列数据作为一个整体，进行纵向的计算

+ `count`：计算个数。指定列名忽略NULL行，使用`*`则不忽略。
+ `max`：计算最大值。忽略NULL行。可以对文本列使用。
+ `min`：计算最小值。忽略NULL行。可以对文本列使用。
+ `sum`：求和。忽略NULL行。
+ `avg`：计算平均值。只能用于某一列，忽略NULL行。

如：

```sql
SELECT COUNT(ID) FROM STUDENT；  -- 一般用主键做变量，或者*，*表示一行中只要有一个值非null就纳入统计
```

**`DISTINCT`关键字的使用：**

`DISTINCT`关键字后跟列名可以对去重后的数据进行聚合函数操作，例如`avg(distinct price)`。`DISTINCT`后面必须跟列名，所以只能用于`count(列名)`的情况。

### 3.5.6 分组查询

```sql
group by 分组字段;  -- 用于需要分组的字段有重复，最后显示的结果中相同的进行合并
```

注意：

1. 分组之后查询的字段只能是：分组字段、聚合函数
2. 分组可以进行嵌套，但是会在最后规定上的分组上进行汇总
3. `group by`子句中不可以有聚合函数，可以是表达式
4. `NULL`会作为一个单独的组返回
5. 可以在分组字段后加上`WITH ROLLUP`关键字得到分组汇总级别的值



`having`：分组后过滤数据

+ where和having的区别：
  1. where在分组之前进行限定，如果不满足条件，则不参与分组
  2. having在分组之后进行限定，如果不满足条件，则不会被查询出来
  3. where后不能跟聚合函数，having后可以进行聚合函数的判断

### 3.5.7 分页查询/部分显示

```sql
limit 开始的索引，查询的条数;  -- 从开始的索引开始，显示n条，索引从0开始
limit 查询的条数 offset 开始的索引;
```

+ limit是一个MySQL的“方言”

### 3.5.8 数据处理函数

函数的可移植性不强，应该保证做好代码的注释

#### 3.5.8.1 文本处理函数

```sql
 Left()       -- 返回串左边的字符
 Length()     -- 返回串的长度
 Locate()     -- 找出串的一个子串
 Lower()      -- 将串转换为小写
 LTrim()      -- 去掉串左边的空格
 Right()      -- 返回串右边的字符
 RTrim()      -- 去掉串右边的空格
 Trim()       -- 去掉串两边的空格
 Soundex()    -- 返回串的SOUNDEX值：将串转换成语音相关的值的一个函数，可以匹配读音相近的词
 SubString()  -- 返回子串的字符
 Upper()      -- 将串转换为大写
```

#### 3.5.8.2 日期和时间处理函数

```sql
AddDate()       -- 增加一个日期（天、周等）
AddTime()       -- 增加一个时间（时、分等）
Now()           -- 返回当前日期和时间
CurDate()       -- 返回当前日期
CurTime()       -- 返回当前时间
Date()          -- 返回日期时间的日期部分
Year()          -- 返回一个日期的年部分
Month()         -- 返回一个日期的月份部分
Day()           -- 返回一个日期的天数部分
DayOfWeek()     -- 对于一个日期，返回对应的星期几
DateDiff()      -- 计算两个日期之差
Date_Add()      -- 高度灵活的日期运算函数
Date_Format()   -- 返回一个格式化的日期或时间串
Time()          -- 返回一个日期时间的时间部分
Hour()          -- 返回一个时间的小时部分
Minute()        -- 返回一个时间的分钟部分
Second()        -- 返回一个时间的秒部分
```

日期处理的注意事项：

1. MySQL中的时间可能是`'2020-10-10'`，也可能是`'2020-10-10 10:10:00'`，所以在`where`语句中要写`where Date(order_date) = '2020-10-10'`
2. 查询9月订单有2种写法`where Date(order_date) between '2020-09-01' and '2020-09-30'`，还可以写`where Year(order_date) = 2020 and Month(order_date) =9`（推荐）

#### 3.5.8.3 数值处理函数

```sql
Pi()          -- 返回圆周率
Rand()        -- 返回一个随机数
Abs()         -- 返回一个数的绝对值
Mod()         -- 返回除操作的余数
Sqrt()        -- 返回一个数的平方根
Exp()         -- 返回一个数的指数值
Cos()         -- 返回一个角度的余弦
Sin()         -- 返回一个角度的正弦
Tan()         -- 返回一个角度的正切
```

### 3.5.9 多表查询

```sql
select
	列名列表
from
	表名列表
where...
```

查询出来的结果叫：笛卡尔积，会出现A，B的全排列

#### 3.5.9.1 内连接查询：交集

+ 隐式内连接：使用where条件消除无用的数据。

```sql
where a.'b_id' = b.'id'
```

引号可以不加。一般写的时候，都在from里给表名起个别名

+ 显式内连接：join

```sql
select 字段列表 from 表名1 inner join 表名2 on 条件
```

inner可以省略

#### 3.5.9.2 外连接查询

+ 左外连接：left join
  查询的是左表所有数据以及其交集的部分

```sql
select 字段列表 from 表1 left [outer] join 表2 on 条件
```

+ 右外连接：right join
  查询的是右表所有数据以及其交集的部分

```sql
select 字段列表 from 表1 right [outer] join 表2 on 条件
```


#### 3.5.9.3 子查询

查询中嵌套查询，称嵌套查询为子查询

```sql
select * from t1 where t1.a = (select max(a) from t1)
```

子查询的不同使用情况：

1. 单行单列：作为条件，判断
2. 多行单列：作为条件，用in判断
3. 多行多列：作为一个虚拟表

### 3.5.10 组合查询

`union`关键字可以把多个查询语句的结果组合在一起

```sql
select ...
union
select ...
union
select ...
```

1. `UNION`的每个查询必须包含相同的列、表达式或聚合函数（顺序可以不一样）
2. 列数据类型必须兼容
3. 默认有去重效果，如果要显示重复内容，使用`UNION ALL`关键字
4. 只能对全部结果一起使用1个`order by`语句

## 3.6 DCL

#### 3.6.1 管理用户

```sql
create user '用户名'@'主机名' identified by '密码';  -- 添加用户，当不指定主机名时，使用%

rename user 原用户名 to 新用户名;  -- 重命名用户

drop user '用户名'@'主机名';  -- 删除用户

update user set password = password('新密码') where user = '用户名';  -- 修改密码
set password for '用户名'@'主机名' = password('新密码');  -- 修改密码
                                                       -- 不指定用户名时，更新当前登录用户的口令
```

+ 查询用户：切换到`mysql`数据库，查询`user`表【`%`表示可以在任意主机使用用户登录】

#### 3.6.2 如果忘记root密码

1. cmd

```shell
net stop mysql   #停止mysql服务，管理员运行
mysqld --skip-grant-tables   #无验证方式启动mysql服务
```
2. 新的cmd窗口

```shell
mysql
```
```sql
use mysql;

update user set password = password('新密码') where user = 'root';
```

3. 关闭窗口，任务管理器结束mysqld.exe进程

#### 3.6.3 权限管理

```sql
show grants for '用户名'@'主机名';  -- 查询权限
                                  -- usage表示没有任何权限

grant 权限列表 on 数据库.表 to '用户名'@'主机名';  -- 授予权限
grant all on *.* to 'root'@'localhost';  -- 使用通配符给root授予全部权限

revoke 权限列表 on 数据库.表 from '用户名'@'主机名';  -- 撤销权限
```

# 4 约束

概念：对表中的数据进行限定，保证数据的正确性、有效性和完整性。

分类：

1. 主键约束：`primary key`
2. 非空约束：`not null`
3. 唯一约束：`unique`
4. 外键约束：`foreign key`

## 4.1 主键约束：primary key

含义：非空且唯一

+ 一张表只能有一个字段为主键

1. 创建表的时候添加：字段后面跟`primary key`，或者在列的后面加`primary key(column_names)` 
2. 删除主键：

```sql
alter table 表名 drop primary key;
```

3. 创建好的表添加主键：用修改命令，字段后面加`primary key`

+ 自动增长：如果某一列是数值类型的，使用`auto_increment`。如果填NULL，就会自动获得一个+1的数。关键字跟在字段后面就行。可以通过`select last_insert_id()`获得最后一次插入的`AUTO_INCREMENT`数值

+ 删除：直接用修改命令

## 4.2 非空约束：值不能为null

`NOT NULL`

1. 创建表添加非空约束
   创建表的时候，在字段后面加上`NOT NULL`

2. 创建表完后添加非空约束
   修改命令

3. 删除非空约束
   用修改命令，不写NOT NULL

```sql
alter table stu modify name varchar(20)
```

## 4.3 唯一约束：值不能重复

`unique`

注意：唯一约束限定的列的值可以有多个null

1. 创建表的时候跟在字段后面
2. 创建表后添加唯一约束：修改的时候加载字段后面
3. 删除唯一约束：删除唯一索引

```sql
alter table stu drop index phone_number;
```

## 4.4 外键约束：foreign key

让表和表产生关系，从而保证数据的正确性。外键不能跨引擎。

创建表时，可以添加外键：

```sql
create table 表名(
    ...
    外键列，
    constraint 外键名称 foreign key (外键列名称) references 主表名称(主表列名称)
);
```

```sql
alter table stu drop foreign key 外键名称;  -- 删除外键

alter table stu add constraint 外键名称 foreign key (外键列名称) references 主表名称(主表列名称);  -- 添加外键
```

### 4.4.1 级联操作

```sql
alter table stu add constraint 外键名称 foreign key (外键列名称) references 主表名称(主表列名称) on update cascade  -- 级联添加
on update cascade  -- 级联更新
on delete cascade  -- 级联删除
```

+ 两个可以只有一个，也可以一起
+ 谨慎使用

# 5 数据库的设计

## 5.1 多表之间的关系

+ 一对一
+ 一对多
+ 多对多

实现：

1. 一对多：在多的一方建立外键，指向一的一方的主键
2. 多对多：借助中间表，中间表至少包含2个字段，作为外键，分别指向两张表的主键
3. 一对一：任意一方添加唯一外键，指向另一个的主键【很少见，直接合成一张表就行了】

架构设计器里可以看到表的关系

## 5.2 数据库设计的范式

分类：有6种

这里只学3种：

+ 第一范式1NF：每一列都是不可分割的原子数据项
+ 第二范式2NF：1NF的基础上，消除非主属性对主码的部分函数依赖
+ 第三范式3NF：2NF的基础上，消除传递依赖

### 5.2.1 1NF

1NF的问题：

1. 数据冗余
2. 添加删除都有一些问题

### 5.2.2 2NF

几个概念：

1. 函数依赖：通过 属性（属性组）A的值，可以确定唯一的属性B的值，则B依赖于A。A-->B 【如 学号-->姓名】【（学号，课程名称）-->分数】
2. 完全函数依赖：A是属性组，B的确定需要A属性组中所有的属性值
3. 部分函数依赖：A是属性组，B的确定只需要A属性组中的部分
4. 传递函数依赖：A-->B，B-->C，则C传递函数依赖于A
5. 码：一张表里，一个属性或属性组，被其他所有的属性完全依赖，则这个属性或属性组为该表的码
6. 主属性：码  属性组中的属性
7. 非主属性：非码的属性

方法：拆分表

缺点：添加和删除还有问题

### 5.2.3 3NF

消除传递依赖

方法：拆分表

# 6 视图

## 6.1 视图概述

视图（View）是一种虚拟存在的表。视图并不在数据库中实际存在，行和列数据来自定义视图的查询中使用的表，并且是在使用视图时动态生成的。

通俗的讲，视图就是一条SELECT语句执行后返回的结果集。所以我们在创建视图的时候，主要的工作就落在创建这条SQL查询语句上。

**每次使用视图，都会重复执行一遍定义的查询语句。可以重用复杂的SQL语句。**

视图相对于普通的表的优势主要包括以下几项。

+ 简单：使用视图的用户完全不需要关心后面对应的表的结构、关联条件和筛选条件，对用户来说已经是过滤好的复合条件的结果集。
+ 安全：使用视图的用户只能访问他们被允许查询的结果集，对表的权限管理并不能限制到某个行某个列，但是通过视图就可以简单的实现。
+ 数据独立：一旦视图的结构确定了，可以屏蔽表结构变化对用户的影响，源表增加列对视图没有影响；源表修改列名，则可以通过修改视图来解决，不会造成对访问者的影响。



**视图的常见应用有：**

1. 重用SQL语句
2. 简化复杂的SQL操作
3. 使用表的部分数据
4. 保护数据
5. 更改数据格式



**规则：**

1. 视图名唯一，相当于一张表
2. 视图数目没有限制
3. 创建视图需要有足够的访问权限
4. 视图可以嵌套
5. 视图可以有`ORDER BY`语句，但是仅有最外层的生效
6. 视图不能索引、不能有触发器或默认值
7. 视图可以和表混用
8. **传递给视图的`where`子句会和视图中的`where`子句自动组合**
9. 对视图`update`会操作基表，并不是所有视图都可以`update`的

## 6.2 使用视图

### 6.2.1 创建视图

```sql
-- 创建视图
create view view_name as
select_statement

-- 如果存在就更新，如果不存在就创建
create or replace view view_name as
select_statement
```

完整语法：

```sql
CREATE [OR REPLACE] [ALGORITHM = {UNDEFINED | MERGE | TEMPTABLE}]

VIEW view_name [(column_list)]

AS select_statement

[WITH [CASCADED | LOCAL] CHECK OPTION]


-- 选项:
  -- WITH [CASCADED | LOCAL] CHECK OPTION 决定了是否允许更新数据使记录不再满足视图的条件。

  -- LOCAL ：只要满足本视图的条件就可以更新。
  -- CASCADED ：必须满足所有针对该视图的所有视图的条件才可以更新。默认值.
```

### 6.2.2 修改视图

完整语法：

```sql
ALTER [ALGORITHM = {UNDEFINED | MERGE | TEMPTABLE}]

VIEW view_name [(column_list)]

AS select_statement

[WITH [CASCADED | LOCAL] CHECK OPTION]
```

### 6.2.3 查看视图

从MySQL 5.1 版本开始，使用`SHOW TABLES`命令的时候不仅显示表的名字，同时也会显示视图的名字，而不存在单独显示视图的`SHOW VIEWS`命令。同样，在使用`SHOW TABLE STATUS`命令的时候，不但可以显示表的信息，同时也可以显示视图的信息。

```sql
SHOW TABLES;

SHOW CREATE VIEW view_name;    -- 查询创建视图的语句
```

### 6.2.4 删除视图

```sql
DROP VIEW view_name;
```

完整语法:

```sql
DROP VIEW [IF EXISTS] view_name [, view_name] ...[RESTRICT | CASCADE]
```

# 7 存储过程和函数

## 7.1 存储过程和函数概述

存储过程和函数是事先经过编译并存储在数据库中的一段SQL语句的集合，可视其为批文件。调用存储过程和函数可以简化应用开发人员的很多工作，减少数据在数据库和应用服务器之间的传输，对于提高数据处理的效率是有好处的（简单、安全、高性能）。

存储过程和函数的区别在于函数必须有返回值，而存储过程没有。

+ 函数：是一个有返回值的过程；

+ 过程：是一个没有返回值的函数；

### 7.1.1 创建存储过程

```sql
CREATE PROCEDURE procedure_name ([proc_parameter[,...]])
begin
    -- SQL语句
end;
```

示例：

```sql
delimiter $     -- 修改默认的分隔符;为$

create procedure pro_test1()
begin
    select 'Hello Mysql' ;
end$

delimiter ;
```

+ **`DELIMITER`**

该关键字用来声明SQL语句的分隔符, 告诉MySQL 解释器，该段命令是否已经结束了，mysql是否可以执行了。默认情况下，delimiter是分号`;`。在命令行客户端中，如果有一行命令以分号结束，那么回车后，mysql将会执行该命令。

### 7.1.2 调用存储过程

```sql
call procedure_name();
```

### 7.1.3 查看存储过程

```sql
-- 查询db_name数据库中的所有的存储过程
select name from mysql.proc where db='db_name';

-- 查询存储过程的状态信息
show procedure status;

-- 查询某个存储过程的定义
show create procedure test.pro_test1 \G;
```

### 7.1.4 删除存储过程

```sql
DROP PROCEDURE [IF EXISTS] procedure_name ；
```

## 7.2 语法

存储过程是可以编程的，意味着可以使用变量，表达式，控制结构，来完成比较复杂的功能。

### 7.2.1 变量

+ `DECLARE`

通过`DECLARE`可以定义一个局部变量，该变量的作用范围只能在`BEGIN…END` 块中。

```sql
DECLARE var_name[,...] type [DEFAULT value]
```

示例:

```sql
delimiter $

create procedure pro_test2()
begin
    declare num int default 5;
    select num + 10;
end$

delimiter ;
```

`declare`可以声明局部变量、游标cursor、handler，相对顺序不能错，局部变量一定要在其他两个之前声明

+ `SET`

直接赋值使用`SET`，可以赋常量或者赋表达式，具体语法如下：

```sql
SET var_name = expr [, var_name = expr] ...
```

示例:

```sql
DELIMITER $

CREATE PROCEDURE pro_test3()
BEGIN
    DECLARE NAME VARCHAR(20);
    SET NAME = 'MYSQL';
    SELECT NAME ;
END$

DELIMITER ;
```

也可以通过`select ... into`方式进行赋值操作:

```sql
DELIMITER $

CREATE PROCEDURE pro_test5()
BEGIN
    declare countnum int;
    select count(*) into countnum from city;
    select countnum;
END$

DELIMITER ;
```

### 7.2.2 if条件判断

语法结构:

```sql
if search_condition then statement_list

    [elseif search_condition then statement_list] ...

    [else statement_list]

end if;
```

需求：

```
根据定义的身高变量，判定当前身高的所属的身材类型
180 及以上 ----------> 身材高挑
170-180   ----------> 标准身材
170 以下   ----------> 一般身材
```

示例:

```sql
delimiter $

create procedure pro_test6()
begin
    declare height int default 175;
    declare description varchar(50);
    
    if height >= 180 then
        set description = '身材高挑';
    elseif height >= 170 and height < 180 then
        set description = '标准身材';
    else
        set description = '一般身材';
    end if;
    
    select description ;
end$

delimiter ;
```

### 7.2.3 传递参数

语法格式:

```sql
create procedure procedure_name([in/out/inout] 参数名参数类型)
    ...

IN : 该参数可以作为输入，也就是需要调用方传入值, 默认
OUT: 该参数作为输出，也就是该参数可以作为返回值
INOUT: 既可以作为输入参数，也可以作为输出参数
```

**IN - 输入**

需求:

```
根据定义的身高变量，判定当前身高的所属的身材类型
```

示例:

```sql
delimiter $

create procedure pro_test5(in height int)
begin
    declare description varchar(50) default '';
    
    if height >= 180 then
        set description='身材高挑';
    elseif height >= 170 and height < 180 then
        set description='标准身材';
    else
        set description='一般身材';
    end if;
    
    select concat('身高', height , '对应的身材类型为:',description);
end$

delimiter ;
```

**OUT-输出**

需求:

```
根据传入的身高变量，获取当前身高的所属的身材类型
```

示例:

```sql
create procedure pro_test5(in height int , out description varchar(100))
begin
    if height >= 180 then
        set description='身材高挑';
    elseif height >= 170 and height < 180 then
        set description='标准身材';
    else
        set description='一般身材';
    end if;
end$
```

调用:

```sql
call pro_test5(168, @description)$

select @description$
```

**小知识**

`@description` : 这种变量要在变量名称前面加上“@”符号，叫做用户会话变量，代表整个会话过程他都是有作用的，这个类似于全局变量一样。

`@@global.sort_buﬀer_size`: 这种在变量前加上"@@" 符号, 叫做系统变量

### 7.2.4 case结构

语法结构:

```sql
方式一:
CASE case_value
    WHEN when_value THEN statement_list
    [WHEN when_value THEN statement_list] ...
    [ELSE statement_list]
END CASE;

方式二:
CASE
    WHEN search_condition THEN statement_list
    [WHEN search_condition THEN statement_list] ...
    [ELSE statement_list]
END CASE;
```

需求:

```
给定一个月份, 然后计算出所在的季度
```

示例:

```sql
delimiter $

create procedure pro_test9(month int)
begin
    declare result varchar(20);
    case
        when month >= 1 and month <=3 then
            set result = '第一季度';
        when month >= 4 and month <=6 then
            set result = '第二季度';
        when month >= 7 and month <=9 then
            set result = '第三季度';
        when month >= 10 and month <=12 then
            set result = '第四季度';
    end case;
    
    select concat('您输入的月份为:', month , ' , 该月份为: ' , result) as content ;
end$

delimiter ;
```

### 7.2.5 while循环

语法结构:

```sql
while search_condition do
    statement_list
end while;
```

需求:

```
计算从1加到n的值
```

示例:

```sql
delimiter $

create procedure pro_test8(n int)
begin
    declare total int default 0;
    declare num int default 1;
    while num<=n do
        set total = total + num;
        set num = num + 1;
    end while;
    select total;
end$

delimiter ;
```

### 7.2.6 repeat结构

有条件的循环控制语句, 当满足条件的时候退出循环。while 是满足条件才执行，repeat 是满足条件就退出循环。
语法结构:

```sql
REPEAT
    statement_list
    UNTIL search_condition
END REPEAT;
```

需求:

```
计算从1加到n的值
```

示例:

```sql
delimiter $

create procedure pro_test10(n int)
begin
    declare total int default 0;
    
    repeat
        set total = total + n;
        set n = n - 1;
        until n=0
    end repeat;
    
    select total ;
end$

delimiter ;
```

### 7.2.7 loop语句

LOOP 实现简单的循环，退出循环的条件需要使用其他的语句定义，通常可以使用LEAVE 语句实现，具体语法如下：

```sql
[begin_label:] LOOP

    statement_list

END LOOP [end_label]
```

如果不在statement_list 中增加退出循环的语句，那么LOOP 语句可以用来实现简单的死循环。

### 7.2.8 leave语句

用来从标注的流程构造中退出，通常和BEGIN ... END 或者循环一起使用。下面是一个使用LOOP 和LEAVE 的简单例子, 退出循环：

```sql
delimiter $

CREATE PROCEDURE pro_test11(n int)
BEGIN
    declare total int default 0;
    
    ins: LOOP
    
        IF n <= 0 then
            leave ins;
        END IF;

        set total = total + n;
        set n = n - 1;
    
    END LOOP ins;
    
    select total;
END$

delimiter ;
```

### 7.2.9 游标/光标

游标是用来存储查询结果集的数据类型, 在存储过程和函数中可以使用光标对结果集进行循环的处理。光标的使用包括光标的声明、OPEN、FETCH 和CLOSE，其语法分别如下。

声明光标：

```sql
DECLARE cursor_name CURSOR FOR select_statement ;
```

OPEN 光标：

```sql
OPEN cursor_name ;
```

FETCH 光标：

```sql
FETCH cursor_name INTO var_name [, var_name] ...
```

CLOSE 光标：

```sql
CLOSE cursor_name ;
```

示例:

初始化脚本:

```sql
create table emp(
    id int(11) not null auto_increment ,
    name varchar(50) not null comment '姓名',
    age int(11) comment '年龄',
    salary int(11) comment '薪水',
    primary key(`id`)
)engine=innodb default charset=utf8 ;


insert into emp(id,name,age,salary) values(null,'金毛狮王',55,3800),(null,'白眉鹰王',60,4000),(null,'青翼蝠王',38,2800),(null,'紫衫龙王',42,1800);
```

```sql
-- 查询emp表中数据, 并逐行获取进行展示
create procedure pro_test11()
begin
    declare e_id int(11);
    declare e_name varchar(50);
    declare e_age int(11);
    declare e_salary int(11);
    declare emp_result cursor for select * from emp;
    
    open emp_result;
    
    fetch emp_result into e_id,e_name,e_age,e_salary;
    select concat('id=',e_id , ', name=',e_name, ', age=', e_age, ', 薪资为:',e_salary);
    
    fetch emp_result into e_id,e_name,e_age,e_salary;
    select concat('id=',e_id , ', name=',e_name, ', age=', e_age, ', 薪资为:',e_salary);
    
    fetch emp_result into e_id,e_name,e_age,e_salary;
    select concat('id=',e_id , ', name=',e_name, ', age=', e_age, ', 薪资为:',e_salary);
    
    fetch emp_result into e_id,e_name,e_age,e_salary;
    select concat('id=',e_id , ', name=',e_name, ', age=', e_age, ', 薪资为:',e_salary);
    
    fetch emp_result into e_id,e_name,e_age,e_salary;
    select concat('id=',e_id , ', name=',e_name, ', age=', e_age, ', 薪资为:',e_salary);
    
    close emp_result;
end$
```

通过循环结构, 获取游标中的数据

```sql
DELIMITER $

create procedure pro_test12()
begin
    DECLARE id int(11);
    DECLARE name varchar(50);
    DECLARE age int(11);
    DECLARE salary int(11);
    DECLARE has_data int default 1;
    
    DECLARE emp_result CURSOR FOR select * from emp;
    DECLARE EXIT HANDLER FOR NOT FOUND set has_data = 0;
    
    open emp_result;
    
    repeat
        fetch emp_result into id , name , age , salary;
        select concat('id为',id, ', name 为' ,name , ', age为' ,age , ', 薪水为: ', salary);
        until has_data = 0
    end repeat;
    
    close emp_result;
end$

DELIMITER ;
```

## 7.3 存储函数

语法结构:

```sql
CREATE FUNCTION function_name([param type ... ])
RETURNS type
BEGIN
    ...
END;
```

案例:
定义一个存储过程, 请求满足条件的总记录数;

```sql
delimiter $

create function count_city(countryId int)
returns int
begin
    declare cnum int ;
    select count(*) into cnum from city where country_id = countryId;
    return cnum;
end$

delimiter ;
```

调用:

```sql
select count_city(1);

select count_city(2);
```

# 8 触发器

## 8.1 介绍

触发器是与表有关的数据库对象，指在insert/update/delete 之前或之后，触发并执行触发器中定义的SQL语句集合。触发器的这种特性可以协助应用在数据库端确保数据的完整性, 日志记录, 数据校验等操作。

仅支持表，视图和临时表不支持触发器。

使用别名OLD 和NEW 来引用触发器中发生变化的记录内容，这与其他的数据库是相似的。现在触发器还只支持行级触发，不支持语句级触发。

| 触发器类型      | NEW 和OLD的使用                                              |
| --------------- | ------------------------------------------------------------ |
| INSERT 型触发器 | NEW 表示将要或者已经新增的数据，可以被更新，自增长列置0即可  |
| UPDATE 型触发器 | OLD 表示修改之前的数据，只读； NEW 表示将要或已经修改后的数据，可以被更新 |
| DELETE 型触发器 | OLD 表示将要或者已经删除的数据                               |

## 8.2 创建触发器

语法结构:

```sql
create trigger trigger_name
before/after insert/update/delete
on tbl_name
[ for each row ] -- 行级触发器
begin
    trigger_stmt ;
end
```

示例
需求

```
通过触发器记录emp 表的数据变更日志, 包含增加, 修改, 删除;
```

首先创建一张日志表:

```sql
create table emp_logs(
    id int(11) not null auto_increment,
    operation varchar(20) not null comment '操作类型, insert/update/delete',
    operate_time datetime not null comment '操作时间',
    operate_id int(11) not null comment '操作表的ID',
    operate_params varchar(500) comment '操作参数',
    primary key(`id`)
)engine=innodb default charset=utf8;
```

创建insert 型触发器，完成插入数据时的日志记录:

```sql
DELIMITER $

create trigger emp_logs_insert_trigger
after insert
on emp
for each row
begin
    insert into emp_logs (id,operation,operate_time,operate_id,operate_params) values(null,'insert',now(),new.id,concat('插入后(id:',new.id,', name:',new.name,', age:',new.age,', salary:',new.salary,')'));
end $

DELIMITER ;
```

创建update 型触发器，完成更新数据时的日志记录:

```sql
DELIMITER $

create trigger emp_logs_update_trigger
after update
on emp
for each row
begin
    insert into emp_logs (id,operation,operate_time,operate_id,operate_params) values(null,'update',now(),new.id,concat('修改前(id:',old.id,', name:',old.name,', age:',old.age,', salary:',old.salary,') , 修改后(id',new.id, 'name:',new.name,', age:',new.age,', salary:',new.salary,')'));
end $

DELIMITER ;
```

创建delete 行的触发器, 完成删除数据时的日志记录:

```sql
DELIMITER $

create trigger emp_logs_delete_trigger
after delete
on emp
for each row
begin
    insert into emp_logs (id,operation,operate_time,operate_id,operate_params) values(null,'delete',now(),old.id,concat('删除前(id:',old.id,', name:',old.name,', age:',old.age,', salary:',old.salary,')'));
end $

DELIMITER ;
```

测试：

```sql
insert into emp(id,name,age,salary) values(null, '光明左使',30,3500);
insert into emp(id,name,age,salary) values(null, '光明右使',33,3200);

update emp set age = 39 where id = 3;

delete from emp where id = 5;
```

注意：

1. 如果BEFORE触发器失败，则不会执行后续的SQL语句
2. 如果BEFORE触发器或语句执行失败，则不会执行后续的AFTER触发器

## 8.3 删除触发器

语法结构:

```sql
drop trigger [schema_name.]trigger_name
```

如果没有指定schema_name，默认为当前数据库。

## 8.4 查看触发器

可以通过执行SHOW TRIGGERS 命令查看触发器的状态、语法等信息。

语法结构：

```sql
show triggers ；
```

# 9 事务

## 9.1 事务的基本介绍

1. 概念：多个操作被事务管理，要么同时成功，要么同时失败

2. 操作
   1. 开启事务：start transaction
   2. 回滚：rollback
   3. 提交：commit

3. MySQL数据库中，事务默认自动提交【即会被保存】
   Oracle数据库默认手动提交
   更改：
   `select @@autocommit;`查看提交方式，1自动，0手动
   `set @@autocommit;`会改为手动，这样增删改命令后如果不手动commit就不会被保存


## 9.2 事务的四大特征ACID

atomic consistency isolation durability

1. 原子性：不可分割的最小操作单位，要么同时成功，要么同时失败
2. 持久性：事务提交或回滚后，数据库会持久化的保存数据
3. 隔离性：多个事务之间相互独立
4. 一致性：事务操作前后，数据总量不变

## 9.3 事务的隔离级别

多个事务操作同一批数据，会出问题：

1. 脏读：一个事务，读取到另一个事务中没有提交的数据
2. 不可重复读（虚读）：同一个事务中，两次读取到的数据不一样
3. 幻读：一个事务操作数据表中所有记录，另一个事务添加了一条数据，则第一个事务会查询到这个数据

隔离级别：

1. read uncommitted：会脏读、虚读、幻读
2. read committed（Oracle默认）：会虚读、幻读
3. repeatable read（MySQL默认）：幻读
4. serializable：没问题

隔离级别越高，效率越低

查询、修改隔离级别（不用记）：

```sql
select @@tx_isolation;
set global transaction isolation level 级别字符串;（图形化界面中重启后才能查看到生效）
```

## 9.4 保留点

可以在事务过程中设置保留点，从而控制回滚到哪里

```sql
-- 定义保留点
savepoint sv_name;

-- 回滚到某一个保留点
rollback to sv_name;
```

+ 事务处理完成后会自动释放保留点，也可以手动释放`release savepoint`

# 10 数据库的备份和还原

## 10.1 命令行

备份：

```shell
mysqldump -u用户名 -p密码 数据库名> 保存的路径
```

还原：

```
登录-->创建-->使用-->source 文件路径
```

## 10.2 图形化工具

备份
还原：执行SQL脚本

