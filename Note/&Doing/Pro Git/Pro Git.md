> https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository
>
> https://git-scm.com/book/zh/v2/Git-%E5%9F%BA%E7%A1%80-%E8%AE%B0%E5%BD%95%E6%AF%8F%E6%AC%A1%E6%9B%B4%E6%96%B0%E5%88%B0%E4%BB%93%E5%BA%93





# 版本控制 Version Control System

## 原始

很多人习惯复制整个项目目录，改名加上备份时间来区别不同版本。

优点：简单

缺点：容易出错，可能会用错目录，写错文件，覆盖不该覆盖的文件

## 本地版本控制 Local  Version Control Systems

最流行的一种叫做RCS，原理是在硬盘上保存补丁集合（文件修改前后的变化），通过应用补丁可以重新计算出各个版本的文件内容

## 集中化的版本控制系统  Centralized VSC (CVCS)

为了让不同系统上的开发者协同工作。有：VCS、Subversion、Perforce等

有一个单一的集中管理的服务器，保存所有文件版本。所有开发者通过客户端连接这台服务器，客户端会存一份当前版本快照。

缺点：中央服务器单点故障，宕机会导致所有人无法工作，且该服务器磁盘损坏时，如果没有恰当备份，会丢掉整个项目的版本数据。

## 分布式版本控制系统 Distributed VSC (DVSC)

客户端把整个代码仓库完整镜像，这样的话，中央服务器故障，都可以用任何一个客户端镜像来恢复。

有：Git、Mercurial、Darcs等

# Git的特点

## Git数据存储

### 基于差异的版本控制

其他版本控制系统，大多存储的是 文件变更列表 。存储的是一组基本文件 和 每个文件版本之间的变化，通常称这些系统为 delta-based VCS，基于差异的。

| version1 | version2 | version3 | version4 |
| -------- | -------- | -------- | -------- |
| File A   | △ 1      | △ 2      | △ 3      |
| File B   |          | △ 1      | △ 2      |

### 基于快照的版本控制

而Git则是每次对全部文件创建一个快照，并保存这个快照的索引。为了效率，如果文件没有修改，只保存一个链接向之前存储文件的索引。

| version1 | version2 | version3 | version4 |
| -------- | -------- | -------- | -------- |
| File A   | A1       | A2       | A3       |
| File B   | B        | B1       | B2       |

所以如果一个1G的文件，修改了3次后，`.git`里会存储4G的内容

## 几乎所有操作本地执行

Git绝大多数操作都只需要访问本地文件和资源，没有网络开销，会非常快。并且没有网络和VPN时，也可以几乎做所有的操作。

## 完整性保证

会基于当前文件内容和目录结构计算SHA-1（一种哈希算法），一个40个16进制字符的字符串。

可以校验传送过程中是否丢失信息和损坏文件。

## 一般只添加数据

几乎所有的操作，都只是往Git数据库里添加数据。所以不用担心丢失数据

## 文件的三种状态

+ committed: 数据已经安全地保存在本地数据库中
+ modified: 修改了文件，还没有保存到数据库
+ staged: 对一个已修改文件的当前版本做了标记，使之包含在下次提交的快照中



Git项目有三个阶段：

![](areas.png)

+ 工作区：从Git仓库的压缩数据库里提取出的某个版本，放在磁盘上供使用和修改
+ 暂存区：是一个文件，保存了下次要提交的文件列表。也叫 index
+ git仓库：保存项目的元数据和对象数据库。clone复制的就是这些数据

基本的 Git 工作流程如下：

1. 在工作区中修改文件。
2. 将你想要下次提交的更改选择性地暂存，这样只会将更改的部分添加到暂存区。
3. 提交更新，找到暂存区的文件，将快照永久性存储到 Git 目录。

如果 Git 目录中保存着特定版本的文件，就属于 **已提交** 状态。 如果文件已修改并放入暂存区，就属于 **已暂存** 状态。 如果自上次检出后，作了修改但还没有放到暂存区域，就是 **已修改** 状态。

# 安装和使用Git

## 安装

官网

## 初次使用的设置

Git自带一个工具 `git config`，可以配置Git的变量。存储在3个不同的位置

1. `/etc/gitconfig`：包括系统上，所有用户和所有仓库的通用配置。`git config --system`就可以修改，需要管理员权限。
2. `~/.gitconfig`或`./config/git/config`：当前用户配置，`git config --global`设置，针对所有仓库
3. `.git/config`：在当前Git目录下，针对此仓库，`git config --local`设置，`git config`默认会用这个。

下方优先级最高。

```shell
git config --list --show-origin
```

可以查看所有的配置和所在的文件。

### 用户信息设置

```shell
git config --global user.name "name"
git config --global user.email email
```

`--global`的命令只需要运行一次。

### 文本编辑器

例如使用 Emacs ，在Windows上要使用别的文本编辑器，必须执行完整的可执行文件路径

```shell
git config --global core.editor emacs
```

### 检查配置

```shell
git config --list
git config user.name
git config --show-origin rerere.autoUpdate
```

可能会看到重复的变量名，因为有上述3中配置文件可以读取。最下面的命令可以看到该变量是通过哪个配置文件设置为了什么。

# 获取帮助

```shell
git help <verb>
git <verb> --help
man git-<verb>

# 简明的help帮助，只列出可用选项快速参考
git <verb> -h
```

还可以在 Libra Chat 的 `#git`或者`#github`频道上寻求帮助。



# 2 Git基础













































