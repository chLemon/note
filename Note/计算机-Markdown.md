目录

- [简介](#简介)
- [1. 基础语法](#1-基础语法)
    - [1.1. 标题](#11-标题)
        - [1.1.1. 标题效果](#111-标题效果)
            - [1.1.1.1. 标题效果](#1111-标题效果)
    - [1.2. 文字效果](#12-文字效果)
    - [1.3. 插入链接](#13-插入链接)
        - [1.3.1. 链接](#131-链接)
        - [1.3.2. 图片](#132-图片)
        - [1.3.3. 引用和脚注](#133-引用和脚注)
    - [1.4. 文字内容](#14-文字内容)
        - [1.4.1. 区块](#141-区块)
        - [1.4.2. 代码块](#142-代码块)
            - [1.4.2.1. 分割线](#1421-分割线)
        - [1.4.3. 无序列表](#143-无序列表)
        - [1.4.4. 有序列表](#144-有序列表)
        - [1.4.5. 列表嵌套](#145-列表嵌套)
        - [1.4.6. 表格](#146-表格)
        - [1.4.7. 换行缩进以及空格](#147-换行缩进以及空格)
        - [1.4.8. 支持部分 HTML 元素](#148-支持部分-html-元素)
            - [1.4.8.1. 居中](#1481-居中)
            - [1.4.8.2. button 符号](#1482-button-符号)
            - [1.4.8.3. 转义](#1483-转义)
        - [1.4.9. 公式](#149-公式)
- [2. 画图 mermaid](#2-画图-mermaid)
- [3. VS Code 支持 和 相关插件](#3-vs-code-支持-和-相关插件)

# 简介

Markdown是一种轻量级标记语言，指定一些文档格式。

根据这个语言写文档，可以方便地渲染成还挺好看的文档。Github 上就常使用这个来写 README。

# 1. 基础语法

## 1.1. 标题

```
## 一级标题
### 二级标题
```

或

```
一级标题
====
二级标题
---
```

### 1.1.1. 标题效果

#### 1.1.1.1. 标题效果

## 1.2. 文字效果

```
*斜体*
**粗体**
***粗斜体***
以上*均可以换成下划线_

~~删除线~~
<u>下划线</u>
```

_斜体_

**粗体**

**_粗斜体_**

~~删除线~~

<u>下划线</u>

## 1.3. 插入链接

### 1.3.1. 链接

```
[链接名称](网址 "可以不写的title，鼠标放在链接上会显示出来的文字")

<链接>

网址还可以用 <> 包裹，在一些 url 上有特殊字符或者空格的时候
```

[链接名称](网址 "可以不写的title，鼠标放在链接上会显示出来的文字")


### 1.3.2. 图片

```
![名称](链接 “title”)

或：

[名称][代号]

[代号]：链接 “title”
```

![名称](链接 "title")

### 1.3.3. 引用和脚注

```
引用和脚注：
名词[^代号]

[^代号]：内容
在正文中[^代号]会自动编号成数字
```

代号[^1]

[^1]: 内容

## 1.4. 文字内容

### 1.4.1. 区块

```
>123
>>123
>>>123
有的需要跟空格
```

> 123
>
> > 123
> >
> > > 123

### 1.4.2. 代码块

````
代码块：用反引号，1左边的

`代码`

​```这里还可以指定语言
代码
​```

程序代码区块
四个空格或一个Tab
````

`代码`

```java
代码
```

    代码

#### 1.4.2.1. 分割线

```
***
---
___
三个以上的*-_可以建立分割线，这些符号中可以加入空格
```

---

---

---

### 1.4.3. 无序列表

```
*-+[空格]文字
```

-   无序列表

### 1.4.4. 有序列表

```
数字. 文字
```

1. 有序列表

### 1.4.5. 列表嵌套

```
下级列表加空格【不同编辑器不太一样，反正在下面和上一级的后面加几个空格试一试就好了】
子列表前加4个空格
```

-   列表
    -   子列表
        -   子子列表

### 1.4.6. 表格

```
----分割表头和其他行
|分割不同单元格
：在两边，居中 在右边，右对齐
```

| 表格表头 |      |
| -------- | :--: |
| 表格内容 | 居中 |

### 1.4.7. 换行缩进以及空格

```
换行：2个以上空格+回车
缩进：&emsp 一个中文字符大小
&ensp 半个中文字符
&nbsp 四分之一个
```

### 1.4.8. 支持部分 HTML 元素

#### 1.4.8.1. 居中

```
<div align=center>居中</div>
```

<div align=center>居中</div>

#### 1.4.8.2. button 符号

```
<kbd>Alt</kbd>
```

<kbd>Alt</kbd>

#### 1.4.8.3. 转义

```
\
```

### 1.4.9. 公式

```
$$
LaTex语法公式
$$
```

$$
LaTex语法公式
$$

# 2. 画图 mermaid

[计算机-mermaid](计算机-mermaid/)

# 3. VS Code 支持 和 相关插件

目前 VS Code 已经原生支持了 markdown 的一些内容。

> https://code.visualstudio.com/docs/languages/markdown


Code Spell Checker - Spelling checker for source code.
Markdown Checkboxes - Adds checkbox support to the VS Code built-in Markdown Preview.
Markdown Emoji - Adds emoji syntax support to Markdown Preview and notebook Markdown cells.
Markdown Footnotes - Adds ^footnote syntax support to the Markdown Preview.
Markdown Preview GitHub Styling - Use GitHub styling in the Markdown Preview.
Markdown Preview Mermaid Support - Mermaid diagrams and flowcharts.
Markdown yaml Preamble - Renders YAML front matter as a table.
markdownlint - Markdown linting and style checking for Visual Studio Code.
Word Count - View the number of words in a Markdown document in the Status Bar.
Read Time - Estimate how long it takes to read your Markdown.

