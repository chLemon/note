# Postman

本笔记总结自：https://www.toutiao.com/i6913538714060800515/?wid=1618971685720

简单目录：



# 一、安装与Quick Start

## 1. 下载与安装

官网：https://www.getpostman.com/

个人使用可以跳过注册页面（在最下方有行灰色的文字）。团队使用需注册。

## 2. 界面说明

![image-20220125114329851](https://s2.loli.net/2022/01/25/NpQhr2FDufsG7LA.png)

## 3. QuickStart

如果你是第一次使用postman发送请求，下面这个例子可以作为一个最基本的入门，可以帮我们建立一个初始印象 。

1. 打开postman，点击+加号打开一个新的请求页。
2. 在请求的URL中输入请求地址：http://www.weather.com.cn/data/sk/101010100.html
3. 点击Send按钮，这时就可以在下部的窗格中看到来自服务器的json响应数据。

![image-20220125114436439](https://s2.loli.net/2022/01/25/E4PrRjaLN6wG9nW.png)

# 二、常用功能

## 1. 发送请求

### GET请求

![image-20220125141543883](https://s2.loli.net/2022/01/25/i3UYwmkpMvLKsO6.png)

### POST请求

#### 表单类型

Content_type: application/x-www-form-urlencoded

![image-20220125142448022](https://s2.loli.net/2022/01/25/ICq3Lk6lBSZDpt5.png)

#### JSON类型

![image-20220125142532074](https://s2.loli.net/2022/01/25/dZt8vpxaKjDn6rM.png)

#### 文件类型

![image-20220125142519050](https://s2.loli.net/2022/01/25/Q2nKhZIgDCYFfrx.png)

## 2. 响应解析

![image-20220125143317085](https://s2.loli.net/2022/01/25/oeHl3KfSJLUwdDM.png)



Body中的几个显示主题，分别是：Pretty，Raw，Preview



Pretty：翻译成中文就是漂亮 ， 也就是说返回的Body数据在这个标签中查看 ，都是经过格式化的，格式化后的数据看起来更加直观，所以postman默认展示的也是这个选项。比如返回html页面，它会经过格式化成HTML格式后展示，比如返回json，那么也会格式化成json格式展示 。

Raw：翻译成中文未经过加工的，也就是原始数据 ，原始数据一般都是本文格式的，未经过格式化处理的，一般在抓包工具中都有这个选项 。

Preview：翻译成中文就是预览，这个选项一般对返回HTML的页面效果特别明显，如请求百度后返回结果，点击这个选项后就直接能查看到的页面 ，如下图 。同时这个选项和浏览器抓包中的Preview也是一样的 。

