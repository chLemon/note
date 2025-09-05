# PPT部分

## InnoDB锁的类型

InnoDB存储引擎实现了2种标准的行级锁：

共享锁S Lock，允许事务读一行数据

排他锁X Lock，允许事务删除或更新一行数据



锁的兼容性：锁兼容：事务T1获取了行r的S Lock，事务T2可以立刻获得行r的共享锁；锁不兼容：事务T3想获得行r的X Lock，需要等待T1T2释放S锁，锁不兼容

|      | X      | S      |
| ---- | ------ | ------ |
| X    | 不兼容 | 不兼容 |
| S    | 不兼容 | 兼容   |

多粒度锁定。为了支持在不同粒度上的加锁操作，允许事务在行级上的锁和表级上的锁同时存在。



意向锁：表级别的锁，设计目的主要是为了表明某个表中有行正在被锁定或将要被锁定。

MySQL Server有实现表锁，为了快速识别某个表中有没有锁。

意向共享锁：IS Lock 事务想要获得一张表中某几行的共享锁

意向排他锁：IX Lock 事务想要获得一张表中某几行的排他锁

表级锁之间的兼容性：

|      | IS     | IX     | S      | X      |
| ---- | ------ | ------ | ------ | ------ |
| IS   | 兼容   | 兼容   | 兼容   | 不兼容 |
| IX   | 兼容   | 兼容   | 不兼容 | 不兼容 |
| S    | 兼容   | 不兼容 | 兼容   | 不兼容 |
| X    | 不兼容 | 不兼容 | 不兼容 | 不兼容 |

意向锁都是表锁，所以只会阻塞对表加锁的操作





锁请求的查看：

```
SHOW ENGINE INNODB STATUS
```

> 在 [《了解常见的锁类型》](https://www.aneasystone.com/archives/2017/11/solving-dead-locks-two.html) 中我们说过，一共有四种类型的行锁：记录锁，间隙锁，Next-key 锁和插入意向锁。这四种锁对应的死锁日志各不相同，如下：
>
> - 记录锁（LOCK_REC_NOT_GAP）: lock_mode X locks rec but not gap
> - 间隙锁（LOCK_GAP）: lock_mode X locks gap before rec
> - Next-key 锁（LOCK_ORNIDARY）: lock_mode X
> - 插入意向锁（LOCK_INSERT_INTENTION）: lock_mode X locks gap before rec insert intention
>
> 这里有一点要注意的是，并不是在日志里看到 lock_mode X 就认为这是 Next-key 锁，因为还有一个例外：如果在 supremum record 上加锁，`locks gap before rec` 会省略掉，间隙锁会显示成 `lock_mode X`，插入意向锁会显示成 `lock_mode X insert intention`。譬如下面这个：
>
> | 12   | `RECORD LOCKS space id 0 page no 307 n bits 72 index `PRIMARY` of table `test`.`test` trx id 50F lock_mode X``Record lock, heap no 1 PHYSICAL RECORD: n_fields 1; compact format; info bits 0` |
> | ---- | ------------------------------------------------------------ |
> |      |                                                              |
>
> 看起来像是 Next-key 锁，但是看下面的 `heap no 1` 表示这个记录是 supremum record（另外，infimum record 的 heap no 为 0），所以这个锁应该看作是一个间隙锁。
>
> 在InnoDB存储引擎中，每个数据页中有两个虚拟的行记录，用来界定记录的边界。Infimum 是比该页中任何主键值都要小的值。Supremum 指的是比任何可能打的值还要大的值。这两个值在页创建时被建立，并且任何情况下不会删除。
>
> 



在INFORMATION_SCHEMA下有表 INNODB_TRX    INNODB_LOCKS    INNODB_LOCK_WAITS





lock_data，如果范围查找，只返回第一行的主键值





## 并发情况下的读取策略

行多版本控制，多版本并发控制MVCC：为了在读写和写读的时候也能进行并发进行，不被阻塞。

一致性的非锁定读和一致性锁定读

一致性的非锁定读

如果当前有事务A正在行r上进行UPDATA或DELETE操作，事务B想要读取r上的数据，事务B不会等待r上的X锁释放，而是回去读取行r的一个快照数据（通过undolog实现，不会产生额外的开销）

一致性锁定读

SELECT ... FOR UPDATA

SELECT ... LOCK IN SHARE MODE

## 锁的三种算法

InnoDB存储引擎有3种行锁的算法

### Record Lock：单个记录上的锁

### Gap Lock：间隙锁，锁定一个范围，但不包含记录本身

锁定一个范围，或者锁住第一个记录之前的部分，或最后一个记录之后的部分

如果没有建立索引，会锁住前面的一个区域？？？

间隙锁没有排他性，有间隙锁的地方可以再加一个间隙锁







### Next-Key Locks 锁定一个范围，并且锁定记录本身

### Insert Intention Locks

一种间隙锁，insert操作的时候会先加一个间隙锁，如47之间加56，都会在47间加上间隙锁，

### auto-inc Locks

特殊的表锁，增加auto_increment列的时候

插入意向锁不会阻止任何锁，对于插入的记录会持有一个记录锁。

![在这里插入图片描述](https://img-blog.csdnimg.cn/20181118210033715.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTA4NDEyOTY=,size_16,color_FFFFFF,t_70)





## 隔离级别

READ UNCOMMITTED
READ COMMITTED
REPEATABLE READ（默认）
SERIALIZABLE

### REPEATABLE READ

默认隔离级别

读取第一次读的时候创建的快照，这意味着同一个事务里的多次读取都是一致的



锁定读取

select with for update or lock in share mode

update

delete

加锁取决于是否在查询条件里使用唯一索引查询 还是一个范围查询



对于使用唯一索引，InnoDB只锁定某一行 record lock

对于其他的情况，InnoDB会锁住所有扫描过的索引，用gap locks和next-key locks 





【此处进行测试】

![image-20210308171753777](/Users/chen/Library/Application Support/typora-user-images/image-20210308171753777.png)

![image-20210308172528536](/Users/chen/Library/Application Support/typora-user-images/image-20210308172528536.png)

![image-20210308180814703](/Users/chen/Library/Application Support/typora-user-images/image-20210308180814703.png)

![image-20210308181032435](/Users/chen/Library/Application Support/typora-user-images/image-20210308181032435.png)

### Read committed

一致性非锁定读：每次都读取最新的快照

对于锁定读取，仅锁定索引记录，而不锁定间隙

因为不锁定间隙，可能会出现幻读问题，大大减少死锁问题

对于这种情况下的UPDATE语句，会先读取最新已提交版本，来确定是否匹配where条件，匹配后再次读取，来锁定或等待锁

而如果用到了索引，就被把所有索引列都锁住



### READ UNCOMMITTED

可能使用更早的版本

### SERIALIZABLE

但是InnoDB将所有普通SELECT 语句隐式转换为SELECT ... LOCK IN SHARE MODE





# 一致性非锁定读取

Repeatable read：读取该事物读取此行时第一个创建的快照，如果这时别的事务删除、插入、更新了，不会看到

创建快照的时间：第一次使用非锁定读取的时候创建。



read committed：每个事务读取最新的快照，可以读取到最新的commit



RR：

快照只适用于查询语句，对DML语句不适用：例如：

![image-20210309173530867](/Users/chen/Library/Application Support/typora-user-images/image-20210309173530867.png)



read COMMITTED和RR的SELECT默认使用一致性非锁定度





如果这个时候还想看到最新的数据

SELECT * FROM t LOCK IN SHARE MODE;



Rr

Mysql会锁住扫描过的每个记录，二级索引还会锁住聚合索引。如果不走索引，全表扫描了，全表都会被加锁

select的锁，update和delete都是next lock，insert不是，没有间隙锁，但是会加插入意图锁，插入意图锁和插入意图锁不会阻塞





## 锁问题

脏读

不可重复读

丢失更新





