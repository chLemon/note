# ssh: connect to host github.com port 22: Connection refused

```
ssh -vT git@github.com
```
ssh: connect to host github.com port 22: Connection refused

ssh -vT -p 443 git@ssh.github.com

~/.ssh/config

Host github.com
HostName ssh.github.com
Port 443


# 中文乱码

https://zhuanlan.zhihu.com/p/133706032

# 0 我的配置

```shell
git config --global user.name "chLemon"
git config --global user.email "550125499@qq.com"
git config --global color.ui true
git config --global
```

.gitconfig

```shell
[alias]
	sw = switch
	swc = switch -c
	br = branch
	brdd = branch -D
	brd = branch -d
	st = status
	sl = stash list
	ss = stash
 	pl = pull
	ps = push
	mm = merge master
	cm = commit
	cmm = commit -m 
	cc = checkout
	lg = log --color --graph --pretty=format:'%Cred%h%Creset-%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit
	lgme = lg --author=chenweijun
	conf = commit -m "合并代码，解决冲突"
[pull]
	rebase = false


[http "https://github.com"]
	proxy = socks5://127.0.0.1:7890
[https "https://github.com"]
	proxy = socks5://127.0.0.1:7890
```



# 1 Git概述

C语言写的，分布式版本控制工具（Distributed Version Control System，DVCS）

+ 代码托管平台：GitHub、GitLab、gitee（码云）
+ 注意GitHub是公开的，不要放敏感信息
+ gitee有免费的5人及以下的私有仓库



github中文官方文档

https://docs.github.com/cn/github

git文档

https://git-scm.com/book/zh/v2

# 2 Git安装

## 2.1 Linux

+ 直接输入git会有提示

```
sudo apt-get install git
```

+ 或根据源码编译

```
./config
make
sudo make install
```

## 2.2 Mac

+ homebrew，http://brew.sh/
+ 从AppStore安装Xcode，Xcode集成了Git，不过默认没有安装，你需要运行Xcode，选择菜单“Xcode”->“Preferences”，在弹出窗口中找到“Downloads”，选择“Command Line Tools”，点“Install”就可以完成安装了。
+ 官网

## 2.3 Windows

官网下载

# 3 几个概念

## 3.1 工作区

Working Directory，电脑里的文件夹

## 3.2 版本库

工作区有一个隐藏目录，.git

版本库=仓库=repository=repo

## 3.3 暂存区

位于版本库中，叫stage或index

## 3.4 远程库

默认叫origin

## 3.5 分支

主分支叫`master`，是一个指针，每次指向该分支最新的版本。`HEAD`指针指向`master`

当创建一个新的分支`dev`的时候，创建一个指针`dev`指向当前版本，然后让`HEAD`指向`dev`，表示当前在分支`dev`上

如果此时有新的提交，指针`dev`指向新的版本，而`master`不变。合并的时候，只需要把`master`指向当前提交即可

这种分支策略叫做 Fast forward ，删除分支后，会丢掉分支信息

强制禁用 Fast forward的话，merge的时候就会生成一个新的commit，就可以从分支历史上看出分支信息

```
git merge --no-ff
```

## 3.6 标签

本身也是一个指针，指向某个commit，与分支的区别就是不能移动，容易记住的名字

# 4 Git配置

git配置的时候如果加了`--global`参数，表示你这台机器上所有的Git仓库都会使用这个配置，当然也可以对某个仓库指定。

配置信息会保存在~/.gitconfig文件中

## 4.1 配置用户名和邮箱

Git每次提交的时候都会使用用户信息

```
git config --global user.name "Your Name"
git config --global user.email "email@example.com"

查看配置信息
git config --list
git config user.name
git config user.email
```

## 4.2 颜色

```
git config --global color.ui true
```

## 4.3 忽略特殊文件

在仓库目录下创建`.gitignore`文件。不需要从头写`.gitignore`文件，GitHub已经为我们准备了各种配置文件，只需要组合一下就可以使用了。所有配置文件可以直接在线浏览：https://github.com/github/gitignore

> 使用Windows的童鞋注意了，如果你在资源管理器里新建一个`.gitignore`文件，它会非常弱智地提示你必须输入文件名，但是在文本编辑器里“保存”或者“另存为”就可以把文件保存为`.gitignore`了。

某个文件被忽略后，强制添加：

```
git add -f <filename>
```

或者你发现，可能是`.gitignore`写得有问题，需要找出来到底哪个规则写错了，可以用`git check-ignore`命令检查：

```
$ git check-ignore -v App.class
.gitignore:3:*.class	App.class
```

例外规则：把指定文件排除在`.gitignore`规则外的写法就是`!`+文件名，所以，只需把例外文件添加进去即可。

```
# 不排除.gitignore和App.class:
!.gitignore
!App.class
```

`.gitignore`文件本身要放到版本库里，并且可以对`.gitignore`做版本管理！

### 注意

`.gitignore`的作用是让没有被trace的文件保持没有被trace的状态，但是之前已经trace的文件想要ignore的话，更新完`.ignore`文件后需要删除cache

```
git rm -r --cached .
git add .
git commit -m "update .gitignore"
git push
```



## 4.4 别名

```
$ git config --global alias.st status
```

把`git status`起个别名`git st`，当然还有别的命令可以简写，很多人都用`co`表示`checkout`，`ci`表示`commit`，`br`表示`branch`

在[撤销修改](https://www.liaoxuefeng.com/wiki/896043488029600/897889638509536)一节中，我们知道，命令`git reset HEAD file`可以把暂存区的修改撤销掉（unstage），重新放回工作区。既然是一个unstage操作，就可以配置一个`unstage`别名：

```
$ git config --global alias.unstage 'reset HEAD'
```

当你敲入命令：

```
$ git unstage test.py
```

实际上Git执行的是：

```
$ git reset HEAD test.py
```

配置一个`git last`，让其显示最后一次提交信息：

```
$ git config --global alias.last 'log -1'
```

这样，用`git last`就能显示最近一次的提交：

```
$ git last
commit adca45d317e6d8a4b23f9811c3d7b7f0f180bfe2
Merge: bd6ae48 291bea8
Author: Michael Liao <askxuefeng@gmail.com>
Date:   Thu Aug 22 22:49:22 2013 +0800

    merge & fix hello.py
```

### 4.4.1 配置文件的位置

#### 4.4.1.1 每个仓库的

每个仓库的Git配置文件都放在`.git/config`文件中：

```
$ cat .git/config
[core]
    repositoryformatversion = 0
    filemode = true
    bare = false
    logallrefupdates = true
    ignorecase = true
    precomposeunicode = true
[remote "origin"]
    url = git@github.com:michaelliao/learngit.git
    fetch = +refs/heads/*:refs/remotes/origin/*
[branch "master"]
    remote = origin
    merge = refs/heads/master
[alias]
    last = log -1
```

别名就在`[alias]`后面，要删除别名，直接把对应的行删掉即可。

#### 4.4.1.2 当前用户的

而当前用户的Git配置文件放在用户主目录下的一个隐藏文件`.gitconfig`中：

```
$ cat .gitconfig
[alias]
    co = checkout
    ci = commit
    br = branch
    st = status
[user]
    name = Your Name
    email = your@email.com
```

配置别名也可以直接修改这个文件，如果改错了，可以删掉文件重新通过命令配置。

#### 4.4.1.3 直接在bash_profile里面改

```
vim ~/.bash_profile
source ~/.bash_profile
```

## 4.5 GitHub的SSH设置

### a 创建SSH Key

在用户主目录下，找有没有.ssh目录，如果有，id_rsa是私钥，id_rsa.pub是公钥，如果没有，用下面的命令创建（Windows用Git Bash）

```
ssh-keygen -t rsa -C "youremail@example.com"
```

一路回车

### b 在GitHub上添加SSH Key

登录GitHub，在Account settings，SSH Keys里，Add SSH Key，title任意，粘贴公钥内容

## 4.6 代理设置

```bash
# 对全部仓库进行http代理
git config --global http.proxy http://127.0.0.1:1080
git config --global https.proxy https://127.0.0.1:1080

# 只对GitHub进行http代理
git config --global http.https://github.com.proxy https://127.0.0.1:1087
git config --global https.https://github.com.proxy https://127.0.0.1:1087

# sock5代理
git config --global http.https://github.com.proxy socks5://127.0.0.1:1086
git config --global https.https://github.com.proxy socks5://127.0.0.1:1086

# 取消代理
git config --global --unset http.proxy
git config --global --unset https.proxy

# 查看已有配置
git config --global -l
```

### 4.6.1 镜像

2个常用的镜像地址：

- https://github.com.cnpmjs.org
- https://hub.fastgit.org

只需要将 [www.github.com](https://link.zhihu.com/?target=http%3A//www.github.com/)/后面为代码库 改为 www.github.com.cnpmjs.org/后面为代码库地址

### 4.6.2 通过Gitee中转fork仓库加速下载

1. 登录gitee，顶部选择，“从GiHhub/GitLab导入仓库”
2. 粘贴链接，等待导入完成。或可以刷新同步（在仓库名旁边）

# 5 常用命令

### init

```
git init <directory>
将指定的目录变成git管理的仓库，不带参数会把当前目录变成git的repo
```

### clone

```
git clone git@github.com:chLemon/repo.git
克隆一个指定的repo到本地
```

关于协议：```git://```使用ssh，也可以使用```https```等，但是```https```速度慢，且每次推送必须输入口令

### add

```
git add <file>
把文件添加到暂存区，可以添加多个文件
```

如果想添加被.gitignore忽略的文件，可以用`-f`强制添加：

```
git add -f App.class
```

`-A`全部添加

### commit

```
git commit -m "message"
把暂存区的文件全部添加至本地仓库
```

### status

```
git status
查看工作区状态
```

### log

查看日志

```
git log

git log --pretty=oneline
git log --oneline
每行显示一条commit

git log --graph --pretty=oneline --abbrev-commit
分支合并图

git log -- <file>
仅显示包含指定文件修改的commit

git log --author="<pattern>"
按指定作者搜索commit

git log --grep="<patter>"
按指定内容搜索commit

```

### diff

```
git diff
比较工作区和暂存区的修改

git diff <file>
比较该文件工作区和暂存区的修改

git diff HEAD
比较工作区和上一次commit后的修改

git diff --cached
比较暂存区和上一次commit后的修改
```

### rm

```
git rm <file>
从工作区删除文件
```

### reflog

```
git reflog
显示所有分支的所有操作记录
查看每一次命令，可以用来找当前版本（reset到这个版本）之后的版本号
```

### rebase

```
git rebase
```

- rebase操作可以把本地未push的分叉提交历史整理成直线；
- rebase的目的是使得我们在查看历史提交的变化时更容易，因为分叉的提交需要三方对比

```
git rebase <base>

基于<base>对当前分⽀进⾏rebase。<base>可以是commit、分⽀名称、tag或相对于HEAD的commit。
```

### reset

```
git reset <file>
移除暂存区的修改，但是工作区不变

git reset --hard commit_id
将暂存区和工作区都回退到commit_id的时候

commit_id的说明：
版本号可以只写前几位，能唯一定位即可；HEAD为当前版本，HEAD^为上个版本，HEAD^^为上上个版本，HEAD~100为往上100个版本
```

### branch

```
git branch
查看分支

git branch dev
创建dev分支

git branch -d dev
删除分支

git branch -D <name>
强制删除一个没有被合并过的分支

git branch --set-upstream-to=origin/dev dev
设置本地分支和远程分支的链接
```

### switch

```
git switch master
切换到master分支
【git checkout master】

git switch -c dev
创建dev分支并切换
【git checkout -b dev】

【git checkout -b dev origin/dev】
创建远程origin的dev分支到本地
```

### merge

```
git merge dev
合并指定分支到当前分支
```

### remote

```
git remote
查看远程库的信息

git remote -v
详细信息

git remote add origin git@github.com:chLemon/repo.git
git remote add <name> <url>
和远程库关联

git remote rm origin
删除关联

多个远程库：起名字起成不一样的，别用origin了
```

### push

```
git push -u origin master
-u：把本地master分支和远程master分支关联起来

git push <remote> <branch>

git push <remote> --tags
推送的时候把本地的tag也推送上去
```

dev和master推送，其他的可以不推送

```
git push 远程主机名 本地分支:远程分支
本地分支和远程分支名字一样可以省略
```

### pull

```
git pull <remote>
拉去所有分支的commit，并立刻合并
```

+ 会合并

### fetch

```
git fetch <remote> <branch>
从指定<remote>抓取指定<branch>的所有commit到本地repo。去掉<branch>将抓取远程所有分⽀的修改。
```

+ 不会合并，会生成一个分支，然后用`git merge <想要合并到的分支>`进行合并

### restore

```
git restore
用版本库的版本替换工作区
丢弃工作区的修改，让这个文件回到最近一次add或commit时的状态
或者是恢复工作区文件
【git checkout】
【git checkout -- file】

git restore --staged
撤销暂存区的修改
【git reset HEAD file】
```

### tag

```
git tag <tagname>
默认在最新的commit上创建标签

git tag <tagname> <commit_id>
之前的版本号，可以用git log找到

git tag -a <tagname> -m <message> <commit_id>
打附注标签，可以加备注

git tag
查看所有标签，按照字母顺序

git show <tagname>
查看标签详情

git tag -d <tagname>
删除标签

推送标签
git push origin <tagname>
git push origin tags
```

删除已经推送到远程的分支

```
git tag -d v0.9 先删本地
git push origin :refs/tags/v0.9 再删远程
```

### stash

```
git stash
保存一下当前工作状态

git stash list
查看所有的stash

git stash apply
恢复到stash

git stash drop
删除stash

git stash pop
恢复到上一个stash并删除

git stash apply stash@{0}
有多个stash时
```

### cherry-pick

复制一个特定的提交到当前分支

```
git cherry-pick <commit_id>
```

### revert

回滚掉一个提交，即撤销掉这次提交做的改动

```
git revert <commit_id>
```

# 6 查看自己的代码量

```
git log --since="2022-10-01" --before="2023-01-01" --author="weijunchen" --pretty=tformat: --numstat | awk '{ add += $1; subs += $2; loc += $1 - $2 } END { printf "added lines: %s, removed lines: %s, total lines: %s", add, subs, loc }'
```

# 图形化工具：Sourcetree

https://www.sourcetreeapp.com/

# 常见问题总结

## RPC failed; curl 56 OpenSSL SSL_read: SSL_ERROR_SYSCALL, errno 10054

有文件太大导致的

**解决：**

文件大小的缓存设置大点:

 git config --global http.postBuffer  524288000

## warning: LF will be replaced by CRLF in ball_pool/assets/Main.js.

1. warning: LF will be replaced by CRLF in ball_pool/assets/Main.js.
2. The file will have its original line endings in your working directory

git add的时候出现，是因为文件中换行符的差别导致的。这个提示的意思是说：会把windows格式（CRLF（也就是回车换行））转换成Unix格式（LF），这些是转换文件格式的警告，不影响使用。

git默认支持LF。windows commit代码时git会把CRLF转LF，update代码时LF换CRLF。

**解决：**

```
git config core.autocrlf false

git config --global core.autocrlf false
```

## fatal: refusing to merge unrelated histories

如果当前本地仓库不是从远程仓库克隆，而是本地创建的仓库，并且仓库中存在文件，此时再从远程仓库拉取文件的时候会报错

**解决：**

此问题可以在git pull命令后加入参数`--allow-unrelated-histories`





