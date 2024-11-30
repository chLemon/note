参数格式说明
```shell
# 必须的参数
<param_name>

# 可选的参数
[param_name]
```

# 1. Need Merge

# 2. Git 基础

## 2.1. 获取 Git 仓库

通常有2种获取 Git 仓库的方式：
1. 将尚未进行版本控制的本地目录转换为 Git 仓库；
2. 从其它服务器 clone 一个已存在的 Git 仓库。

### 2.1.1. 在已存在目录中初始化仓库

```shell
git init
```

会创建一个名为`.git`的文件夹，这个文件夹里有 Git 仓库所有必须的文件。现在所有的文件都还没有被跟踪，如果需要：

```shell
git add -A
git commit -m 'initial project version'
```

### 2.1.2. clone 现有的仓库

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

Git 支持多种数据传输协议，上面这个例子用的是`http://`协议，你也可以用SSH传输协议：`git://`或者`user@server:path/to/repo.git`。

## 2.2. 将更改记录到仓库中

### 文件状态

当获取到一个 Git 仓库后，Git 会将最新版本的全部文件拷贝到当前目录下。

将最新版本的全部文件拷贝，称为 checkout（检出，指从图书馆/档案室借阅出来） 或者 working copy。将当前目录称为 工作目录(working directory)。

在工作目录里的文件有2种状态：已跟踪（tracked）、未跟踪（untracked）。

已跟踪的文件是指存在于上一个快照（snapshot）中，或者新暂存（staged）的文件。它们可能是未修改（unmodified）、已修改（modified）、已暂存（staged）。简单的说，已跟踪的文件就是 Git 知道的文件。

未跟踪的文件就是工作目录里除了已跟踪文件外的所有文件（不在上一个快照中，也不在暂存区）。

当 clone 一个仓库后，所有的文件都是已跟踪、未修改状态（tracked & unmodified）。当你修改了文件后，这些文件就是已修改状态（modified）。然后可以将一些修改的文件暂存起来（staged），然后提交（commit）这些暂存的更改。
![](lifecycle.png)

### 查看文件的状态 git status

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

### 跟踪新文件

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

### 暂存修改的文件

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





