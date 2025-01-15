# 1. 前言

> 基于[Mockito 官方文档 5.14.2 版本](https://javadoc.io/doc/org.mockito/mockito-core/latest/org/mockito/Mockito.html)，2024年12月18日阅读
> 标题上（4.3.1+）的意思是，自 Mockito 4.3.1 版本开始有该功能

Mockito 的文档都写在了源码的 javadoc 中， Mocktio 团队说他们的目的有：
1. 保持源码和网站的内容一致
2. 在开发者没有联网的时候，也可以在 IDE 里获取到详尽的文档
3. 鼓励 Mockito 的开发者，在提交每个 commit 时，都将文档更新至最新

> 阅读完感觉，最新是最新，但是质量也就那样

## 1.1. 测试流程

通常测试会进行以下四阶段：setup, exercise, verify, teardown. 

BDD风格的测试则会进行以下三步：given, when, then

BDD风格是目前很流行的编写测试的方法，非常推荐。Mockito也提供了对BDD风格的支持。

> given: 一些准备的内容，如准备环境、准备数据、准备mock
> when: 实际要测试的操作
> then: 验证结果的部分
> 整个测试是可以直接读出来的，例如测试 Math.add();
> given a = 1, b = 2, when s = a + b, then s = 3

## 1.2. Mock框架

mock框架是在 敏捷开发/极限编程 社区中逐渐发展出来的。可以用于TDD风格的开发，允许在开发前通过一些 mock 对象 约定好程序的逻辑，在没有实际代码逻辑的情况下就写好测试，然后再进行代码的开发；这样有助于提前梳理清楚需求内容，并且驱使程序员在开发时给出进行更好地系统设计（让系统更加松耦合、易读）。

## 1.3. 测试代码的书写目标

1. 干净
2. 简单

# 2. 初步了解

## 2.1. Mock 含义和主要作用

可以 mock 一些类、接口，便于测试。mock 会记录所有的交互细节，

### 2.1.1. Mock 的含义

> mock 作形容词有“仿制的”意思，如 mock castle, 指现代建造的仿制城堡，意思和“仿古建筑”一词类似。

可以对一个类进行 mock，创建一个 mock 对象 (mock object, 或者直接称为 mock)。这创建的 mock 主要有 3 个特点：

1. 使用时可以看作类的一个实例
2. 调用所有的方法都会返回默认值，不会执行真正的代码逻辑
3. 会记录所有的交互细节

可以看出，mock 是某个类的一个仿制的对象，并不具有该类的真实功能，并且具有一些其他功能。

### 2.1.2. Mock 的主要作用：基于交互的测试

通常 mock 被用来验证交互，由于 mock 会记录所有的交互细节，我们可以验证 mock 上是否调用了某些方法、用什么参数调用的、调用了几次

基于交互的测试 会测试各个对象之间是否按照预期的方式交互，不关心对象的状态和值。

### 2.1.3. 简单例子

```java
import static org.mockito.Mockito.*;

// 创建 mock
List mockedList = mock(List.class);

// 使用 mock
mockedList.add("one");

mockedList.clear();

// 验证：调用了1次 add() 方法，且参数是 "one"
verify(mockedList).add("one");
// 验证：调用了1次 clear() 方法
verify(mockedList).clear();
```

当调用 mock 的方法时，默认会根据方法返回值类型返回：

-   null
-   Java 原生类型对应默认值，例如 int 返回 0，boolean 返回 false
-   包装类对应默认值，例如 Integer 返回 0，Boolean 返回 false
-   空集合

## 2.2. Stub 的含义

> stub 作名词指砍树后留下的树桩，支票撕掉后留下的存根，电影票检票后留下的副券

可以对一个 mock 进行 stub 操作，可以指定 mock 特定方法在这之后返回特定的返回值，或者抛出异常。

通常 verify 用来验证 mock 的交互信息，称为基于交互的测试；而 stub 用来验证 mock 的状态信息，称为基于状态的测试。

通常不会验证被 stub 方法的调用。

一旦 mock 的某个方法被 stub，方法会永远返回 stub 的值

```java
LinkedList mockedList = mock(LinkedList.class);

// stubbing
when(mockedList.get(0)).thenReturn("first");
when(mockedList.get(1)).thenThrow(new RuntimeException());

//following prints "first"
System.out.println(mockedList.get(0));

//following throws runtime exception
System.out.println(mockedList.get(1));

//following prints "null" because get(999) was not stubbed
System.out.println(mockedList.get(999));
```

## 2.3. Spy 的含义

> spy 有作动词监视的意思。

可以在一个真实对象的基础上创建 spy，spy 的方法调用默认会调用真实方法，除非该方法被 stub 了。

事实上 spy 就是一个 mock。区别在于：
1. spy 创建需要一个真实对象
2. 调用 spy 的方法时，会执行真实的代码逻辑

```java
List list = new LinkedList();
List spy = spy(list);

// （可选）stub 一些方法
when(spy.size()).thenReturn(100);

// 调用真实方法
spy.add("one");
spy.add("two");

// 输出 one
System.out.println(spy.get(0));

// 输出 100
System.out.println(spy.size());

// spy 对象 的方法调用也可以进行验证
verify(spy).add("one");
verify(spy).add("two");
```

注意，Mockito 调用 spy 的方法时，不会将方法委托给真实对象，spy 其实是真是对象的一个副本。

所以：
1. 上个例子中的`list`还是空的。
2. 如果对`list`操作，`spy`对象不会意识到这些操作，也就不能进行验证

注意，过度使用 spy 是一个代码异味
