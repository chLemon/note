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

### 共享锁

标准的行级锁

### 排他锁


