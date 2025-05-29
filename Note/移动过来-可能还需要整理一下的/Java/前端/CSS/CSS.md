
## 11 CSS：页面美化和布局控制

+ Cascading Style Sheets 层叠样式表

+ 层叠：多个样式可以作用在同一个html的元素上，同时生效

+ 好处：
1. 功能强大
2. 将内容展示与样式控制分离：降低耦合度，解耦，让分工协作更容易，提高开发效率

### 11.1 CSS的使用：CSS与html结合方式

1. 内联样式
    在标签内使用style属性指定css代码。【不推荐使用】

2. 内部样式
    在head标签内，定义style标签，```<style>```标签的标签体内容就是css代码

3. 外部样式
    先定义css资源文件，然后在head标签内，定义link标签，引入外部的资源文件
```
<link rel="stylesheet" href="css/a.css">

还有一种不太常用的写法
<style>
    @import "css/a.css"
</style>
```

### 11.2 CSS基本语法

```
选择器{
    属性名1：属性值1；
    属性名1：属性值1；
    ...
}
```

+ 选择器：筛选具有相似特征的元素
+ 注意：每一对属性要用分号隔开，最后一对可写可不写。
+ 注释：```/* */```

### 11.3 选择器

筛选具有相似特征的元素

#### 11.3.1 基础选择器

```
#id属性值{}
	id选择器：选择具体的id属性值的元素.多个属性用逗号隔开

标签名称{}
	元素选择器：选择具有相同标签名称的元素

.class属性值{}
	类选择器：选择具有相同的class属性值的元素
```

+ 一般设置id唯一，class可以多个共用
+ 优先级：id>类>元素

#### 11.3.2. 扩展选择器

```
*{}
	选择所有元素：

选择器1，选择器2{}
	并集选择器。【逗号】

选择器1 选择器2{}
	子选择器：筛选选择器1元素下的选择器2元素。【空格】

选择器1>选择器2{}
	父选择器：筛选选择器2的父元素选择器1。有属性first-child

元素名称[属性名=“属性值”]{}
	属性选择器：选择元素名称，属性名=属性值的元素

元素：状态{}
	伪类选择器：选择一些元素具有的状态。如超链接标签<a>上就常见。
    link：初始化的状态
    visited：被访问过的状态
    active：正在访问的状态
    hover：鼠标悬浮状态
```

### 11.4 属性

#### 11.4.1 字体、文本

```
font-size
	字体大小

color
	文本颜色

text-align
	对齐方式

line-height
	行高
```

#### 11.4.2 背景

```
background
	复合属性
	可以设置图片：url
```

#### 11.4.3 边框

```
border
	设置边框，复合属性
	边框有4条边，可以分别设置：border-bottom/left/right/type
	复合属性一次可以传入一个列表，如：
	border: 1px solid red;
```

#### 11.4.4 尺寸

```
height
	高度

width
	宽度
```

#### 11.4.5 盒子模型

```
margin
	外边距，复合属性。
	一个值会赋值给所有。left/bottom/right/top。auto，水平居中

padding
	内边距，复合属性。
	默认情况下内边距会影响整个盒子的大小。
	用box-sizing:border-box;设置盒子的属性，让width和height就是最终盒子的大小。

float
	浮动
    left
	    左浮动。有点像左对齐的感觉，位置够就会并在一行。
    right
    	右浮动。
```











































# CSS Reset

HTML中，比如下拉框这种比较复杂的元素，是自带默认样式的。如果没有这个默认样式，则该元素在页面上不会有任何表现，则必然增加一些工作量。

同时，默认样式也会带来一些问题：比如，有些默认样式我们是不需要的；有些默认样式甚至无法去掉。

如果我们不需要默认的样式，这里就需要引入一个概念：**CSS Reset**。

## 方案一

CSS Tools: Reset CSS。链接：https://meyerweb.com/eric/tools/css/reset/

## 方案二

雅虎的 CSS Reset。链接：https://yuilibrary.com/yui/docs/cssreset/

我们可以直接通过 CDN 的方式引入：

```html
<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/3.18.1/build/cssreset/cssreset-min.css">
```

## 方式三

```css
*{
    margin: 0;
    padding: 0;
}
```

这写法，比较简洁，但也有争议。有争议的地方在于，可能会导致 css 选择器的性能问题。

## Normalize.css

上面的几种 css reset 的解决思路是：将所有的默认样式清零。

但是，[Normalize.css](https://necolas.github.io/normalize.css/) 的思路是：既然浏览器提供了这些默认样式，那它就是有意义的。**既然不同浏览器的默认样式不一致，那么，`Normalize.css`就将这些默认样式设置为一致**。
