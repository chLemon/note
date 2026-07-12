# Pro Git 笔记

> https://git-scm.com/book/en/v2
>
> https://git-scm.com/book/zh/v2

参数格式说明：

```shell
# 必须的参数
<param_name>

# 可选的参数
[param_name]
```

## 1. 版本控制 Version Control System

### 1.1. 原始

很多人习惯复制整个项目目录，改名加上备份时间来区别不同版本。

优点：简单

缺点：容易出错，可能会用错目录，写错文件，覆盖不该覆盖的文件

### 1.2. 本地版本控制 Local Version Control Systems

最流行的一种叫做 RCS，原理是在硬盘上保存补丁集合（文件修改前后的变化），通过应用补丁可以重新计算出各个版本的文件内容

### 1.3. 集中化的版本控制系统 Centralized VSC (CVCS)

为了让不同系统上的开发者协同工作。有：VCS、Subversion、Perforce 等

有一个单一的集中管理的服务器，保存所有文件版本。所有开发者通过客户端连接这台服务器，客户端会存一份当前版本快照。

缺点：中央服务器单点故障，宕机会导致所有人无法工作，且该服务器磁盘损坏时，如果没有恰当备份，会丢掉整个项目的版本数据。

### 1.4. 分布式版本控制系统 Distributed VSC (DVCS)

客户端把整个代码仓库完整镜像，这样的话，中央服务器故障，都可以用任何一个客户端镜像来恢复。

有：Git、Mercurial、Darcs 等

## 2. Git 的特点

### 2.1. Git 数据存储

#### 2.1.1. 基于差异的版本控制

其他版本控制系统，大多存储的是 文件变更列表 。存储的是一组基本文件 和 每个文件版本之间的变化，通常称这些系统为 delta-based VCS，基于差异的。

| version1 | version2 | version3 | version4 |
| -------- | -------- | -------- | -------- |
| File A   | △ 1      | △ 2      | △ 3      |
| File B   |          | △ 1      | △ 2      |

#### 2.1.2. 基于快照的版本控制

而 Git 则是每次对全部文件创建一个快照，并保存这个快照的索引。为了效率，如果文件没有修改，只保存一个链接向之前存储文件的索引。

| version1 | version2 | version3 | version4 |
| -------- | -------- | -------- | -------- |
| File A   | A1       | A2       | A3       |
| File B   | B        | B1       | B2       |

所以如果一个 1G 的文件，修改了 3 次后，`.git`里会存储 4G 的内容

### 2.2. 几乎所有操作本地执行

Git 绝大多数操作都只需要访问本地文件和资源，没有网络开销，会非常快。并且没有网络和 VPN 时，也可以几乎做所有的操作。

### 2.3. 完整性保证

会基于当前文件内容和目录结构计算 SHA-1（一种哈希算法），一个 40 个 16 进制字符的字符串。

可以校验传送过程中是否丢失信息和损坏文件。

### 2.4. 一般只添加数据

几乎所有的操作，都只是往 Git 数据库里添加数据。所以不用担心丢失数据

### 2.5. 文件的三种状态

- committed: 数据已经安全地保存在本地数据库中
- modified: 修改了文件，还没有保存到数据库
- staged: 对一个已修改文件的当前版本做了标记，使之包含在下次提交的快照中

Git 项目有三个阶段：

![](images/areas.png)

- 工作区：从 Git 仓库的压缩数据库里提取出的某个版本，放在磁盘上供使用和修改
- 暂存区：是一个文件，保存了下次要提交的文件列表。也叫 index
- git 仓库：保存项目的元数据和对象数据库。clone 复制的就是这些数据

基本的 Git 工作流程如下：

1. 在工作区中修改文件。
2. 将你想要下次提交的更改选择性地暂存，这样只会将更改的部分添加到暂存区。
3. 提交更新，找到暂存区的文件，将快照永久性存储到 Git 目录。

如果 Git 目录中保存着特定版本的文件，就属于 **已提交** 状态。 如果文件已修改并放入暂存区，就属于 **已暂存** 状态。 如果自上次检出后，作了修改但还没有放到暂存区域，就是 **已修改** 状态。

## 3. 安装和初次设置

### 3.1. 安装

官网

### 3.2. 初次使用的设置

Git 自带一个工具 `git config`，可以配置 Git 的变量。存储在 3 个不同的位置

1. `/etc/gitconfig`：包括系统上，所有用户和所有仓库的通用配置。`git config --system`就可以修改，需要管理员权限。
2. `~/.gitconfig`或`./config/git/config`：当前用户配置，`git config --global`设置，针对所有仓库
3. `.git/config`：在当前 Git 目录下，针对此仓库，`git config --local`设置，`git config`默认会用这个。

下方优先级最高。

```shell
git config --list --show-origin
```

可以查看所有的配置和所在的文件。

#### 3.2.1. 用户信息设置

```shell
git config --global user.name "name"
git config --global user.email email
```

`--global`的命令只需要运行一次。

#### 3.2.2. 文本编辑器

例如使用 Emacs ，在 Windows 上要使用别的文本编辑器，必须执行完整的可执行文件路径

```shell
git config --global core.editor emacs
```

#### 3.2.3. 检查配置

```shell
git config --list
git config user.name
git config --show-origin rerere.autoUpdate
```

可能会看到重复的变量名，因为有上述 3 中配置文件可以读取。最下面的命令可以看到该变量是通过哪个配置文件设置为了什么。

## 4. 获取帮助

```shell
git help <verb>
git <verb> --help
man git-<verb>

## 简明的help帮助，只列出可用选项快速参考
git <verb> -h
```

还可以在 Libra Chat 的 `#git`或者`#github`频道上寻求帮助。

## 5. Git 基础

### 5.1. 获取 Git 仓库

通常有 2 种获取 Git 仓库的方式：

1. 将尚未进行版本控制的本地目录转换为 Git 仓库；
2. 从其它服务器 clone 一个已存在的 Git 仓库。

#### 5.1.1. 在已存在目录中初始化仓库

```shell
git init
```

会创建一个名为`.git`的文件夹，这个文件夹里有 Git 仓库所有必须的文件。现在所有的文件都还没有被跟踪，如果需要：

```shell
git add -A
git commit -m 'initial project version'
```

#### 5.1.2. clone 现有的仓库

```shell
git clone <url> [localDirName]
```

默认配置下，会将远程 Git 仓库里的每一个文件的每一个版本都拉取下来。

举个例子：

```shell
git clone https://github.com/libgit2/libgit2
```

会在当前目录下创建一个名为`libgit2`的文件夹，并且在这个文件夹里初始化一个`.git`文件夹，将所有从远程仓库拉取到的数据放入`.git`中，然后读取最新版本的文件拷贝（check out a working copy），放入`libgit2`中。这样你可以直接进行工作。

如果你希望 clone 下来的仓库，放入一个其他名字的文件夹，可以在命令后添加额外参数来制定新文件夹的名称。

Git 支持多种数据传输协议，上面这个例子用的是`http://`协议，你也可以用 SSH 传输协议：`git://`或者`user@server:path/to/repo.git`。

### 5.2. 将更改记录到仓库中

#### 文件状态

当获取到一个 Git 仓库后，Git 会将最新版本的全部文件拷贝到当前目录下。

将最新版本的全部文件拷贝，称为 checkout（检出，指从图书馆/档案室借阅出来） 或者 working copy。将当前目录称为 工作目录(working directory)。

在工作目录里的文件有 2 种状态：已跟踪（tracked）、未跟踪（untracked）。

已跟踪的文件是指存在于上一个快照（snapshot）中，或者新暂存（staged）的文件。它们可能是未修改（unmodified）、已修改（modified）、已暂存（staged）。简单的说，已跟踪的文件就是 Git 知道的文件。

未跟踪的文件就是工作目录里除了已跟踪文件外的所有文件（不在上一个快照中，也不在暂存区）。

当 clone 一个仓库后，所有的文件都是已跟踪、未修改状态（tracked & unmodified）。当你修改了文件后，这些文件就是已修改状态（modified）。然后可以将一些修改的文件暂存起来（staged），然后提交（commit）这些暂存的更改。

![](images/lifecycle.png)

#### 查看文件的状态 `git status`

`git status` 可以检查文件当前所处的状态。

如果在一个刚刚 clone 的仓库里执行 `git status`，会如下输出：

```shell
$ git status
On branch master
Your branch is up-to-date with 'origin/master'.
nothing to commit, working tree clean
```

这说明现在工作目录是干净的，也就是说，没有任何已跟踪的文件（tracked）是已修改状态（modified）。另外，这个命令的输出还会显示当前所处的分支，和该分支在服务器上的偏离。

如果现在新建一个文件 `README`（之前项目里不存在这个文件）：

```shell
$ echo 'My Project' > README
$ git status
On branch master
Your branch is up-to-date with 'origin/master'.
Untracked files:
  (use "git add <file>..." to include in what will be committed)

    README

nothing added to commit but untracked files present (use "git add" to track)
```

可以看到，在 Untracked files （未跟踪文件）标题下面，有一个 `README` 文件。未跟踪文件意味着 Git 发现有一个之前的快照/提交中（snapshot / commit）没有的文件，并且还没有暂存起来。Git 不会自动将之纳入到跟踪范围里，除非你显式告诉它这么做。这样你就不会意外将一些生成的二进制文件或者其他不想跟踪的文件跟踪起来。

你现在想开始跟踪 `README` 文件了，让我们开始跟踪这个文件

#### 跟踪新文件

为了开始跟踪一个新文件，你使用 `git add` 命令。

```shell
git add README
```

如果再运行一次 `git status`，就会看到 `README` 文件现在已经被跟踪了，并且被暂存了，等待被提交：

```shell
$ git status
On branch master
Your branch is up-to-date with 'origin/master'.
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)

    new file:   README
```

文件在 Changes to be committed 标题下，所以这个文件已经被暂存了。如果你此时提交，你运行 `git add` 时的文件版本就会被加入到接下来的历史快照中。

你可能会想起来，之前我们运行 `git init` 的时候，你运行了 `git add <files>` ，那会儿就是将目录下的文件进行了跟踪。`git add` 命令需要的参数是路径名称，既可以是文件，也可以是目录。如果是目录，这个命令就会将该目录下的所有文件递归地加入到暂存区。

#### 暂存修改的文件

修改一个已经被跟踪的文件。如果你修改了一个之前就被跟踪的文件，叫做 `CONTRIBUTING.md` ，然后运行 `git status`，你会得到：

```shell
$ git status
On branch master
Your branch is up-to-date with 'origin/master'.
Changes to be committed:
  (use "git reset HEAD <file>..." to unstage)

    new file:   README

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

    modified:   CONTRIBUTING.md
```

### 5.3. 忽略特殊文件

在仓库目录下创建`.gitignore`文件。不需要从头写`.gitignore`文件，GitHub 已经为我们准备了各种配置文件，只需要组合一下就可以使用了。所有配置文件可以直接在线浏览：https://github.com/github/gitignore

> 使用 Windows 的童鞋注意了，如果你在资源管理器里新建一个`.gitignore`文件，它会非常弱智地提示你必须输入文件名，但是在文本编辑器里"保存"或者"另存为"就可以把文件保存为`.gitignore`了。

某个文件被忽略后，强制添加：

```shell
git add -f <filename>
```

或者你发现，可能是`.gitignore`写得有问题，需要找出来到底哪个规则写错了，可以用`git check-ignore`命令检查：

```shell
$ git check-ignore -v App.class
.gitignore:3:*.class	App.class
```

例外规则：把指定文件排除在`.gitignore`规则外的写法就是`!`+文件名，所以，只需把例外文件添加进去即可。

```shell
# 不排除.gitignore和App.class:
!.gitignore
!App.class
```

`.gitignore`文件本身要放到版本库里，并且可以对`.gitignore`做版本管理！

注意：`.gitignore`的作用是让没有被 track 的文件保持没有被 track 的状态，但是之前已经 track 的文件想要 ignore 的话，更新完`.ignore`文件后需要删除 cache：

```shell
git rm -r --cached .
git add .
git commit -m "update .gitignore"
git push
```
