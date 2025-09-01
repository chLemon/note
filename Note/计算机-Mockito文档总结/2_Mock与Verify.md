# 1. 可以 Mock 什么？

可以创建 mock 的有：

1. 接口
2. 类

# 2. Mock 的返回值

当调用 mock 的方法时，默认会根据方法返回值类型返回：

-   null
-   Java 原生类型对应默认值，例如 int 返回 0，boolean 返回 false
-   包装类对应默认值，例如 Integer 返回 0，Boolean 返回 false
-   空集合

## 2.1. 改变默认返回值（1.7+）

可以创建有着特殊返回值的 mock，通常不会使用这个高级功能。不过在处理遗留代码时，可能会很有用。

```java
Foo mock = mock(Foo.class, Mockito.RETURNS_SMART_NULLS);
Foo mockTwo = mock(Foo.class, new YourOwnAnswer());
```

> `Answer` 是 Mockito 提供的一个接口，用来表示 mock 的返回值，详见 [4_Stub](4_Stub.md)

### 2.1.1. RETURNS_SMART_NULLS

当调用没有被 stub 的方法时，如果返回值是对象，默认会返回 null，那么很容易导致 `NullPointerException`，而使用 `Mockito.RETURNS_SMART_NULLS` 时，会返回一个 `SmartNull` 。它会给出更好的异常信息，指出没有 stub 的方法被调用的行，可以直接点一下 stack trace 跳转过去。

`RETURNS_SMART_NULLS` 首先会尝试返回 0 / 空集合 / 空字符串，都不行时返回 `SmartNull`。不过，如果返回值是 final 的，会返回一个单纯的 null

## 2.2. 部分模拟 partial mock（1.8+）

详见 [3_Spy 与部分 mock](3_Spy与部分mock.md)

可以通过 `thenCallRealMethod()` 调用 mock 方法的真实实现

```java
// 你可以选择性的在 mock 上启用 部分mock 的能力
Foo mock = mock(Foo.class);

// 确保方法的真实实现是安全的。如果方法抛出了异常或者依赖了某些对象的状态，就很麻烦了
when(mock.someMethod()).thenCallRealMethod();
```

# 3. 创建 mock 的方法

## 3.1. `mock()`方法

```java
List mockedList = Mockito.mock(List.class);
```

### 3.1.1. 不指定类（4.10.0+）

```java
Foo foo = Mockito.mock();
Bar bar = Mockito.spy();
```

mock 被赋值的对象必须是有显式类型的，编译器会自动解析。

## 3.2. 注解方式`@Mock`（推荐）

```java
public class ArticleManagerTest {

    @Mock
    private ArticleDatabase database;

    @Test
    void testSomethingInJunit5(@Mock ArticleDatabase database) {
        ...
```

优点：

1. 不同测试方法里，不用重复写 mock 的代码
2. 测试代码更容易读，mock 的变量名一致

> 注意：如果要使用注解方式，需要在某个地方调用`openMocks()`或者使用`MockitoJUnitRunner`或`MockitoRule`，详见 [5\_框架能力](5_框架能力.md)

### 3.2.1. `@InjectMocks`

被这个注解标记的字段，Mockito 会自动创建一个对象，并尝试将用`@Mock`和`@Spy`创建的 mock 注入到这个对象中。

例子：

```java
public class ArticleManagerTest extends SampleBaseTestCase {

    @Mock
    private ArticleCalculator calculator;

    // 注意 @Mock 的 name 属性
    @Mock(name = "database")
    private ArticleDatabase dbMock;

    @Spy
    private UserProvider userProvider = new ConsumerUserProvider();

    @InjectMocks
    // 会尝试创建 manager 实例，并将以上3个 mock 注入
    private ArticleManager manager;

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

Mockito 会依次尝试 3 种策略注入 mock，注意，**如果注入失败并不会报错**

1. 构造器注入 constructor injection
2. setter 注入 property setter injection
3. field 注入 field injection

#### 3.2.1.1. 构造器注入

Mockito 会选择参数最多的构造器，然后将测试代码中通过注解创建的 mock 传入，来构造被`@InjectMocks`标记的字段。未匹配成功的参数会传 null。
如果这个对象通过构造器成功创建了，Mockito 不会继续尝试其他注入策略。

```java
public class ArticleManager {
    ArticleManager(ArticleCalculator calculator, ArticleDatabase database) {
        // parameterized constructor
    }
}
```

如果 `ArticleManager` 有这样一个构造器，上述例子中会进行 manager 的实例化，并将 calculator 和 database 注入。
构造器的可见性可以是 publc / package-protected / protected / private ，但是 Mockito 不能实例化 普通内部类、本地类、抽象类、接口。对于静态内部类可能看情况。

#### 3.2.1.2. setter 注入

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

如果 `ArticleManager` 只有无参构造器，并且有一系列 setter 方法，会根据无参构造器实例化，并使用 setter 方法将 calculator 和 database 注入。

Mockito 不能实例化 普通内部类、本地类、抽象类、接口。对于静态内部类可能看情况。

setter 方法可以是 private 的。

Mockito 优先根据类型进行匹配，如果存在多个相同类型的 property，则会通过 name 进行匹配。

1. 如果有多个相同类型的 property，最好对所有使用`@Mock`的字段标注 name
2. 如果 `@InjectMocks` 标记的字段没有实例化，并且该类有无参构造器，然后它会通过无参构造器初始化。

#### 3.2.1.3. field 注入

```java
public class ArticleManager {
    private ArticleDatabase database;
    private ArticleCalculator calculator;
}
```

这种情况下，会进行 field 注入。

field 可以是 private 的，但是 static 和 final 的不会进行注入。

Mockito 优先根据类型进行匹配，如果存在多个相同类型的 field，则会通过 name 进行匹配。

1. 如果有多个相同类型的 field，最好对所有使用`@Mock`的字段标注 name
2. 如果 `@InjectMocks` 标记的字段没有实例化，并且该类有无参构造器，然后它会通过无参构造器初始化。

最后，在这个例子里，没有注入会发生：

```java
public class ArticleManager {
    private ArticleDatabase database;
    private ArticleCalculator calculator;

    ArticleManager(ArticleObserver observer, boolean flag) {
        // 在测试代码里没有通过注解创建 observer 的 mock
        // flag 是 boolean 类型，不能被 mock
    }
}
```

#### 3.2.1.4. 注意

1. `@InjectMocks`仅仅会注入使用`@Spy`和`@Mock`注解创建的 mocks / spies
2. 要使用注解方式，需要在某个地方调用`openMocks()`或者使用`MockitoJUnitRunner`或`MockitoRule`，详见 [5\_框架能力](5_框架能力.md)
3. Mockito 不是一个依赖注入的框架，不要指望这个简单的依赖注入可以构造好一个特别复杂的对象
4. `@InjectMocks` 和 `@Spy` 可以同时使用，详见 [3_Spy 与部分 mock](3_Spy与部分mock.md)

## 3.3. Mock final 类型，enums 和 final 方法 （2.1.0+，5.0.0+默认开启）

需要 inline mock maker 的支持，详见 [5\_框架能力](5_框架能力.md)。注意以下方法不能 mock

1. `java.*` 下 package-visible 的 方法
2. `native`的方法

## 3.4. Mock 静态方法（3.4.0+）

需要 inline mock maker 的支持。

```java
// Foo.method() 默认返回 foo
assertEquals("foo", Foo.method());
try (MockedStatic mocked = mockStatic(Foo.class)) {
    // stub 为 bar
    mocked.when(Foo::method).thenReturn("bar");
    assertEquals("bar", Foo.method());
    mocked.verify(Foo::method);
}
// 恢复返回 foo
assertEquals("foo", Foo.method());
```

mock 生效范围：当前线程内，用户指定的范围内。

在上述例子中，生效范围在 try-with-resources 代码块内，即 `mockStatic()` 返回值调用 `close()` 前。

Mockito 可以保证这个区域内的代码 顺序执行，并发安全，不受干扰。推荐在 try-with-resources 内使用。

## 3.5. 自动 mock 指定类用构造器创建的对象（3.5.0+）

需要 inline mock maker 的支持。

```java
// Foo.method() 默认返回 foo
assertEquals("foo", new Foo().method());
// 这个范围里所有的 用所有构造器 new 的 Foo 对象 都会被 mock
try (MockedConstruction mocked = mockConstruction(Foo.class)) {
    Foo foo = new Foo();
    // 可以stub
    when(foo.method()).thenReturn("bar");
    assertEquals("bar", foo.method());
    verify(foo).method();
}
// 离开有效区域，恢复原来的状态
assertEquals("foo", new Foo().method());
```

mock 生效范围：当前线程内，用户指定的范围内。

在上述例子中，生效范围在 try-with-resources 代码块内，即 `mockConstruction()` 返回值调用 `close()` 前。

Mockito 可以保证这个区域内的代码 顺序执行，并发安全，不受干扰。推荐在 try-with-resources 内使用。

## 3.6. 可序列化的 mock （1.8.1+）

可以通过序列化的方式创建 mock 。

**警告：这应该很少用在单元测试中。**

这个功能的实现是为了一个特殊的情况：在 web 环境中，系统有一个不可靠的外部依赖，需要从这个外部依赖返回若干对象，这个对象在传递过程中需要被序列化。

使用 `MockSettings.serializable()` 来创建可序列化的 mock

```java
List serializableMock = mock(List.class, withSettings().serializable());
```

这个 mock 可以被序列化，可以认为该类满足所有的普通序列化需求。这里指的是，满足 jdk 定义的 `serializable`

spy 的可序列化会更麻烦一点。

```java
List<Object> list = new ArrayList<Object>();
List<Object> spy = mock(ArrayList.class, withSettings()
                .spiedInstance(list)
                .defaultAnswer(CALLS_REAL_METHODS)
                .serializable());
```

# 4. Verify 验证

当不关心方法的返回值，只关心方法的交互情况时，使用 verify

## 4.1. verify 基础用法

```java
import static org.mockito.Mockito.*;

// mock 创建
List mockedList = mock(List.class);

// 使用 mock
mockedList.add("one");

mockedList.clear();

// verify 调用1次 add() 方法，且参数是 "one"
verify(mockedList).add("one");
// verify 调用1次 clear() 方法
verify(mockedList).clear();
```

这里参数是否相同的判断，是调用了对象的 `equals()` 方法。

## 4.2. verify 调用指定次数

```java
List mockedList = mock(List.class);

mockedList.add("once");

mockedList.add("twice");
mockedList.add("twice");

// verify 调用1次 add() 方法，且参数是 "one"。不填写次数时，默认是 times(1)
verify(mockedList).add("once");
// verify add("twice") 调用过2次
verify(mockedList, times(2)).add("twice")
// verify 从来没有交互过
verify(mockedList, never()).add("never happened");
// 至多，至少
verify(mockedList, atMostOnce()).add("once");
verify(mockedList, atMost(5)).add("three times");
verify(mockedList, atLeastOnce()).add("three times");
verify(mockedList, atLeast(2)).add("three times");
```

## 4.3. 自定义 verify 失败的信息（2.1.0+）

可以指定 verify 失败时，打印一个指定的信息
允许指定当验证失败时打印一个自定义的信息

```java
// 会在 verify 失败时，打印
verify(mock, description("This will print on failure")).someMethod();

// 可以在任何 verify 方式里添加
verify(mock, times(2).description("someMethod should be called twice")).someMethod();
```

## 4.4. verify 除了已验证的交互外，无其他方法交互

```java
mockedList.add("one");
mockedList.add("two");

verify(mockedList).add("one");

// 这个判断会失败，因为还有 add("two") 被调用
verifyNoMoreInteractions(mockedList);
```

不推荐大量使用此方法，更推荐使用`never()`，以准确描述测试意图。

这个方法可以结合 `ignoreStubs()` 使用，详见 [4_Stub](4_Stub.md)

## 4.5. verify 按照指定顺序进行方法调用

可以通过 `inOrder` verify 某些方法调用之间是按照指定顺序进行的

```java

// A. 要验证 singleMock 的方法是按照指定顺序调用的
List singleMock = mock(List.class);

// A.1 调用 mock 的方法
singleMock.add("was added first");
singleMock.add("was added second");

// A.2 创建 inOrder 验证器
InOrder inOrder = inOrder(singleMock);

// A.3 下面会 verify，一定是先调用 frist 再调用 second ，注意是调用 inorder 的 verify 方法
inOrder.verify(singleMock).add("was added first");
inOrder.verify(singleMock).add("was added second");

// B. 接下来验证这样的场景：多个 mock 必须以特定顺序调用
List firstMock = mock(List.class);
List secondMock = mock(List.class);

// B.1 调用 mock 的方法
firstMock.add("was called first");
secondMock.add("was called second");

// B.2 把所有需要验证调用顺序的 mock 传入
InOrder inOrder = inOrder(firstMock, secondMock);

//following will make sure that firstMock was called before secondMock
// B.3 下面会 verify，一定是先调用 firstMock 再调用 secondMock ，注意是调用 inorder 的 verify 方法
inOrder.verify(firstMock).add("was called first");
inOrder.verify(secondMock).add("was called second");

// 上面 A 和 B 2种场景可以任意混合使用
```

`inOrder`的 verify 是很灵活的，不需要一一 verify 所有的交互，只需要按照顺序 verify 关心的交互

当然，创建 `InOrder` 对象的时候，你也可以只把和顺序验证相关的 mock 传进去

## 4.6. 对 verify 指定超时时间

允许 验证 超时。这会导致一个 verify 去等待一个期望的交互 特定的时间，而不是在还没有发生的时候立刻失败。
可能对并发条件下的测试有用。

这个特征应该非常少用——这到一个更好的方法去测试你的多线程系统
还没有实现 和 InOrder 验证 一起用。

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

## 4.7. 捕捉参数，进行进一步的断言（1.8+）

推荐使用上面的写法对参数进行验证，会调用参数的`equals()`方法对参数进行匹配。但是在有些特殊场景下，先捕捉到 mock 调用时使用的参数，再进行参数的验证也很有用：

```java
ArgumentCaptor<Person> argument = ArgumentCaptor.forClass(Person.class);
verify(mock).doSomething(argument.capture());
assertEquals("John", argument.getValue().getName());
// 这个测试中，只需要验证 Person 的某个属性 name ，而不是验证 Person 是否相同
```

### 4.7.1. 警告

`ArgumentCaptor`只推荐与 verify 使用，不推荐和 stub 使用。和 stub 使用时，由于 captor 是创建在 assert block 的外面，会降低测试的可读性。同时，stub 方法如果没有调用，没有参数会被捕捉到，那么在报错时，不容易定位到问题的代码

> assert block: 也称为 then block，指的是测试时，在调用被测方法后，集中进行 assert 的代码部分

在某种程度上，ArgumentCaptor 和自定义参数匹配器很像，这两种技术都可以确保特定的参数传递给了 mock。通常，ArgumentCaptor 更适合：

1. 需要复用传入 mock 方法的参数
2. 只是需要 assert 参数的值用来完成 verify

通常 自定义参数匹配器 对于更合适用于 stub。

### 4.7.2. 注解方式（1.8.3+）

`@Captor`简化了`ArgumentCaptor`的创建

并且可以避免如果要抓的参数和泛型相关时，烦人的编译器警告

## 4.8. ArgumentMatcher 参数匹配器

-   mock 在 verify 交互时，可以指定具体参数；
-   stub 时也可以指定具体的参数。这里参数是否匹配默认使用对象的`equals()`方法。

Mockito 还提供了若干参数匹配器来进行更灵活的参数指定：

```java
// stub : 使用 anyInt() 参数匹配器，匹配任意整数
when(mockedList.get(anyInt())).thenReturn("element");

// 输出 element
System.out.println(mockedList.get(999));

// verify : 使用 anyInt() 匹配任意整数
verify(mockedList).get(anyInt());

// stub : 使用自定义的参数匹配器，通过 argThat() 方法来创建自定义的参数匹配器
when(mockedList.contains(argThat(isValid()))).thenReturn(true);

// 也可以用 lambda 表达式
verify(mockedList).add(argThat(someString -> someString.length() > 5));
```

### 4.8.1. 注意

1. 应该尽量少地使用参数匹配器，这样写出来的测试更加干净简单
2. 如果方法里的某个参数使用了参数匹配器，那么所有参数都必须是参数匹配器
3. 如果方法参数是原生类型（int long ...）不能使用 `any()`，必须使用对应的 `anyInt()`

```java
// 正确，使用 eq()
verify(mock).someMethod(anyInt(), anyString(), eq("third argument"));

// 错误
verify(mock).someMethod(anyInt(), anyString(), "third argument");
```

### 4.8.2. 推荐使用的参数匹配器类 ArgumentMatchers

#### 4.8.2.1. anyX()

| Modifier and Type | Method             | Description                                        | 翻译                                             |
| ----------------- | ------------------ | -------------------------------------------------- | ------------------------------------------------ |
| static <T> T      | any()              | Matches anything, including nulls.                 | 匹配所有东西，包括`null`，注意原生类型不能用这个 |
| static <T> T      | any(Class<T> type) | Matches any object of given type, excluding nulls. | 匹配给定类型的所有东西，不包括`null`             |
| static boolean    | anyBoolean()       | Any boolean or non-null Boolean                    | 任何`boolean`或者非`null`的`Boolean`             |
| static byte       | anyByte()          | Any byte or non-null Byte.                         | 任何`byte`或者非`null`的`Byte`                   |
| static char       | anyChar()          | Any char or non-null Character.                    | 任何`char`或者非`null`得`Character`              |
| static short      | anyShort()         | Any short or non-null Short.                       | 任何`short`或者非`null`的`Short`                 |
| static int        | anyInt()           | Any int or non-null Integer.                       | 任何`int`或者非`null`的`Integer`                 |
| static long       | anyLong()          | Any long or non-null Long.                         | 任何`long`或非`null`的`Long`                     |
| static float      | anyFloat()         | Any float or non-null Float.                       | 任何`float`或者非`null`的`Float`                 |
| static double     | anyDouble()        | Any double or non-null Double.                     | 任何`double`或者非`null`的`Double`               |
| static String     | anyString()        | Any non-null String                                | 任何非`null`的`String`                           |

#### 4.8.2.2. any集合()

| Modifier and Type        | Method          | Description              | 翻译                       |
| ------------------------ | --------------- | ------------------------ | -------------------------- |
| static <T> Collection<T> | anyCollection() | Any non-null Collection. | 任何非`null`的`Colleciton` |
| static <T> List<T>       | anyList()       | Any non-null List.       | 任何非`null`的`List`       |
| static <T> Set<T>        | anySet()        | Any non-null Set.        | 任何非`null`的`Set`        |
| static <K,V> Map<K,V>    | anyMap()        | Any non-null Map.        | 任何非`null`的`Map`        |
| static <T> Iterable<T>   | anyIterable()   | Any non-null Iterable.   | 任何非`null`的`Iterable`   |

#### 4.8.2.3. eq() / same()

| Modifier and Type | Method                                  | Description                                                                                                          | 翻译                                   |
| ----------------- | --------------------------------------- | -------------------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| static <T> T      | same(T value)                           | Object argument that is the same as the given value.                                                                 | 和给的参数是同一个对象 ==              |
| static <T> T      | eq(T value)                             | Object argument that is equal to the given value.                                                                    | 和给的参数`equals()`返回 true          |
| static boolean    | eq(boolean value)                       | boolean argument that is equal to the given value.                                                                   |
| static byte       | eq(byte value)                          | byte argument that is equal to the given value.                                                                      |
| static char       | eq(char value)                          | char argument that is equal to the given value.                                                                      |
| static short      | eq(short value)                         | short argument that is equal to the given value.                                                                     |
| static int        | eq(int value)                           | int argument that is equal to the given value.                                                                       |
| static long       | eq(long value)                          | long argument that is equal to the given value.                                                                      |
| static float      | eq(float value)                         | float argument that is equal to the given value.                                                                     |
| static double     | eq(double value)                        | double argument that is equal to the given value.                                                                    |
| static <T> T      | refEq(T value, String... excludeFields) | Object argument that is reflection-equal to the given value with support for excluding selected fields from a class. | 和给的参数反射相等的，支持排除一些字段 |
| static <T> T      | isA(Class<T> type)                      | Object argument that implements the given class.                                                                     |

#### 4.8.2.4. null 相关

| Modifier and Type | Method                   | Description                                        | 翻译 |
| ----------------- | ------------------------ | -------------------------------------------------- | ---- |
| static <T> T      | isNotNull()              | Not null argument.                                 |
| static <T> T      | isNull()                 | null argument.                                     |
| static <T> T      | isNotNull(Class<T> type) | Not null argument.                                 |
| static <T> T      | isNull(Class<T> type)    | null argument.                                     |
| static <T> T      | notNull()                | Not null argument.                                 |
| static <T> T      | notNull(Class<T> type)   | Not null argument.                                 |
| static <T> T      | nullable(Class<T> clazz) | Argument that is either null or of the given type. |

#### 4.8.2.5. argThat()

| Modifier and Type | Method                                        | Description                                                                                                                                        | 翻译                                                                 |
| ----------------- | --------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| static <T> T      | argThat(ArgumentMatcher<T> matcher)           | Allows creating custom argument matchers.                                                                                                          | 支持创建自定义的参数匹配器                                           |
| static boolean    | booleanThat(ArgumentMatcher<Boolean> matcher) | Allows creating custom boolean argument matchers.                                                                                                  | 支持创建自定义的 boolean 参数匹配器                                  |
| static byte       | byteThat(ArgumentMatcher<Byte> matcher)       | Allows creating custom byte argument matchers.                                                                                                     | 支持创建自定义的 byte 参数匹配器                                     |
| static char       | charThat(ArgumentMatcher<Character> matcher)  | Allows creating custom char argument matchers.                                                                                                     | 支持创建自定义的 char 参数匹配器                                     |
| static short      | shortThat(ArgumentMatcher<Short> matcher)     | Allows creating custom short argument matchers.                                                                                                    |
| static int        | intThat(ArgumentMatcher<Integer> matcher)     | Allows creating custom int argument matchers.                                                                                                      |
| static long       | longThat(ArgumentMatcher<Long> matcher)       | Allows creating custom long argument matchers.                                                                                                     |
| static float      | floatThat(ArgumentMatcher<Float> matcher)     | Allows creating custom float argument matchers.                                                                                                    |
| static double     | doubleThat(ArgumentMatcher<Double> matcher)   | Allows creating custom double argument matchers.                                                                                                   | 支持创建自定义的 double 参数匹配器                                   |
| static <T> T      | assertArg(Consumer<T> consumer)               | Allows creating custom argument matchers where matching is considered successful when the consumer given by parameter does not throw an exception. | 支持创建自定义参数匹配器，当`consumer`没有抛出异常时，认为是成功的   |
| static <T> T      | assertArg(ThrowingConsumer<T> consumer)       | Allows creating custom argument matchers where matching is considered successful when the consumer given by parameter does not throw an exception. | 支持创建自定义的参数匹配器，当`consumer`没有抛出异常时，认为是成功的 |

#### 4.8.2.6. String 相关

| Modifier and Type | Method                     | Description                                                 | 翻译                     |
| ----------------- | -------------------------- | ----------------------------------------------------------- | ------------------------ |
| static String     | contains(String substring) | String argument that contains the given substring.          | 匹配包含指定子串的字符串 |
| static String     | startsWith(String prefix)  | String argument that starts with the given prefix.          |
| static String     | endsWith(String suffix)    | String argument that ends with the given suffix.            | 匹配指定子串结尾字符串   |
| static String     | matches(String regex)      | String argument that matches the given regular expression.  |
| static String     | matches(Pattern pattern)   | Pattern argument that matches the given regular expression. |

### 4.8.3. Java 8 Lambda Matcher 支持（2.1.0+）

可以使用 Java 8 的 lambda 表达式来写 `ArgumentMatcher` 来减少对于 `ArgumentCaptor` 的依赖。

如果需要 verify mock 的某个方法调用的参数是正确的，通常会使用 `ArgumentCaptor` 来捕捉到参数，然后做一些后续的断言。虽然对于复杂的例子，这样很有用，但是这样做通常都太麻烦了。

用 lambda 表达式来写 自定义参数匹配器 非常的简单。如下：

```java
// verify 往 list 里2次添加的字符串长度都是小于5的
verify(list, times(2)).add(argThat(string -> string.length() < 5));

// Java 7 里等效的写法，不够简洁
verify(list, times(2)).add(argThat(new ArgumentMatcher<String>(){
    public boolean matches(String arg) {
        return arg.length() < 5;
    }
}));

// 更复杂的例子 你可以方便地指定复杂的验证行为
verify(target, times(1)).receiveComplexObject(argThat(obj -> obj.getSubObject().get(0).equals("expected")));

// 也可以用于 stub ，使得在特定输入下有特定的输出
// 如果 list 内的元素小于3个，会返回 null
when(mock.someMethod(argThat(list -> list.size()<3))).thenReturn(null);
```

## 4.9. verify 里直接写 assert（5.3.0+）

相较于 `ArgumentCaptor`，现在可以使用 `ArgumentMatchers.assertArg(Consumer)`

```java
verify(serviceMock).doStuff(assertArg(param -> {
    assertThat(param.getField1()).isEqualTo("foo");
    assertThat(param.getField2()).isEqualTo("bar");
}));
```

# 5. 元数据和泛型类型的保留（2.1.0+）

Mockito 现在会保留所 mock 的类中方法和类型上的注解，包括泛型元数据。之前，mock 是不会保留类型上的注解的，除非显式继承，并且永远不会保留方法上的注解。因此，下面这些条件现在可以成立：

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

# 6. 重置/清除 mock 的状态

## 6.1. reset（1.8+）

通常情况下是不需要重置 mock 的，只需要给每个测试方法创建新的 mock 就可以了。与其使用 reset 方法，更应该写简单、小、并且聚焦的测试方法，而不是超长的、超特殊指定的测试。

使用这个方法是一种代码异味，说明测试代码写的不好。

reset 出现在测试方法的中间，这意味着在一次测试里要测的东西太多了。测试代码应该小，并且专注在一个小的行为上。

Mockito 添加这个方法的唯一理由是：配合通过容器注入的 mock。

```java
List mock = mock(List.class);
when(mock.size()).thenReturn(10);
mock.add(1);

reset(mock);
//at this point the mock forgot any interactions and stubbing
```

## 6.2. 清除 inline mocking 里的 mock 状态（2.25.0+）

在一些特殊、罕见的情况下，inline mocking 会导致内存泄漏。现在不知道怎么解决这个问题，所以，Mockito 引入了一个新的 API 来明确的清除 mock 状态（只在 inline mocking 里有意义）。

### 6.2.1. `MockitoFramework.clearInlineMocks()`

清除掉 inline mock 的所有内部状态。在这个方法调用后尝试和 mock 进行交互的话会抛出 `DisableMockException`

这个方法只对 inline mock maker 有意义。对于其他情况，此方法都是没有用的，且无需使用。

这个方法对于解决 inline mocking 中细微的内存泄漏非常有用。如果你遇到了这个问题，在测试的最后调用这个方法（或者在 `@After` 方法中）。请参阅在 Mockito 测试代码中使用 "clearInlineMocks "的示例。要了解为什么内联模拟生成器会跟踪 mock 对象 ，请参阅 `InlineMockMaker`。

Mockito 的 inline mock 可以 mock final 类型、枚举 和 final 方法（更多信息请参阅 Mockito javadoc 第 39 节）。该方法只有在使用 InlineMockMaker 时才有意义。如果您使用的是其他 MockMaker，则此方法无效。

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
