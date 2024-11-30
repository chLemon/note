# JavaScript

+ 概念：一门客户端脚本语言

+ 运行在客户端浏览器中的。每一个浏览器都有JS的解析引擎。

+ 脚本语言：不需要编译，直接就可以被浏览器解析执行

+ 功能：可以增强用户和html页面的交互过程，可以控制html元素，让页面有一些动态效果，增强用户的体验。

**JavaScript = ECMAScript + JavaScript自己特有的东西（BOM + DOM）**

# 1 ECMAScript

客户端脚本语言的标准

## 1.1 基本语法

### 1.1.1 与html的结合方式：

1. 内部JS：定义```<script>  </script>```，标签体内容就是js代码

2. 外部JS：定义```<script>  </script>```，通过src属性引入外部的js文件

**注意：**

+ ```<script>```可以定义在html页面的任何地方，但是定义的位置会影响执行顺序。
+ 可以定义多个```<script>```

### 1.1.2. 注释

和java一样

### 1.1.3. 数据类型：

+ 原始数据类型

  1. number：数字。整数/小数/NaN(not a number)
  2. string：字符串。没有字符。
  3. boolean：true/false
  4. null：对象为空
  5. undefined：未定义。如果一个变量没有给初始化的值，那么默认赋值为undefined。

+ 引用数据类型：对象

### 1.1.4. 变量：弱类型

```
var 变量名 = 初始化值;
```

```
document.write(a);
	换行用<br>

typeof(a)
	显示a的类型
```

### 1.1.5. 运算符

1. 一元运算符
   在JS中，如果运算数不是运算符所要求的类型，那么JS引擎会自动的将运算数进行类型转换。
   + string转number：按字面值转换。如果不是数字，转换为NaN，NaN与任何数运算还是NaN。
   + boolean转number：true转为1，false转为0
2. 算术运算符
3. 赋值运算符
4. 比较运算符
   ```===```：全等于
   + 类型相同，直接比较。字符串会按字典顺序，逐位比较。
   + 类型不同，先进行类型转换，再比较。

   + 全等于会先判断类型，类型不一样则直接返回false。
5. 逻辑运算符
    其他类型转boolean：
   + number：0或NaN为假，其他为真。
   + string：除了空字符串```""```，其他都是true。
   + null&undefined：都是false。
   + 对象：所有对象都是true。
6. 三元运算符
    ```boolean ? a : b ```

### 1.1.6. 流程控制语句

JS里switch语句没有类型限制。

### 1.1.7. 特殊语法

1. 句尾的分号可以省略（不建议）
2. 定义变量的时候，如果不写var，是全局变量，写var是局部变量。

## 1.2. 基本对象

### 1.2.1 Function：函数对象

1. 创建
```
var fun = new Function(形参列表，方法体);//这种方法不用

function 方法名称(形参列表){
    方法体
}

var 方法名 = function(形参列表){
    方法体
}
```
2. 方法
3. 属性
```length：形参的个数```

4. 特点
   + 方法定义的时候，形参的类型不用写，返回值类型也不写
   + 方法是一个对象，如果定义名称相同的方法，会覆盖
   + 在JS中，方法的调用只与方法的名称有关，和参数列表无关
   + 在方法声明中有一个隐藏的内置对象：数组arguments，封装了所有的实际参数
5. 调用
```
方法名称(实际参数列表);
```

### 1.2.2 Array：数组对象

1. 创建
```
var arr = new Array(元素列表);

var arr = new Array(默认长度);

var arr = [元素列表];
```
2. 方法
```
join(参数)
	将数组中的元素按照指定的分隔符拼接成字符串（默认为逗号）

push()
	向数组的末尾添加一个或更多元素，并返回新的长度。
```
3. 属性
```length：数组的长度```
4. 特点
   + 在JS中，数组的元素的类型可变
   + 在JS中，数组的长度可变

### 1.2.3 Boolean

### 1.2.4 Date

1. 创建
```
var data = new Date();
```
2. 方法
```
toLocaleString()
	返回当前Date对象对应的时间本地字符串格式
getTime()
	获取毫秒值。
```

### 1.2.5 Math

1. 创建
不用创建，直接使用。Math.方法名()

2. 方法
```
random():返回0~1之间的随机数。含0不含1
ceil(X)：向上取整
floor(X)：向下取整
round(x)：四舍五入
```
3. 属性
```PI```

### 1.2.6 Number

### 1.2.7 String

### 1.2.8 RegExp：正则表达式对象

正则表达式：

+ 单个字符：[ ]
如```[a] [ab] [a-zA-Z0-9_]=\w \d```
+ 量词符号：
```
?
	0/1
*
	任意
+
	1+
{m,n}
	m到n位，包含两边
```
+ 开始结束符号：```^ $```

RegExp：

1. 创建
```
var reg = new RegExp("正则表达式");//这里要注意，\表示转义字符，\w要写成\\w

var reg = /正则表达式/;常用这个
```
2. 方法
```
test(参数)
	验证指定的字符串是否符合正则表达式
```

### 1.2.9 Global：全局对象

其中封装的方法不需要对象，直接调用。```方法名();```
```
encodeURI():URI编码
decodeURI():URI解码

encodeURIComponent():URI编码，冒号等也编码
decodeURIComponent():URI解码，冒号等也编码

parseInt():字符串转为数字。会逐一判断每个字符是否是数字，直到不是数字为止，将前边数字部分转为number

isNaN():判断一个值是否是NaN。NaN六亲不认，参与的比较全是false

eval：将字符串转换为JS脚本代码来执行
```

URL对中文进行编码，一个百分号是一个字节

# 2 BOM

+ 概念：Browser Object Model 浏览器对象模型
+ 将浏览器的各个组成部分封装成对象。

Window：窗口对象
Navigator：浏览器对象
Screen：显示器屏幕对象
History：历史记录对象
Location：地址栏对象

## 2.1 Window

窗口对象

### 2.1.1 创建

不需要创建

### 2.1.2 方法

1. 与弹出框有关的方法
```
alert()
	显示带有一段消息和一个确认按钮的警告框

confirm()
	显示带有一段消息以及确认按钮和取消按钮的对话框
	如果用户点确定，方法返回true，用户点取消，方法返回false

prompy()
	显示可提示用户输入的对话框
	返回值：用户的输入
```
2. 与打开关闭有关的方法
```
close()
	关闭浏览器窗口
    谁调用，关闭谁
open()
    打开一个新的浏览器窗口
    返回新的window对象
```
3. 与定时器有关的方法
```
setTimeout()
    在指定的毫秒数后调用函数或计算表达式
    参数
        1. js代码或方法对象
        2. 毫秒值
    返回值：唯一标识，用于取消定时器

clearTimeout()
    取消setTimeoutsetTimeout()方法设置的timeout

setInterval()
	按指定的周期（毫秒计）来调用函数或计算表达式

clearInterval()
	取消setInterval()方法设置的timeout
```

### 2.1.3 属性

1. 获取其他BOM对象
```
history
location
Navigator
Screen
```
2. 获取DOM对象
```
document
```
### 2.1.4 特点

+ window对象不需要创建，可以直接使用。
```
window.方法名()
```
+ window引用也可以省略，直接
```
方法名()
```

## 2.2. Navigator：浏览器对象

## 2.3. Screen：显示器屏幕对象

## 2.4. History：历史记录对象

### 2.4.1 创建（获取）

```
window.history
或
history
```

### 2.4.2. 方法

```
back()
	加载history列表中的前一个URL

forward()
	加载history列表中的后一个URL

go(参数)
	加载history列表中的某个具体页面
    参数：
	    正数：前进几个历史记录，go(1)=forward()
    	负数：后退几个历史记录
```

### 2.4.3. 属性

```
length
	返回当前窗口历史列表中的URL数量
```

## 2.5. Location：地址栏对象
### 2.5.1. 创建（获取）

```
window.location
或
location
```

### 2.5.2. 方法

```
reload
	重新加载当前文档。刷新
```

### 2.5.3. 属性

```
href
	设置或返回完整的URL
```

# 3 DOM

+ 概念：Document Object Model 文档对象模型
+ 将标记语言文档的各个组成部分，封装为对象。可以使用这些对象，对标记语言文档进行CRUD的动态操作
+ 功能：控制html文档的内容

W3C DOM 标准被分为3个不同的部分：

+ 核心 DOM：针对任何结构化文档的标准模型
   + Document：文档对象
   + Element：元素对象
   + Attribute：属性对象
   + Text：文本对象
   + Comment：注释对象

   + Node：节点对象，其他5个对象的父对象
+ XML DOM：针对XML文档的标准模型
+ HTML DOM：针对HTML文档的标准模型

## 3.1 DOM 使用简单流程

获取页面标签（元素）对象：Element
```
document.getElementById("id值")：通过元素的id获取元素对象
```

操作Element对象：
1. 修改属性值：
   + 明确获取的对象是哪一个？
   + 查看API文档，找其中有哪些属性可以设置

2. 修改标签体内容：
    属性：```innerHTML```
   + 获取元素对象
   + 使用innerHTML属性修改标签体内容

## 3.2 核心DOM模型

### 3.2.1 Document：文档对象

1. 创建（获取）
在html dom模型中，可以使用window对象来获取

2. 方法

+ 获取Element对象
```
getElementById()
	根据id属性值获取元素对象，id属性值一般唯一

getElementByTagName()
	根据元素名称获取元素对象们，返回值是一个数组

getElementByClassName()
	根据Class属性获取元素对象们，返回值是一个数组

getElementByName()
	根据name属性获取元素对象们，返回值是一个数组
```

+ 创建其他DOM对象
```
createAttribute()
createComment()
createElement()
createTextNode()
```

### 3.2.2 Element：元素对象

1. 创建（获取）：通过document来获取和创建
2. 方法
```
removeAttribute()：删除属性

setAttribute()：设置属性
```

### 3.2.3 Node：节点对象，其他5个的父对象

1. 特点：所有dom对象都可以被认为是一个节点
2. 方法
CRUD dom树
```
appendChild()
	向节点的子节点列表的结尾添加新的子节点

removeChild()
	删除（并返回）当前节点的指定子节点

replaceChild()
	用新节点替换一个子节点
```
3. 属性
```
parentNode 返回节点的父节点
```

### 3.2.4 其他

超链接
```
href = "javascript:void(0)"; //可以被点击的样式，但是不跳转
```
+ value属性获取内容
+ this获取当前对象

## 3.3 HTML DOM

1. 标签体的设置和获取：innerHTML
```
var div = document.getElementById("div1");
var innerHTML = div.innerHTML;
```
2. 使用html元素对象的属性
```
div.innerHTML = "<input type='text'>";
```
3. 控制元素样式
   + 使用元素的style属性来设置（每个元素都有这个属性，后面直接点CSS的属性）
   + 提前定义好类选择器的样式，通过元素的className属性来设置其class属性值
```
div.style.border="1px solid red";

div.className = "cls";
```

# 4 事件

功能：某些组件被执行了某些操作后，触发某些代码的执行。

## 4.1 简单流程

如何绑定事件：
1. 直接在html标签上，指定事件的属性（操作），属性值就是js代码
```
<a href="..." onclick="js代码">
```

2. 通过js获取元素对象，指定事件属性，设置一个函数
```
document.getElementById("01").onclick=function(){
    ...
}
```

debug：正常打断点，然后在浏览器按下F12，在Console里看

## 4.2 事件监听机制

+ 事件：某些操作
+ 事件源：组件
+ 监听器：代码
+ 注册监听：将事件，事件源，监听器结合在一起。当事件源上发生了某个事件，则触发执行某个监听器代码。

## 4.3 常见的事件

## 4.3.1 点击事件

```
onclick：单击事件

ondbclick：双击事件
```

## 4.3.2. 焦点事件

```
onblur:失去焦点：一般用于表单校验

onfocus:元素获得焦点
```

## 4.3.3. 加载事件

```
onload
	一张页面或一幅图像完成加载
	window.onload = ..
```

## 4.3.4. 鼠标事件

```
onmousedown：鼠标按钮被按下

onmouseup：鼠标按键被松开

onmousemove：鼠标被移动

onmouseover：鼠标移动到某元素智商

onmouseout：鼠标从某元素移开
```

定义方法时，定义一个形参，接受event对象。调用event.button属性可以判断哪个键点击的

## 4.3.5. 键盘事件

```
onkeydown：某个键盘按键被按下

onkeyup：某个键盘按键被松开

onkeypress：某个键盘按键被按下并松开
```
event.keyCode

## 4.3.6. 选中和改变

```
onchange：域的内容被改变

onselect：文本被选中
```

## 4.3.7. 表单事件

```
onsubmit
	确认按钮被点击，可以阻止表单的提交，return false就会阻止提交。
	如果写在onclick属性里，要写return checkForm()

onreset：重置按钮被点击
```



































































## 12 JavaScript

+ 概念：一门客户端脚本语言

+ 运行在客户端浏览器中的。每一个浏览器都有JS的解析引擎。

+ 脚本语言：不需要编译，直接就可以被浏览器解析执行

+ 功能：可以增强用户和html页面的交互过程，可以控制html元素，让页面有一些动态效果，增强用户的体验。

**JavaScript = ECMAScript + JavaScript自己特有的东西（BOM + DOM）**

### 12.1 ECMAScript

客户端脚本语言的标准

#### 12.1.1 基本语法

##### 12.1.1.1 与html的结合方式：

1. 内部JS：定义```<script>  </script>```，标签体内容就是js代码

2. 外部JS：定义```<script>  </script>```，通过src属性引入外部的js文件

**注意：**

+ ```<script>```可以定义在html页面的任何地方，但是定义的位置会影响执行顺序。
+ 可以定义多个```<script>```

##### 12.1.1.2. 注释

和java一样

##### 12.1.1.3. 数据类型：

+ 原始数据类型

  1. number：数字。整数/小数/NaN(not a number)
  2. string：字符串。没有字符。
  3. boolean：true/false
  4. null：对象为空
  5. undefined：未定义。如果一个变量没有给初始化的值，那么默认赋值为undefined。

+ 引用数据类型：对象

##### 12.1.1.4. 变量：弱类型

```
var 变量名 = 初始化值;
```

```
document.write(a);
	换行用<br>

typeof(a)
	显示a的类型
```

##### 12.1.1.5. 运算符

1. 一元运算符
在JS中，如果运算数不是运算符所要求的类型，那么JS引擎会自动的将运算数进行类型转换。
   + string转number：按字面值转换。如果不是数字，转换为NaN，NaN与任何数运算还是NaN。
   + boolean转number：true转为1，false转为0
2. 算术运算符
3. 赋值运算符
4. 比较运算符
```===```：全等于
   + 类型相同，直接比较。字符串会按字典顺序，逐位比较。
   + 类型不同，先进行类型转换，再比较。

   + 全等于会先判断类型，类型不一样则直接返回false。
5. 逻辑运算符
    其他类型转boolean：
   + number：0或NaN为假，其他为真。
   + string：除了空字符串```""```，其他都是true。
   + null&undefined：都是false。
   + 对象：所有对象都是true。
6. 三元运算符
    ```boolean ? a : b ```

##### 12.1.1.6. 流程控制语句

JS里switch语句没有类型限制。

##### 12.1.1.7. 特殊语法

1. 句尾的分号可以省略（不建议）
2. 定义变量的时候，如果不写var，是全局变量，写var是局部变量。

#### 12.1.2. 基本对象

##### 12.1.2.1 Function：函数对象

1. 创建
```
var fun = new Function(形参列表，方法体);//这种方法不用

function 方法名称(形参列表){
    方法体
}

var 方法名 = function(形参列表){
    方法体
}
```
2. 方法
3. 属性
```length：形参的个数```

4. 特点
   + 方法定义的时候，形参的类型不用写，返回值类型也不写
   + 方法是一个对象，如果定义名称相同的方法，会覆盖
   + 在JS中，方法的调用只与方法的名称有关，和参数列表无关
   + 在方法声明中有一个隐藏的内置对象：数组arguments，封装了所有的实际参数
5. 调用
```
方法名称(实际参数列表);
```

##### 12.1.2.2 Array：数组对象

1. 创建
```
var arr = new Array(元素列表);

var arr = new Array(默认长度);

var arr = [元素列表];
```
2. 方法
```
join(参数)
	将数组中的元素按照指定的分隔符拼接成字符串（默认为逗号）

push()
	向数组的末尾添加一个或更多元素，并返回新的长度。
```
3. 属性
```length：数组的长度```
4. 特点
   + 在JS中，数组的元素的类型可变
   + 在JS中，数组的长度可变

##### 12.1.2.3 Boolean

##### 12.1.2.4 Date

1. 创建
```
var data = new Date();
```
2. 方法
```
toLocaleString()
	返回当前Date对象对应的时间本地字符串格式
getTime()
	获取毫秒值。
```

##### 12.1.2.5 Math

1. 创建
不用创建，直接使用。Math.方法名()

2. 方法
```
random():返回0~1之间的随机数。含0不含1
ceil(X)：向上取整
floor(X)：向下取整
round(x)：四舍五入
```
3. 属性
```PI```

##### 12.1.2.6 Number

##### 12.1.2.7 String

##### 12.1.2.8 RegExp：正则表达式对象

正则表达式：

+ 单个字符：[ ]
如```[a] [ab] [a-zA-Z0-9_]=\w \d```
+ 量词符号：
```
?
	0/1
*
	任意
+
	1+
{m,n}
	m到n位，包含两边
```
+ 开始结束符号：```^ $```

RegExp：

1. 创建
```
var reg = new RegExp("正则表达式");//这里要注意，\表示转义字符，\w要写成\\w

var reg = /正则表达式/;常用这个
```
2. 方法
```
test(参数)
	验证指定的字符串是否符合正则表达式
```

##### 12.1.2.9 Global：全局对象

其中封装的方法不需要对象，直接调用。```方法名();```
```
encodeURI():URI编码
decodeURI():URI解码

encodeURIComponent():URI编码，冒号等也编码
decodeURIComponent():URI解码，冒号等也编码

parseInt():字符串转为数字。会逐一判断每个字符是否是数字，直到不是数字为止，将前边数字部分转为number

isNaN():判断一个值是否是NaN。NaN六亲不认，参与的比较全是false

eval：将字符串转换为JS脚本代码来执行
```

URL对中文进行编码，一个百分号是一个字节

### 12.2 BOM

+ 概念：Browser Object Model 浏览器对象模型
+ 将浏览器的各个组成部分封装成对象。

Window：窗口对象
Navigator：浏览器对象
Screen：显示器屏幕对象
History：历史记录对象
Location：地址栏对象

#### 12.2.1 Window

窗口对象

##### 12.2.1.1 创建

不需要创建

##### 12.2.1.2 方法

1. 与弹出框有关的方法
```
alert()
	显示带有一段消息和一个确认按钮的警告框

confirm()
	显示带有一段消息以及确认按钮和取消按钮的对话框
	如果用户点确定，方法返回true，用户点取消，方法返回false

prompy()
	显示可提示用户输入的对话框
	返回值：用户的输入
```
2. 与打开关闭有关的方法
```
close()
	关闭浏览器窗口
    谁调用，关闭谁
open()
    打开一个新的浏览器窗口
    返回新的window对象
```
3. 与定时器有关的方法
```
setTimeout()
    在指定的毫秒数后调用函数或计算表达式
    参数
        1. js代码或方法对象
        2. 毫秒值
    返回值：唯一标识，用于取消定时器

clearTimeout()
    取消setTimeoutsetTimeout()方法设置的timeout

setInterval()
	按指定的周期（毫秒计）来调用函数或计算表达式

clearInterval()
	取消setInterval()方法设置的timeout
```

##### 12.2.1.3 属性

1. 获取其他BOM对象
```
history
location
Navigator
Screen
```
2. 获取DOM对象
```
document
```
##### 12.2.1.4 特点

+ window对象不需要创建，可以直接使用。
```
window.方法名()
```
+ window引用也可以省略，直接
```
方法名()
```

#### 12.2.2. Navigator：浏览器对象

#### 12.2.3. Screen：显示器屏幕对象

#### 12.2.4. History：历史记录对象

##### 12.2.4.1 创建（获取）

```
window.history
或
history
```

##### 12.2.4.2. 方法

```
back()
	加载history列表中的前一个URL

forward()
	加载history列表中的后一个URL

go(参数)
	加载history列表中的某个具体页面
    参数：
	    正数：前进几个历史记录，go(1)=forward()
    	负数：后退几个历史记录
```

##### 12.2.4.3. 属性

```
length
	返回当前窗口历史列表中的URL数量
```

#### 12.2.5. Location：地址栏对象
##### 12.2.5.1. 创建（获取）

```
window.location
或
location
```

##### 12.2.5.2. 方法

```
reload
	重新加载当前文档。刷新
```

##### 12.2.5.3. 属性

```
href
	设置或返回完整的URL
```

### 12.3 DOM

+ 概念：Document Object Model 文档对象模型
+ 将标记语言文档的各个组成部分，封装为对象。可以使用这些对象，对标记语言文档进行CRUD的动态操作
+ 功能：控制html文档的内容

W3C DOM 标准被分为3个不同的部分：

+ 核心 DOM：针对任何结构化文档的标准模型
   + Document：文档对象
   + Element：元素对象
   + Attribute：属性对象
   + Text：文本对象
   + Comment：注释对象

   + Node：节点对象，其他5个对象的父对象
+ XML DOM：针对XML文档的标准模型
+ HTML DOM：针对HTML文档的标准模型

#### 12.3.1 DOM 使用简单流程

获取页面标签（元素）对象：Element
```
document.getElementById("id值")：通过元素的id获取元素对象
```

操作Element对象：
1. 修改属性值：
   + 明确获取的对象是哪一个？
   + 查看API文档，找其中有哪些属性可以设置

2. 修改标签体内容：
    属性：```innerHTML```
   + 获取元素对象
   + 使用innerHTML属性修改标签体内容

#### 12.3.2 核心DOM模型

##### 12.3.2.1 Document：文档对象

1. 创建（获取）
在html dom模型中，可以使用window对象来获取

2. 方法

+ 获取Element对象
```
getElementById()
	根据id属性值获取元素对象，id属性值一般唯一

getElementByTagName()
	根据元素名称获取元素对象们，返回值是一个数组

getElementByClassName()
	根据Class属性获取元素对象们，返回值是一个数组

getElementByName()
	根据name属性获取元素对象们，返回值是一个数组
```

+ 创建其他DOM对象
```
createAttribute()
createComment()
createElement()
createTextNode()
```

##### 12.3.2.2 Element：元素对象

1. 创建（获取）：通过document来获取和创建
2. 方法
```
removeAttribute()：删除属性

setAttribute()：设置属性
```

##### 12.3.2.3 Node：节点对象，其他5个的父对象

1. 特点：所有dom对象都可以被认为是一个节点
2. 方法
CRUD dom树
```
appendChild()
	向节点的子节点列表的结尾添加新的子节点

removeChild()
	删除（并返回）当前节点的指定子节点

replaceChild()
	用新节点替换一个子节点
```
3. 属性
```
parentNode 返回节点的父节点
```

##### 12.3.2.4 其他

超链接
```
href = "javascript:void(0)"; //可以被点击的样式，但是不跳转
```
+ value属性获取内容
+ this获取当前对象

#### 12.3.3 HTML DOM

1. 标签体的设置和获取：innerHTML
```
var div = document.getElementById("div1");
var innerHTML = div.innerHTML;
```
2. 使用html元素对象的属性
```
div.innerHTML = "<input type='text'>";
```
3. 控制元素样式
   + 使用元素的style属性来设置（每个元素都有这个属性，后面直接点CSS的属性）
   + 提前定义好类选择器的样式，通过元素的className属性来设置其class属性值
```
div.style.border="1px solid red";

div.className = "cls";
```

## 13 事件

功能：某些组件被执行了某些操作后，触发某些代码的执行。

### 13.1 简单流程

如何绑定事件：
1. 直接在html标签上，指定事件的属性（操作），属性值就是js代码
```
<a href="..." onclick="js代码">
```

2. 通过js获取元素对象，指定事件属性，设置一个函数
```
document.getElementById("01").onclick=function(){
    ...
}
```

debug：正常打断点，然后在浏览器按下F12，在Console里看

### 13.2 事件监听机制

+ 事件：某些操作
+ 事件源：组件
+ 监听器：代码
+ 注册监听：将事件，事件源，监听器结合在一起。当事件源上发生了某个事件，则触发执行某个监听器代码。

### 13.3 常见的事件

#### 13.3.1 点击事件

```
onclick：单击事件

ondbclick：双击事件
```

#### 13.3.2. 焦点事件

```
onblur:失去焦点：一般用于表单校验

onfocus:元素获得焦点
```

#### 13.3.3. 加载事件

```
onload
	一张页面或一幅图像完成加载
	window.onload = ..
```

#### 13.3.4. 鼠标事件

```
onmousedown：鼠标按钮被按下

onmouseup：鼠标按键被松开

onmousemove：鼠标被移动

onmouseover：鼠标移动到某元素智商

onmouseout：鼠标从某元素移开
```

定义方法时，定义一个形参，接受event对象。调用event.button属性可以判断哪个键点击的

#### 13.3.5. 键盘事件

```
onkeydown：某个键盘按键被按下

onkeyup：某个键盘按键被松开

onkeypress：某个键盘按键被按下并松开
```
event.keyCode

#### 13.3.6. 选中和改变

```
onchange：域的内容被改变

onselect：文本被选中
```

#### 13.3.7. 表单事件

```
onsubmit
	确认按钮被点击，可以阻止表单的提交，return false就会阻止提交。
	如果写在onclick属性里，要写return checkForm()

onreset：重置按钮被点击
```

## 14 Bootstrap

+ 概念：一个前端开发的框架。
+ 好处：
1. 定义了很多CSS样式和JS插件。开发人员可以直接使用这些样式和插件得到丰富的页面效果。
2. 响应式布局：同一套页面可以兼容不同分辨率的设备。

### 14.1 bootstrap下载

1. 下载解压。
2. 项目中把3个文件夹复制进去
3. 创建html页面，引入必要的资源文件【min是压缩版，体积小，删掉了各种换行】模板在官网上有

### 14.2 响应式布局

+ 同一套页面可以兼容不同分辨率的设备
+ 实现：依赖于栅格系统，将一行平均分成12个格子，可以指定元素占几个格子。

+ 步骤：
1. 定义容器。
    相当于之前的table。容器分
   + container：除手机以外，两边有留白。
   + container-fluid：每一种设备都是100%宽度
2. 定义行。
    相当于tr。样式：```row```
3. 定义元素。指定该元素在不同设备上，所占的格子数目。
    样式：```col-设备代号-格子数目```
    设备代号：
   + xs：超小，手机
   + sm：小，平板
   + md：中，桌面
   + lg：大，大桌面

+ 定义的时候，指定class为样式。
不同的class用空格隔开，可以指定不止一个class

+ 按住滚轮，往下移动，可以一次修改多行

+ 注意事项：
  1. 一行中如果格子数目超过12，则超出部分自动换行。写大于12的数就按12处理。
  2. 栅格类属性可以向上兼容，适用于屏幕宽度大于或等于分界点大小的设备。
  3. 如果真是设备宽度小于定义的设备代码的最小值，会一个元素占满一整行。

### 14.3 CSS样式和JS插件

+ 全局CS样式：
   + 按钮
   + 图片
   + 表格
   + 表单

+ 组件：
   + 导航条
   + 分页条

+ 插件：
   + 轮播图
