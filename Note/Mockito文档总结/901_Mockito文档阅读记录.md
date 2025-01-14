# 参考

[Mockito 官方文档 5.14.2 版本](https://javadoc.io/doc/org.mockito/mockito-core/latest/org/mockito/Mockito.html)，2024年12月18日阅读

Mockito 的文档都写在了源码的 javadoc 中， Mocktio 团队说他们的目的有：
1. 保持源码和网站的内容一致
2. 在开发者没有联网的时候，也可以在 IDE 里获取到详尽的文档
3. 鼓励 Mockito 的开发者，在提交每个 commit 时，都将文档更新至最新

# 0. 迁移到 mockito 2

希望你升级到 2.0.1 及以上

## 0.1 安卓支持

## 0.2 无需配置的 inline mock making

从 2.7.6 开始，我们提供了 mockito-inline ，允许 inline mock making ，并且无需配置 MockMaker 扩展文件。为了使用这个，添加 mockito-inline，而不是 mockito-core。

从 5.0.0 开始，inline mock maker 会成为默认的 mock maker

更多信息看 section 39

## 0.3 Java21+ 为了 inline mocking 明确设置 instrumentation

> In computer programming, instrumentation is the act of modifying software so that analysis can be performed on it.
> Generally, instrumentation either modifies source code or binary code.
> Instrumentation enables profiling: [1] measuring dynamic behavior during a test run. This is useful for properties of a program that cannot be analyzed statically with sufficient precision, such as performance and alias analysis.
> Instrumentation can include:
>
> - Logging events such as failures and operation start and end [2]
> - Measuring and logging the duration of operations

21 开始，JDK 限制了库的动态代理能力。所以 inline-mock-maker 使用时需要就明确设置 enable instrumentation ，并且 JVM always 展示一个 warning

为了明确的在测试执行的时候 attach Mockito，库的 jar 文件需要在执行 JVM 的时，被-javaagent 明确指定为一个参数。

如果要把 mockito 加到 Maven's surefile plugin 的话，需要设置：（这个插件是 maven 生命周期里专门用来执行单元测试的，可以生成报告）

```xml
<plugin>
     <groupId>org.apache.maven.plugins</groupId>
     <artifactId>maven-dependency-plugin</artifactId>
     <executions>
         <execution>
             <goals>
                 <goal>properties</goal>
             </goals>
         </execution>
     </executions>
 </plugin>
 <plugin>
     <groupId>org.apache.maven.plugins</groupId>
     <artifactId>maven-surefire-plugin</artifactId>
     <configuration>
         <argLine>@{argLine} -javaagent:${org.mockito:mockito-core:jar}</argLine>
     </configuration>
 </plugin>
```

# 1 verify

下面的例子，mock 了一个 List 用作展示，因为大家对 List 都很熟悉，不过实际不要 mock List，使用真正的 List

```java
 //Let's import Mockito statically so that the code looks clearer
 //静态引入，让代码更干净
 import static org.mockito.Mockito.*;

 //mock creation  mock 创建
 List mockedList = mock(List.class);

 //using mock object	使用mock对象
 mockedList.add("one");
 mockedList.clear();

 //verification	   验证
 verify(mockedList).add("one");
 verify(mockedList).clear();
```

一旦创建，mock 会记住所有的交互，然后你就可以选择性的验证你感兴趣的任何交互

# 2 stubbing

```java
 //You can mock concrete classes, not just interfaces
// 可以 mock 实体类，不止是接口
 LinkedList mockedList = mock(LinkedList.class);

 //stubbing
 when(mockedList.get(0)).thenReturn("first");
 when(mockedList.get(1)).thenThrow(new RuntimeException());

 //following prints "first"
 System.out.println(mockedList.get(0));

 //following throws runtime exception
 System.out.println(mockedList.get(1));

 //following prints "null" because get(999) was not stubbed
 System.out.println(mockedList.get(999));

 //Although it is possible to verify a stubbed invocation, usually it's just redundant
 //If your code cares what get(0) returns, then something else breaks (often even before verify() gets executed).
 //If your code doesn't care what get(0) returns, then it should not be stubbed.

// 尽管，验证stubbed 的调用也是可能的，但是通常 这只是 多余的
// 如果你的代码关心 get(0) 返回了什么，一些其他的东西会 breaks？通常甚至会发生在 verify() 执行之前
// 如果你的代码不关心返回值，它就不应该被 stub
 verify(mockedList).get(0);
```

- 默认情况下，所有的有返回值的方法，mock 会根据情况返回 null / 原生类型 / 原生类型的包装类 / 空集合。例如，int / Integer 返回 0 ， boolean/Boolean 返回 false

- stub 可以被覆盖，例如可能会在 fixture 里设置一些通用的 stub，然后在测试方法里 override it。注意，override stub 是一个潜在的代码异味，指出可能用了太多的存根

- 一旦 stub，方法永远返回 stub 值，无论被调用多少次

- 最后一个 stub 更加的重要，当你用同样的参数 stub 同一个方法很多次的时候。换句话说，stub 的顺序很重要，虽然很少有意义。例如 stub 特定方法调用，或者有时使用参数匹配器等

test fixture: 也称为 test context，用于设置测试的系统状态和输入

# 3 参数匹配器

mockito 用 自然的 java 风格验证参数值，使用 equals 方法。有时，当你需要额外的灵活性时，你看你使用参数匹配器

```java
 //stubbing using built-in anyInt() argument matcher
// stub  使用 内置 anyInt() 参数匹配器
 when(mockedList.get(anyInt())).thenReturn("element");

 //stubbing using custom matcher (let's say isValid() returns your own matcher implementation):
// stub 使用 自定义的matcher ，换句话说 isValid 返回你自己的匹配器实现
 when(mockedList.contains(argThat(isValid()))).thenReturn(true);

 //following prints "element"
 System.out.println(mockedList.get(999));

 //you can also verify using an argument matcher
// verify的时候也可以用参数匹配器
 verify(mockedList).get(anyInt());

 //argument matchers can also be written as Java 8 Lambdas
// 也可以用 lambda 表达式
 verify(mockedList).add(argThat(someString -> someString.length() > 5));
```

argThat 方法用来创建自定义的参数匹配器

- 参数匹配器 允许灵活的 verification 或者 stubbing ，ArgumentMatchers 里可以查看一些内置的 和 自定义参数匹配器的信息，另外也有一些 hamcrest matchers (hamcrest：一个三方库，里面含有大量的 matchers)

- 合理使用复杂的参数匹配。使用 自然的 equals 方法匹配，和少量的 anyX() 匹配器，有写出干净而简单的测试。有时候，重构代码使得 equals 匹配可以生效，甚至实现 equals 方法来帮助测试，都是一个更好的选择

- 另外，阅读 section 15 ，ArgumentCaptor 是一个参数匹配器的特殊实现，可以捕获参数，来进行进一步的断言

## 参数匹配器警告

如果你使用参数匹配器，所有的参数都必须通过参数匹配器提供，下面展示了一个例子

```java
verify(mock).someMethod(anyInt(), anyString(), eq("third argument"));
   //above is correct - eq() is also an argument matcher
// 这个是对的

   verify(mock).someMethod(anyInt(), anyString(), "third argument");
   //above is incorrect - exception will be thrown because third argument is given without an argument matcher.
// 这个不对
```

匹配器方法，像 any() eq() 不会返回匹配器。在内部，他们在堆里记录了一个匹配器，然后反悔了一个虚拟值，通常是 null。

这个实现是由于 java 编译器强加的 静态类型安全。结果就是，你不能在 已验证 / 存根 方法之外，调用 any() eq() 方法

> 这里有个坑，如果方法是原生的，那么不能用any 只能用 anyInt()

## 参数匹配器 ArgumentMatchers

```java
 //stubbing using anyInt() argument matcher
 when(mockedList.get(anyInt())).thenReturn("element");

 //following prints "element"
 System.out.println(mockedList.get(999));

 //you can also verify using argument matcher
 verify(mockedList).get(anyInt());
```

```java
// stubbing using anyBoolean() argument matcher
 when(mock.dryRun(anyBoolean())).thenReturn("state");

 // below the stub won't match, and won't return "state"
 mock.dryRun(null);

 // either change the stub
 when(mock.dryRun(isNull())).thenReturn("state");
 mock.dryRun(null); // ok

 // or fix the code ;)
 when(mock.dryRun(anyBoolean())).thenReturn("state");
 mock.dryRun(true); // ok
```

由于 any anyX 家族的方法会执行类型检查，所以不匹配 null

用 isNull 匹配器

https://javadoc.io/static/org.mockito/mockito-core/5.14.2/org/mockito/ArgumentMatchers.html

| Modifier and Type        | Method                                        | Description                                                                                                                                        | 翻译                                 |
| ------------------------ | --------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| static <T> T             | any()                                         | Matches anything, including nulls.                                                                                                                 | 匹配所有东西，包括`null`             |
| static <T> T             | any(Class<T> type)                            | Matches any object of given type, excluding nulls.                                                                                                 | 匹配给定类型的所有东西，不包括`null` |
| static boolean           | anyBoolean()                                  | Any boolean or non-null Boolean                                                                                                                    | 任何`boolean`或者非`null`的`Boolean` |
| static byte              | anyByte()                                     | Any byte or non-null Byte.                                                                                                                         | 任何`byte`或者非`null`的`Byte`       |
| static char              | anyChar()                                     | Any char or non-null Character.                                                                                                                    |
| static <T> Collection<T> | anyCollection()                               | Any non-null Collection.                                                                                                                           |
| static double            | anyDouble()                                   | Any double or non-null Double.                                                                                                                     |
| static float             | anyFloat()                                    | Any float or non-null Float.                                                                                                                       |
| static int               | anyInt()                                      | Any int or non-null Integer.                                                                                                                       |
| static <T> Iterable<T>   | anyIterable()                                 | Any non-null Iterable.                                                                                                                             |
| static <T> List<T>       | anyList()                                     | Any non-null List.                                                                                                                                 |
| static long              | anyLong()                                     | Any long or non-null Long.                                                                                                                         |
| static <K,V> Map<K,V>    | anyMap()                                      | Any non-null Map.                                                                                                                                  |
| static <T> Set<T>        | anySet()                                      | Any non-null Set.                                                                                                                                  |
| static short             | anyShort()                                    | Any short or non-null Short.                                                                                                                       |
| static String            | anyString()                                   | Any non-null String                                                                                                                                |
| static <T> T             | argThat(ArgumentMatcher<T> matcher)           | Allows creating custom argument matchers.                                                                                                          |
| static <T> T             | assertArg(Consumer<T> consumer)               | Allows creating custom argument matchers where matching is considered successful when the consumer given by parameter does not throw an exception. |
| static <T> T             | assertArg(ThrowingConsumer<T> consumer)       | Allows creating custom argument matchers where matching is considered successful when the consumer given by parameter does not throw an exception. |
| static boolean           | booleanThat(ArgumentMatcher<Boolean> matcher) | Allows creating custom boolean argument matchers.                                                                                                  |
| static byte              | byteThat(ArgumentMatcher<Byte> matcher)       | Allows creating custom byte argument matchers.                                                                                                     |
| static char              | charThat(ArgumentMatcher<Character> matcher)  | Allows creating custom char argument matchers.                                                                                                     |
| static String            | contains(String substring)                    | String argument that contains the given substring.                                                                                                 |
| static double            | doubleThat(ArgumentMatcher<Double> matcher)   | Allows creating custom double argument matchers.                                                                                                   |
| static String            | endsWith(String suffix)                       | String argument that ends with the given suffix.                                                                                                   |
| static boolean           | eq(boolean value)                             | boolean argument that is equal to the given value.                                                                                                 |
| static byte              | eq(byte value)                                | byte argument that is equal to the given value.                                                                                                    |
| static char              | eq(char value)                                | char argument that is equal to the given value.                                                                                                    |
| static double            | eq(double value)                              | double argument that is equal to the given value.                                                                                                  |
| static float             | eq(float value)                               | float argument that is equal to the given value.                                                                                                   |
| static int               | eq(int value)                                 | int argument that is equal to the given value.                                                                                                     |
| static long              | eq(long value)                                | long argument that is equal to the given value.                                                                                                    |
| static short             | eq(short value)                               | short argument that is equal to the given value.                                                                                                   |
| static <T> T             | eq(T value)                                   | Object argument that is equal to the given value.                                                                                                  |
| static float             | floatThat(ArgumentMatcher<Float> matcher)     | Allows creating custom float argument matchers.                                                                                                    |
| static int               | intThat(ArgumentMatcher<Integer> matcher)     | Allows creating custom int argument matchers.                                                                                                      |
| static <T> T             | isA(Class<T> type)                            | Object argument that implements the given class.                                                                                                   |
| static <T> T             | isNotNull()                                   | Not null argument.                                                                                                                                 |
| static <T> T             | isNotNull(Class<T> type)                      | Not null argument.                                                                                                                                 |
| static <T> T             | isNull()                                      | null argument.                                                                                                                                     |
| static <T> T             | isNull(Class<T> type)                         | null argument.                                                                                                                                     |
| static long              | longThat(ArgumentMatcher<Long> matcher)       | Allows creating custom long argument matchers.                                                                                                     |
| static String            | matches(String regex)                         | String argument that matches the given regular expression.                                                                                         |
| static String            | matches(Pattern pattern)                      | Pattern argument that matches the given regular expression.                                                                                        |
| static <T> T             | notNull()                                     | Not null argument.                                                                                                                                 |
| static <T> T             | notNull(Class<T> type)                        | Not null argument.                                                                                                                                 |
| static <T> T             | nullable(Class<T> clazz)                      | Argument that is either null or of the given type.                                                                                                 |
| static <T> T             | refEq(T value, String... excludeFields)       | Object argument that is reflection-equal to the given value with support for excluding selected fields from a class.                               |
| static <T> T             | same(T value)                                 | Object argument that is the same as the given value.                                                                                               |
| static short             | shortThat(ArgumentMatcher<Short> matcher)     | Allows creating custom short argument matchers.                                                                                                    |
| static String            | startsWith(String prefix)                     | String argument that starts with the given prefix.                                                                                                 |


## 附加的/另外的/补充的参数匹配器 AdditionalMatchers

https://javadoc.io/static/org.mockito/mockito-core/5.14.2/org/mockito/AdditionalMatchers.html

这个类只是为了和 EasyMock 兼容，是一些很少使用的匹配器。尽量不要使用这里的匹配器，它们会破坏测试的可读性。更推荐 ArgumentMatchers 中的匹配器。

# 4 验证精确的调用次数

```java

 //using mock
 mockedList.add("once");

 mockedList.add("twice");
 mockedList.add("twice");

 mockedList.add("three times");
 mockedList.add("three times");
 mockedList.add("three times");

 //following two verifications work exactly the same - times(1) is used by default
 // 这两个效果一样，times(1)是默认的
 verify(mockedList).add("once");
 verify(mockedList, times(1)).add("once");

 //exact number of invocations verification
 // 验证确切数字
 verify(mockedList, times(2)).add("twice");
 verify(mockedList, times(3)).add("three times");

 //verification using never(). never() is an alias to times(0)
 // 验证从来没有交互过
 verify(mockedList, never()).add("never happened");

 //verification using atLeast()/atMost()
 // 至少，至多
 verify(mockedList, atMostOnce()).add("once");
 verify(mockedList, atLeastOnce()).add("three times");
 verify(mockedList, atLeast(2)).add("three times");
 verify(mockedList, atMost(5)).add("three times");

```
> 经过测试，多次验证同样的是可以通过的

# 5 stub void方法抛出异常

```java
   doThrow(new RuntimeException()).when(mockedList).clear();

   //following throws RuntimeException:
   mockedList.clear();
```

`doThrow()|doAnswer()`家族的方法会在 section12 介绍

# 6 按顺序验证

```java

 // A. Single mock whose methods must be invoked in a particular order
 List singleMock = mock(List.class);

 //using a single mock
 singleMock.add("was added first");
 singleMock.add("was added second");

 //create an inOrder verifier for a single mock
 // 给这个简单的mock创建一个 顺序验证器
 InOrder inOrder = inOrder(singleMock);

 //following will make sure that add is first called with "was added first", then with "was added second"
 // 下面会确保，先调用 frist 再调用 second，注意最前面的 inorder
 inOrder.verify(singleMock).add("was added first");
 inOrder.verify(singleMock).add("was added second");

 // B. Multiple mocks that must be used in a particular order
 // 多个 mock 必须以特定顺序调用
 List firstMock = mock(List.class);
 List secondMock = mock(List.class);

 //using mocks
 firstMock.add("was called first");
 secondMock.add("was called second");

 //create inOrder object passing any mocks that need to be verified in order
 // 把所有的需要确保调用顺序的mock传入
 InOrder inOrder = inOrder(firstMock, secondMock);

 //following will make sure that firstMock was called before secondMock
 inOrder.verify(firstMock).add("was called first");
 inOrder.verify(secondMock).add("was called second");

 // Oh, and A + B can be mixed together at will
 // A+B可以任意混合使用
 ```

按顺序验证 是灵活的，你不需要一一验证所有的交互，只需要按照顺序验证你关心的测试

当然，创建 InOrder 对象的时候，你也可以只把和顺序验证相关对象传进去

# 7 验证 mock 上没有发生过交互（和上面重复了）

```java
 //using mocks - only mockOne is interacted
 mockOne.add("one");

 //ordinary verification
 verify(mockOne).add("one");

 //verify that method was never called on a mock
 verify(mockOne, never()).add("two");
```

# 8 找到冗余的调用

```java

 //using mocks
 mockedList.add("one");
 mockedList.add("two");

 verify(mockedList).add("one");

 //following verification will fail
 verifyNoMoreInteractions(mockedList);
```

警告：有些使用过很多经典的 expect-run-verify mocking 的用户倾向于非常频繁的使用 verifyNoMoreInteractions() ，甚至会在每一个测试方法里使用。
不推荐在每个测试方法里都用这个。它是一个来自交互测试工具的方便的断言。只在相关的时候使用它，滥用会导致 过度指定、很难维护的测试

看看`never()`，它更明确，也可以更好的传达意图

# 9 mock创建的简写 `@Mock` 注解

+ 最少的重复 mock 创建的代码
+ 让测试类更易读
+ 让验证错误更容易读，因为 field 名字被用来识别谁是mock

```java
  public class ArticleManagerTest {

       @Mock private ArticleCalculator calculator;
       @Mock private ArticleDatabase database;
       @Mock private UserProvider userProvider;

       private ArticleManager manager;

       @org.junit.jupiter.api.Test
       void testSomethingInJunit5(@Mock ArticleDatabase database) {
```

重要！需要在某个地方加上这个，要么加在 base class 里，要么在 test runner
```java
MockitoAnnotations.openMocks(testClass);
```

你可以使用内置的 runner `MockitoJUnitRunner`或者 rule `MockitoRule`。
对于 JUnit5 的测试，查看 section 45 里的部分

# 10 stubbing 连续调用 (iterator-style stubbing 迭代器形式的stub)

有时候，我们需要对同一个方法的调用进行stub，返回不同的值/exception。
典型的使用场景是 mocking iterators ？
最初版本的 Mockito 没有这个功能来 促进 简单 mocking
例如，可以用 Iterable 或者 简单集合 来替代 iterators。
这些提供了更自然的方法来 stubbing ，使用真正的集合。
在很少的 场景下，stubbing 连续调用是很有用的：

```java

 when(mock.someMethod("some arg"))
   .thenThrow(new RuntimeException())
   .thenReturn("foo");

 //First call: throws runtime exception:
 mock.someMethod("some arg");

 //Second call: prints "foo"
 System.out.println(mock.someMethod("some arg"));

 //Any consecutive call: prints "foo" as well (last stubbing wins).
 System.out.println(mock.someMethod("some arg"));
```

可选的，连续stubbing的更短的版本：

```java
 when(mock.someMethod("some arg"))
   .thenReturn("one", "two", "three");
```

警告：
如果没用链式调用 `.thenReturn()` ，多个同样 matcher 或者参数的 stubbing 只有最后一个会生效。

# 11 stubbing with callbacks

允许 stubbing 含有泛型的 `Answer` 接口，该接口指定了 执行的方法和与该mock交互时的返回值

另一个有争议的功能，在最初的 Mockito 里没有。
我们推荐 简单的用 `thenReturn()` 和 `thenThrow()` 来stubbing，这个应该足够测试（或者测试驱动）任何干净和简单的代码。
然而，如果你确实需要 stub 泛型 `Answer`接口，这里有个例子

```java
 when(mock.someMethod(anyString())).thenAnswer(
     new Answer() {
         public Object answer(InvocationOnMock invocation) {
             Object[] args = invocation.getArguments();
             Object mock = invocation.getMock();
             return "called with arguments: " + Arrays.toString(args);
         }
 });

 //Following prints "called with arguments: [foo]"
 System.out.println(mock.someMethod("foo"));
```

# 12 `doReturn() | doThrow() | doAnswer() | doNothing() | doCallRealMethod()` 家族方法

stubbing void方法需要使用和`when(Object)`不同的方法，因为编译器不喜欢括号内的`void`方法

使用 `doThrow()` 当你想 stub 一个 void 方法 抛出一个异常时：

```java

   doThrow(new RuntimeException()).when(mockedList).clear();

   //following throws RuntimeException:
   mockedList.clear();
```

对于任何方法，你可以使用 `doReturn() | doThrow() | doAnswer() | doNothing() | doCallRealMethod()` 以替代响应的 `when()`调用。当你遇到下面情况的时候，必须使用
+ stub void 方法
+ stub spy 对象的方法
+ stub 同一个方法多次，在测试的过程中，想要改变一个 mock 的行为

但是你可能更想使用这些方法替代在`when()`调用的地方，对于你所有的stubbing calls

## doReturn(Object)

在无法使用 `when(Object)` 的情况下，使用`doReturn()`

注意，`when(Object)`总是在stubbing的时候更推荐，因为 它是参数类型安全的，并且更易读（尤其是当连续调用的时候）

下面是一些`doReturn()`用起来更方便的罕见的场景：
1. 当spying 真实对象，并且调用有 side effects 的真实方法时候

```java
   List list = new LinkedList();
   List spy = spy(list);

   //Impossible: real method is called so spy.get(0) throws IndexOutOfBoundsException (the list is yet empty)
   // 不可能成功调用，因为真实方法还是[]，会报错
   when(spy.get(0)).thenReturn("foo");

   //You have to use doReturn() for stubbing:
   doReturn("foo").when(spy).get(0);
```

2. 覆盖之前的一个 exception-stubbing
```java

   when(mock.foo()).thenThrow(new RuntimeException());

   //Impossible: the exception-stubbed foo() method is called so RuntimeException is thrown.
   // 不可能，为什么这里不会覆盖呢？
   when(mock.foo()).thenReturn("bar");

   //You have to use doReturn() for stubbing:
   // 必须这样
   doReturn("bar").when(mock).foo();

```

很神奇，普通 stub 会覆盖，但是 exception 的不会。多个exception也不会

上面这个场景展示了 Mockito 对于优雅语法的权衡。
注意，这些场景非常的罕见。 spying 应该很少出现，并且覆盖 exception-stubbing 也非常罕见。不要提在一般情况下，覆盖stubbing 是一个潜在的代码异味，标识存在了太多的 stubbing


## doThrow(Throwable...)

当你想要 stub void 方法抛出一个异常的时候用`doThrow()`

stub void 需要和`when(Object)`不同的方法，由于编译器。


## doThrow(Class)

当你想要 stub void 方法抛出一个异常的时候用`doThrow()`

一个新的exception 实例会在每次方法调用的时候创建

## doAnswer(Answer)

当你想要 stub void 方法一个泛型Answer的时候


## doNothing()

使用`doNothing()`来设置 void 方法什么都不做
注意，mock对象的void方法默认就是 do nothing
然而，也有一些非常罕见的情况下，`doNothing`非常方便

1. 给一个 void 方法进行 stubbing 连续调用

```java

   doNothing().
   doThrow(new RuntimeException())
   .when(mock).someVoidMethod();

   //does nothing the first time:
   mock.someVoidMethod();

   //throws RuntimeException the next time:
   mock.someVoidMethod();
```

2. 当你 spy 真实对象，并且你希望其中的 void 方法 do nothing

```java

   List list = new LinkedList();
   List spy = spy(list);

   //let's make clear() do nothing
   doNothing().when(spy).clear();

   spy.add("one");

   //clear() does nothing, so the list still contains "one"
   spy.clear();
```


## doCallRealMethod()

使用`doCallRealMethod()`当你想调用一个方法的真实实现时。
像往常一样，你应该去读一下 部分mock警告：OOP是一个 差不多/或多或少 解决复杂性，是通过将复杂性划分为独立的、特定的 单一职责 (SRP 加y是想变成形容词 垃圾英语)对象。
那么 partial mock 怎么匹配到这一范式中呢？嗯，它就是不符合…… 部分mock通常意味着，复杂性被转移到了同一个对象里的另一个不同方法中了。
在大部分情况下，这不是你想要设计你应用程序的方式。

然而，还是有一些罕见的场景，partial mocks会很方便：
处理代码你不能轻易修改的（第三方的接口，临时重构遗留代码 等）。然而，我不会给新的，测试驱动的，并且设计良好的代码用 部分mock

更推荐用`Mockito.spy()`来创建 部分mock。原因是，它保证了真实的方法被调用在正确创建的对象上，因为 构造传给 spy() 方法的对象是你负责的。

例子：
```java

   Foo mock = mock(Foo.class);
   doCallRealMethod().when(mock).someVoidMethod();

   // this will call the real implementation of Foo.someVoidMethod()
   mock.someVoidMethod();
```

# 13 对真实对象spy

你可以在真实对象上创建 spy。当你使用spy，真实的方法会被调用（除非这个方法已经被stub了）
spy应该被十分小心、偶尔的使用，例如处理遗留代码。

在真实对象上 spy 与 部分mocking 这个概念有关。
在1.8之前，Mockito的spy不是真正的 partial mock。原因是我们觉得 部分Mock 是一个代码异味。在有的时候，我们发现了 部分mock 的合理使用场景，如 第三方的接口，临时重构遗留代码

```java

   List list = new LinkedList();
   List spy = spy(list);

   //optionally, you can stub out some methods:
   when(spy.size()).thenReturn(100);

   //using the spy calls *real* methods
   spy.add("one");
   spy.add("two");

   //prints "one" - the first element of a list
   System.out.println(spy.get(0));

   //size() method was stubbed - 100 is printed
   System.out.println(spy.size());

   //optionally, you can verify
   verify(spy).add("one");
   verify(spy).add("two");
 
```

## 在真实对象上spy的重要 启示/陷阱

1. 有时候，不可能在 stubbing spy 的对象上使用 `when(Object)`，。因此，当使用spy的时，考虑用`doReturn|Answer|Throw()`家族方法来stub。例如
```java

   List list = new LinkedList();
   List spy = spy(list);

   //Impossible: real method is called so spy.get(0) throws IndexOutOfBoundsException (the list is yet empty)
   when(spy.get(0)).thenReturn("foo");

   //You have to use doReturn() for stubbing
   doReturn("foo").when(spy).get(0);
 
```
2. Mockito **不会**将调用 委托给 传进去的真实实例，而是实际上会创建一个副本。所以如果你保留了真实实例，并且与之交互，不要期望 被spy的 意识到了这些交互 和 这些交互对真实实例状态的影响 。这必然会导致，当一个 **没有stub**的方法，被 **spy 对象**上调用，但是**没有在真实实例上**调用，你不会在真实实例上看到任何影响。
3. 小心那些 final 的方法。 Mockito 不会 mock final方法，所以底线是：当你 spy 了真实对象，然后你又尝试 stub 一个final方法，会导致麻烦。并且你也不能正常verify那些方法

测试后发现，mock是可以正常运行的

# 14 改变未stub调用的默认返回值（1.7引入）

你可以创建有着特殊策略 返回值 的mock。这是一个高级功能，并且通常你不需要它就能写合适的测试。然而，它在处理遗留系统的时候很有用。
这是默认的答案，所以只有当你没有stub方法调用的时候，会使用。

```java

   Foo mock = mock(Foo.class, Mockito.RETURNS_SMART_NULLS);
   Foo mockTwo = mock(Foo.class, new YourOwnAnswer());
 

```

## RETURNS_SMART_NULLS

可选的 `Answer` 被用于 `mock(Class, Answer)`

`Answer`被用于定义 未stub 调用的返回值
这个实现当和遗留代码配合的时候非常有用。没有stub的方法通常返回null。如果你的代码使用了没有stub调用的返回值，你会得到一个 NullPointerException。
这个Answer的实现会返回 SmartNull 。SmartNull会给出一个比NPE更好的异常信息，因为它直接指出了没有 stub 的方法被调用 所在的行。你可以直接点一下 stack trace。
`ReturnsSmartNulls` 首先尝试返回普通的值（0，空集合，空字符串 等）。然后它会尝试返回 SmartNull。如果返回值是 final 的，那么会返回一个单纯的 null 

# 15 捕捉参数，用于进一步断言（1.8+）

Mockito 用java原生方式验证参数：通过使用`equals()`方法。这也是更推荐的匹配参数的方式，因为这样可以使得测试干净、简单。然而在有些场景下，这样也很有用，在实际验证后，assert 特定的参数，例如：

```java

   ArgumentCaptor<Person> argument = ArgumentCaptor.forClass(Person.class);
   verify(mock).doSomething(argument.capture());
   assertEquals("John", argument.getValue().getName());
 
```

警告：ArgumentCaptor 推荐和 verification 用，但是不推荐和stub用。使用 ArgumentCaptor 和 stub 用可能会降低测试的可读性，因为 captor 是创建在了 aseert 部分的外面（assert block 有时候也叫 then block）。同时，它可能会减少缺陷定位，因为 如果stub方法没有被调用，那么没有参数会被 captured

在某种程度上，ArgumentCaptor 和自定义参数匹配器有关。两种技术都可以确保特定的参数传递给了mocks。然而 ArgumentCaptor 可能更适合：
1. 自定义参数匹配器不可能被复用
2. 你只是需要 assert 参数值就可以完成验证

通常 自定义参数匹配器对于 stubbing 更合适。

# 16 真正的 部分 mock （1.8+）

最终，经过内部的多次辩论和邮件讨论，Mockito添加了 部分mock 的支持。之前我们认为 部分mock 是一个代码异味。然而，我们发现了一些部分mock的合法用例：

在 1.8 之前，spy 不会生成真正的 部分mock，然后它会让有些用户疑惑。

```java

    //you can create partial mock with spy() method:
    List list = spy(new LinkedList());

    //you can enable partial mock capabilities selectively on mocks:
    // 你可以选择性的在 mock 上启用 部分mock 的能力，通过 thenCallRealMethod()
    Foo mock = mock(Foo.class);
    //Be sure the real implementation is 'safe'.
    // 确保真实实现是 安全的
    //If real implementation throws exceptions or depends on specific state of the object then you're in trouble.
    when(mock.someMethod()).thenCallRealMethod();
  
```

像往常一样，你应该去读一下 部分mock警告：OOP是一个 差不多/或多或少 解决复杂性，是通过将复杂性划分为独立的、特定的 单一职责 (SRP 加y是想变成形容词 垃圾英语)对象。
那么 partial mock 怎么匹配到这一范式中呢？嗯，它就是不符合…… 部分mock通常意味着，复杂性被转移到了同一个对象里的另一个不同方法中了。
在大部分情况下，这不是你想要设计你应用程序的方式。

然而，还是有一些罕见的场景，partial mocks会很方便：
处理代码你不能轻易修改的（第三方的接口，临时重构遗留代码 等）。然而，我不会给新的，测试驱动的，并且设计良好的代码用 部分mock

# 17 重置mock（1.8+）

使用这个方法，可能是说明测试写的不太行。正常情况下，你不需要重置你的mock，你就给每个测试方法创建新的mock就行了。

与其使用 reset 方法，不如考虑一下写简单、小、并且聚焦的测试方法，而不是 超长的，超特殊指定的测试。
第一个潜在的代码异味是，reset 是在测试方法中间的。这个可能意味着你测试的太多了。
遵循你测试代码的低语：“请让我们小，并且专注于一个小的行为上”。在mockito 邮件列表上，有几个 threads（感觉是邮件一来一回的那种帖子）

我们添加 reset 的唯一理由是 让和 容器注入 的mock 可以一起使用。更多信息查看FAQ（有的mock可能是DI注入的，所以需要重置）

不要伤害你自己。在测试代码中的 reset 是一个代码异味。

```java
   List mock = mock(List.class);
   when(mock.size()).thenReturn(10);
   mock.add(1);

   reset(mock);
   //at this point the mock forgot any interactions and stubbing
 
```

# 18 故障排除 和 验证框架使用情况 (1.8+)

首先，遇到了任何问题，我们都鼓励你先去读 FAQ
 https://github.com/mockito/mockito/wiki/FAQ

你也可以发到 mailing list 里
https://groups.google.com/g/mockito

然后，你应该知道 mockito 会验证你是否始终正确使用它。然而，这里还有一个启示，所以请阅读 validateMockitoUsage() 的javadoc 

## validateMockitoUsage

validateMockitoUsage() 显式验证框架状态来检测出 Mockito 的无效使用。然而，这个功能是可选的，因为 Mockito 始终都会验证……
但是这里还有一个 gotcha，所以继续往下看：

错误使用的例子
```java
 //Oops, thenReturn() part is missing:
 // 没有 thenReturn()
 when(mock.get());

 //Oops, verified method call is inside verify() where it should be on the outside:
 // 要验证的方法调用放在了 verify() 里面
 verify(mock.execute());

 //Oops, missing method to verify:
 // 少写了要验证的方法
 verify(mock);
 
```

> gotcha : 在计算机领域指的是，合法有效，但是容易会误会意思的构造，容易造成错误
> got you 的简称，常用语口语，逮到你了，你中计了，骗到你了
> 典型例子：c 和 c++ 里  if(a=b) doSomething

Mockito 抛出异常，如果你错误使用了它，这样你就可以知道你的测试写的对不对。
有一个易错点是，Mockito 会在你下一次使用框架的时候做检查（例如下一次 verify, stub, call mock 等）。
但是尽管这个异常会在下一次测试的时候被抛出，异常的信息包含一个 可导航的栈跟踪元素 包括了缺陷的位置。所以你可以点击，然后找到 Mockito 错用的地方

但是有时候，你可能想显式校验 Mockito 框架的使用。例如，其中一个用户想把 `validateMockitoUsage()` 方在他的 `@After` 方法中，这样它就能在误用 Mockito 的时候立刻知道了。如果没有这个，他只有在下一次使用框架功能的时候才知道。另一个这样做的好处是，JUnit runner 和 rule 会总是失败在有问题的测试方法里，但是普通的 next-time 校验可能会失败在下一个测试方法里。
不过尽管JUnit可能会将下一个测试标红，也不用担心，只需要点击一下错误消息里的 可导航的栈跟踪元素 立刻就可以定位到你误用 Mockito 的位置。

内置的 runner  MockitoJUnitRunner 和 rule  MockitoRule 都会在每一个方法执行后调用 `validateMockitoUsage()`

记住，通常你不需要 `validateMockitoUsage()` 并且 基本的在下一次进行的框架验证 就足够用了，主要是因为 加强的异常信息 有一个可以点击位置 of defect。
然而，我想推荐 `validateMockitoUsage()` 如果你已经有一些足够的测试基础设施（比如说你自己的 runner 或者 所有类的base class），因为在`@After`上加上这么一个行为没什么成本。

# 19 给BDD用的别名 (1.8+)

BDD风格写测试时使用 //given //when //then 注释作为测试方法的基本部分。这正是我们编写测试的方法，并且我们也热切鼓励你也这样用。

从这里开始学习 BDD：https://en.wikipedia.org/wiki/Behavior-driven_development

问题是，现在的 stub api 使用了 when ，无法很好的和 //given //when //then 注释集成在一起。
因为 stub 属于 测试的 given 部分，而不是 when 部分
所以， `BDDMockito` 这个类 引入了一个别名，这样你可以用 `BDDMockito.given(Object)` 来进行 stub。现在他可以和BDD风格测试的given部分很好的集成了。

这里有个例子：
```java
 import static org.mockito.BDDMockito.*;

 Seller seller = mock(Seller.class);
 Shop shop = new Shop(seller);

 public void shouldBuyBread() throws Exception {
   //given
   given(seller.askForBread()).willReturn(new Bread());

   //when
   Goods goods = shop.buyBread();

   //then
   assertThat(goods, containBread());
 }

```

# 20 可序列化的 mock （1.8.1+）

mock 可以通过序列化的方式创建。用这个特性，你可以在需要依赖可序列化的地方使用mock。
警告：这应该很少用在单元测试中。
这个行为实现是为了一个特殊的用例，有依赖了一个不可靠的外部依赖 BDD 规范。在web环境，对象从外部依赖获得，这个对象在层和层之间传递，要被序列化。

使用 `MockSettings.serializable()` 来创建可序列化的mock

```java
 List serializableMock = mock(List.class, withSettings().serializable());
```

这个mock可以被序列化，假设该类可以满足所有的普通序列化需求。这里指的是，满足jdk定义的 `serializable`


使 真实对象的 spy 可序列化需要一些更多的努力，由于 `spy(...)` 方法没有一个 overloaded 版本可以接受 `MockSettings` 的参数。不用担心，你几乎不会用到：
```java
 List<Object> list = new ArrayList<Object>();
 List<Object> spy = mock(ArrayList.class, withSettings()
                 .spiedInstance(list)
                 .defaultAnswer(CALLS_REAL_METHODS)
                 .serializable());
```

# 21 新的注解 `@Captor`, `@Spy`, `@InjectMocks` （1.8.3+）

1.8.3带来了几个新的注解，有时候可能会很有用：
+ `@Captor`简化了`ArgumentCaptor`的创建 - 很有用，当要抓的参数是一个令人讨厌的泛型类，并且你想避免编译器告警
+ `Spy` - 可以作为 `spy(Object)` 的提单
+ `@InjectMocks` - 自动注入 mock 或者 spy 对象到被测对象里

注意 `@InjectMocks` 也可以和 `@Spy` 注解结合使用，它意味着 Mockito 会将 mocks 注入到 被测试的 partial mock 里。这个复杂性是另一个原因，为什么你应该只在不得不的情况下使用 partial mock。

所有的这些新注解只会在 `MockitoAnnotations.openMock(Object)` 时生效。就像 `@Mock` 一样，你也可以用内置的 `MockitoJUnitRunner` 或者 `MockitoRule`

# 22 超时验证

允许 验证 超时。这会导致一个 verify 去等待一个期望的交互 特定的时间，而不是在还没有发生的时候立刻失败。
可能对并发条件下的测试有用。

这个特征应该非常少用——这到一个更好的方法去测试你的多线程系统
还没有实现 和InOrder 验证 一起用。

例子：
```java

   //passes when someMethod() is called no later than within 100 ms
   //exits immediately when verification is satisfied (e.g. may not wait full 100 ms)
   // 通过，当 someMethod() 被调用 不迟于100ms内
   // 立刻退出，当验证满足的时候，不会等满100ms
   // 这里有点神奇，如果说调用到 verify 已经 2次了，会报错，但是如果1次都没有时，不会报错
   verify(mock, timeout(100)).someMethod();
   //above is an alias to:
   // 上面是这个的 alias
   verify(mock, timeout(100).times(1)).someMethod();

   //passes as soon as someMethod() has been called 2 times under 100 ms
   // 通过，只要 someMethod 在100ms内调用2次
   verify(mock, timeout(100).times(2)).someMethod();

   //equivalent: this also passes as soon as someMethod() has been called 2 times under 100 ms
   verify(mock, timeout(100).atLeast(2)).someMethod();
 
```

# 23 自动实例化 `@Spies`，`@InjectMocks` 和 构造器注入的优点 （1.9.0+）

Mockito 现在会试着实例化 `@Spy` 和 将实例化 `@InjectMocks` 字段使用 constructor injection 构造器注入，setter injection 或 field injection
为了利用这个功能，你需要使用  MockitoAnnotations.openMocks(Object), MockitoJUnitRunner or MockitoRule.

可用技巧和注入的规则详见 InjectMocks

```java

 //instead:
 @Spy BeerDrinker drinker = new BeerDrinker();
 //you can write:
 @Spy BeerDrinker drinker;

 //same applies to @InjectMocks annotation:
 @InjectMocks LocalPub;
 
```

## InjectMocks

标记一个 field 应该执行注入
+ 允许 shorthand mock 和 spy 的注入 指的是通过 @Mock 注解的mock和spy
+ 尽可能少的对 mock spy 注入的重复

Mockito 会尝试注入 mock 仅仅在 constructor injection, property injection 或者 setter injection 以上注入按顺序，下方会详细描述。如果任何一个下方的策略失败了，Mockito 不会报错，也就是说你必须自己提供依赖：
1. Constructor injection；会选择最大的构造器，然后仅处理在测试中声明的mock的参数。如果这个对象成功的通过构造器创建了，然后Mockito就不会尝试别的策略了。Mockito已经决定，如果一个对象有一个参数化的构造器，不会破坏该对象。
   注意：如果参数没有找到，会传null进去。如果需要一个不可mock的类型，构造器注入不会发生。在这些情况里，你必须自己满足依赖。

2. Property setter injection; mocks会首先按照类型解析（如果单一类型匹配了注入，那么会忽视掉名称），然后，如果同一个类型有好几个property，会根据property的名称和mock的名称进行匹配。
   
   注意1：如果你有同样类型的property （或者相同擦除），最好去命名所有的 @Mock 注解的 field 用匹配的 properties，否则 Mockito 会感到困惑，然后注入不会发生
   注意2：如果 `@InjectMocks` 实例没有实例化，并且有一个无参构造器，然后它会通过无参构造器初始化。

3. Field injection： mock首先会根据类型解析（如果只有一个匹配注入了，就会注入，无视name），然后... 同2
   
   注意1：如果你有 fields ....和2一样
   注意2：如果....

例子：
```java

   public class ArticleManagerTest extends SampleBaseTestCase {

       @Mock private ArticleCalculator calculator;
       // 注意 mock 的 name 属性
       @Mock(name = "database") private ArticleDatabase dbMock; // note the mock name attribute
       @Spy private UserProvider userProvider = new ConsumerUserProvider();

       @InjectMocks private ArticleManager manager;

       @Test public void shouldDoSomething() {
           manager.initiateArticle();
           verify(database).addListener(any(ArticleListener.class));
       }
   }

   public class SampleBaseTestCase {

       private AutoCloseable closeable;

       @Before public void openMocks() {
           closeable = MockitoAnnotations.openMocks(this);
       }

       @After public void releaseMocks() throws Exception {
           closeable.close();
       }
   }
```

在上面这个例子中，被`@InjectMocks`注解的field `ArticleManager` 可以只有一个参数化的构造器，或者只有一个无参构造器，或者都有。这些所有的构造器可以是 package protected, protected 或者 private 的，然而 mockito 不能实例化内部类，local classes（方法里的class）, 抽象类，和 接口。也要注意 私有嵌套的静态类。

这也同样适用于 setters 或者 fields，他们可以声明为 private 的可见性，Mockito可以看见他们通过反射。然而 field 如果是 static 和 final 的会被忽略。

因此，在需要被注入的字段上，例如构造函数注入会在这里发生：
```java
  public class ArticleManager {
       ArticleManager(ArticleCalculator calculator, ArticleDatabase database) {
           // parameterized constructor
       }
   }
 
```

Property setter注入会在这里发生：

```java

   public class ArticleManager {
       // no-arg constructor
       ArticleManager() {  }

       // setter
       void setDatabase(ArticleDatabase database) { }

       // setter
       void setCalculator(ArticleCalculator calculator) { }
   }
```

field 注入会在这里被使用：

```java

   public class ArticleManager {
       private ArticleDatabase database;
       private ArticleCalculator calculator;
   }
 
```

并且最后，在这个例子里，没有注入会发生：
```java


   public class ArticleManager {
       private ArticleDatabase database;
       private ArticleCalculator calculator;

       ArticleManager(ArticleObserver observer, boolean flag) {
           // observer is not declared in the test above.
           // flag is not mockable anyway
       }
   }
 
```

再然后，注意`@InjectMocks`仅仅会注入 使用`@Spy`和`@Mock`注解创建的 mocks / spies

`MockitoAnnotations.openMocks(this)`方法必须被调用来初始化被注解的对象。在之前的例子里，`openMocks()`被测试基类里的`@Before`调用了。作为替代的，你可以通过内置的 `MockitoJUnitRunner`。此外，确保在释放了所有的mock，用一个相关的钩子，在处理完你的测试类。

Mockito 不是一个依赖注入的框架，不要指望这个简单的实用程序可以注入一个复杂的对象图，无论是 mocks/spies/还是真实对象

用这个注解注解的元素，也可以是 spied ，这个对象可以有 @Spy 注解

# 24 一行的stub 1.9.0+

Mockito 现在允许你 stubbing 的时候创建 mock。基本上，它允许在一行代码里创建 stub。这有助于让测试代码干净。例如，有一些无聊的stub可以被创建，被stub 在field初始化的时候。

```java
 public class CarTest {
   Car boringStubbedCar = when(mock(Car.class).shiftGear()).thenThrow(EngineNotStarted.class).getMock();

   @Test public void should... {}
```

# 25 验证忽略的stub 1.9.0+

Mockito 现在允许忽略 stub 为了verification 的原因。有时候有用，当 结合 `verifyNoMoreInterations()` 或者 `inOrder()`验证。
帮助避免对 stubbed 调用冗余的 verfiy - 典型的是我们对于 验证stub不感兴趣

警告：`ignoreStubs()`可能会导向过度使用 `verifyNoMoreInteractions(ignoreStubs(...))` 。记着 mockito 不推荐 使用 `verifyNoMoreInteractions` 对每个测试进行轰炸。

一些例子
```java

 verify(mock).foo();
 verify(mockTwo).bar();

 //ignores all stubbed methods:
 verifyNoMoreInteractions(ignoreStubs(mock, mockTwo));

 //creates InOrder that will ignore stubbed
 InOrder inOrder = inOrder(ignoreStubs(mock, mockTwo));
 inOrder.verify(mock).foo();
 inOrder.verify(mockTwo).bar();
 inOrder.verifyNoMoreInteractions();

```

# 26 mocking 细节 （2.2.x增强

mockito 提供API来检查mock对象的细节。这个API对于高级用户很有用，或者 mocking 框架集成者

```java

   //To identify whether a particular object is a mock or a spy:
   Mockito.mockingDetails(someObject).isMock();
   Mockito.mockingDetails(someObject).isSpy();

   //Getting details like type to mock or default answer:
   MockingDetails details = mockingDetails(mock);
   details.getMockCreationSettings().getTypeToMock();
   details.getMockCreationSettings().getDefaultAnswer();

   //Getting invocations and stubbings of the mock:
   MockingDetails details = mockingDetails(mock);
   details.getInvocations();
   details.getStubbings();

   //Printing all interactions (including stubbing, unused stubs)
   System.out.println(mockingDetails(mock).printInvocations());
 

```

# 27 将调用委托给真实对象 （1.9.5+）

有用 对于 spies 和 部分模拟的对象 很难 mock 或者使用普通spy API spy的。
自 Mockito 1.10.11 ，委托可能，也可能不，mock的同一类型 （委托可能和mock是一个类型，也可能不是）。如果类型不同，一个匹配的方法是需要在委托类型上找到的，否则会抛出异常。可能的使用场景：
+ 有接口的 final class
+ 已经被自定义代理的类
+ 特殊的类，带有一个 finalize 方法，也就是说要避免它被执行2次

和普通 spy 不同的是：
+ 普通的spy 包含被spy实例的所有状态，并且方法是在spy上被调用的。被spy的实例仅仅被用于创建mock和复制状态。如果你在常规spy上调用一个方法，它内部调用这个spy上的其他方法，这些调用被记录用于 verification ， 并且他们也可以有效的进行 stub
+ 委托的mock只是简单的将所有方法委托给委托。委托始终被调用。如果你在一个被委托的mock上调用一个方法，那么它内部会调用此mock上的其他方法，这些调用不会被记录用来验证，stub也没有用。委托的模拟不如常规spy强大，但是对于无法创建常规spy的时候很有用。

更多看 `AdditionalAnswers.delegatesTo(Object)`

# 28 `MockMaker` API (1.9.5+)

在 Google Android 开发人员的要求和补丁的推动下，Mockito 现在提供了一个扩展点，允许替换代理生成引擎。默认情况下，Mockito 使用Byte Buddy 创建动态代理。

该扩展点适用于想要扩展 Mockito 的高级用户。例如，现在可以借助dexmaker使用 Mockito 进行 Android 测试。

有关更多详细信息、动机和示例，请参阅文档MockMaker。

# 29 BDD风格的验证 （1.10.0+）

允许使用 BDD 风格的验证，启用 then 关键字来验证
```java


 given(dog.bark()).willReturn(2);

 // when
 ...

 then(person).should(times(2)).ride(bike);
 

```

更多详见 `BDDMockito.then(Object)`

# 30 Spy或者Mock抽象类 （1.10.12+ 增强于2.7.13, 2.7.14）

现在可以更方便的spy抽象类。注意 过度使用 spy 其实是一个代码设计异味

之前，spy只看用在对象实例上。新的API使得创建mock实例的时候可以用构造器。这点对mock抽象类非常有用，因为用户不再需要提供一个抽象类的实例了。现在，只有无参构造器支持，如果不够请告诉我们。

```java


 //convenience API, new overloaded spy() method:
 // 方便的API，现在 overload 了 spy方法
 SomeAbstract spy = spy(SomeAbstract.class);

 //Mocking abstract methods, spying default methods of an interface (only available since 2.7.13)
 // mock 抽象方法，会spy接口的default方法
 Function<Foo, Bar> function = spy(Function.class);

 //Robust API, via settings builder:
 // 更鲁邦的API，通过 settings 建造者模式
 OtherAbstract spy = mock(OtherAbstract.class, withSettings()
    .useConstructor().defaultAnswer(CALLS_REAL_METHODS));

 //Mocking an abstract class with constructor arguments (only available since 2.7.14)
 // 指定构造器参数，mock抽象类
 SomeAbstract spy = mock(SomeAbstract.class, withSettings()
   .useConstructor("arg1", 123).defaultAnswer(CALLS_REAL_METHODS));

 //Mocking a non-static inner abstract class:
 // mock一个非静态的内部类
 InnerAbstract spy = mock(InnerAbstract.class, withSettings()
    .useConstructor().outerInstance(outerInstance).defaultAnswer(CALLS_REAL_METHODS));
 

```

# 31 Mockito 的mock可以是跨类加载器 `serialized | deserialized`

Mockito 引入了跨类加载器的序列化。与任何其他形式的序列化一样，模拟层次结构中的所有类型都必须可序列化，包括答案。由于此序列化模式需要做更多工作，因此这是一个可选设置。

```java
 // use regular serialization
 mock(Book.class, withSettings().serializable());

 // use serialization across classloaders
 mock(Book.class, withSettings().serializable(ACROSS_CLASSLOADERS));
 ```

详情请参阅 `MockSettings.serializable(SerializableMode)`

# 32 通过 deep stub 对 泛型更好的支持 (1.10.0+)

deep stubbing 已经被提升了为可以寻找泛型信息，如果在类里可能的话。这意味着，像这样的类可以直接用，不用mock这个行为了。

```java
class Lines extends List<Line> {
     // ...
 }

 lines = mock(Lines.class, RETURNS_DEEP_STUBS);

 // Now Mockito understand this is not an Object but a Line
 Line line = lines.iterator().next();
 
```

注意，在大多数情况下，mock返回mock是错误的。

> 注意到 mock这个词，即可以指被mock的对象，也可以指 mock 的方法

# 33 Mockito JUnit Rule 1.10.17+

Mockito 现在提供 JUnit rule。截至目前，JUnit有2种方法初始化被像`@Mock @Spy @InjectMocks`注解的字段

+ 注解JUnit测试类用 `@RunWith(MockitoJUnitRunner.class)`
+ 调用 `MockitoAnnotations.openMocks(Object)`在`@Before`方法里

现在你还可以选择使用一个 rule

```java
@RunWith(YetAnotherRunner.class)
 public class TheTest {
     @Rule public MockitoRule mockito = MockitoJUnit.rule();
     // ...
 }
```

# 34 打开或关闭插件 1.10.15+

mockito 中正在酝酿一项功能，允许切换 mockito 插件。更多信息请见此处 `PluginSwitch`

# 35 自定义验证失败的信息 2.1.0+

允许指定当验证失败时打印一个自定义的信息

```java

 // will print a custom message on verification failure
 verify(mock, description("This will print on failure")).someMethod();

 // will work with any verification mode
 verify(mock, times(2).description("someMethod should be called twice")).someMethod();
 
```

# 36 Java 8 Lambda Matcher 支持 2.1.0+

你可以使用 Java 8 的 lambda 表达式来写 `ArgumentMatcher` 来减少对于`ArgumentCaptor`的依赖。如果你需要验证 mock上一个方法调用的参数是正确的，然后你会通常的使用 `ArgumentCaptor`来查找使用的操作数，然后对他们做一些后续的断言。虽然对于复杂的例子，这很有用，但是它太啰嗦。

写一个lambda表达式来表示匹配非常的简单。你函数的参数，当和`argThat`共同使用的时候，会被传入 `ArgumentMatcher` 作为一个强类型的对象，然后你就可以做任意的操作了。

```java
 // verify a list only had strings of a certain length added to it
 // note - this will only compile under Java 8
 verify(list, times(2)).add(argThat(string -> string.length() < 5));

 // Java 7 equivalent - not as neat 不够整洁
 verify(list, times(2)).add(argThat(new ArgumentMatcher<String>(){
     public boolean matches(String arg) {
         return arg.length() < 5;
     }
 }));

 // more complex Java 8 example - where you can specify complex verification behaviour functionally
 // 更复杂的例子 你可以实用地指定复杂的验证行为
 verify(target, times(1)).receiveComplexObject(argThat(obj -> obj.getSubObject().get(0).equals("expected")));

 // this can also be used when defining the behaviour of a mock under different inputs
 // in this case if the input list was fewer than 3 items the mock returns null
 // 这个也可以用于在不同输入下有不同行为的mock
 when(mock.someMethod(argThat(list -> list.size()<3))).thenReturn(null);

```

# 37 java 8 Custom Answer 支持 2.1.0+

由于 `Answer` 接口只有一个方法，所以对于一些非常简单的情况，它现在已经可以在 java 8 里用 lambda 表达式来实现。
`InvocationOnMock`中，你用的参数越多，你越需要强制转换。

```java

 // answer by returning 12 every time
 // 每次都返回12的answer
 doAnswer(invocation -> 12).when(mock).doSomething();

 // answer by using one of the parameters - converting into the right
 // type as your go - in this case, returning the length of the second string parameter
 // as the answer. This gets long-winded quickly, with casting of parameters.

 // 使用其中一个参数的answer - 转换为你想要的右边的类型 - 在这个例子里，返回第二个string参数的长度作为answer，随着 cast 参数，很快就会变得啰嗦
 doAnswer(invocation -> ((String)invocation.getArgument(1)).length())
     .when(mock).doSomething(anyString(), anyString(), anyString());
```

为了方便起见，可以自定义 answer / action，使用方法调用的参数，以Java 8 lambda的形式。
尽管在 Java 7 或者更低版本里，这些自定义 answers 基于一个类型化的接口可以减少 样板文件/公式化。特别的是，这种方法让用callback的测试功能更容易。方法`AdditionalAnswers.answer(Answer1)`和`AdditionalAnswers.answerVoid(VoidAnswer1)`可以用来创造answer。他们依赖于`org.mockito.stubbing`中的相关的answer接口，支持最多5个参数。

```java


 // Example interface to be mocked has a function like:
 // 示例接口，要被mock的，有一个函数
 void execute(String operand, Callback callback);

 // the example callback has a function and the class under test
 // will depend on the callback being invoked
 // 示例callback有一个函数，并且被测的类会依赖于callback的调用
 void receive(String item);

 // Java 8 - style 1
 doAnswer(AdditionalAnswers.<String,Callback>answerVoid((operand, callback) -> callback.receive("dummy")))
     .when(mock).execute(anyString(), any(Callback.class));

 // Java 8 - style 2 - assuming static import of AdditionalAnswers
 doAnswer(answerVoid((String operand, Callback callback) -> callback.receive("dummy")))
     .when(mock).execute(anyString(), any(Callback.class));

 // Java 8 - style 3 - where mocking function to is a static member of test class
 private static void dummyCallbackImpl(String operation, Callback callback) {
     callback.receive("dummy");
 }

 doAnswer(answerVoid(TestClass::dummyCallbackImpl))
     .when(mock).execute(anyString(), any(Callback.class));

 // Java 7
 doAnswer(answerVoid(new VoidAnswer2<String, Callback>() {
     public void answer(String operation, Callback callback) {
         callback.receive("dummy");
     }})).when(mock).execute(anyString(), any(Callback.class));

 // returning a value is possible with the answer() function
 // and the non-void version of the functional interfaces
 // so if the mock interface had a method like
 boolean isSameString(String input1, String input2);

 // this could be mocked
 // Java 8
 // 注意第一个的Boolean
 doAnswer(AdditionalAnswers.<Boolean,String,String>answer((input1, input2) -> input1.equals(input2)))
     .when(mock).execute(anyString(), anyString());

 // Java 7
 // 这里 Answer2是不是写错了啊
 doAnswer(answer(new Answer2<String, String, String>() {
     public String answer(String input1, String input2) {
         return input1 + input2;
     }})).when(mock).execute(anyString(), anyString());
 
```

# 38 元数据和泛型类型的保留 2.1.0+

Mockito 现在会保留mock方法和类型上的注解，包括泛型元数据。之前，mock类型是不会保留类型上的注解的，除非显式继承，并且永远不会保留方法上的注解。因此，下面这些条件现在可以成立：

```java
 @MyAnnotation
  class Foo {
    List<String> bar() { ... }
  }

  Class<?> mockType = mock(Foo.class).getClass();
  assert mockType.isAnnotationPresent(MyAnnotation.class);
  assert mockType.getDeclaredMethod("bar").getGenericReturnType() instanceof ParameterizedType;
 
```

当用 Java 8 的时候，Mockito 现在还会保留类型注解。这是个默认行为，但是如果用`MockMaker`的话，可能不会保留。

# 39 Mock final 类型，enums，和final 方法 （2.1.0+）

Mockito 现在默认提供对于 final 类、方法的支持。这是个几号的提升，说明Mockito不断追求改善测试体验的决心。我们的目标是 Mockito 可以和 final 类和方法 交互。之前他们被认为是不可 mock的  unmockable，组织用户模拟。自 5.0.0，这个功能默认开启了。

这个可替换的 mock maker 结合使用了 Java instrumentation API和 sub-classing 子类 rather than 创建一个新类来表示mock。这样，mock final 类型和方法就成为了可能。

在5.0.0之前的版本，这个 mock maker 默认关闭，由于它基于一个完全不同的mock机制，需要从社区中获取更多的反馈。可以通过 mockito扩展机制显式激活，只需要在 classpath 里创建一个文件 `/mockito-extensions/org.mockito.plugins.MockMaker`，文件内容包括 `mock-maker-inline`

为了方便起见，Mockito 团队提供了一个制品 预配置了这个 mock maker 。替代使用 `mockito-core`制品，把 `mockito-inline`放在你的项目里。请注意，一旦将最终类和方法的模拟集成到默认模拟生成器中，此工件可能会停用。

关于这个 mock maker ，有一些值得注意的：
+ mock final类型和enums和下面这些mock设置不兼容：
  + 显式序列化支持`withSettings.serializable()`
  +  额外接口 `withSettings().extraInterfaces()`
+  有些方法不能被mock
   +  `java.*` 下 package-visible 的 方法
   +  `native`的方法
+  这个 mock maker 是围绕 Java Agent runtime attachment 设计的。这需要一个兼容的JVM。JDK里有，如果只是虚拟机VM，9+的才有，让运行在一个非JDK的，9之前的VM，需要通过运行JVM的时候加参数 `-javaagent` 加上 Byte Buddy Java agent jar
 
> https://bytebuddy.net/#/

更多细节见：`org.mockito.internal.creation.bytebuddy.InlineByteBuddyMockMaker`

# 40 使用 更严格 的mockito 来提升生产力和更干净的测试

为了快速了解 “更严格” 的mockito如何帮助你更有生产力，且让测试更干净，请参阅：

> https://javadoc.io/static/org.mockito/mockito-core/5.14.2/org/mockito/quality/Strictness.html

+ Strict stubbing with JUnit4 Rules - MockitoRule.strictness(Strictness) with Strictness.STRICT_STUBS
+ Strict stubbing with JUnit4 Runner - MockitoJUnitRunner.Strict
+ Strict stubbing with JUnit5 Extension - org.mockito.junit.jupiter.MockitoExtension
+ Strict stubbing with TestNG Listener MockitoTestNGListener
+ Strict stubbing if you cannot use runner/rule - MockitoSession
+ Unnecessary stubbing detection with MockitoJUnitRunner    // 非必要的stub监测
+ Stubbing argument mismatch warnings, documented in MockitoHint

Mockito 默认是一个松散的mock框架。mocks 可以在无需设置任何期望下进行交互。这是故意的，这样可以强制用户明确出他们到底想 stub / verify 什么东西。这也非常的直观，容易使用，并且和 given when then 这种干净测试代码的模板 完美融合。这也是不同于之前的mock框架的区别，之前都是严格的。

默认 宽松 使得有时候 mockito 测试 难以debug。在一些场景下，错误配置的stub（比如说用了错误的参数）会强制用户debug测试代码。理想情况下，测试失败是显而易见的，不需要debugger来识别根因。从 2.1 开始，mockito 有了一些新的特性，推动框架往 严格 发展。
我们希望mockito 提供 非常好的debug能力，同时不丢失核心 mock 风格，优化 直观性、明确性、干净测试

# 41 用于框架集成的高级公共API 2.10.+

2017 年夏天，我们决定 Mockito 应该提供更好的 API  以实现高级框架集成。新 API 不适用于想要编写单元测试的用户。它适用于需要使用一些自定义逻辑扩展或包装 Mockito 的其他测试工具和模拟框架。在设计和实施过程中（问题 1110），我们开发并更改了以下公共 API 元素：


+ New MockitoPlugins - Enables framework integrators to get access to default Mockito plugins. Useful when one needs to implement custom plugin such as MockMaker and delegate some behavior to the default Mockito implementation.
+ New MockSettings.build(Class) - Creates immutable view of mock settings used later by Mockito. Useful for creating invocations with InvocationFactory or when implementing custom MockHandler.
+ New MockingDetails.getMockHandler() - Other frameworks may use the mock handler to programmatically simulate invocations on mock objects.
+ New MockHandler.getMockSettings() - Useful to get hold of the setting the mock object was created with.
+ New InvocationFactory - Provides means to create instances of Invocation objects. Useful for framework integrations that need to programmatically simulate method calls on mock objects.
+ New MockHandler.getInvocationContainer() - Provides access to invocation container object which has no methods (marker interface). Container is needed to hide the internal implementation and avoid leaking it to the public API.
+ Changed Stubbing - it now extends Answer interface. It is backwards compatible because Stubbing interface is not extensible (see NotExtensible). The change should be seamless to our users.
+ NotExtensible - Public annotation that indicates to the user that she should not provide custom implementations of given type. Helps framework integrators and our users understand how to use Mockito API safely.

# 42 用于集成的新API：监听 verification start events 2.11.+

像Spring之类的框架集成时需要 公共API 来 解决 double-proxy 使用场景。我们加了：

+ New VerificationStartedListener and VerificationStartedEvent enable framework integrators to replace the mock object for verification. The main driving use case is Spring Boot integration. For details see Javadoc for VerificationStartedListener.
+ New public method MockSettings.verificationStartedListeners(VerificationStartedListener...) allows to supply verification started listeners at mock creation time.
+ New handy method MockingDetails.getMock() was added to make the MockingDetails API more complete. We found this method useful during the implementation.

# 43 用于集成的新API: `MockitoSession` 可以通过测试框架使用了 2.15+

MockitoSessionBuilder 和 MockitoSession  被增强了，可以被测试框架集成重新使用，例如（MockitoRule for JUnit）

+ MockitoSessionBuilder.initMocks(Object...) allows to pass in multiple test class instances for initialization of fields annotated with Mockito annotations like Mock. This method is useful for advanced framework integrations (e.g. JUnit Jupiter), when a test uses multiple, e.g. nested, test class instances.
+ MockitoSessionBuilder.name(String) allows to pass a name from the testing framework to the MockitoSession that will be used for printing warnings when Strictness.WARN is used.
+ MockitoSessionBuilder.logger(MockitoSessionLogger) makes it possible to customize the logger used for hints/warnings produced when finishing mocking (useful for testing and to connect reporting capabilities provided by testing frameworks such as JUnit Jupiter).
+ MockitoSession.setStrictness(Strictness) allows to change the strictness of a MockitoSession for one-off scenarios, e.g. it enables configuring a default strictness for all tests in a class but makes it possible to change the strictness for a single or a few tests.
+ MockitoSession.finishMocking(Throwable) was added to avoid confusion that may arise because there are multiple competing failures. It will disable certain checks when the supplied failure is not null.

# 44 弃用 `org.mockito.plugins.InstantiatorProvider` ，它泄露了内部API，替换为了 `org.mockito.plugins.InstantiatorProvider2` 2.15.4+

# 45 新的 JUnit Jupiter (JUnit5+)扩展

为了集成JUnit5+，使用 `org.mockito:mockito-junit-jupiter` 制品。想知道集成的更多信息，看 `MockitoExtension` 的 JavaDoc

# 46 新的 `Mockito.lenient()` 和 `MockSettings.lenient()` 方法 2.20.0+

自动早期的 Mockito 2 开始，严格stub特性就可用的。它非常有用，因为它可以推动更清晰的测试并提高生产率。严格的存根会报告不必要的存根，检测存根参数不匹配 并使测试更加 DRY（Strictness.STRICT_STUBS）。这需要权衡：在某些情况下，您可能会从严格的存根中得到假阴性。为了解决这些问题，您现在可以将特定存根配置为 宽松 的，而所有其他存根和模拟都使用严格的存根：

```java
  lenient().when(mock.foo()).thenReturn("ok");
  // lenient 宽容的
```

如果你希望有个 mock 上的所有 stub都是 宽容的，则可以相应地配置模拟：

```java

   Foo mock = Mockito.mock(Foo.class, withSettings().lenient());
```

更多参见 `lenient`

# 47 新的API 用来清除 inline mocking 里的 mock 状态 2.25.0+

在特定的，罕见的情况下，inline mocking 会导致内存泄漏。现在没有一个干净的方法来完全缓解这个问题。所以，我们引入了一个新的API来明确的清除mock状态（只在inline mocking里有意义）。

## MockitoFramework.clearInlineMocks()

清除掉 inline mock 的所有内部状态。在这个方法调用后尝试和mock进行交互的话会抛出 `DisableMockException`

这个方法只对 inline mock maker 有意义。对于其他情况，此方法都是没有用的，且无需使用。

由于 inline mocking 的问题，这个方法对于解决细微的内存泄漏问题，非常有用。如果你遇到了这个问题，在测试的最后调用这个方法（或者在 `@After` 方法中）。请参阅在 Mockito 测试代码中使用 "clearInlineMocks "的示例。要了解为什么内联模拟生成器会跟踪模拟对象，请参阅 `InlineMockMaker`。

Mockito 的 "内联模拟 "可以模拟最终类型、枚举和最终方法（更多信息请参阅 Mockito javadoc 第 39 节）。该方法只有在使用 InlineMockMaker 时才有意义。如果您使用的是其他 MockMaker，则此方法无效。



```java

 public class ExampleTest {

     @After
     public void clearMocks() {
         Mockito.framework().clearInlineMocks();
     }

     @Test
     public void someTest() {
         ...
     }
 }
```

# 48 Mock静态方法  3.4.0

当使用 inline mock maker 的时候，可以 mock static 方法的调用，在当前线程中，在一个用户定义的范围内。
这样，Mockito 确保并发的顺序的运行测试，并且不受干扰。为了确保 staic 的 mock 保持临时性，推荐在 try-with-resources 结构里定义。在下面的这个例子中，Foo的静态方法会返回 foo 除非被mock:

```java
assertEquals("foo", Foo.method());
try (MockedStatic mocked = mockStatic(Foo.class)) {
    mocked.when(Foo::method).thenReturn("bar");
    assertEquals("bar", Foo.method());
    mocked.verify(Foo::method);

    // java 7 stub 和 verify 也可以这么写
    when(Foo.method()).thenReturn("bar");

    verify(Foo.class, time(1));
    Foo.method();
    // 或者
    mocked.verify(new MockedStatic.Verification() {
        @Override
        public void apply() throws Throwable {
            Foo.method();
        }
    }, times(1));
}
assertEquals("foo", Foo.method());
```

由于 静态模拟的 范围已定义，一旦范围被释放，就会返回原始的行为。为了定义 mock 行为 并且 验证静态调用，使用 `MockedStatic` 返回值。

# 49 Mocking 对象构造 3.5.0+

当使用 inline mock maker 的时候，可以在当前线程、用户定义的范围内，创建 mock 通过构造器的调用。这种方式，Mockito 保证 并发和顺序运行测试，并且不受干扰。为了保证 ... 临时性……

```java

 assertEquals("foo", new Foo().method());
 try (MockedConstruction mocked = mockConstruction(Foo.class)) {
 Foo foo = new Foo();
 when(foo.method()).thenReturn("bar");
 assertEquals("bar", foo.method());
 verify(foo).method();
 }
 assertEquals("foo", new Foo().method());
```

由于 mock 范围已定义，一旦范围被释放，就会返回原始的行为。为了定义 mock 行为 并且 验证静态调用，使用 `MockedConstruction` 返回值。

# 50 避免在仅模拟接口的时候生成代码 3.12.2+

JVM提供了 Proxy 功能来给接口类型创建动态代理。对于大多数应用程序，Mockito 必须能够通过默认的 mock maker 来 mock 类，或者甚至是 final class 由 inline mock maker。为了创建这些mock，mockito需要设置不同的JVM能力，并且必须应用 code generation。如果只有接口被mock，
如果只模拟接口，则可以选择使用基于 API 的 org.mockito.internal.creation.proxy.ProxyMockMaker，Proxy 这可以避免其他模拟生成器的多种开销，但也将模拟限制在接口上。可以通过 mockito 扩展机制明确激活此模拟生成器，只需在类路径中创建一个 /mockito-extensions/org.mockito.plugins.MockMaker包含值的文件即可mock-maker-proxy。
If only interfaces are supposed to be mocked, one can however choose to use a org.mockito.internal.creation.proxy.ProxyMockMaker that is based on the Proxy API which avoids diverse overhead of the other mock makers but also limits mocking to interfaces. This mock maker can be activated explicitly by the mockito extension mechanism, just create in the classpath a file /mockito-extensions/org.mockito.plugins.MockMaker containing the value mock-maker-proxy.

# 51 标记类为 unmockable 4.1.0+

In some cases, mocking a class/interface can lead to unexpected runtime behavior. For example, mocking a java.util.List is difficult, given the requirements imposed by the interface. This means that on runtime, depending on what methods the application calls on the list, your mock might behave in such a way that it violates the interface.
For any class/interface you own that is problematic to mock, you can now mark the class with @DoNotMock. For usage of the annotation and how to ship your own (to avoid a compile time dependency on a test artifact), please see its JavaDoc.

# 52 @Mock 注解的新严格性属性 和 `MockSettings.strictness()` 方法 4.6.0+

你现在可以给单个mock自定义 严格性 级别，要么使用 `@Mock`注解的 strictness 属性，或者使用`MockSettings.strictness()`。这对于你想要所有的mock都严格，但是其中一个mock很宽容很有用。
```java
  @Mock(strictness = Strictness.LENIENT)
   Foo mock;
   // using MockSettings.withSettings()
   Foo mock = Mockito.mock(Foo.class, withSettings().strictness(Strictness.WARN));
 
```

# 53 指定 mock maker 给独立的 mock 4.8.0+

你可能遇到这种情况，你只想给某个特殊的测试 使用一个不同的 mock maker （模拟生成器）。在这些情况下，你可以临时的使用 `MockSettings.mockMaker(String)`和`Mock.mockMaker()`来指定 mock maker 给一个特殊的 mock (which) 导致了问题

```java

   // using annotation
   @Mock(mockMaker = MockMakers.SUBCLASS)
   Foo mock;
   // using MockSettings.withSettings()
   Foo mock = Mockito.mock(Foo.class, withSettings().mockMaker(MockMakers.SUBCLASS));
 
```

# 54 mock / spy 不指定类 4.10.0+

你现在可以不用指定参数调用`mock()`和`spy()`方法了。
```java
   Foo foo = Mockito.mock();
   Bar bar = Mockito.spy();
```

Mockito 会自动监测需要的类

它只在你将 `mock()`或`spy()`分配给一个变量/字段 有显式类型的 有效。如果用于了隐式类型，java编译器不能自动判断出mock的类型，你需要显式传递 `Class`

# 55 和 assertion 验证 （使用断言进行验证） 5.3.0+

为了验证 verification 里的参数，相较于 `ArgumentCaptor`，你现在可以使用 `ArgumentMatchers.assertArg(Consumer)`

```java
   verify(serviceMock).doStuff(assertArg(param -> {
     assertThat(param.getField1()).isEqualTo("foo");
     assertThat(param.getField2()).isEqualTo("bar");
   }));
 
```



