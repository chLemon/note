# InnoDB锁和事务模型

> <https://dev.mysql.com/doc/refman/8.4/en/innodb-locking-transaction-model.html>

## 1. 锁定 Locking

| 锁类型                              |
| ----------------------------------- |
| Shared (S) Locks                    |
| Exclusive (X) Locks                 |
| Intention Locks                     |
| Record Locks                        |
| Gap Locks                           |
| Next-Key Locks                      |
| Insert Intention Locks              |
| AUTO-INC Locks                      |
| Predicate Locks for Spatial Indexes |

### 1.1. 行级锁

InnoDB 的行锁都是加载索引上的，如果表没有定义索引，InnoDB 会创建一个隐式的聚簇索引来使用。

#### 1.1.1. Shared (S) Locks 和 Exclusive (X) Locks

- S lock: 允许持有锁的事务读取行。
- X lock: 允许持有锁的事务更新或删除行。

如果有事务持有行 `r` 的 S 锁，那么其他事务可以继续获取到 S 锁，但是无法获取到 X 锁。

如果有事务持有行 `r` 的 X 锁，那么其他事务无法获取到任何锁。

锁结构在监控中输出如下

```shell
RECORD LOCKS space id 58 page no 3 n bits 72 index `PRIMARY` of table `test`.`t`
trx id 10078 lock_mode X locks rec but not gap
Record lock, heap no 2 PHYSICAL RECORD: n_fields 3; compact format; info bits 0
 0: len 4; hex 8000000a; asc     ;;
 1: len 6; hex 00000000274f; asc     'O;;
 2: len 7; hex b60000019d0110; asc        ;;
```

#### 1.1.2. Gap Locks

间隙锁锁定的是索引间隙。目的是阻止向间隙内插入。

间隙锁是在性能和并发性的权衡，只在部分隔离级别中使用。

gap lock 数据结构也是记录在某行上，锁定该行前方的那个 gap。InnoDB 会在每个索引页前后增加两个虚拟记录（pseudo-record）：

- Infimum: 小于页内所有记录的
- Supremum: 大于页内所有记录的，可以用于锁定最后一个 gap

对于使用唯一索引来搜索唯一行时，不会有 gap lock。（这不包括搜索条件仅包括一个多列唯一索引的部分列，这种情况下会有间隙锁定。）

注意，间隙锁之间没有冲突，gap S-lock 和 gap X-lock 不冲突，起到一样的功能，这个锁唯一的目的是阻止其他事务向间隙内插入数据。

允许 gap S-lock 和 gap X-lock 共存是因为锁结构是存在于 index 上，当某个 index 删除时，需要合并 gap locks。如 (1, 2) 和 (2, 3) 这两个 gap lock，当 2 数据删除时，前者需要将锁结构移动到 3，2个 gap lock 都会变成 (1, 3)

当事务隔离级别设置为 READ COMMITTED 时，搜索和索引扫描时的 gap lock 会被禁用，仅用于外键约束检查和重复性检查。READ COMMITTED 还有一些其他影响。在计算完 WHERE 条件后，不匹配的行锁会被释放。UPDATE 语句时，InnoDB 会执行“半一致性（semi-consistent）”读取，返回最新提交的版本，这样 MySQL 可以知道该行是否和 UPDATE 的 WHERE 条件匹配。

#### 1.1.3. Next-Key Locks

next-key lock 是 2 个锁的组合，索引记录上的行锁和这个索引记录前 gap 的 gap lock。是同一个 index record 上的 2 个锁结构。

InnoDB 在搜索或扫描索引时，对遇到的 index record 设置 X 或者 S 锁，锁定索引记录和之前的 gap，阻止其他事务插入数据。

在 Supremum 上的 next-key lock 效果是锁定最后一个 gap（因为 Supremum 只是一个虚拟节点）。

默认情况下，InnoDB 是 REPEATABLE READ 隔离级别。这时 InnoDB 使用 next-key lock 来避免 phantom rows（换行）。

锁结构在监控中输出如下

```shell
RECORD LOCKS space id 58 page no 3 n bits 72 index `PRIMARY` of table `test`.`t`
trx id 10080 lock_mode X
Record lock, heap no 1 PHYSICAL RECORD: n_fields 1; compact format; info bits 0
 0: len 8; hex 73757072656d756d; asc supremum;;

Record lock, heap no 2 PHYSICAL RECORD: n_fields 3; compact format; info bits 0
 0: len 4; hex 8000000a; asc     ;;
 1: len 6; hex 00000000274f; asc     'O;;
 2: len 7; hex b60000019d0110; asc        ;;
```

#### 1.1.4. Insert Intention Locks

INSERT 语句会在插入行之前设置 insert intention lock，锁定一个间隙，之后再去获取行的 X 锁。

insert intention lock 之间不冲突。但是当有 gap lock 时，获取 insert intention lock 时会阻塞冲突；反之不会。

| 当前已持有的锁 \ 请求的新锁 | Gap Lock (新请求) | Insert Intention (新请求) |
| --------------------------- | ----------------- | ------------------------- |
| Gap Lock                    | 兼容 (不阻塞)     | 冲突 (阻塞)               |
| Insert Intention            | 兼容 (不阻塞)     | 兼容 (不阻塞)             |

```shell
RECORD LOCKS space id 31 page no 3 n bits 72 index `PRIMARY` of table `test`.`child`
trx id 8731 lock_mode X locks gap before rec insert intention waiting
Record lock, heap no 3 PHYSICAL RECORD: n_fields 3; compact format; info bits 0
 0: len 4; hex 80000066; asc    f;;
 1: len 6; hex 000000002215; asc     " ;;
 2: len 7; hex 9000000172011c; asc     r  ;;...
```

### 1.2. 表级锁

#### 1.2.1. S Locks 和 X Locks

表级锁。

```sql
-- X 锁
LOCK TABLES ... WRITE
```

#### 1.2.2. Intention Locks

为了在锁表时快速判断表内是否存在行锁，在进行行锁时会先设置 Intention Lock （意向锁）。

- Intention shared lock (IS): 有事务意图给表中的若干行设置 S lock
- Intention exclusive lock (IX): 有事务意图给表中的若干行设置 X lock

- 事务在获取某行的 S 锁前，必须先获取到表的 IS 锁，或者更强的锁。
- 事务在获取某行的 X 锁前，必须先获取到表的 IX 锁。

Intention locks 只会阻塞 表级 S/X 锁

锁结构在监控中输出如下

```shell
TABLE LOCK table `test`.`t` trx id 10080 lock mode IX
```

#### 1.2.3. X S IS IX 兼容性表格

|     | X        | IX         | S          | IS         |
| --- | -------- | ---------- | ---------- | ---------- |
| X   | Conflict | Conflict   | Conflict   | Conflict   |
| IX  | Conflict | Compatible | Conflict   | Compatible |
| S   | Conflict | Conflict   | Compatible | Compatible |
| IS  | Conflict | Compatible | Compatible | Compatible |

- 当有事务获取到 IS 锁，有行获取了 S 锁
    - 只阻塞 X 锁的获取
    - IS IX 本身不冲突，S 锁也不冲突
- 当有事务获取到 S 锁
    - 阻塞 X 锁的获取
    - 阻塞 IX 锁的获取，相当于所有行获取了 S 锁，不能有行继续获取 X 锁
- 当有事务获取到 IX 锁，有行获取了 X 锁
    - 阻塞所有表锁： X 锁 / S 锁
    - IS IX 本身不冲突
- 当有事务获取到 X 锁
    - 阻塞所有锁

#### 1.2.4. AUTO-INC Locks

当 insert 时有 AUTO_INCREMENT 列时使用的一种特殊的表级锁。当有事务插入时，其他事务需要等待。

`innodb_autoinc_lock_mode` 变量可以更改其算法，在自增值的可预测性和并发性能间进行权衡。

### 1.3. 其他

Predicate Locks for Spatial Indexes

给 SPATIAL 索引（一种用于空间数据的索引）设计的锁。

