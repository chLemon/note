# 1 安装

快捷方式：32要求JDK1.7以上，64要求JDK1.8以上

create assocations 推荐不选

+ 向导配置

没什么要在意的

# 2 基础设置

设置有2种：全局设置和项目设置

**全局设置**可在打开界面右下角Configure--Settings进入 或 编码界面File -- Other Settings -- Default Settings

File -- Settings 是项目设置，只针对当前项目生效


+ **修改主题**：Appearance & Behavior --Appearance --> UI Options -- Theme

+ 字体修改：在上述界面的 UI Options -- Override default fonts by 要使用含有中文的字体，不然会在部分地方乱码，不建议【此项已没】

+ 写**代码时的字体**：Editor -- Font --> 是否使用等宽字体（Show only monospaced fonts），字体设置成16，行距1.2 大一点好看

+ **控制台字体**：Editor -- Color Scheme -- Console Font

+ **控制台颜色**：Editor -- Color Scheme -- Console Colors

+ **文件编码方式**：Editor -- File Encodings --> 全改成UTF-8，并勾选Transparent native-to-ascii conversion

其他：

+ Appearance & Behavior -- System Settings --> Startup/Shutdown -- Reopen last project on startup去掉，**开启IDEA时自动打开上次最后一个工程**
+ Editor -- General --> Mouse 勾选Change font size with Ctrl+Mouse Wheel按住Ctrl和鼠标滚轮可以**放大代码字体**
+ Editor -- General -- Appearance --> 勾选Show line numbers 显示行号；Show method separators 在**方法间显示分割线**
+ Editor -- Code Style -- Java --> Blank Lines将Keep Maximum Blank Lines中的3个2改成1（declarations，code，befor")"）：代码**格式化时将空行合并**
+ Editor -- Genral -- Code Completion -->将Match case的勾去掉：代码**提示的时候不匹配大小写**
+ Editor -- General -- Auto Import -->Java -- Insert imports on paste选为All：自动导包，**粘贴代码时自动导入之前需要的包**
+ 同页面勾选Add unambiguous imports on the fly和Optimize imports on the fly（for current project）
+ Editor -- General --> Other -- 勾选Show quick documentation on mouse move：**鼠标放在类名上可以看到快速文档**



+ 代码补充不区分大小写，Editor -- General -- Code Completion --> Case sensitive completion: None
+ 自动导包和删除无用的import，Editor -- General -- Auto Import --> Java --> Optimiaze imports on the fly  和  Add unambiguous imports on the fly
+ 代码默认展开还是折叠（勾选表示折叠），Editor -- General -- Code Folding --> Collapse by default
+ 同一个文件垂直分屏和水平分屏：右键标签，Split Vertically   / Split Horizontally
+ 快捷键设置， Settings -- Keymap -- 》
+ 多行tabs显示，Editor -- General -- Editor Tabs -- Tab Appearance -- Show tabs in single row
+ 软分行，代码左侧 soft-wrap



# 3 安装插件

首页 -- Configure -- Plugins 或 首页 -- Configure -- Settings--Plugins

| 名称                  | 简介                    | 备注                                    |
| --------------------- | ----------------------- | --------------------------------------- |
| background image plus | 背景图片                | 在performance，appearance里可以设置目录 |
| code glance           | 右侧导航条              |                                         |
| translation           | 右键翻译                | other settings里面设置翻译引擎          |
| grep console          | 日志显示颜色            | other里设置                             |
| statistic             | 代码统计信息            | 就在下面                                |
| restfultoolkit        | 接口搜索和调试          | command + \ 搜索                        |
| free mybatis plugin   | 可以从mapper直接跳到xml |                                         |

# 4 JDK环境配置

首页 -- Configure -- Project Defaults -- Project Structure -- Project Settrings -- Project --> Project SDK -- New -- 本地JDK的安装路径【Ctrl+Alt+Shift+S可快捷进入该界面】

## 4.1 配置JVM参数

可提高响应速度
Help -- Edit Custom VM Options
-Xms和-Xmx：占用的内存，最小和最大，可改为1024m与2048m，ReservedCodeCacheSize = 500m

# 5 创建JavaSE工程

首页 -- Create New Project -- 左侧选JAVA，JDK版本选择，Next，Next，Project name和location进行命名和选择存储位置

## 5.1 打开菜单：

View -- appearance 中 Toolbar和Tool Buttons选上

## 5.2 创建JAVA文件

在src文件夹上右键，New，Java Class，指定类名的时候可以同时指定包名，即Name中可以填写完整的类名

## 5.3 几个快捷键入，后缀补全等

+ Main函数
快捷键:
psvm或main回车即可
+ System.out.println()
sout
+ IDEA会自动保存，不需要频繁的Ctrl+S
+ 运行代码：在类和方法的左边有绿色的小箭头，或Ctrl+Shift+F10
+ `5.fori`快速生成for循环



```
.var 声明
.null 判空
.notnull 判非空
.nn 同上，判非空
.for
.fori
.not 取反
布尔表达式后面  .if 条件判断
.cast 强转
.return 返回


```



# 6 Debug的使用

打断点：左侧直接点一下
F7：执行一行，且会进入到方法内部
F8：执行一行，不会进到方法内部
F9：直接跳到下一个断点

# 7 创建JavaWeb工程

Create New Project -- 左侧Java -- 右侧勾选Web Application -- 点上方Java EE -- 指定相应版本 -- 再点击 Web Application -- 选择servlet版本
部署工程：上方有个下拉列表，点击 -- Edit Configurations -- 左上角加号 -- 最下方34 items more -- Tomcat Server -- Local
指定server环境：Application server右侧的Configure，指定Tomcat的安装路径
指定部署的项目：直接在下方点击FIX
其他：
Open browser：打开浏览器
On 'Update' action：Redeploy
On frame deactivation：Update Classes and resources
选择后，更新代码后不用重启，自动发布
【乱码可能是Tomcat的编码格式有问题】

## 7.1 为JavaWeb工程添加第三方依赖

在WEB.INF文件夹下创建lib文件夹，向其中拷贝jar包。点击上方的Project Structures（Ctrl+Alt+Shift+S）【右下角有很多格子的一个按钮】--左侧Libraries--点左边中间上面的加号--Java--找到刚才创建的lib文件夹--OK--Apply--左侧Modules--勾选lib并Apply

## 7.2 创建Servlet

https://www.bilibili.com/video/av21735428?p=13

# 8 Maven的配置

首页-Configure-Settings -- Build，Execution， Deployment -- Build Tools -- Maven -->可以更改maven版本，更改配置文件，更改本地仓库位置

## 8.1 使用Maven创建JavaSE工程

New Project -- 左侧找到Maven -- 勾选Create from archetype选择骨架 -- 找到quickstart -- 指定Groupid和Artifactid --  等待 下面有进度条，如果出错失败的话，控制台输入： mvn -U idea：idea -- 可以在settings里写阿里云镜像 -- 右下角Maven projects need to be imported 选择Enable Auto-Import
## 8.2 Maven菜单项的介绍

右侧：Maven Projects里有一些快捷按钮
第一个：刷新
点开工程有一些Maven操作，双击即可
第三个：下载源码或文档
第六个（方块的样子，下面有个蓝色的m）：自己输入Maven命令
选择当前工程后，会多出来一个按钮（倒数第三个），可以显示依赖关系

## 8.3 使用Maven创建JavaWeb工程

https://www.bilibili.com/video/av21735428?p=17
在Maven骨架选择的webapp
新建的写代码的java文件夹，右键单击，Mark Directory as 选择 Source Root

## 8.4 使用Maven创建聚合工程

https://www.bilibili.com/video/av21735428?p=18

# 10 使用GIT管理代码

开启版本控制：上方菜单VCS -- Enable Version Control Integration -- 下拉列表中选择git
忽略文件 File -- Settings -- Version Control -- Ignored Files -- 点右侧的加号 -- 第一个忽略文件iml，第二个忽略文件夹.idea
上传到本地git仓库：VCS -- commit -- 选择上传文件（可以全选），填写信息
上传到远程仓库：VCS -- Git -- Push -- Define remote -- URL中输入远程仓库地址（如https://github.com/user/a.git，在github网页上可以找到的样子） -- 点击右下角push -- 输入GitHub账户密码

# 11 IDEA常用快捷键

File -- Settings：
Editor--Font
Keymap：小齿轮点一下Duplicate，复制一份快捷键。Main menu--Code--Completion--Basic：双击，Remove，Add，Alt+/

| 快捷键               | 功能                             |
| -------------------- | -------------------------------- |
| `Alt+Enter`          | 导入包，自动修正代码             |
| `Ctrl+Y`             | 删除光标所在行                   |
| `Ctrl+D`             | 重复当前行                       |
| `Ctrl+Alt+L`         | 格式化代码                       |
| `Ctrl+/`             | 单行注释                         |
| `Ctrl+Shift+/`       | 多行注释`/*  */`                 |
| `Alt+Ins`            | 自动生成toString，get，set等方法 |
| `Alt+Shift+上下箭头` | 移动当前代码行                   |
| `Shift+F6`           | 变量重构重命名                   |

# 12 IDEA导入和关闭项目

模块的导入：
Project Structure里，Module，+，import

# 13 开发工具概述

项目project-->模块module-->包package

# 14 IDEA内存调整

```
Help` --> `Diagnostic` --> `Change memory settings
```

把内存设大一点，IDEA自己跑起来会快

# 15 render documentation comments

让注释变成java doc的格式

Editor -- Appearance

# 16 Live Templates

Editor -- Live Templates

找一下有没有user，没有就+一个

写完在define记得选Java

常用的：

```
@tr
@JsonDeserialize(using = TrimDeserializer.class)


aslist
Arrays.asList($start$)

reok
return RespUtil.respOk();

rerr
return RespUtil.respError($END$);

```

# 17 Code Template

Settings -File and Code Templates -Code (tab) -JUnit4 Test Class 

可以修改JUnit的模板代码

# 18 变量快速处理

```
.var
.par  圆括号
.cast / castvar 强转
.fori / forr
.sout / soutv
.lambda
.try
.switch
.return
```

## var出现final的问题

1. 保证 settings -> editor -> code style -> java 里的 Final Modifier 中的 Make generated local variables final 和 parameters final 不勾选
2. 生成变量出现final的时候，按下Alt+F，或者取消上方出现的Declare final的勾

# 只格式化自己的代码

在这种情况下，您可以使用**⌥⇧⌘L** (macOS) 或**Ctrl+Alt+Shift+L** (Windows/Linux) 调出重新格式化选项对话框：
