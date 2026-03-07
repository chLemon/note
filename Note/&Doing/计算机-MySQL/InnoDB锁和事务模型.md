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

#### Next-Key Locks

next-key lock 是 2 个锁的组合，索引记录上的行锁和这个索引记录前 gap 的 gap lock。是同一个 index record 上的 2 个锁结构。




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

#### 1.2.3. 表级锁兼容性表格

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
