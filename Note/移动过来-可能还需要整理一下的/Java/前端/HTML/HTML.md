# Web标准

W3C做出了对Web的标准。包括：结构标准、表现标准、行为标准，即HTML、CSS、JS。浏览器的实现需要遵守该标准。

HTML定义对网页的结构，CSS定义样式，JS定义行为。

# HTML

是最基础的网页开发语言，全称 Hyper Text Markup Language 超文本标记语言。

+ 超文本：不止文本，还包括图片、音频等多媒体。并且可以用超链接，将各种不同的、不同空间的文本信息组织在一起。

+ 标记语言：由标签构成的语言。如html，xml。标记语言不是编程语言。

文档后缀：`.html`或`.htm`

# 作用

**负责描述文档的语义，主要用于标记。提供网页的结构。**

标记这部分内容为“标题”，这部分为“段落”。

# 元素

![HTML元素](html元素.png)

开始标签/标记、内容、结束标签，共同组成一个HTML元素。

## 标签

+ 标签分为：

  + 围堵标签 / 双边标记 / 双标签：有开始标签和结束标签。如`<html> <\html>`，里面有内容。

  + 自闭合标签 / 单边标记 / 单标签：只有一个标签，开始标签和结束标签在一起。`<br\>`，里面没有内容。

+ 标签可以嵌套

+ 标签不区分大小写，但是**建议使用小写**

### 属性

标签有属性，作为辅助信息。在开始标签中定义，由键值对构成，值需要用引号（单双都可以）引起来

属性名称不区分大小写，但是**属性值区分大小写**

# 注释

```html
<!-- 注释的内容 -->
```

# 骨架

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
    <title>Document</title>
</head>
<body>

</body>
</html>
```

`<html>`：根标签，页面内最大的标签

`<head>`：必须设置`<title>`，网页的标题

可以看到html骨架是根据人的身体来命名的

## 语法规范版本

HTML文件的第一行`<!DOCTYPE>`会声明HTML的规范版本。DocType Declaration，DTD。

HTML有众多版本，但是html的语法并不是很严格。

另外，html5已不支持的语法，浏览器依旧可以显示，浏览器会向下兼容

## html标签

属性lang用于制定页面的语言类型，最常见的2个：

+ `en`：英语
+ `zh-CN` / `ch`：中文

## head标签

通常在这里配置 字符集、关键词、页面描述、页面标题、IE适配、视口、iPhone小图标等等。

常用的有：

```html
<!-- 字符集 -->
<meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
<!-- 移动端使用 -->
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<!-- 搜索引擎SEO里的说明文字 -->
<meta name="Description" content="网易是中国领先的互联网技术公司，为用户提供免费邮箱、游戏、搜索引擎服务，开设新闻、娱乐、体育等30多个内容频道，及博客、视频、论坛等互动交流，网聚人的力量。" />
<!-- 3s后刷新跳转到百度 -->
<meta http-equiv="refresh" content="3;http://www.baidu.com">
<!-- 标题 -->
<title>网页的标题</title>
<!-- 文档内所有超链接标签的基础路径 -->
<base href="/">
```

# 标签

## 标签全局属性

所有标签都有以下属性（仅列举常用的）：

+ `class`：指定元素的类，用空格隔开的列表。允许CSS和JS通过类选择器或类似`Document.getElementsByClassName()`的函数来选择和访问特定元素。

+ `id`：定义一个唯一标识符，该标识符在文档内唯一。用于在链接定位、JS脚本、CSS样式中识别出元素。

+ `style`：声明该元素的CSS样式。和`<style>`的主要目的是允许快速设置，便于测试。

+ `data-*`：自定义属性，可以在js里通过`label.*`来获取属性

+ `draggable`：布尔，设置元素是否可以拖拽

+ 

[形成一类属性，称为自定义数据属性，允许在HTML](https://developer.mozilla.org/en-US/docs/Web/HTML)和其[DOM](https://developer.mozilla.org/en-US/docs/Glossary/DOM)表示之间交换专有信息，这些信息可能由脚本使用。所有此类自定义数据都可通过[`HTMLElement`](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement)设置属性的元素的接口获得。属性[`HTMLElement.dataset`](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/dataset)允许访问它们。

## 标签的分类

标签分为两类：

- 块级元素 / 容器级标签：在新的一行开始，宽度占据整行，可以包含其他块级元素和行内元素
- 行内元素：同一行内呈现，不会单独占据一行，只占据内容需要的宽度，不能包含块级元素

常见的块级元素有：`div / h1-h6 / p / ul / ol / li / table / form`

常见的行内元素有：`span / a / strong / em / img / br / input`

块级元素 和 行内元素 的本质区别在于是否会独占一行。而包含关系能力并不是这个分类的核心。

虽然用`div`和`span`可以灵活地对网页的行块关系进行表述，但是HTML的核心作用还是对网页进行语义化描述。所以虽然`p`和`h1`都是块元素，但是在`p`内包括`h1`并不是一个合理的情况，所以标准（浏览器）并不支持这样的写法。

## 块级元素 

### h1 - h6 标题标签

定义标题。

### p 段落标签

paragraph

### hr 水平线标签

horizontal rule 水平线将文档分割

### br 换行标签

写为`<br/>`和`<br>`都可以

在网页中，另起一个段落应该用2个`<p>`，而不是用`br`，尽量不用

### div

content division 分割，把标签中的内容分割成独立的区块。

#### h5语义化标签

- `<section>` 表示区块
- `<article>` 表示文章。如文章、评论、帖子、博客
- `<header>` 表示页眉
- `<footer>` 表示页脚
- `<nav>` 表示导航
- `<aside>` 表示侧边栏。如文章的侧栏
- `<figure>` 表示媒介内容分组。
- `<mark>` 表示标记 (用得少)
- `<progress>` 表示进度 (用得少)
- `<time>` 表示日期

本质上新语义标签与`<div>`、`<span>`没有区别，只是其具有表意性，使用时除了在HTML结构上需要注意外，其它和普通标签的使用无任何差别，可以理解成`<div class="nav">` 相当于`<nav>`。

### ul 无序列表 unordered list

每一项是`li`，list item

+ `ul`的子标签只能是`li`
+ `li`只能在`ul / ol`内
+ `li`是一个块级元素，里面什么都能放

### ol 有序列表 ordered list

属性：

+ `type`：序号样式，可以有`1 / a / A / i / I`，分别是阿拉伯数字 / 小写字母 / 大写字母 / 小写罗马数字 / 大写罗马数字
+ `start`：从几开始，值为数字
+ `reversed`：布尔，序号从大到小

#### li 列表项 list item

对于有序列表中的`li`，还有`value`和`type`属性。

+ `value`：当前项的编号，值为数字
+ `type`：同`ol`

### dl 描述列表 Description List

子元素只能是`dt`和`dd`

`dt`：description term，要描述的术语，必须要有

`dd`：description detail，要描述的细节，可选

### table 表格标签

一个表格由`tr` table row 组成，一个`tr`由`td` table data cell 组成。

#### tr 表格行 table row

#### td 单元格 table data cell

属性：

- `colspan`：横向合并。例如`colspan="2"`表示当前单元格在水平方向上要占据两个单元格的位置。
- `rowspan`：纵向合并。例如`rowspan="2"`表示当前单元格在垂直方向上要占据两个单元格的位置。
- `headers`：标识该单元格是哪个`<th>`的，无视觉效果。

#### th 表格头 table header

属性：

- `colspan`：横向合并。例如`colspan="2"`表示当前单元格在水平方向上要占据两个单元格的位置。
- `rowspan`：纵向合并。例如`rowspan="2"`表示当前单元格在垂直方向上要占据两个单元格的位置。
- `headers`：标识该单元格是哪个`<th>`的，无视觉效果。
- `scope`：定义标题所涉及到的单元格
  - `row`：标题和所在行相关
  - `col`：标题和所在列相关
  - `rowgroup`：和一组行的所有单元格相关
  - `colgroup`：和一组列的所有单元格相关

#### caption 表格标题 table caption

和`tr`并列，指定表格的名称：表1-1 什么什么表

#### 表格的`<thead>`标签、`<tbody>`标签、`<tfoot>`标签

这三个标签有与没有的区别：语义化标签

- 1、如果写了，那么这三个部分的**代码顺序可以任意**，浏览器显示的时候还是按照thead、tbody、tfoot的顺序依次来显示内容。如果不写thead、tbody、tfoot，那么浏览器解析并显示表格内容的时候是从按照代码的从上到下的顺序来显示。
- 2、当表格非常大内容非常多的时候，如果用thead、tbody、tfoot标签的话，那么**数据可以边获取边显示**。如果不写，则必须等表格的内容全部从服务器获取完成才能显示出来。

### form 表单标签

表单就是让用户填写、选择，收集用户信息的。

属性：

- `action`：指定提交数据的url
- `method`：表单数据的提交方式，常用GET（默认） / POST

#### input 文本输入框

`<input>`工作方式取决于属性`type`属性的值。默认是`text`。

| Type                                                         | 描述                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| text                                                         | 默认，文本                                                   |
| password                                                     | 密码类型                                                     |
| radio                                                        | 单选按钮，相同的`name`按钮可以互斥                           |
| checkbox                                                     | 多选按钮，相同的`name`作为一组                               |
| hidden                                                       | 隐藏框，表单中包含不希望用户看见的信息                       |
| button                                                       | 普通按钮                                                     |
| submit                                                       | 提交按钮，不写`value`就自动会有“提交”文字。点击后表单会提交到`<form>`标签的`action`属性指定的地方 |
| reset                                                        | 充值按钮，清空表单内容，并设置为最初的默认值                 |
| image                                                        | 图片按钮，和提交按钮功能完全一样                             |
| file                                                         | 文件选择框                                                   |
| date                                                         | 选择日期，年月日                                             |
| datetime-local                                               | 日期，包括时分秒                                             |
|                                                              |                                                              |
|                                                              |                                                              |
| image<br/>	图片提交按钮<br/>	src属性:<br/>		指定图片的路径 |                                                              |

属性：

| 属性        | Type                                                         | 描述                                                         |
| ----------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| checked     | `checkbox / radio`                                           | 将单选按钮或多选按钮默认处于选中状态                         |
| name        | 所有                                                         | form的名称，提交时会将 name/value 作为一对一起提交<br />表单项中的数据想要被提交，必须指定其name属性 |
| value       | 除了 image 以外的所有                                        | 文本框中的默认内容                                           |
| size        | text / search / url / tel / email / password                 | 文本框可以显示的字符数                                       |
| readonly    | 除了 hidden / range / color /checkbox / radio / 按钮类 以外的所有 | 只读，不能编辑                                               |
| disabled    | 所有                                                         | 只读，不能编辑，点不了                                       |
| placeholder | text`, `search`, `url`, `tel`, `email`, `password`, `number  | 输入框的提示信息，只在无内容的时候显示                       |

#### select 下拉列表标签

里面每一项用`<option>`表示。

- `multiple`：布尔，是否多选。多选时通常表现为一个滚动条的列表盒子。
- `size="3"`：如果属性值大于1，则列表为滚动视图，表示一次性可以看见的条数。默认属性值为0，即下拉视图。（根据规范，默认值应该是1，但是有的网站在1的情况下会崩溃，所以Firefox目前还是默认实现为了0）

##### option 选项

- `selected`：布尔，是否预选

#### datalist 数据列表

和`<select>`一样

#### textarea 多行文本输入框

属性：

- `rows="4"`：指定文本区域的行数。
- `cols="20"`：指定文本区域的列数。
- `readonly`：只读。

#### fieldset 一组表单

可以将多个`<input>`形成一组，用`<legend>`可以起一个标题

#### label 标签

用`<label for="id">`可以将`label`标签和一个表单元素绑定在一起，这样点击`<label>`里的文字，就可以选中对应的选项框









**label**

```
label
	指定输入项的文字描述信息
	for属性：
		与input的id属性值对应。对应后，点击label区域，会让input输入框获得焦点。【id可以是一个字符串】
```

+ **select：下拉列表**

```
子元素：option
	指定列表项
        value
        	指定提交值
        selected
        	默认值

textarea
	文本域

cols
	指定列数，每行有多少个字符

rows
	默认多少行
```



## 行内元素

### span

span 范围，跨度，和div作用一样，但是不换行。

#### div 和 span 的区别

1. `div`换行，`span`不换行
2. `div`作为块级元素，里面可以由别的块级元素；`span`作为行内元素，里面不能有`p / h / ul / dl / ol /div `等块级元素

这两个标签都是为了和css联动来实现各种样式的，默认不会增加任何效果。

### a 超链接

anchor，锚

属性：

+ `href`：hypertext reference，超文本地址，可以填外部url，本地文件，还可以跟上`#id`，跳转到指定`id`（`name`现在被`id`替代了）
+ `target`：用什么方式打开目标页面
  + `_self`：在同一个网页中显示，默认值
  + `_blank`：在新窗口打开
  + `_parent`：在父窗口中显示
  + `_top`：在顶级窗口中显示

### img 图片

image 图片

属性：

+ `src`：source，图片的路径，可以写相对路径或绝对路径
+ `width`：图像的宽度，单位像素。如果高度、宽度只指定了一个，浏览器会根据原始图像进行等比例缩放。
+ `height`：图像的高度，单位像素。
+ `alt`：alternate 替代，当图片不可用时，代替图片显示的内容

以下在现在都不太用了：

u 下划线

del 删除线

strong 加粗强调

em 倾斜强调

sup 上标

sub 下标

## 特殊字符

| 字符     | 说明                       |
| -------- | -------------------------- |
| `&nbsp;` | 空格，non-breaking spacing |
| `&lt;`   | 小于号`<`，less than       |
| `&gt;`   | 大于号`>`，greater than    |
| `&amp;`  | 符号`&`                    |

## 框架

内嵌框架用`<iframe>`表示。`<iframe>`是`<body>`的子标记。

内嵌框架inner frame：嵌入在一个页面上的框架(仅仅IE、新版google浏览器支持，可能有其他浏览器也支持，暂时我不清楚)。

**属性：**

- `src="subframe/the_second.html"`：内嵌的那个页面
- `width=800`：宽度
- `height=“150`：高度
- `scrolling="no"`：是否需要滚动条。默认值是true。
- `name="mainFrame"`：窗口名称。公有属性。

# 查看网页大纲的工具

我们可以通过 http://h5o.github.io/ 这个工具查看一个网页的大纲。

**使用方法**：

（1）将网址 http://h5o.github.io/ 里中间的部分拖到书签栏

（2）去目标网页，点击书签栏的网址，即可查看该网页的大纲。

这个工具非常好用，既可以查看网页的大纲，也可以查看 markdown 在线文档的结构。

