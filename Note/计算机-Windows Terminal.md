# 安装

Microsoft Store 搜索 WindowsTerminal 即可安装。

如果 Microsoft Store 因为网络问题打不开，关闭代理。因为 windows 为了安全，禁止应用链接到本地端口（UWP应用联网限制）

# Powershell 7

win10默认的 `Windows Powershell`版本是`5.1`。

可以在 Github 上下载 PowerShell 7 的版本。

但是微软在设计上，这两个终端是并行存在的关系，并不是将原本5.1的`Windows PowerShell`升级。

在`Windows Terminal`里，设置 >> 启动 >> 默认配置文件，修改为`PowerShell`

# 自定义设置

## 配置文件

```shell
$profile
# 显示的位置就是配置文件所在的位置

code $profile
# 直接用 VS Code 打开配置文件

New-Item -Path $PROFILE -Type File -Force
# 默认没有配置文件，用此命令生成一个

. $PROFILE
# 重新加载配置文件
```

### 报错 无法加载文件……，因为此系统上禁止运行脚本

右键左下角的win图标（开始菜单） > Windows Powershell（管理员） > 输入`set-ExecutionPolicy RemoteSigned` > 输入`y`

## 设置快捷键冲突

Windows开始菜单 > 设置 > 搜索 高级键盘设置 > 输入语言热键 > 删除掉搜狗的ctrl + ,

## 窗口半透明

设置 > 默认值 > 外观 > 透明度 > 背景不透明度：70%左右

设置 > 默认值 > 外观 > 透明度 > 启用亚克力材料：开启

如果透明不生效，在 桌面右键 > 个性化 > 颜色 > 透明效果：开启

## 主题

### 安装  Oh My Posh

> https://ohmyposh.dev/docs/installation/windows

#### Microsoft Store即可安装。

#### 通过 winget 安装：

Powershell（管理员）

```shell
winget install JanDeDobbeleer.OhMyPosh -s winget
```

### 安装字体 nerd font

#### 命令行安装

安装好`oh-my`posh`后，重启 PowerShell ，`oh-my-posh`应该就在环境变量里了，如果没有自己再加一下

```shell
on-my-posh font install Meslo
# 官方推荐 Meslo 字体
```

#### 官网下载

> https://www.nerdfonts.com/font-downloads

下载后解压，将所有 font 文件拖到 `C:\Windows\Fonts`中

### 修改 PowerShell 字体

#### json文件修改

`ctrl + shift + ,`，在里面找到 `profiles.defaults`，紧跟着下面加这段

```json
{
    "profiles":
    {
        "defaults":
        {
            "font":
            {
                "face": "MesloLGL Nerd Font"
            }
        }
    }
}
```

#### 设置里修改

设置 > 默认值 > 外观 > 字体 > MesloLGL Nerd Font

### 主题修改

`$profile`文件中添加

```shell
oh-my-posh init pwsh --config ~/iterm2.omp.json | Invoke-Expression
```

# 快捷键

## 修改

关闭窗格：`ctrl + w`

新建标签页：`ctrl + n`

## 常用

`alt + shift + +/-`  横竖分割窗口

# alias设置 / function

在 powershell 的 `$profile` 里，可以写 function 。

## 打开 jupyter notebook

```shell
function note {
    jupyter notebook --notebook-dir=D:\jupyterNote
}
```

## 打开某个目录

```shell
function cdnote {
    set-location "D:\坚果云\Note"
}
function cdjo {
    set-location "D:\坚果云\Journal"
}
```

# 快速打开

可以将 WindowsTerminal 放在下方任务栏的第一个，然后通过 `Win + 1` 快速打开

另外，可以在文件资源管理器的地址栏，输入 `wt` 快速打开。删除掉 `设置 > 默认值 > 启动目录` 里的内容后，可以快速进入当前目录。

# 代码补全

带有管理员权限的情况下执行下面的命令，安装`posh-git`和`readline`

```shell
Install-Module -Name PowerShellGet -Force
PowerShellGet\Install-Module posh-git -Force
Install-Module PSReadLine -Force
```

修改配置文件：

```shell
Set-PSReadLineKeyHandler -Key Tab -Function MenuComplete #Tab键会出现自动补全菜单
Set-PSReadlineKeyHandler -Key UpArrow -Function HistorySearchBackward
Set-PSReadlineKeyHandler -Key DownArrow -Function HistorySearchForward
# 上下方向键箭头，搜索历史中进行自动补全
Import-Module posh-git # git的自动补全
```

