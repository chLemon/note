# 1. 更现代的 Shell: iterm2

## 1.1. 下载

官网：

https://iterm2.com/index.html

# 2. fish

fish 是一个界面更好，并且无需特别配置的 shell

## 2.1. 安装

```shell
brew install fish
```

## 2.2. oh-my-fish

主题管理

https://github.com/oh-my-fish/oh-my-fish

### 2.2.1. 安装

```shell
curl https://raw.githubusercontent.com/oh-my-fish/oh-my-fish/master/bin/install | fish
```

### 2.2.2. 主题预览

https://github.com/oh-my-fish/oh-my-fish/blob/master/docs/Themes.md

觉得不错的：
+ default
+ ays
+ batman
+ bobthefish

## 2.3. 配置文件

**配置文件路径**

```shell
open -e ~/.config/fish/config.fish
```

```shell
alias cdw="cd ~/work/"
alias cdxx=""
#或者起名叫to...

# HomeBrew
export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.ustc.edu.cn/homebrew-bottles
export PATH="/usr/local/bin:$PATH"
export PATH="/usr/local/sbin:$PATH"
# HomeBrew END

# mysql
export PATH="/usr/local/mysql/bin:$PATH"

# 多版本JAVA相关
alias jdk7="export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk1.7.0_80.jdk/Contents/Home"
alias jdk8="export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk1.8.0_281.jdk/Contents/Home"
alias jdk11="export JAVA_HOME=/Users/chen/Library/Java/JavaVirtualMachines/corretto-11.0.13/Contents/Home"
alias jdk17="export JAVA_HOME=/Users/chen/Library/Java/JavaVirtualMachines/openjdk-17.0.1/Contents/Home"
alias jdk21="export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk-21.jdk/Contents/Home"
export JAVA_HOME="/Library/Java/JavaVirtualMachines/jdk1.8.0_281.jdk/Contents/Home"
export PATH="$JAVA_HOME/bin:$PATH:."
export CLASSPATH="$JAVA_HOME/lib/tools.jar:$JAVA_HOME/lib/jrt-fs.jar:."

# maven
export MAVEN_HOME="/Users/chen/program/apache-maven-3.6.3"
export PATH="$PATH:$MAVEN_HOME/bin"

# jupyter notebook
alias note="python3 -m notebook --notebook-dir='/Users/chen/Documents/jupyter_notes'"
alias cdnote="cd /Users/chen/Documents/jupyter_notes"
```

## 2.4. 修改默认shell

先打开终端，左上角，终端，偏好设置，通用，Shell的打开方式，命令`/usr/local/bin/fish`


# 3. iterm2 &fish



https://iterm2.com/index.html

https://lobster1234.github.io/2017/04/08/setting-up-fish-and-iterm2/

https://github.com/oh-my-fish/oh-my-fish

https://www.bilibili.com/video/BV16c411M78T/?spm_id_from=333.337.search-card.all.click&vd_source=9f68829e78088d41d3127b97b83ed97f

https://www.bilibili.com/video/BV1zA411v7a2/?spm_id_from=333.337.search-card.all.click&vd_source=9f68829e78088d41d3127b97b83ed97f

https://segmentfault.com/a/1190000007164195?utm_source=sf-related

https://cloud.tencent.com/developer/article/2008550

https://www.jianshu.com/p/fa9c09302ffc

https://www.bilibili.com/video/BV1cf4y157sv/?spm_id_from=333.337.search-card.all.click&vd_source=9f68829e78088d41d3127b97b83ed97f