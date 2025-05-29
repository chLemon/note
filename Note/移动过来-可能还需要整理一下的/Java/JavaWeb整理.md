# JavaWeb

## 1 数据库的基本概念

DataBase（DB）

数据库的特点：
1. 持久化存储数据的。其实数据库就是一个文件系统
2. 方便存储和管理数据
3. 使用统一方式操作数据库——SQL

## 2 MySQL数据库软件

### 2.1 安装

6.x开始收费

配置的时候如果有哪一个不是勾，就得删了重装

控制台：```mysql -uroot -p[password]```
查看是否安装成功

### 2.2 卸载

1. 找到MySQL的安装路径
2. 找到my.ini文件，从里面找到datadir
3. 控制面板卸载MySQL
4. 删掉datadir那个路径最高的MySQL文件夹

### 2.3 配置

计算机——右键——管理——服务和应用程序——可以查看服务
cmd——> services.msc也可以打开服务

（管理员cmd）
```
net start mysql  开启服务
```
```
net stop mysql  关闭服务
```

### 2.4 登录

cmd：
```
mysql -uroot -p[password]

mysql -h[ip] -uroot -p[password]

mysql --host=[ip] --user=root --password=[password]
```

### 2.6 退出

cmd：
```
exit
quit
```

### 2.7 MySQL目录结构

my.ini 配置文件

### 2.8 数据目录

每个文件夹：一个数据库
.frm文件：表
数据记录

### 2.9 客户端图形化工具：SQLYog

12.0.9-0
破解码：
姓名：cr173
序列号：
8d8120df-a5c3-4989-8f47-5afc79c56e7c
59adfdfe-bcb0-4762-8267-d7fccf16beda
ec38d297-0543-4679-b098-4baadf91f983

IDEA也有

## 3 SQL

Structured Query Language：结构化查询语言

所有关系型数据库都可以用SQL操作，而每种数据库方式里不一样的地方称为“方言”。

### 3.1 SQL通用语法

1. 可以单行或多行书写，分号结尾。
2. 不区分大小写，但是关键字建议大写
3. 注释有3种：
```
-- 单行注释【这个必须有空格】

# 单行注释【这个可以没有空格】

/* 多行注释 */
```

### 3.2 SQL语句的分类

1. DDL（Data Definition Language），数据定义语言
操作数据库、表

2. DML（Manipulation）操作
增删改表中的数据

3. DQL（Query）查询
查询表中的数据

4. DCL（Control）控制
授权

### 3.3 DDL：操作数据库、表

#### 3.3.1 操作数据库

##### 3.3.1.1 C：创建

Create

```
create database 数据库名称;  -- 创建数据库
create database if not exists 数据库名称;  -- 判断不存在再创建：
create database 数据库名称 character set 字符集名;  -- 指定字符集：
```

##### 3.3.1.2 R：查询

Retrieve

```
show databases;  -- 查询所有数据库的名称
show create database 数据库名;  -- 查看某个数据库的字符集（编码），本意是查询某个数据库的创建语句
```

##### 3.3.1.3 U：修改

Update

```
alter database 数据库名称 character set 字符集名;  -- 修改数据库的字符集。utf8，没有中间的横杠.
```

##### 3.3.1.4 D：删除

Delete

```
drop database 数据库名称;  -- 删除数据库
drop database if exists 数据库名称;  -- 判断存在再删除
```

##### 3.3.1.5 使用数据库

```
select database();  -- 查询当前正在使用的数据库名称

use 数据库名称;  -- 使用数据库
```

#### 3.3.2 操作表

##### 3.3.2.1 创建

语法：
```
create table 表名(
    列名1 数据类型1,
    列名2 数据类型2,
    ...
    列名n 数据类型n,
);
```
注意：最后一列不要加逗号


```
create table 新表 like 源表;  -- 复制
```

数据库数据类型有：
1. int：整数。```age int```
2. double：小数类型。```score double(5,2)```前一个参数是总位数，后一个是小数点后的位数
3. date：日期，只包含年月日，```yyyy-MM-dd```
4. datetime：日期，包含年月日时分秒，```yyyy-MM-dd HH:mm:ss```
5. timestamp：时间戳类型，包含年月日时分秒，```yyyy-MM-dd HH:mm:ss```。如果不给这个字段赋值，或赋值为null，则默认使用当前的系统时间来自动赋值
6. varchar：字符串。```name varchar(20)```参数是可以包含的最大字符数
7. 如果包含中文，用nvarchar和nchar

##### 3.3.2.2 查询

```
show tables;  -- 查询某个数据库中所有的表名称

desc 表名;  -- 查询表结构
```

##### 3.3.2.3 修改

```sql
alter table 表名 rename to 新的表名;  -- 修改表名

alter table 表名 character set utf8;  -- 修改表的字符集

alter table 表名 add 列名 数据类型;  -- 添加一列

alter table 表名 change 原列名 新列名 新类型;  -- 修改列名和类型
alter table 表名 modify 列名 新类型;  -- 只修改类型

alter table 表名 drop 列名;  -- 删除列
```

##### 3.3.2.4 删除

```
drop table 表名;
drop table if exists 表名;
```

### 3.4 DML：增删改表中数据

#### 3.4.1 添加数据

```
insert into 表名(列名1,列名2,...,列名n) values(值1,值2,...值n);
```

注意：
1. 列名和值要一一对应
2. 如果表名后没有指定列名，则默认给所有列添加值
3. 除了数字类型和NULL，其他类型需要使用引号（单双均可）引起来
4. 在值前面加上N表示用Unicode编码，所有字符占2个字节

#### 3.4.2 删除数据

```
delete from 表名 where 条件;
```

注意：
如果不加where，会删除表中所有的记录。
但是该操作会重复执行很多次（一条记录一次），如果希望清空表，用
```
truncate table 表名;
```

#### 3.4.3 修改数据

```
update 表名 set 列名1 = 值1, 列名2 = 值2, ... [where 条件];
```

注意：如果不加条件，会修改所有值。

### 3.5 DQL：查询表中的记录

```
select * from 表名;  -- 查询表中所有的数据
```

#### 3.5.1 语法

```
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

#### 3.5.2 基础查询

1. 多个字段的查询
```
select 字段名1, 字段名2, ... from 表名;
```
注意：如果查询所有字段，则可以用```*```来替代字段列表

2. 去除重复：```distinct```关键字

3. 计算列
一般可以使用四则运算计算一些列的值，如果有null参与，结果都为null。

```
ifnull(表达式1,表达式2);
```
表达式1为可能会出现null的字段，判断是否有null的字段名。如果字段为null，会替换为表达式2的值

4. 起别名：```as```关键字，as也可以省略，用空格

#### 3.5.3 条件查询

+ where子句后跟条件

+ 运算符
```
> < <= >= = <>  -- 【不等于有2种<>或<!=>，等于只有一个等号】

BETWEEN ... AND  -- 选取介于两个值之间的数据范围

IN(集合)

LIKE  -- 模糊查询，配合占位符一起使用。
	_  -- 占位符，单个任意字符
	%  -- 占位符，多个任意字符

IS NULL  -- NULL不能用等于和不等于判断
IS NOT NULL

and或&&，推荐and，下同
or或||
not或！
```

#### 3.5.4 排序查询

```
order by 子句

即：
order by 排序字段1 排序方式1， 排序字段2 排序方式2...
```
排序方式：
  ASC：升序，默认
  DESC：降序

注意：
如果有多个排序条件，则当前面的条件值一样时，才会判断第二个条件。

#### 3.5.5 聚合函数

将一列数据作为一个整体，进行纵向的计算

+ count：计算个数
+ max：计算最大值
+ min：计算最小值
+ sum：求和
+ avg：计算平均值

如：
```
SELECT COUNT(ID) FROM STUDENT；  -- 一般用主键做变量，或者*，*表示一行中只要有一个值非null就纳入统计
```

**注意：聚合函数的计算，会排除null值。**

#### 3.5.6 分组查询

```
group by 分组字段;  -- 用于需要分组的字段有重复，最后显示的结果中相同的进行合并
```

+ 分组之后查询的字段：分组字段、聚合函数

+ where和having的区别：
  1. where在分组之前进行限定，如果不满足条件，则不参与分组
  2. having在分组之后进行限定，如果不满足条件，则不会被查询出来
  3. where后不能跟聚合函数，having后可以进行聚合函数的判断

#### 3.5.7 分页查询

```
limit 开始的索引，每页查询的条数;  -- 从开始的索引开始，显示n条，索引从0开始
```

+ limit是一个MySQL的“方言”

#### 3.5.8 多表查询

```
select
	列名列表
from
	表名列表
where...
```

查询出来的结果叫：笛卡尔积，会出现A，B的全排列

##### 3.5.8.1 内连接查询：交集

+ 隐式内连接：使用where条件消除无用的数据。

```
where a.'b_id' = b.'id'
```
引号可以不加。一般写的时候，都在from里给表名起个别名

+ 显式内连接：join

```
select 字段列表 from 表名1 inner join 表名2 on 条件
```
inner可以省略

##### 3.5.8.2 外连接查询

+ 左外连接：left join
查询的是左表所有数据以及其交集的部分
```
select 字段列表 from 表1 left [outer] join 表2 on 条件
```

+ 右外连接：right join
查询的是右表所有数据以及其交集的部分
```
select 字段列表 from 表1 right [outer] join 表2 on 条件
```


##### 3.5.8.3 子查询

查询中嵌套查询，称嵌套查询为子查询
```
select * from t1 where t1.a = (select max(a) from t1)
```

子查询的不同情况：
1. 单行单列：作为条件，判断
2. 多行单列：作为条件，用in判断
3. 多行多列：作为一个虚拟表

### 3.6 DCL

#### 3.6.1 管理用户

```
create user '用户名'@'主机名' identified by '密码';  -- 添加用户

drop user '用户名'@'主机名';  -- 删除用户

update user set password = password('新密码') where user = '用户名';  -- 修改密码：
set password for '用户名'@'主机名' = password('新密码');  -- 修改密码：
```
+ 查询用户：切换到mysql数据库，查询user表【%表示可以在任意主机使用用户登录】

#### 3.6.2 如果忘记root密码

```
1. cmd --> net stop mysql   停止mysql服务，管理员运行
2. mysqld --skip-grant-tables   无验证方式启动mysql服务
3. 新cmd窗口，mysql
4. use mysql
5. update user set password = password('新密码') where user = 'root';
6. 关闭窗口，任务管理器结束mysqld.exe进程
```

#### 3.6.3 权限管理

```
show grants for '用户名'@'主机名';  -- 查询权限

grant 权限列表 on 数据库.表 to '用户名'@'主机名';  -- 授予权限
grant all on *.* to 'root'@'localhost';  -- 使用通配符给root授予全部权限

revoke 权限列表 on 数据库.表 from '用户名'@'主机名';  -- 撤销权限
```

## 4 约束

概念：对表中的数据进行限定，保证数据的正确性、有效性和完整性。

分类：

  1. 主键约束：primary key

  2. 非空约束：not null

  3. 唯一约束：unique

  4. 外键约束：foreign key

### 4.1 主键约束：primary key

含义：非空且唯一
+ 一张表只能有一个字段为主键

1. 创建表的时候添加：字段后面跟```primary key```
2. 删除主键：
```
alter table stu drop primary key;
```
3. 创建好的表添加主键：用修改命令，字段后面加```primary key```

+ 自动增长：如果某一列是数值类型的，使用```auto_increment```。如果填NULL，就会自动获得一个+1的数。关键字跟在字段后面就行

+ 删除：直接用修改命令

### 4.2 非空约束：值不能为null

```NOT NULL```

1. 创建表添加非空约束
创建表的时候，在字段后面加上```NOT NULL```

2. 创建表完后添加非空约束
修改命令

3. 删除非空约束
    用修改命令，不写NOT NULL
```
alter table stu modify name varchar(20)
```

### 4.3 唯一约束：值不能重复

```unique```

注意：唯一约束限定的列的值可以有多个null

1. 创建表的时候跟在字段后面
2. 创建表后添加唯一约束：修改的时候加载字段后面
3. 删除唯一约束：删除唯一索引
```
alter table stu drop index phone_number;
```

### 4.4 外键约束：foreign key

让表和表产生关系，从而保证数据的正确性

创建表时，可以添加外键：
```
create table 表名(
    ...
    外键列，
    constraint 外键名称 foreign key (外键列名称) references 主表名称(主表列名称)
);
```


```
alter table stu drop foreign key 外键名称;  -- 删除外键

alter table stu add constraint 外键名称 foreign key (外键列名称) references 主表名称(主表列名称);  -- 添加外键
```

#### 4.4.1 级联操作

```
alter table stu add constraint 外键名称 foreign key (外键列名称) references 主表名称(主表列名称) on update cascade  -- 级联添加
on update cascade  -- 级联更新
on delete cascade  -- 级联删除
```

+ 两个可以只有一个，也可以一起
+ 谨慎使用

## 5 数据库的设计

### 5.1 多表之间的关系

+ 一对一
+ 一对多
+ 多对多

实现：
1. 一对多：在多的一方建立外键，指向一的一方的主键
2. 多对多：借助中间表，中间表至少包含2个字段，作为外键，分别指向两张表的主键
3. 一对一：任意一方添加唯一外键，指向另一个的主键【很少见，直接合成一张表就行了】

架构设计器里可以看到表的关系

### 5.2 数据库设计的范式

分类：有6种

这里只学3种：
+ 第一范式1NF：每一列都是不可分割的原子数据项
+ 第二范式2NF：1NF的基础上，消除非主属性对主码的部分函数依赖
+ 第三范式3NF：2NF的基础上，消除传递依赖

#### 5.2.1 1NF

1NF的问题：
1. 数据冗余
2. 添加删除都有一些问题

#### 5.2.2 2NF

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

#### 5.2.3 3NF

消除传递依赖

方法：拆分表

## 6 数据库的备份和还原

### 6.1 命令行

备份：
```
mysqldump -u用户名 -p密码 数据库名> 保存的路径
```
还原：
```
登录-->创建-->使用-->source 文件路径
```

### 6.2 图形化工具

备份
还原：执行SQL脚本

## 7 事务

### 7.1. 事务的基本介绍

1. 概念：多个操作被事务管理，要么同时成功，要么同时失败

2. 操作
    1. 开启事务：start transaction
    2. 回滚：rollback
    3. 提交：commit

3. MySQL数据库中，事务默认自动提交【即会被保存】
   Oracle数据库默认手动提交
   更改：
   ```select @@autocommit;```查看提交方式，1自动，0手动
   ```set @@autocommit;```会改为手动，这样增删改命令后如果不手动commit就不会被保存


### 7.2. 事务的四大特征ACID

atomic consistency isolation durability

1. 原子性：不可分割的最小操作单位，要么同时成功，要么同时失败
2. 持久性：事务提交或回滚后，数据库会持久化的保存数据
3. 隔离性：多个事务之间相互独立
4. 一致性：事务操作前后，数据总量不变

### 7.3. 事务的隔离级别（了解）

多个事务操作同一批数据，会出问题：

​	1. 脏读：一个事务，读取到另一个事务中没有提交的数据
​	2. 不可重复读（虚读）：同一个事务中，两次读取到的数据不一样
​	3. 幻读：一个事务操作数据表中所有记录，另一个事务添加了一条数据，则第一个事务会查询到这个数据

隔离级别：
1. read uncommitted：会脏读、虚读、幻读
2. read committed（Oracle默认）：会虚读、幻读
3. repeatable read（MySQL默认）：幻读
4. serializable：没问题

隔离级别越高，效率越低
查询、修改隔离级别（不用记）：

```
select @@tx_isolation;
set global transaction isolation level 级别字符串;（图形化界面中重启后才能查看到生效）
```

## 8 JDBC

概念：Java DataBase Connectivity

**Java数据库连接**，Java语言操作数据库

定义的一套操作所有关系型数据库的规则，即接口。

数据库驱动：数据库厂商实现接口的jar包。

### 8.1 JDBC使用流程

步骤：
1. 下载jar包，导包
2. 注册驱动
3. 获取数据库连接对象 **Connection**
4. 定义**sql**
5. 获取执行sql语句的对象 **Statement**
6. 执行sql，接受返回结果
7. 处理结果
8. 释放资源

```
//1. 导包：建了libs文件夹，右键，add as library

//2. 注册驱动，mysql5后可以省略
Class.forName("com.mysql.jdbc.Driver");

//3. 获取数据库连接对象
Connection conn = DiverManager.getConnection("jdbc:mysql://localhost:3306/db3","root","password");

//4. 定义sql语句
String sql = "update account set balance = 500 where id = "1";

//5. 获取执行sql的对象
Statement stmt = conn.createStatement();

//6. 执行sql
int count = stmt.executeUpdate(sql);

//7. 处理结果

//8. 释放资源
stmt.close();conn.close();
```

### 8.2 详解

#### 8.2.1 获取数据库连接对象：Connection

##### 8.2.1.1 DriverManager：驱动管理对象

功能：
1. 注册驱动：告诉程序应该使用哪一个数据库驱动jar
包里面有个静态方法registerDriver。有个静态代码块调用了这个方法，所以可以**直接Class,forName导包即可**。

mysql5之后的驱动jar包可以省略注册驱动的步骤

2. 获取数据库连接
```
static Connection getConnection(String url, String user, String password);
```
+ url：指定的ip端口和数据库的名称```jdbc:mysql://ip:端口/数据库名称```。如果是本机的3306端口的mysql，可以简写为```jdbc:mysql:///数据库名称```

##### 8.2.1.2 Connection：数据库连接对象

功能：

1. 获取执行sql的对象
```
Statement createStatement();
PreparedStatement prepareStatement(String sql);
```

2. 管理事务
  + 开启事务：
```
setAutoCommit(boolean autoCommit);调用该方法，参数设置成false，即开启事务
```
  + 提交事务：
```
commit()
```
  + 回滚事务：
```
rollback()
```

#### 8.2.2 sql语句执行对象：Statement/PreparedStatement

Statement：执行sql的对象

##### 8.2.2.1 执行sql的方法

```
boolean execute(String sql)
	可以执行任意的sql【了解】

int executeUpdate
	执行DML语句（insert、update、delete）、DDL语句（create、alter、drop）
	返回值：影响的行数，>0说明执行成功，否则失败

ResultSet executeQuery(String sql)
	执行DQL语句（select）
```

##### 8.2.2.1 结果集对象：ResultSet

ResultSet：结果集对象，封装查询结果

```
游标向下移动一行：
boolean next();

初始游标位于第一行之前，第一次调用后移动到第一行。当当前行已经在最后一行以下，返回false，否则为true。


获取数据：
getXxx(参数);

Xxx代表数据类型，如getInt、getString。参数包括2种：
    int：列的编号，从1开始。
    String：列的名称


遍历：
while(rs.next()){
int id = rs.getInt(1);
...
}
```

##### 8.2.2.2 PreparedStatement：执行sql的对象

SQL注入问题：在拼接sql语句的时候，有一些sql的特殊关键字参与字符串的拼接，会造成安全问题

+ 解决：使用PreparedStatement

+ 预编译的SQL：参数使用```?```作为占位符

步骤：

1. 导包，注册驱动，获取数据库连接对象
2. 定义sql，注意这时用```?```作为占位符
3. 获取执行sql语句的对象，注意需要传入参数```Connection.prepareStatement(String sql)```
4. 给```?```赋值：
    方法：```setXXX(参数1,参数2)```
        参数1：```?```的位置编号，从1开始
        参数2：```?```的值
5. 执行sql，接受返回结果，不需要传递sql语句
6. 处理结果，释放资源

### 8.3 写工具类案例
+ 获取src路径下的文件路径：

```
ClassLoader cl = JDBCUtils.class.getClassLoader();//随便找个类
URL r = classLoader.getResource("jdbc.properties");
String path = r.getPath();
```

### 8.4 JDBC控制事务

使用Connection对象管理事务

### 8.5 数据库连接池DataSource

概念：存放数据库连接的容器（集合）。

+ 系统初始化好后，容器被创建，容器中会申请一些连接对象。用户访问数据库时，从容器中获取连接对象，访问完后，连接对象归还给容器。

+ 好处：
节约资源，访问高效。

+ 实现：
1. 标准接口：```DataSource``` ```javax.sql```包下的。
    方法：
        获取连接：```getConnection()```
        归还连接：调用```Connection.close()```表示归还连接

2. 数据库厂商实现
    1. C3P0：
    2. Druid：阿里巴巴，德鲁伊

#### 8.5.1 C3P0

步骤：
1. 导入jar包（3个，包括一个数据库驱动包）
2. 定义配置文件：```c3p0.properties或者c3p0-config.xml```，路径放置在src目录下即可【要在classpath的最顶层】
3. 创建核心对象：数据库连接池对象ComboPooledDataSource
4. 获取连接：getConnection

连接池参数：
初始化申请的连接数
最大的连接数量
超时时间

ComboPooledDataSource();可以传入一个字符串参数，可以使用别的配置

#### 8.5.2 Druid

步骤：
1. 导入jar包（1个+数据库驱动）
2. 定义配置文件：可以用.properties，可以叫任意名称，可以放在任意目录下
```
driverClassName=com.mysql.jdbc.Driver
url=jdbc:mysql://localhost:3306/learn
username=root
password=root
initialSize=5
maxActive=10
maxWait=3000
```
3. 获取数据库连接池对象：通过工厂类```DruidDataSourceFactory```来获取
4. 获取连接：getConnection

```
//加载配置文件
Properties pro = new Properties();
InputStream is = DruidDemp.class.getClassLoader().getResourceAsStream("wenjianming.properties");
pro.load(is);

//获取连接池，获取连接
DataSource sc = DruidDataSourceFactory.createDataSource(pro);
Connection conn = ds.getConnection();
```

### 8.6 Spring JDBC

Spring框架对JDBC的简单封装，提供了一个JDBCTemplate对象简化JDBC的开发。

步骤：
1. 导包
2. 创建JDBCTemplate对象，依赖于数据源DataSource

```
JdbcTemplate template = new JdbcTemplate(传入一个连接池);
```
3. 调用方法进行CRUD：

```
update()执行DML语句，增删改，sql语句里可以用？占位

queryForMap()查询结果，结果封装为map集合。只能查询1条记录
queryForList()查询结果，结果封装为list集合，list集合里的元素是Map，对应一条记录

query()查询结果，结果封装为JavaBean对象
queryForObject(sql,A.class)查询结果，结果封装为A的对象//这句在实际时候的时候有问题，别传A.class，传new BeanPropertyRowMapper<T>(T.class)


注意：
query()方法传入的第二个参数：
是一个接口：RowMapper，可以自己实现，返回一个需要的JavaBean对象，也可以用现成的
new BeanPropertyRowMapper<T>(T.class)
注意这里的JavaBean的变量都用包装类定义，不然null传入的时候会报错
```

Ctrl+P显示需要传入的参数

## 9 Web概念概述

JavaWeb：使用Java语言开发基于互联网的项目，或开发互联网相关的java技术。

### 9.1软件架构

+ C/S：
  + 优点：用户体验好
  + 缺点：开发、安装、部署、维护 麻烦

+ B/S：
  + 优点：开发、安装、部署、维护 简单
  + 缺点：对硬件要求高，应用过大用户体验会很差

### 9.2 B/S架构资源分类

#### 9.2.1 静态资源

使用静态网页开发技术发布的资源。

特点：
+ 所有用户访问，得到的结果是一样的
+ 如：文本，图片，音频，视频，HTML，CSS，JavaScript
+ 如果用户请求的是静态资源，那么服务器会直接将静态资源发送给浏览器。浏览器中内置了静态资源的解析引擎，可以展示静态资源

#### 9.2.2 动态资源

使用动态网页技术发布的资源，

特点：
+ 所有用户访问，得到的结果可能不一样
+ 如：jsp/servlet，php，asp...
+ 如果用户请求的是动态资源，那么服务器会执行动态资源，转换为静态资源后，发送给浏览器

#### 9.2.3 静态资源内容

学习动态资源，要先学习静态资源

静态资源有：
+ HTML：用于搭建基础网页，展示页面的内容
+ CSS：用于美化页面，布局页面
+ JavaScript：控制页面的元素，让页面有一些动态的效果

## 15 XML

### 15.1 概念

+ Extensible Markup Language 可扩展标记语言
+ 可扩展：标签都是自定义的。

+ 功能：存储数据
  1. 配置文件
  2. 在网络中传输

+ 与html的区别
  1. xml的标签是自定义的，html是预定义
  2. xml语法严格，html语法松散
  3. xml存储数据，html展示数据

### 15.2 语法

#### 15.2.1 基本语法

1. xml文档的后缀名：.xml
2. xml第一行必须定义为文档声明【空行都不行】
3. xml文档中有且仅有一个根标签
4. 属性值必须用引号（单双均可）引起来
5. 标签必须正确关闭
6. xml标签名称区分大小写

#### 15.2.2 组成部分

1. 文档声明
```
<?xml 属性列表 ?>
```
属性列表
```
version
	版本号，写1.0。必须写的

encoding
	编码方式。告诉解析引擎当前文档使用的字符集，默认值ISO-8859-1【IDE会自己识别，写上就行】

standalone
	是否独立。可以不设置，现在很多yes也可以依赖
    yes
    	不依赖其他文件
    no
    	以来其他文件
```

2. 指令（了解）：结合CSS的

3. 标签：名称自定义
   规则：名称可以包含字母、数字、其他字符。不能以数字或标点开始，不能以xml开始，不能包含空格

4. 属性：
   id属性值唯一

5. 文本
   CDATA区：该区域的字符会原样展示。
```
<![CDATA[展示的数据]]>
```

#### 15.2.3 约束：规定xml文档的书写规则

作为框架的使用者：
1. 能够在xml中引入约束文档
2. 能够简单的读懂约束文档

分类：
1. DTD：一种简单的约束技术
2. Schema：一种复杂的约束技术

##### 15.2.3.1 DTD

引入DTD文档到xml文档中

内部dtd：将约束规则定义在xml文档中
外部dtd：将约束的规则定义在外部的dtd文件中

本地：
```
<!DOCTYPE 根标签名 SYSTEM “dtd文件的位置”>
```
网络：
```
<!DOCTYPE 根标签名 SYSTEM “dtd文件名字” “dtd文件的位置URL”>
```

##### 15.2.3.2 Schema

后缀：xsd
引入：不用自己写，能看懂就行

1. 填写xml文档的根元素
2. 引入xsi前缀
3. 引入xsd文件命名空间
4. 为每一个xsd约束声明一个前缀作为表示
```
<students xmlin:xsi="..."					//2
    xmlns="..."								//默认前缀
    xsi:schemaLocation="命名空间 路径"		//3
    xmlns:a = "命名空间"					//取前缀，4
>
```

### 15.3 解析

操作xml文档，将文档中的数据读取到内存中

+ 操作xml文档
  1. 解析（读取）：将文档中的数据读取到内存中
  2. 写入：将内存中的数据保存到xml文档中。持久化的存储

+ 解析xml的方式：

  1. DOM：将标记语言文档一次性加载进内存，在内存中形成一棵dom树
      优点：操作方便，可以对文档进行CRUD的所有操作
      缺点：占内存

  2. SAX：逐行读取，基于事件驱动的。
      优点：不占内存
      缺点：只能读取，不能增删改

+ xml常见的解析器：
  1. JAXP：sun公司提供的解析器，支持dom和sax两种思想。不好用，没人用
  2. DOM4J：一款非常优秀的解析器
  3. Jsoup：本身是解析HTML的。
  4. PULL：安卓内置的解析器，sax方式。

#### 15.3.1 Jsoup

##### 15.3.1.1 快速入门

步骤：
1. 导入jar包
2. 获取Document对象
3. 获取对应的标签，Element对象
4. 获取数据

##### 15.3.1.2 对象的使用

1. Jsoup：工具类，可以解析html或xml文档，返回Document。
   parse方法：
```
parse(File in, String charsetName);解析xml或html文件

parse(String html);解析xml或html字符串

parse(URL url, int timeoutMillis);通过网络路径获取指定的html或xml的文档对象
```

2. Document：文档对象。代表内存中的dom树。
   获取Element对象。Document继承自Element
```
getElementById(String id);根据id属性的值获取唯一的element对象

getElementsByTag(String tagName);根据标签名称获取元素对象集合

getElementsByAttribute(String key);根据属性名称获取元素对象集合

getElementsByAttributeValue(String key, String value);根据对应的属性名和属性值获取元素对象集合
```

3. Elements：元素Element对象的集合。可以当做```ArrayList<Element>```来使用

4. Element：元素对象
   + 获取子元素对象：上面那4个方法
   + 获取属性值
```
String attr(String key);根据属性名称获取属性值
```
   + 获取文本内容
```
String text();获取所有子标签的纯文本内容

String html();获取标签体的所有内容（包括子标签的文本和标签）
```
5. Node：节点对象
    Document和Element的父类

##### 15.3.1.3 快捷查询方式

1. selector：选择器
使用的方法：
```
Elements select(String cssQuery);cssQuery：css选择器
```
定义在Element里，一般用Document调用
参考Selector类中定义的语法

2. XPath：XML路径语言，用来确定XML文档中某部分位置的语言
使用Jsoup的XPath需要额外导入jar包
查询w3cSchool参考手册，使用Xpath的语法完成查询

## 16 Web服务器软件

+ 服务器：安装了服务器软件的计算机

+ 服务器软件：接受用户的请求，处理请求，做出响应

+ web服务器软件：接受用户的请求，处理请求，做出响应

+ 在web服务器软件中，可以部署web项目，让用户通过浏览器来访问这些项目
  也被称为web容器，动态资源要在里面运行

### 16.1 常见的java相关的web服务器软件

+ webLogic：Oracle，大型JavaEE服务器，支持所有的JavaEE规范，收费

+ webSphere：IBM公司，大型JavaEE服务器，支持所有的JavaEE规范，收费

+ JBOSS：JBOSS公司，大型JavaEE服务器，支持所有的JavaEE规范，收费

+ Tomcat：Apache基金组织，中小型的JavaEE服务器，仅仅支持少量的JavaEE规范servlet/jsp。开源免费

### 16.2 JavaEE介绍

JavaEE：Java语言在企业级开发中使用的技术规范的总和，一共规定了13项大的规范。

### 16.3 Tomcat简介

+ Tomcat：web服务器软件

1. 下载：官网
2. 安装：解压，建议目录不要有中文和空格
3. 卸载：删除目录即可
4. 启动：startup。
    可能遇到的问题：

   + 黑窗口一闪而过【没有正确配置JAVA_HOME环境变量】

   + 启动报错【端口被占用。netstat -ano查看占用的进程。改自己的端口：conf/server.xml】
5. 关闭：bin/shutdown.bat或ctrl+c【这个也是正常关闭】
6. 配置：
   部署项目的方式：

   + 直接将web项目放在webapps目录下即可。
    项目的访问路径/虚拟目录：和项目名称一致
   简化部署：war包直接放到webapps里，会自动解压，删除war包也会自动删除
   + 配置conf/server.xml
    在host标签体中配置```<Context docBase="项目路径" path="虚拟目录" />```
   + 在conf/Catalina/localhost里创建任意名称xml文件。
    在文件中写```<Context docBase="项目路径" />```。现在虚拟目录就是xml文件的名称【推荐】【热部署，不用重启服务器】

#### 16.3.1 目录结构

##### 16.3.1.1 java动态项目的目录结构
```
--项目的根目录
--WEB-INF目录：
    --web.xml：web项目的核心配置文件
    --classes目录：放置字节码文件的目录
    --lib目录：放置依赖的jar包
```

+ Tomcat默认端口：8080
+ 一般会修改成80，HTTP默认的端口号
+ https是443


##### 16.3.1.2 Tomcat的目录结构

bin：可执行文件
conf：配置文件
lib：依赖jar包
logs：日志文件
temp：临时文件
webapps：存放web项目
work：存放运行时的数据

#### 16.3.2 IDEA与tomcat

+ Tomcat集成到IDEA中，并创建JavaEE项目
菜单栏--Run--Edit Configurations...--Default--Tomcat Server--Local：Application server，Configure

+ 新建：Java Enterprise
选servlet3.1，选Java EE 7。下面选中Web Application

+ 修改配置：
Run--Edit Configurations--Tomcat Server -- Tomecat 8.5.31：On update action和On frame deactivation，都改为Update resources

另外：

1. IDEA会为每一个tomcat部署的项目单独建立一份配置文件
    查看控制台的log：Using CATALINA_BASE： “C：......”
    有个路径，这个路径就是
2. 工作空间项目 和 tomcat部署的web项目
    tomcat真正访问的是  tomcat部署的web项目【out文件夹里】，“ tomcat部署的web项目”对应着“工作空间项目”的web目录下的所有资源
    WEB-INF目录下的资源不能被浏览器直接访问
3. 断点调试：使用debug启动

## 17 Servlet

+ 概念：server applet，运行在服务器端的小程序
+ servlet就是一个接口，定义了Java类被浏览器访问到（tomcat识别）的规则
+ 将来我们自定义一个类，实现servlet接口，复写方法。

### 17.1 快速入门

1. 创建JavaEE项目
2. 定义一个类，实现Servlet接口：implements Servlet
3. 实现接口中的抽象方法：在service里写一句话【每次刷新都会运行一下】
4. 配置servlet：WEB-INF里的web.xml里，写：
```
<servlet>
    <servlet-name>demo1名字</servlet-name>
    <servlet-class>全类名</servlet-class>
</servlet>

<servlet-mapping>
    <servlet-name>demo1</servlet-name>
    <url-pattern>/资源路径<url-pattern>
</servlet-mapping>
```

+ servlet包一般起名是：com.xxx.web.servlet

+ 每个项目都可以起一个虚拟目录

### 17.2 servlet执行原理

1. 当服务器接收到客户端浏览器的请求后，会解析请求URL，获取访问的Servlet的资源路径
2. 查找web.xml，是否有对应的```<url-pattern>```标签体内容
3. 如果有，找到对应的```<servlet-class>```全类名
4. tomcat会将字节码文件加载进内存，并且创建其对象
5. 调用其方法

### 17.3 Servlet的生命周期：

#### 17.3.1. 被创建：执行init方法，只执行一次

默认情况下，第一次被访问时，Servlet被创建

可以配置执行Servlet的创建时机。
```
<servlet>
    ...
    <load-on-startup>  </load-on-startup>
</servlet>
```

+ 上面这个标签的值是负数：第一次访问时被创建。默认值是-1
  0或正数：服务器启动时，创建

Servlet的init方法只执行一次，说明在内存中只存在一个Servlet对象

+ 多个用户同时访问时，可能存在线程安全问题
  解决：尽量不要在Servlet中定义成员变量。即使定义了成员变量，也不要修改。

#### 17.2.2. 提供服务：执行service方法，执行多次

每次访问Servlet时，service方法都会被调用一次


#### 17.2.3. 被销毁：执行destroy方法，只执行一次

只有服务器正常关闭时，才会执行。

#### 17.2.4 Servlet要重写的方法

```
init：初始化方法。Servlet创建时，执行，只会执行一次

ServletConfig：获取ServletConfig对象，Servlet的配置对象

service：提供服务方法。每一次Servlet被访问时，执行，执行多次

getServletInfo：获取Servlet的一些信息，版本，作者等等

destroy：销毁方法，服务器正常关闭时执行，执行一次
```

### 17.3 Servlet3.0

好处：
1. 支持注解配置，可以不需要web.xml

步骤：
1. 创建JavaEE项目，选择Servlet的版本3.0【下面选择里的Web Application】以上，可以不创建web.xml
2. 定义一个类，实现Servlet接口
3. 覆写方法
4. 在类上使用@WebServlet注解，进行配置

```
@WebServlet(urlPattern="/demo")

也可以直接写
@WebServlet("/demo")
```

### 17.4 体系结构

+ Servlet：接口

+ GenericServlet：抽象类，实现了Servlet接口

+ HTTPServlet：抽象类，继承了GenericServlet

说明：

+ GenericServlet：将Servlet接口中的其他方法做了默认空实现，只将service方法作为抽象方法
  将来定义Servlet类时，可以继承GenericServlet，实现service方法即可。如果需要写别的方法，覆写就好。

+ HTTPServlet：对http协议的一种封装，简化操作【比如判断传输的方式是get还是post】
   1. 定义类继承HTTPServlet
   2. 覆写doGet/doPost方法


### 17.5 Servlet相关配置

1. urlpattern：Servlet访问路径。一个Servlet可以定义多个访问路径。
```
@WebServlet({"/1","/2","/3"})
```
2. 路径定义规则：
```
1. /xxx
2. /xxx/xxx			//如果用*通配符，优先级是最低的
3. *.do				//千万注意,前面没有/
```

## 18 HTTP
+ Hyper Text Transfer Protocol：超文本传输协议

+ 传输协议：定义了，客户端和服务器通信时，发送数据的格式

特点：

 1. 基于TCP/IP的高级协议
 2. 默认端口：80
 3. 基于请求/响应模型的：一次请求对应一次响应
 4. 无状态的：每次请求之间互相独立，不能交互数据

历史版本：
1.0：每一次请求响应都会建立新的连接
1.1：复用连接【还有很多别的区别】

### 18.1 请求消息

+ 请求消息数据格式
    请求行
    请求头
    请求空行
    请求体

#### 18.1.1 请求行

```
请求方式 请求url 请求协议/版本
GET /login.html HTTP/1.1
```

+ 请求方式：
HTTP协议有7种请求方式，常用的有2种

   + **GET**：
    1. 请求参数在请求行中，在url后
  2. 请求的url长度有限制

   + **POST**：
    1. 请求参数在请求体中
    2. 请求长度没有限制

#### 18.1.2. 请求头

```
请求头名称：请求头值1，请求头值2
```

常见请求头：

+ User-Agent：浏览器告诉服务器，浏览器的版本信息【可以在服务器端获取该信息，解决浏览器的兼容性问题】
+ Referer：告诉服务器，请求从哪里来【超链接】
  作用：        1. 防盗链;        2. 统计工作

#### 18.1.3. 请求空行

空行，分割POST请求的请求头和请求体

#### 18.1.4. 请求体（正文）

封装POST请求消息的请求参数

### 18.2 Request对象

#### 18.2.1 request对象和response对象的原理

两个对象都是由服务器tomcat创建的，我们来使用它们

+ request对象：获取请求消息
+ response对象：设置响应消息

#### 18.2.2 request对象继承体系结构

ServletRequest  -- 接口
  |  继承
HttpServlet  --接口
  |  实现
org.apache.catalina.connector.RequestFacade  --类，tomcat写的

#### 18.2.3 request功能

##### 18.2.3.1 获取请求消息

1. 获取请求行数据
```
GET /day14/demo1?name=zhangsan HTTP/1.1
```

方法：
```
String getMethod();
	获取请求方式，如GET，POST

String getContextPath();
	获取虚拟目录：/day14 【常用】

String getServletPath();
	获取Servlet路径：/demo1

String getQueryString();
	获取get方式请求参数：name=zhangsan

String getRequestURI();
	获取请求的URI：/day14/demo1 【常用】
String getRequestURL();
	获取请求的URL：http://localhost/day14/demo1

String getProtocol();
	获取协议及版本：HTTP/1.1

String getRemoteAddr();
	获取客户机的IP地址：
```

URL：统一资源定位符。
URI：统一资源标识符。范围更大

2. 获取请求头数据

方法：
```
String getHeader(String name);
	通过请求头的名称获取请求头的值，请求头不区分大小写

Enumeration<String> getHeaderNames();
	获取所有的请求头名称，后面一般不用
```
+ Enumeration：可以当做一个迭代器去使用。
```
while(headerNames.hasMoreElements()){
    String name = headerNames.nextElement();
}
```

3. 获取请求体数据

+ 请求体：只有POST请求方式，才有请求体，在请求体中封装了POST请求的请求参数

步骤：
1. 获取流对象
```
BufferedReader getReader();
	获取字符输入流，只能操作字符数据

ServletInputStream getInputStream();
	获取字节输入流，可以操作所有类型数据
```
2. 再从流对象中拿数据


##### 18.2.3.2 其他功能

**1. 获取请求参数通用方式**
```
String getParameter(String name);
	根据参数名称获取参数值【常用】

String[] getParameterValues(String name);
	获取参数值的数组，多用于复选框，参数名称相同的

Enumeration<String> getParameterNames();
	获取所有请求的参数名称

Map<String,String[]> getParameterMap();
	获取所有参数的map集合，键值对【常用】
```
中文乱码问题：
+ get方式：tomcat 8 已经解决了
+ post方式：会乱码
解决：在获取参数前，设置request的编码
```
request.setCharacterEncoding("utf-8");【干脆每次都写，以防万一】
```

**2. 请求转发：一种在服务器内部的资源跳转方式**

步骤：
1. 通过request对象获取请求转发器对象
```
RequestDispatcher getRequestDispatcher(String path);
```
2. 使用RequestDispatcher对象来进行转发
```
forward(ServletRequest request, ServletResponse response);
```

+ 特点
  1. 浏览器地址栏路径不发生变化
  2. 只能转发到当前服务器内部资源中
  3. 转发是一次请求


**3. 共享数据**
+ 域对象：一个有作用范围的对象，可以在范围内共享数据
+ request域：代表一次请求的范围，一般用于请求转发的多个资源中共享数据

方法：
```
void setAttribute(String name, Object obj);存储资源

Object getAttribute(String name);通过键获取值

void removeAttribute(String name);通过键移除键值对
```

**4. 获取ServletContext**

```
ServletContext getServletContext();
```

##### 18.2.3.3 案例

login.html中form表单的action路径的写法：
虚拟目录+Servlet的资源路径

### 18.3 BeanUtils工具类：简化数据封装

用于封装JavaBean，网上找

#### 18.3.1 JavaBean：标准的Java类

1.要求：
+ 类必须被public修饰
+ 必须提供空参的构造器
+ 成员变量必须使用private修饰
+ 提供public的setter和getter方法

2. 功能：封装数据

**一般会把JavaBean放在domain，entity这种包里。**

#### 18.3.2 属性概念

+ 成员变量
+ 属性：setter和getter方法截取后的产物。就是set后面的那段。一般和成员变量一样

#### 18.3.3 方法：
```
setProperty()

getProperty()

populate(Object obj, Map map);把map集合的键值对信息，封装到对应的JavaBean对象中
```

这些方法里传入的是属性和值

+ 意思是：
```
private bb;

public void setAa(){
    ....
}

这种情况下，要调用这3个方法，不能传bb作为名字，要传aa
```

### 18.3 响应消息

1. 请求消息：客户端发送给服务器端的数据
   数据格式：
   1. 请求行
   2. 请求头
   3. 请求空行
   4. 请求体

2. 响应消息：服务器端发送给客户端的数据
   数据格式：
   1. 响应行
   2. 响应头
   3. 响应空行
   4. 响应体

#### 18.3.1 响应行
```
协议/版本 响应状态码 状态码描述
```
+ 响应状态码：服务器告诉客户端浏览器本次请求和响应的一个状态。
  状态码都是3位数字
```
1xx：服务器接收客户端消息，但是没有接收完成，等待一段时间后，发送1xx状态码
2xx：成功。如，200
3xx：重定向。如：302重定向，304访问缓存
4xx：客户端错误。如：404请求路径没有对应的资源，405请求方式没有对应的doXxx方法
5xx：服务器端错误。如：500服务器内部出现异常
```
#### 18.3.2. 响应头

```
头名称：值
```
+ 常见的响应头：
  1. Content-Type：服务器告诉客户端本次响应体数据格式以及编码格式
  2. Content-disposition：服务器告诉客户端以什么格式打开响应体数据
      值：
      ```in-line```：默认值，在当前页面内打开
      ```attachment;filename=xxx```：以附件形式打开响应体。文件下载

#### 18.3.3. 响应空行

#### 18.3.4. 响应体

传输的数据

## 18.4 Response对象

功能：设置响应消息

### 18.4.1 设置响应行

1. 格式：HTTP/1.1 200 ok
2. 设置状态码
```
setStatus(int sc)
```

### 18.4.2 设置响应头

```
setHeader(String name, String value);
```

### 18.4.3 设置响应体

使用步骤：
1. 获取输出流
```
PrintWriter getWriter();字符输出流
ServletOutputStream getOutputStream();字节输出流
```

2. 使用输出流，将数据输出到客户端浏览器

### 18.4.4 重定向

重定向：资源跳转的方式

```
response.setStatus(302);
	设置状态码302
response.setHeader("location","/day15/demo2")

等价于：
response.sendRedirect("/day15/demo2");
```

+ 重定向的特点：redirect
  1. 地址栏发生变化
  2. 重定向可以访问其他站点（服务器）的资源
  3. 重定向是两次请求。不能使用request对象来共享数据

+ 转发的特点：forward
  1. 转发地址栏路径不变
  2. 转发只能访问当前服务器下的资源
  3. 转发是一次请求，可以使用request对象来共享数据

### 18.4.5 路径的写法

+ 相对路径：
```
./ 和 ../
找当前资源和目标资源之间的相对位置关系，注意不是本地文件里的关系，是访问时候的关系。即URL里看到的关系
```
+ 绝对路径：
```
本地可以省略ip和端口，/day15/demo2也是绝对路径
```

+ 规则：判断定义的路径给谁用？判断请求从哪里发出
   + 给客户端使用：需要加虚拟目录（项目的访问路径）
     建议虚拟目录动态获取：request.getContextPath()
     重定向
   + 给服务器使用：不需要加虚拟目录
     转发

### 18.4.6 其他

+ 服务器输出字符数据到浏览器：
  PrintWriter
  这里用write和print相关方法效果一样，因为一次请求结束后这个流就会被关闭

+ 乱码问题：
  设置响应头里的content-type。
  获取流之前设置
```
response.setContentType("text/html;charset=utf-8");
```

+ 验证码问题：
  切换验证码：onclick事件里，改变img的src，相当于重新随机一张验证码。但是有缓存问题，为了避免：
```
src = "/.../...?"+data;
```
data是时间戳，?表示传了个参数。data = new Data().getTime()

## 19 ServletContext对象

+ 概念：代表整个web应用，可以和程序（Servlet）的容器（服务器Tomcat）来通信

+ 获取：```request.getServletContext()```

+ 功能：
1. 获取MIME类型
    MIME类型：在互联网通信过程中定义的一种文件数据类型
    格式：```大类型/小类型```  如：```text/html``` ```image/jpeg```
```
String getMimeType(String file)
```
2. 域对象：共享数据
```
void setAttribute(String name, Object obj);存储资源
Object getAttribute(String name);通过键获取值
void removeAttribute(String name);通过键移除键值对
```

+ ServletContext对象范围：所有用户所有请求的数据
3. 获取文件的真实（服务器）路径
```
String getRealPath(String path)


web目录下的资源访问:
String b = context.getRealPath("/b.txt");

WEB-INF目录下的资源访问:
String c = context.getRealPath("/WEB-INF/c.txt");

src目录下的资源访问，或通过classloader:
String a = context.getRealPath("/WEB-INF/classes/a.txt");
```

### 19.1 案例

+ 弹窗下载图片
  设置响应头content-disposition【这里还设置了content-type】

+ 问题：中文文件名。
  解决：根据客户端的浏览器不同，用不同的方式编码filename【IE：URL，火狐：BASE64，这种工具类有很多，不用自己写】

## 20 会话技术

1. 会话：一次会话中包含多次请求和响应
    一次会话：浏览器第一次给服务器资源发送请求，会话建立，直到有一方断开为止。

2. 功能：在一次会话的范围内，多次请求间共享数据
3. 方式
   + 客户端会话技术：**Cookie**
   + 服务器端会话技术：**Session**

### 20.1 Cookie

概念：客户端会话技术，将数据保存在客户端

#### 20.1.1 快速入门

使用步骤：
```
new Cookie(String name, String value);	创建Cookie对象，绑定数据

response.addCookie(Cookie cookie);	发送Cookie对象

Cookie[] request.getCookies();	获取Cookie，拿到数据
```
```
cookie.getName()
cookie.getValue()
cookie.setValue()
```

#### 20.1.3. 实现原理

基于响应头```set-cookie```和请求头```cookie```实现

+ IDEA修改Servlet模板：
File -- Settings -- Editor -- File and Code Templates -- Other：Web -- Java code templates -- Servlet Annotated Class.java

#### 20.1.4. cookie的细节

1. 一次可不可以发送多个cookie？

   可以
   可以创建多个Cookie对象，然后调用多次addCookie方法

2. cookie在浏览器中保存多长时间？

   默认情况下，当浏览器关闭后，Cookie数据被销毁

   持久化存储
```
setMaxAge(int seconds)
	正数：将Cookie数据写到硬盘文件中，持久化存储。并制定cookie存活时间，时间到后，cookie文件自动失效
	负数：默认值
	零：删除cookie信息
```

3. cookie能不能存中文？

   在tomcat 8 之前，cookie中不能直接存储中文，需要编码
   在tomcat 8 之后，cookie支持中文数据，但是特殊字符还是需要编码

4. cookie共享问题
   1. 一个tomcat服务器中，部署了多个web项目
      默认情况下不能。
```
setPath(String path)；
设置cookie的获取范围。默认情况下，是当前的虚拟目录，如果要共享，设置成"/"
```

   2. 不同的tomcat服务器间cookie共享问题。默认不能
```
setDomain(String path);
如果一级域名相同，那么多个服务器间cookie可以共享。如
setDomain(".baidu.com");
```

#### 20.1.5. Cookie的特点和作用

1. cookie存储数据在客户端浏览器
2. 浏览器对于单个cookie的大小有限制（4kb）以及对同一个域名下的总cookie数量也有限制（20个）

**作用：**

1. cookie一般用于存储少量的不太敏感的数据
2. 在不登录的情况下，完成服务器对客户端的身份识别

### 20.2 Session

服务器端会话技术，在一次会话的多次请求间共享数据，将数据保存在服务器端的对象中。HttpSession

#### 20.2.1 快速入门

```
HttpSession session = request.getSession()	获取HTTPSession对象

使用HTTPSession对象
getAttribute、set、remove
```

#### 20.2.3. 原理

session的实现是依赖于Cookie的

#### 20.2.4. 细节

1. 当客户端关闭后，服务器不关闭，两次获取的session默认不是同一个
   如果需要相同，可以创建Cookie，设置键为JSESSIONID，设置值为session.getId()，设置存活时间，让cookie持久化保存

2. 客户端不关闭，服务器关闭后，两次获取的session不是同一个
   但是要确保数据不丢失，tomcat会自动完成以下工作【IDEA内不行，启动前会删掉work目录，活化不了】
   + session的钝化：
    在服务器正常关闭之前，将session对象序列化到硬盘上
   + session的活化：
    在服务器启动后，将session文件转化为内存中的session对象

3. session什么时候被销毁？
   1. 服务器关闭
   2. session对象调用方法```invalidate()```
   3. session默认失效时间：30分钟，可以在web.xml里修改

#### 20.2.5. session的特点

1. session用于存储一次会话的多次请求的数据，存在服务器端
2. session可以存储任意类型，任意大小的数据

**session和cookie的区别：**【主菜，小甜点】

1. session存储数据在服务器端，cookie在客户端
2. session没有数据大小限制，cookie有
3. session数据安全，cookie相对不安全

## 21 JSP

+ Java Server Pages：java服务器端页面
可以理解为：一个特殊的页面，其中既可以定义html标签，又可以定义java代码。
可以用于简化书写

### 21.1 原理

JSP本质上就是一个Servlet

### 21.2 JSP脚本：JSP定义Java代码的方式

```
1. <%  代码  %>：定义的java代码，在service方法中。
2. <%!  代码  %>：定义的java代码，会在jsp转换后的java类的成员位置。
3. <%=  代码  %>：会直接输出到页面上，会转换为service方法内的print的内容。
```
可以被HTML等截断，最后会被拼在一起。如：
```
<%
    ...
%> HTML<%
    ...
%>
```

### 21.3 指令

作用：用于配置JSP页面，导入资源文件

```
<%@ 指令名称 属性名1=属性值1 属性名2=属性值2 ... %>
```

#### 21.3.1 page

配置JSP页面的

contentType：等同于```response.setContentType()```

1. 设置响应体的mime类型以及字符集
2. 设置当前jsp页面的编码（高级IDE，低级工具要设置pageEncoding属性来设置当前页面的编码）

```
import：导包

errorPage：当前页面发生异常后，会自动跳转到指定的错误页面

isErrorPage：标识当前页面是否为错误页面
	true：是，可以使用内置对象exception
	false：否，默认值。不能使用内置对象exception
```
#### 21.3.2 include

页面包含的，导入页面的资源文件。可以把多个页面共同的部分抽取成一个其他的页面

```
<%@include file="top.jsp" %>
```

#### 21.3.3 taglib

导入资源

```
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
	prefix：前缀，自定义的
```

### 21.4 注释

1. html注释```<!-- -->```只能注释html代码片段，被注释的内容依旧会被写到response里
2. jsp注释```<%-- --%>```可以注释所有。

在代码里面java的注释依旧可以使用

### 21.5 内置对象

在jsp页面中不需要获取和创建，可以直接使用的对象

一共有9个内置对象：

|   变量名        |真实类型               |作用|
|---|---|---|
|    pageContext |PageContext           |域对象，当前页面共享数据，还可以获取其他八个内置对象|
|    request     |HttpServletRequest    |域对象，一次请求访问的多个资源（转发）|
|    session     |HttpSession           |域对象，一次会话的多个请求间|
|    application |ServletContext        |域对象，所有用户间共享数据，该对象唯一|
|    response    |HttpServletResponse   |响应对象|
|    page        |Object                |当前页面（Servlet）的对象，this|
|    out         |JspWriter             |输出对象，数据输出到页面上|
|    config      |ServletConfig         |Servlet的配置对象|
|    exception    |Throwable            |异常对象|

+ 注释：
out：字符输出流对象。可以将数据输出到页面上。和response.getWriter()类似
两者的区别：
在tomcat服务器真正给客户端做出响应之前，会先找response缓冲区的数据，再找out缓冲区数据。
所以response.getWriter().write()数据输出永远在out.write()之前

## 22 EL表达式

+ Expression Language 表达式语言

+ 替换和简化JSP页面中java代码的编写

```
${表达式}
```

+ 注意
   jsp默认支持el表达式。如果要忽略el表达式：
   1. 设置jsp中page指令中：```isELIgnored=“true”```忽略当前jsp页面中所有的el表达式
   2. ```\${表达式}```：忽略当前这个el表达式

在JavaScript里也可以用EL表达式

### 22.1 使用

#### 22.1.1 运算

运算符：
1. 算术运算符：其中除和取模既可以用```/,%```也可以用div和mod
2. 比较运算符
3. 逻辑运算符：```&& || ! 或 and or not```
4. 空运算符：empty
   功能：判断字符串、集合、数组对象是否为null或长度为0```${empty list}只有当list为null或长度为0的时候返回true``````${not empty list}```

#### 22.1.2 获取值

el表达式只能从域对象中获取值

1. 从指定域中获取指定键的值
```
${域名称.键名}
```
域名称：
+ pageScope					-->pageContext
+ requestScope				-->request
+ sessionScope				-->session
+ applicationScope			-->application（ServletContext）

举例：在request域中存储了name=张三，获取：```${requestScope.name}```如果获取不到显示空字符串，不会报错

2. 依次从最小的域中查找是否有该键对应的值，直到找到为止。
```
${键名}
```

3. 获取对象、List集合、Map集合的值
```
${域名称.键名.属性名}
	对象。
	本质上会去调用对象的getter方法。
	逻辑视图：可以在类里定义一个getXxx方法来格式化一些属性的输出。

${域名称.键名[索引]}
	List集合

${域名称.键名.key名称}
${域名称.键名["key名称"]}
	Map集合
```


#### 22.1.3. 隐式对象

el表达式中有11个隐式对象，这里只学一个**pageContext**

功能：
1. 获取jsp其他8个内置对象【直接点，相当于get属性】
2. 动态获取虚拟目录
```
${pageContext.request.contextPath}
```

## 23 JSTL

+ JavaServer Pages Tag Library JSP标准标签库
  是由Apache组织提供的开源的免费的jsp标签
+ 作用：用于简化和替换JSP页面上的java代码

### 23.1 使用步骤：

1. 导入jstl相关jar包
2. 引入标签库：taglib指令
```
<%@ taglib %>
```
3. 使用标签

### 23.2 常用的JSTL标签

1. if
+ 属性：
  test 必须属性，接受boolean表达式
  如果表达式为true，则显示if标签体内容，如果为false，则不展示
  一般情况下，test属性值会结合el表达式一起使用

+ 注意
  ``c:if``标签没有else情况，想要else，可以再定义一个```c:if```标签

2. choose
使用choose标签声明
when标签判断
otherwise标签做其他情况的声明
```
<c:choose>
    <c:when test="${n == 1}">星期一...</c:when>
    ...
</c:choose>
```
3. foreach
+ 循环属性
```
begin：开始值，包括
end：结束值，包括
var：临时变量
step：步长
varStatus：循环状态对象
    index：索引，此时与var的数相同
    count：循环次数，从1开始
```
+ 遍历属性
```
items：容器对象
var：容器中元素的临时变量
varStatus：循环状态对象
    index：索引，从0开始
    count：循环次数，从1开始
```

## 24 MVC：开发模式

MVC：
1. M：Model，模型。JavaBean
完成具体的业务操作，如：查询数据库，封装对象

2. V：View，视图。JSP
展示数据

3. C：Controller，控制器。Servlet
获取用户的输入
调用模型
将数据交给视图进行展示

## 25 三层架构：软件设计架构

1. 界面层（表示层）：用户看得到的界面。用户可以通过界面上的组件和服务器进行交互。【Servlet接受用户参数，封装处理，调用业务逻辑层完成处理，转发JSP页面完成显示】
2. 业务逻辑层（service层）：处理业务逻辑。【组合DAO层的简单方法，形成复杂的功能】
3. 数据访问层（dao层Data Access Object）：操作数据存储文件

## 26 大案例中的一点东西

获取复选框的内容：把复选框用form包裹起来，然后提交的时候会将选中的部分传参【记得设置value】
获取的form对象（Element）后，有方法submit()，表示表单提交

## 27 Filter：过滤器

+ javaweb的三大组件：Servlet、Filter、Listener

+ web中的过滤器：当访问服务器的资源时，过滤器可以将请求拦截下来，完成一些特殊功能。

+ 过滤器的作用：
一般用于完成通用的操作。如：登录验证、统一编码处理、敏感字符过滤...

### 27.1 快速入门

1. 定义一个类，实现接口Filter【javax.servlet】
2. 复写方法
3. 配置拦截路径
+ web.xml
```
<filter>
    <filter-name>demo1</filter-name>
    <filter-class>全类名</filter-class>
</filter>
<filter-mapping>
    <filter-name>demo1</filter-name>
    <url-pattern>拦截路径</url-pattern>
</filter-mapping>
```
+ 注解
```
@WebFilter("/*")

在doFilter里
chain.doFilter(req,resp) //放行

可以像改Servlet模板一样更改模板
```

### 27.2 细节

#### 27.2.1 过滤器执行流程

1. 执行过滤器
2. 执行放行后的资源
3. 回来执行过滤器放行代码下边的代码

#### 27.2.2 过滤器生命周期方法

1. init：在服务器启动后，会创建Filter对象，然后调用init方法，只执行一次。用于加载资源
2. doFilter：每一次请求被拦截资源时，会执行。执行多次
3. destroy：在服务器关闭后，Filter对象被销毁。如果服务器是正常关闭，则会执行destroy方法。只执行一次。用于释放资源

#### 27.2.3 过滤器配置详解

#### 27.2.3.1 拦截路径配置：

1. 具体资源路径：```/index.jsp```	只有访问index.jsp资源时，过滤器才会被执行
2. 拦截目录：```/user/*```	访问/user下的所有资源时，过滤器都会被执行
3. 后缀名拦截：```*.jsp```	访问所有后缀名为jsp资源时，过滤器都会被执行
4. 拦截所有资源：```/*```	访问所有资源时，过滤器都会被执行

#### 27.2.3.2 拦截方式配置：

1. 注解配置
设置dispatchTypes属性【可以传入数组】
   + REQUEST：默认值。浏览器直接请求资源
   + FORWARD：转发访问资源
   + INCLUDE：包含访问资源【没讲】
   + ERROR：错误跳转资源【没讲】
   + ASYNC：异步访问资源【没讲】

2. web.xml配置
设置```<dispatcher></dispatcher>```标签即可【在```<filter-mapping>```里】

### 27.3 过滤器链（配置多个过滤器）

+ 执行顺序：如果有两个过滤器：过滤器1和过滤器2
   1. 过滤器1
   2. 过滤器2
   3. 资源执行
   4. 过滤器2
   5. 过滤器1

+ 过滤器先后顺序问题：
   1. 注解配置：按照类名的字符串比较规则比较，值小的先执行
        如：AFilter和BFilter，AFilter先执行
   2. web.xml配置：```<filter-mapping>```谁定义在上边，谁先执行

### 27.4 案例

+ 登录验证

1. 要先判断是否是登录相关的页面。
2. 要获取资源请求路径
3. 先对request进行强制转型：HttpServletRequest

+ 敏感词过滤

增强对象的功能：用设计模式

## 28 代理模式

设计模式：一些通用的解决固定问题的方式

解决敏感词过滤问题可以用到的两种设计模式：装饰模式和代理模式


### 28.1 概念

+ 真实对象：被代理的对象
+ 代理对象
+ 代理模式：代理对象代理真实对象，达到增强真实对象功能的目的

### 28.2 实现方式：

+ 静态代理：有一个类文件描述代理模式
+ 动态代理：在内存中形成代理类

+ 实现步骤：
   1. 代理对象和真实对象实现相同的接口
   2. 代理对象 = Proxy.newProxyInstance();
   3. 使用代理对象调用方法
   4. 增强方法

+ 增强方式：
   1. 增强参数列表
   2. 增强返回值类型
   3. 增强方法体执行逻辑


### 28.3 动态代理

1. 创建真实对象
2. 动态代理增强真实对象

#### 28.3.1 创建代理对象

```
Proxy.newProxyInstance()
```
传入三个参数：固定写法
1. 类加载器
2. 接口数组
3. 处理器

```
真实对象接口 代理对象 =(真实对象接口)Proxy.newProxyInstance(req.getClass().getClassLoader(), req.getClass().Interface， new InvocationHandler(){
	@Override
	public Object invoke(Object proxy, Method method, Object[] args) throws Trowable{
		Object obj = method.invoke(真实对象，args)
		return obj;
	}
})
```
#### 28.3.2 invoke方法

```
@Override
	public Object invoke(Object proxy, Method method, Object[] args) throws Trowable{
		Object obj = method.invoke(真实对象，args)
		return obj;
	}
```

+ 代理逻辑部分：代理对象调用的所有方法都会触发该方法执行
+ 参数：
   1. proxy：代理对象
   2. method：代理对象调用的方法，被封装为的对象
   3. args：代理对象调用的方法，传递的实际参数

#### 28.3.3 代理对象调用方法

在一个Filter里的doFilter写：

1. 建个代理，返回代理对象为proxy_req，然后放行的时候传proxy_req进去。
2. 代理内部：
   + 判断方法是否是xxx方法【getParameter/getParameterMap/getParameterValue】
   + 获取返回值
   + 替换返回值
```
ServletRequest proxy_req = (ServletRequest) Proxy.newProxyInstance(req.getClass().getClassLoader(), req.getClass().Interface， new InvocationHandler(){

	@Override
	public Object invoke(Object proxy, ...){

    	method.getName().equals(...);	//判断方法名

        String value = (String) method.invoke(req,args);	//获取返回值

		//替换返回值
        if(value != null){
            for(String str :list){
                if(value.contains(str)){
                    value = value.replaceAll(str,"***");
                }
            }
        }

        return value;
	}

})
```

#### 28.3.4 在init里加载资源

```
ServletContext servletContext = config.getServletContext()

String realPath = servletContext.getRealPath("WEB-INF/classes/敏感词汇.txt")//txt是GBK的

BufferedReader br = new BufferedReader(new FileReader(realPath));//本地的流，默认GBK的流

String line = null;
while((line=br.readLine())!=null){
	list.add(line);//list定义在外面
}

br.close();
```

## 29 Listener：监听器

web的三大组件之一

### 29.1 事件监听机制

+ 事件：一件事情
+ 事件源：事件发生的地方
+ 监听器：一个对象
+ 注册监听：将事件、事件源、监听器绑定在一起。当事件源上发生某个事件后，执行监听器代码

### 29.2 ServletContextListener

+ ServletContextListener：监听ServletContext对象的创建和销毁

方法：
```
void contextDestroyed(ServletContextEvent sce)：ServletContext对象被销毁之前会调用该方法【ServletContext对象服务器正常关闭后自动销毁】

void contextInitialized(ServletContextEvent sce)：ServletContext对象创建后会调用该方法。【ServletContext对象服务器启动后自动创建】
```

#### 29.2.1 步骤

1. 定义一个类，实现ServletContextListener接口
2. 覆写方法
3. 配置
+ web.xml
```
    <listener>
        <listener-class>全类名</listener-class>
    </listener>
```
+ 注解
```
@Listener
	不需要指定路径，直接写一个注解就行了
```

#### 29.2.2 作用

+ 主要用于加载资源文件

在web.xml里指定初始化参数：
```
<context-param>
	<param-name>contextConfigLocation变量名</param-name>
	<param-value>/WEB-INF/... 路径</param-value>
</context-param>
```

+ ```servletContextEvent.getServletContext()```可以获得```ServletContext```对象

+ ````servletContext.getInitParameter(contextConfigLocation)```获取一个值

+ 然后用getRealPath方法可以获取真实路径

+ 然后就用流加载进内存

+ 一般这样来加载全局的资源

+ 框架基本上都实现了，以后不用自己写，用就行

## 30 JQuery

+ 一个JavaScript框架。简化JS开发。
+ JavaScript框架：本质上就是一些JS文件，封装了JS的原生代码

jQuery是一个快速、简洁的JavaScript框架，是继Prototype之后又一个优秀的JavaScript代码库（或JavaScript框架）。jQuery设计的宗旨是“write Less，Do More”，即倡导写更少的代码，做更多的事情。它封装JavaScript常用的功能代码，提供一种简便的JavaScript设计模式，优化HTML文档操作、事件处理、动画设计和Ajax交互。

### 30.1 快速入门

1. 下载JQuery
   + 目前JQuery有三个大的版本
      1.x：使用最广，兼容ie678，不再更新
      2.x：没人用了，不再更新
      3.x：不兼容ie678，只支持最新的浏览器。主要维护版本【用的这个】
   + 带min和不带min：不带min的只有一行，缩小体积，加载更快
2. 导入JQuery的js文件
3. 使用：```$(选择器)```【EL表达式是大括号{}】

获得对象后，获取html内容：```$(选择器).html()```
```JS：innerHTML```

### 30.2 JQuery对象和JS对象区别与转换

1. JQuery对象在操作时，更加方便
2. JQuery对象和JS对象方法不通用
3. 两者相互转换
   JQuery -->js：```jq对象[索引]```或者```jq对象.get(索引)```
   js -->JQuery：```$(js对象)```

### 30.3 选择器：筛选具有相似特征的元素（标签）

#### 30.3.1 基本语法学习

1. 事件绑定
```
$("#button").click(function(){...})
```

2. 入口函数
```
$( funtion(){

} )
```
+ dom文档加载完成之后执行该函数中的代码
+ 相当于```window.onload = function(){...}```
+ 区别：```window.onload```只能写一个，多个会覆盖；``` $( funtion )```可以写多个

3. 样式控制
```
$("#id").css("background-color","red")
$("#id").css("backgroundColor","red")//这个按住ctrl，backgroundColor上会有小手，如果写错就没有
```

#### 30.3.2 基本选择器

1. 标签选择器
```
$("html标签名") 		获得所有匹配标签名称的元素
```
2. id选择器
```
$("#id的属性值")		获得与指定id属性值匹配的元素
```
3. 类选择器
```
$(".class的属性值")		获得与指定的class属性值匹配的元素
```
4. 并集选择器
```
$("选择器1,选择器2,...")
```

#### 30.3.3 层级选择器

1. 后代选择器
```
$("A B ")			选择A元素内部的所有B元素【包括孙子等等】
```
2. 子选择器
```
$("A > B")			选择A元素内部的所有B子元素【只有儿子】
```

#### 30.3.2.4 属性选择器

1. 属性名称选择器
```
$("A[属性名]")			包含指定属性的选择器
```
2. 属性选择器
```
$("A[属性名='值']")		包含指定属性等于指定值的选择器
    !=：属性不等于和不包含该属性的
    ^=：属性以某些值开始
    $=：属性以某些值结尾
    *=：属性包含某些值
```
3. 复合属性选择器
```
$("A[属性名='值'][]...")		包含多个属性条件的选择器
```

#### 30.3.2.5 过滤选择器

1. 首元素选择器
```
:first					获得选择的元素中的第一个元素 $("div:first")
```
2. 尾元素选择器
```
: last					获得选择的元素中的最后一个元素
```
3. 非元素选择器
```
:not(selector)			不包括指定内容的元素
```
4. 偶数选择器
```
:even					偶数，从0开始计数
```
5. 奇数选择器
```
:odd					奇数，从0开始计数
```
6. 等于索引选择器
```
:eq(index)				指定索引元素
```
7. 大于索引选择器
```
:gt(index)				大于指定索引元素
```
8. 小于索引选择器
```
:lt(index)				小于指定索引元素.
```
9. 标题选择器
```
:header					获得标题（h1~h6）元素，固定写法
```

#### 30.3.2.6 表单过滤选择器

1. 可用元素选择器
```
:enabled				获得可用元素
```
2. 不可用元素选择器
```
:disabled				获得不可用元素
```
3. 选中选择器
```
:checked				获得单选/复选框选中的元素
```
4. 选中选择器
```
:selected				获得下拉框选中的元素
```

+ val()方法，相当于JS的value属性，改变值

+ 下拉列表select选中个数的获取，注意要用option：
```$("#job > optiion:selected").length```

### 30.4 DOM操作

#### 30.4.1 内容操作

```
html()
	获取/设置元素的标签体内容
	<a><font>内容</font></a> --> <font>内容</font>

text()
	获取/设置元素的标签体纯文本内容
	<a><font>内容</font></a> --> 内容

val()
	获取/设置元素的value属性值
```

+ 设置时，往里传参。text设置的时候和html一样，都会把最外层标签里面的全替换掉

#### 30.4.2 属性操作

##### 3.4.2.1 通用属性操作
```
attr()
	获取/设置元素的属性

removeAttr()
	删除属性

prop()
	获取/设置元素的属性

removeProp()
	删除属性
```

+ 设置时传2个参数

+ 其中attr和prop的区别：
   1. 如果操作的是元素的固有属性，则建议使用prop【checkBox的checked和option的selected用attr获取不到】
   2. 如果操作的是元素的自定义的属性，则建议使用attr

##### 3.4.2.2 对class属性操作
```
addClass()
	添加class属性值

removeClass()
	删除class属性值

toggleClass()
	切换class属性值【存在则删除，不存在则添加】

css()
	设置css
```

#### 30.4.3 CRUD操作【移动】

```
append()
	父元素将子元素追加到末尾
    对象1.append(对象2)：将对象2添加到对象1元素内部，并且在末尾

prepend()
	父元素将子元素追加到开头
    对象1.prepend(对象2)：将对象2添加到对象1元素内部，并且在开头

appendTo()
    对象1.appendTo(对象2)：将对象1添加到对象2元素内部，并且在末尾

prependTo()
    对象1.prepenTo(对象2)：将对象1添加到对象2元素内部，并且在开头



after()
	添加元素到元素后边
    对象1.after(对象2)：将对象2添加到对象1后边。对象1和对象2是兄弟关系

before()
	添加元素到元素前边
    对象1.before(对象2)：将对象2添加到对象1前边。对象1和对象2是兄弟关系

insertAfter()
    对象1.insertAfter(对象2)：将对象1添加到对象2后边。对象1和对象2是兄弟关系

insertBefore()
    对象1.insertBefore(对象2)：将对象1添加到对象2前边。对象1和对象2是兄弟关系



remove()
	移除元素
    对象.remove()：将对象删除掉

empty()
	清空元素的所有后代元素
    对象.empty()：将对象的后代元素全部清空，但是保留当前对象以及其属性节点

clone()
	复制一个
```

### 30.5 动画

有三种方式显示和隐藏元素

#### 30.5.1 默认显示和隐藏方式

```
show([speed,[easing],[fn]])
    参数：
    1. speed：动画的速度。三个预定义的值（“slow”，“normal”，“fast”）或表示动画时长的毫秒数值（如：1000）
    2. easing：用来指定切换效果，默认是“swing”，可用参数“linear”
       swing：动画执行时速度是 先慢，中间快，最后又慢
       linear：动画执行时速度是匀速的
    3. fn：在动画完成时执行的函数，每个元素执行一次

hide([speed,[easing],[fn]])

toggle([speed,[easing],[fn]])
```

#### 30.5.2 滑动显示和隐藏方式

```
slideDown([speed,[easing],[fn]])

slideUp([speed,[easing],[fn]])

slideToggle([speed,[easing],[fn]])
```

#### 30.5.3 淡入淡出显示和隐藏方式

```
fadeIn([speed,[easing],[fn]])

fadeOut([speed,[easing],[fn]])

fadeToggle([speed,[easing],[fn]])
```

### 30.6 遍历

#### 30.6.1 js的遍历方式

```
for(初始化值;循环结束条件;步长)
```

#### 30.6.2 jq的遍历方式

1. **```jq对象.each(callback)```**
```
jQuery对象.each(function(index,element){});
    index：元素在集合中的索引
    element：集合中的每一个元素对象

    this：集合中的每一个元素对象【JS对象】前两个可以一起不写

    回调函数返回值
        true：如果当前function返回false，则结束循环。break
        false：如果当前function返回true，continue
```
2. **```$.each(Object,[callback])```**
```
$.each(Object,[callback])
```
3. **```for...of```**

```
for(元素对象 of 容器对象)
	jquery3.0版本之后提供的方式
```

### 30.7 事件绑定

#### 30.7.1 jQuery标准的绑定方式

```
jq对象.事件方法(回调函数);
```
+ 注：如果调用事件方法，不传递回调函数，则会触发浏览器默认行为。
```
表单对象.submit();//让表单提交
```

#### 30.7.2. on绑定事件/off解除绑定

```
    jq对象.on("事件名称",回调函数)
    jq对象.off("事件名称")
        如果off方法不传递任何参数，则将组件上的所有事件全部解锁
```

#### 30.7.3. 事件切换：toggle

```
jq对象.toggle(fn1,fn2...)
    当单击jq对象对应的组件后，会执行fn1，第二次点击会执行fn2...

注意：1.9版本删除了该方法，使用JQuery Migrate插件可以恢复此功能
```

### 30.8 插件：增强JQuery的功能

1. **```$.fn.extend(object)```**
```
$.fn.extend({
    方法名:function(){
        this：调用该方法的jq对象
    },
    方法名2...
})

增强通过JQuery获取的对象的功能
调用：
    jq对象.方法名
```
2. **```$.extend(object)```**
```
$.extend(object)

增强JQuery对象自身的功能 对$或JQuery对象增强，全局方法
调用：
    $.方法名
```

## 31 AJAX

+ Asynchronous Javascript And XML 异步的JavaScript 和 XML

### 31.1 异步和同步：客户端和服务器端相互通信的基础上

+ 同步：客户端必须等待服务器端的响应。在等待的期间客户端不能做其他操作
+ 异步：客户端不需要等待服务器端的响应。在服务器处理请求的过程中，客户端可以进行其他的操作

+ AJAX：无需重新加载整个网页的情况下，能够更新部分网页的技术。

### 32.2 实现方式

+ 原生的JS实现方式【了解，不用，可以看w3school的文档，859集】

+ JQuery实现方式

#### 32.2.1 ```$.ajax()```

```
function fun(){ //绑定的按钮的单击事件的函数

	$.ajax({
		url:"ajaxServlet",//请求路径

		type:"POST",//请求方式

		data:"username=a&age=1",//请求参数写法1
		data:{"username":"jack","age":23},//请求参数写法2，JSON，推荐

		success:function(data){
			data：定义一个形参，名字无所谓，可以接受返回值
		},//响应成功后的回调函数

		error:function(){
			...
		},//请求响应出现错误，会执行的回调函数

		dataType:"text"//设置接收到的相应数据的格式
	});

}
```

#### 32.2.2 ```$.get()```

```
$.get(url,[data],[callback],[type])
    参数：
        url：请求路径
        data：请求参数
        callback：回调函数
        type：响应结果的类型
```

#### 32.2.3 ```$.post()```

```
$.post(...)
```

## 32 JSON

+ JavaScript Object Notation	JavaScript对象表示法
+ json现在多用于存储和交换文本信息的语法
+ 进行数据的传输
+ JSON比XML更小、更快、更易解析

### 32.1 语法

#### 32.1.1 基本规则

+ 数据在名称/值对中：json数据是由键值对构成的
   + 键用引号引起来，也可以不使用引号
   + 值的取值类型
      1. 数字（整数或浮点数）
      2. 字符串（在双引号中）
      3. 逻辑值（true 或 false）
      4. 数组（在方括号中）
      5. 对象（在花括号中）
      6. null
+ 数据由逗号分隔：多个键值对由逗号分隔
+ 花括号保存对象：使用{}定义json格式
+ 方括号保存数组：[]

#### 32.1.2 获取数据

```
json对象.键名

json对象["键名"]

数组对象[索引]
```
遍历：
```
for in 循环:
for(var key in person){
    这样获取的key是字符串，所以取值要用
    person[key];
}

数组循环：
for(var i =0; i<ps.length; i++){
    ...
}
```
### 33.2 JSON数据和Java对象的相互转换

+ JSON解析器：
常见的解析器：Jsonlib, Gson, Fastjson, jackson

#### 33.2.1 JSON转为Java对象

1. 导入Jackson的相关jar包
2. 创建Jackson核心对象```ObjectMapper```
3. 调用ObjectMapper的相关方法进行转换
```
readValue(json字符串数据,Class)
```

#### 33.2.2 Java对象转为JSON

1. 导入Jackson的相关jar包
2. 创建Jackson核心对象ObjectMapper
3. 调用ObjectMapper的相关方法进行转换
+ 转换方法
```
writeValue(参数1, obj)：
    参数1：
        File：将obj对象转换为JSON字符串，并保存到指定的文件中
        Writer：将obj对象转换为JSON字符串，并将json数据填充到字符输出流中
        OutputStream：将obj对象转换为JSON字符串，并将JSON数据填充到字节输出流中

writeValueAsString(obj)：将对象转为JSON字符串
```

+ 注解：加在类的成员变量上或get方法上。
```
@JsonIgnore：排除属性。

@JsonFormat：属性值的格式化。传入属性pattern
```
+ 复杂java对象转换
```
List：数组
Map：对象格式一致，键值对
```

### 33.3 案例

检验用户名是否存在

+ 服务器响应的数据，在客户端使用时，要想当做json数据格式使用
   1. ```$.get(type)```：将最后一个参数type指定为“json”
   2. 在服务器端设置MIME类型
      ```response.setContentType("application/json;charset=utf-8");```

## 33 Redis

+ redis是一款高性能的NoSQL系列的非关系型数据库。可以用来做缓存

### 33.1 下载安装

redis中文网，解压即可

redis.windows.conf：配置文件
redis-cli.exe：redis的客户端
redis-server.exe：redis服务器端

### 33.2 命令操作

#### 33.2.1 redis的数据结构：

+ redis存储的是：key，value格式的数据，其中key都是字符串，value有5种不同的数据结构
+ value的数据结构：
   1. 字符串类型string
   2. 哈希类型hash：每个key对应一个map
   3. 列表类型list：linkedlist格式。支持重复元素
   4. 集合类型set：不允许重复元素
   5. 有序集合类型sortedset：不允许重复元素，且元素有顺序

#### 33.2.2. 字符串类型string

```
存储：
	set key value

获取：
	get key

删除：
	del key
```

#### 33.2.3. 哈希类型hash

```
存储：
	hset key field value

获取：
	hget key field：获取指定的field对应的值
	hgetall key：获取所有的field和value

删除：
	hdel key field
```

#### 33.2.4. 列表类型list

可以添加一个元素到列表的头部（左边）或者尾部（右边）
```
添加：
	lpush key value：将元素加入列表左边【value可以直接写多个，空格隔开】
	rpush key value：将元素加入列表右边

获取：
    lrange key start end：范围获取，获取所有：0 -1

删除：
    lpop key：删除列表最左边的元素，并将元素返回
    rpop key：删除列表最右边的元素，并将元素返回
```

#### 33.2.5. 集合类型set：不允许重复元素

```
存储：
	sadd key value【value可以直接写多个，空格隔开】

获取：
	smembers key：获取set集合中所有元素

删除：
	srem key value：删除set集合中的某个元素
```

#### 33.2.6. 有序集合类型sortedset：不允许重复元素，且元素有顺序

```
存储：
	zadd key score value：会按照score从小到大排序

获取：
	zrange key start end：要显示分数，后面加withscores

删除：
	zrem key value
```

#### 33.2.7. 通用命令

```
keys *：查询所有的键【正则表达式】

type key：获取键对应的value的类型

del key：删除指定的key value
```

### 33.3 持久化

+ redis是一个内存数据库，当redis服务器重启，数据会丢失，我们可以将redis内存中的数据持久化保存到硬盘的文件中
+ redis持久化机制：RDB和AOF

#### 33.3.1 RDB

+ 默认方式，不需要进行配置，默认使用这种机制
+ 在一定的间隔时间内，检测key的变化情况，然后持久化数据
+ 编辑redis.windows.conf进行配置。
  save 900 1那里，表示900秒内有1条k以上的key更改就会进行持久化存储
+ 启动的时候必须要用命令行，redis-server.exe redis.windows.conf

#### 33.3.2 AOF

+ 日志记录的方式，可以记录每一条命令的操作。每一条命令操作后，持久化数据，对性能影响较大

1. 编辑edis.windows.conf文件。
   appendonly改成yes
   然后
```
#appendsysnc always：每一次操作都进行持久化
appendsysnc everysec：每隔一秒进行一次持久化
#appendsysnc no：不进行持久化
```
2. 命令行指定配置文件打开

### 33.4 使用Java客户端操作redis：Jedis

+ Jedis：一款java操作redis数据库的工具

#### 33.4.1 使用步骤

1. 下载Jedis的jar包
2. 使用：
```
1. 获取连接
Jedis jedis = new Jedis("localhost",6379);//空参默认localhost：6379

2. 操作
jedis.set("key","value");【jedis的方法名和redis的命令一样】

3. 关闭连接
jedis.close();
```

```
setex(key,seconds,value)方法：把key：value存入redis，seconds秒后自动删除掉
```

#### 33.4.2 jedis连接池：JedisPool

使用：
1. 创建JedisPool连接池对象，可以空参，也可以把创建配置对象传入
2. 调用方法```getResource()```获取Jedis连接

创建配置对象：
```
JedisPoolConfig config = new JedisPoolConfig();
config.setXxx(n);
```

#### 33.4.3 缓存案例

先查redis里有没有，没有再去数据库查，查到后放入redis里
清除缓存的话：在数据库增删改的时候，删除redis里的对应数据

## 34 Maven

+ pom：项目对象模型Project Object Model

### 34.1 下载安装配环境变量

MAVEN_HOME
PATH  MAVEN_HOME \bin

```mvn -v```查看是否安装成功

### 34.2 文件

配置：conf/settings.xml
里面可以配置本地仓库的位置。在注释里，复制出来就行。

远程仓库【私服】

### 34.3 maven标准目录结构

src/main/java	核心代码部分
src/main/resources	配置文件部分
src/test/java	测试代码部分
src/test/resources	测试配置文件
src/main/webapp	web项目的页面资源，js，css，图片等等

+ cmd里面。cd 路径后要再敲一个盘符

### 34.4 maven命令

mvn clean 删除编译的东西，因为每个人的环境都不一样，一般拿到别人项目先clean
mvn complie：编译main下的代码
mvn test：编译main和test下的代码
mvn package：编译main和test下的代码，并打包，打成什么包在pom.xml里设置
mvn install：编译，打包，并放在本地仓库

发布：
mvn deploy 需要一些配置

### 34.5 Maven概念模型

1. 依赖管理：
    项目对象模型：pom，包括
   + 项目自身信息
   + 项目运行依赖的jar包
   + 项目运行环境信息，比如jdk，tomcat信息

  其中项目运行依赖的jar包：即依赖管理模型Dependency
     一个jar包坐标必须包括：公司组织的名称、项目名、版本号

2. 一键构建：
构建生命周期：没讲
默认生命周期：compile,test,...
每一个构建项目的命令都对应了maven底层的一个插件

### 34.6 IDEA相关配置

Maven --Runner里
VM Options：填写-DarchetypeCatalog=internal

没有联网的时候也能根据之前下载过的骨架（模板）创建maven工程

### 34.7 创建项目

使用骨架创建java：
quickstart

使用骨架创建web：
webapp

### 34.8 tomcat

tomcat运行命令
tomcat:run

### 34.9 jar包冲突

```
在dependency里写
<scope>provided</scope>
```
表示只在编译测试过程中起作用，test表示只在测试阶段起作用
web工程，这里导入的servlet包和tomcat软件里的包冲突了

### 34.10 工程运行环境修改

添加插件，修改tomcat版本
```
<build>
	<plugins>
		<plugin>
			<groupId>org.apache.tomcat.maven
			<artifactId>tomcat7-maven-plugin
			<version>
			<configuration>
				<port>修改端口

```
tomcat7:run 启动tomcat7

### 34.11 创建模板

Settings里搜索live
Live Templates

之后直接输入模板名字一回车就出来模板了

插件里也可以设置jdk

### 34.12 数据库

scope的配置
test：junit
provide：servlet，jsp
runtime：JDBC

# 35 黑马旅游网
## 35.1 前期准备

数据库数据导入

## 35.2 功能实现
### 35.2.1 注册

1. js表单校验
2. ajax表单提交

表单校验：
1. 用户名：单词8-20位
2. 密码：单词8-20位
3. email：邮件格式
4. 姓名：非空
5. 手机号：手机号格式
6. 出生日期：非空
7. 验证码：非空

异步提交：
这里用HTML作为视图层，不能直接从servlet相关的域对象中获取值，只能通过ajax获取响应数据
获取表单数据：JQuery方法：$("form").serialize()可以把表单数据转换为字符串："key=value&k=v"

【疑问：$.post的url要不要写虚拟目录，草 还虚拟目录呢，斜杠都不能加】

后台代码实现：
RegistUserServlet
UserService和UserServiceImpl
UserDao和UserDaoImpl

激活码唯一：UuidUtils.getUuid()


退出：销毁session

session的一些问题【百度的】：session并不是一开始就创建的，而是在调用了getSession后才创建。
session也不会在浏览器关闭后立刻被销毁，而是要过一段时间。session销毁要么手动，要么超过xml里配置的生命周期
【百度remove应该也可以】


9	优化Servlet
9.1	目的
减少Servlet的数量，现在是一个功能一个Servlet，将其优化为一个模块一个Servlet，相当于在数据库中一张表对应一个Servlet，在Servlet中提供不同的方法，完成用户的请求。


Idea控制台中文乱码解决：-Dfile.encoding=gb2312

9.2	BaseServlet编写：
```
	public class BaseServlet extends HttpServlet {


    @Override
    protected void service(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        //System.out.println("baseServlet的service方法被执行了...");

        //完成方法分发
        //1.获取请求路径
        String uri = req.getRequestURI(); //   /travel/user/add
        System.out.println("请求uri:"+uri);//  /travel/user/add
        //2.获取方法名称
        String methodName = uri.substring(uri.lastIndexOf('/') + 1);
        System.out.println("方法名称："+methodName);
        //3.获取方法对象Method
        //谁调用我？我代表谁
        System.out.println(this);//UserServlet的对象cn.itcast.travel.web.servlet.UserServlet@4903d97e
        try {
            //获取方法
            Method method = this.getClass().getMethod(methodName, HttpServletRequest.class, HttpServletResponse.class);
            //4.执行方法
            //暴力反射
            //method.setAccessible(true);
            method.invoke(this,req,resp);
        } catch (NoSuchMethodException e) {
            e.printStackTrace();
        } catch (IllegalAccessException e) {
            e.printStackTrace();
        } catch (InvocationTargetException e) {
            e.printStackTrace();
        }


    }
}
```
然后写一个9.3	UserServlet
将之前的Servlet实现的功能，抽取到UserServlet中的不同方法中实现


location.search 拿连接，可以获取一些变量值

还有一些小方法，就没记录了

