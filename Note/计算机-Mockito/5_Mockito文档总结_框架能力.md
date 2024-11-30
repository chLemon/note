# 1. Mockito 版本 和 Java 版本

-   `mockito-core` 4.\* 要求 Java 8
-   `mockito-core` 5.\* 要求 Java 11

# 2. 和 BDD 风格的适配

BDD 风格写测试时使用 //given //when //then 注释作为测试方法的基本部分。这正是我们编写测试的方法，并且我们也热切鼓励你也这样用。

从这里开始学习 BDD：https://en.wikipedia.org/wiki/Behavior-driven_development

问题是，现在的 stub api 使用了 `when()` ，无法很好的和 //given //when //then 注释集成在一起。

因为 stub 属于 测试的 given 部分，而不是 when 部分

所以，在`BDDMockito` 这个类里引入了一个别名，这样你可以用 `BDDMockito.given(Object)` 来进行 stub。现在他可以和 BDD 风格测试的 given 部分很好的集成了。

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

## 2.1. BDD 风格的验证 （1.10.0+）

允许使用 BDD 风格的验证，启用 `then 关键字来验证

```java
given(dog.bark()).willReturn(2);

// when
...

then(person).should(times(2)).ride(bike);
```

更多详见 `BDDMockito.then(Object)`

# 3. 使用注解

现在 Mockito 提供 3 种方法来激活注解功能：

1. 用`@RunWith(MockitoJUnitRunner.class)`注解 JUnit 测试类
2. 在`@Before`方法里调用 `MockitoAnnotations.openMocks(Object)`
3. 用 Mockito Junit Rule （1.10.17+）

```java
@RunWith(YetAnotherRunner.class)
public class TheTest {
    @Rule public MockitoRule mockito = MockitoJUnit.rule();
    // ...
}
```

# 4. 正确使用框架

如果在使用 Mockito 的过程中遇到了任何问题，都推荐先去读 FAQ：https://github.com/mockito/mockito/wiki/FAQ

也可以发邮件：https://groups.google.com/g/mockito

## 4.1. 正确性验证

Mockito 始终会验证用户是否正确使用它。并提供了一个验证方法 `validateMockitoUsage()`

### 4.1.1. validateMockitoUsage

这个方法会显式验证用户有没有正确使用 Mockito。由于 Mockito 始终都会验证这一点，所以这个方法通常不需要调用。

错误使用 Mockito 的例子

```java
// 没有 thenReturn()
when(mock.get());

// 要验证的方法调用放在了 verify() 里面
verify(mock.execute());

// 少写了要验证的方法
verify(mock);
```

这里还有个易错点 (gotcha)：

Mockito 会在“下一次”使用框架时对之前的内容做检查，包括下一次 verify, stub, 调用 mock 等。所以当前测试里的错误用法，Junit 会将下一个测试方法标红，报告测试失败。

通常这不会有什么问题，因为失败时 Mockito 会打印错误堆栈，里面有出错的地方，点击后可以直接导航到出错的地方。

不过如果你们已经有一些足够的测试基础设施（比如说自定义的 runner，或者所有测试类的 base class），那么在 `@After` 上加上这个函数也是极好的。

> gotcha: 口语中 got you 的简称，意思是 抓住你了，你中计了，骗到你了。
> 在计算机领域指那些，语法上合法的，但是极有可能是写错了的东西，例如 C 和 C++ 中的：
>
> ```c
> while(flag = true) {  // 死循环
>     // doSomething
> }
> ```

## 4.2. 使用更严格的 Mockito 来促使开发者写出更干净的测试，提升生产力

Mockito 默认是一个松散的 mock 框架。

mock 可以在无需设置任何期望下进行交互。是故意设置成这样的，这样可以强制用户明确出他们到底想 stub / verify 什么东西。这也非常的直观，容易使用，并且和 given when then 这种干净测试代码的模板 完美融合。这也是 Mockito 和之前的 mock 框架 的区别，之前都是严格的。

默认宽松的策略有时候会让 mockito 测试难以 debug。例如用户写错了 stub，可能是写了错误的参数，那么用户为了发现问题，只能用 debugger 去 debug 测试代码。理想情况下，测试的失败原因应该是显而易见的，不需要用 debugger 来识别根因。

从 2.1 开始，mockito 有了一些新的特性，推动框架往**严格**发展。

我们希望 Mockito 提供非常好的 debug 能力，同时不丢失核心 mock 风格，进而优化框架的 直观性、明确性、测试代码的干净简洁。

> https://javadoc.io/static/org.mockito/mockito-core/5.14.2/org/mockito/quality/Strictness.html

-   Strict stubbing with JUnit4 Rules - MockitoRule.strictness(Strictness) with Strictness.STRICT_STUBS
-   Strict stubbing with JUnit4 Runner - MockitoJUnitRunner.Strict
-   Strict stubbing with JUnit5 Extension - org.mockito.junit.jupiter.MockitoExtension
-   Strict stubbing with TestNG Listener MockitoTestNGListener
-   Strict stubbing if you cannot use runner/rule - MockitoSession
-   Unnecessary stubbing detection with MockitoJUnitRunner // 非必要的 stub 监测
-   Stubbing argument mismatch warnings, documented in MockitoHint

### 4.2.1. 新的 `Mockito.lenient()` 和 `MockSettings.lenient()` 方法（2.20.0+）

严格 stub 的特性（Strictness.STRICT_STUBS）在 Mockito 2 的早期就引入了。它非常有用，可以推动开发者写出更清晰、干净的测试代码，并提高生产效率。

严格 stub 会报告出不必要的 stub，监测出参数不匹配的 stub，并让测试代码更干净。

不过注意，在某些情况下，可能会产生误报。为了解决这个问题，可以只将特定的 stub 设置为 宽松 的，而其他所有的 stub 和 mock 依旧使用严格策略。

```java
lenient().when(mock.foo()).thenReturn("ok");
// lenient 宽容的
```

如果你希望有个 mock 上的所有 stub 都是 宽容的，则可以相应地配置模拟：

```java
Foo mock = Mockito.mock(Foo.class, withSettings().lenient());
```

更多参见 `lenient`

### 4.2.2. `@Mock`注解的新严格性属性 和 `MockSettings.strictness()` 方法（4.6.0+）

你现在可以给单个 mock 自定义 严格性 级别，要么使用 `@Mock` 注解的 strictness 属性，或者使用 `MockSettings.strictness()`。这对于你想要所有的 mock 都严格，但是其中一个 mock 很宽容很有用。

```java
@Mock(strictness = Strictness.LENIENT)
Foo mock;
// using MockSettings.withSettings()
Foo mock = Mockito.mock(Foo.class, withSettings().strictness(Strictness.WARN));
```

# 5. Mock 生成器 (MockMaker) ，新的 mockito-inline

Mockito 现在默认提供对于 final 类、方法的支持。自 5.0.0，这个功能默认开启了。

老的 mock maker 是创建一个新的类来生成 mock。现在我们提供了一个新的 mock maker，它结合使用了 Java instrumentation API 和 sub-classing 子类。这样，mock final 类型和方法就成为了可能。

在 5.0.0 之前的版本，这个 mock maker 默认是关闭的，由于它基于一个完全不同的 mock 机制，需要从社区中获取更多的反馈。可以通过 Mockito 扩展机制显式激活，只需要在 classpath 里创建一个文件 `/mockito-extensions/org.mockito.plugins.MockMaker`，文件内容包括 `mock-maker-inline`

为了方便起见，Mockito 团队提供了一个制品，预配置了这个 mock maker 。只需要将 `mockito-inline` 放在你的项目里。请注意，一旦将 final 类和方法的 mock 集成到默认 mock maker 中，此制品可能会停用。

（原来的 mock maker 在 `mockito-core`里，现在提供了一个新的 `mockito-inline`，有一些增强功能，但是长远来看，这些功能是会被整合进 `mockito-core` 中的，所以在整合进去后，`mockito-inline` 就不会继续保留了，在 5.3 的时候已经完成了这个操作）

关于这个 mock maker ，有一些值得注意的：

-   mock final 类型 和 enums 和下面这些 mock 设置不兼容：
    -   显式序列化支持 `withSettings.serializable()`
    -   额外接口 `withSettings().extraInterfaces()`
-   有些方法不能被 mock
    -   `java.*` 下 package-visible 的 方法
    -   `native`的方法
-   这个 mock maker 是围绕 Java Agent runtime attachment 设计的。这需要一个兼容的 JVM。JDK 里有，如果只是虚拟机 VM，9+的才有，让运行在一个非 JDK 的，9 之前的 VM，需要通过运行 JVM 的时候加参数 `-javaagent` 加上 Byte Buddy Java agent jar

> https://bytebuddy.net/#/

更多细节见：`org.mockito.internal.creation.bytebuddy.InlineByteBuddyMockMaker`

# 6. 其他

这部分不太重要，只是为了完整性先放在了这里

## 6.1. 获取 mock 的细节（2.2.x 增强）

Mockito 提供了一些 API 来检查 mock 的细节。这些 API 对于高级用户或在写 mock 框架集成的开发者很有用

```java
// 识别某个对象是否是 mock 或者 spy
Mockito.mockingDetails(someObject).isMock();
Mockito.mockingDetails(someObject).isSpy();

// 获取细节信息，如 mock 的类型，默认的返回值
MockingDetails details = mockingDetails(mock);
details.getMockCreationSettings().getTypeToMock();
details.getMockCreationSettings().getDefaultAnswer();

// 获取 mock 上的方法调用和 stub
MockingDetails details = mockingDetails(mock);
details.getInvocations();
details.getStubbings();

// 打印出所有的交互，包括 stub 和未使用的 stub
System.out.println(mockingDetails(mock).printInvocations());
```

## 6.2. `MockMaker` API (1.9.5+)

在 Google Android 开发人员的要求和补丁的推动下，Mockito 现在提供了一个扩展点，允许替换代理生成引擎。默认情况下，Mockito 使用 Byte Buddy 创建动态代理。

该扩展点适用于想要扩展 Mockito 的高级用户。例如，现在可以借助 dexmaker 使用 Mockito 进行 Android 测试。

有关更多详细信息、动机和示例，请参阅文档 MockMaker。

## 6.3. 31 Mockito 的 mock 可以是跨类加载器 `serialized | deserialized`

Mockito 引入了跨类加载器的序列化。与任何其他形式的序列化一样，模拟层次结构中的所有类型都必须可序列化，包括答案。由于此序列化模式需要做更多工作，因此这是一个可选设置。

```java
// use regular serialization
mock(Book.class, withSettings().serializable());

// use serialization across classloaders
mock(Book.class, withSettings().serializable(ACROSS_CLASSLOADERS));
```

详情请参阅 `MockSettings.serializable(SerializableMode)`

## 6.4. 34 打开或关闭插件 1.10.15+

mockito 中正在酝酿一项功能，允许切换 mockito 插件。更多信息请见此处 `PluginSwitch`

## 6.5. 41 用于框架集成的高级公共 API 2.10.+

2017 年夏天，我们决定 Mockito 应该提供更好的 API 以实现高级框架集成。新 API 不适用于想要编写单元测试的用户。它适用于需要使用一些自定义逻辑扩展或包装 Mockito 的其他测试工具和模拟框架。在设计和实施过程中（问题 1110），我们开发并更改了以下公共 API 元素：

-   New MockitoPlugins - Enables framework integrators to get access to default Mockito plugins. Useful when one needs to implement custom plugin such as MockMaker and delegate some behavior to the default Mockito implementation.
-   New MockSettings.build(Class) - Creates immutable view of mock settings used later by Mockito. Useful for creating invocations with InvocationFactory or when implementing custom MockHandler.
-   New MockingDetails.getMockHandler() - Other frameworks may use the mock handler to programmatically simulate invocations on mock objects.
-   New MockHandler.getMockSettings() - Useful to get hold of the setting the mock object was created with.
-   New InvocationFactory - Provides means to create instances of Invocation objects. Useful for framework integrations that need to programmatically simulate method calls on mock objects.
-   New MockHandler.getInvocationContainer() - Provides access to invocation container object which has no methods (marker interface). Container is needed to hide the internal implementation and avoid leaking it to the public API.
-   Changed Stubbing - it now extends Answer interface. It is backwards compatible because Stubbing interface is not extensible (see NotExtensible). The change should be seamless to our users.
-   NotExtensible - Public annotation that indicates to the user that she should not provide custom implementations of given type. Helps framework integrators and our users understand how to use Mockito API safely.

## 6.6. 42 用于集成的新 API：监听 verification start events 2.11.+

像 Spring 之类的框架集成时需要 公共 API 来 解决 double-proxy 使用场景。我们加了：

-   New VerificationStartedListener and VerificationStartedEvent enable framework integrators to replace the mock object for verification. The main driving use case is Spring Boot integration. For details see Javadoc for VerificationStartedListener.
-   New public method MockSettings.verificationStartedListeners(VerificationStartedListener...) allows to supply verification started listeners at mock creation time.
-   New handy method MockingDetails.getMock() was added to make the MockingDetails API more complete. We found this method useful during the implementation.

## 6.7. 43 用于集成的新 API: `MockitoSession` 可以通过测试框架使用了 2.15+

MockitoSessionBuilder 和 MockitoSession 被增强了，可以被测试框架集成重新使用，例如（MockitoRule for JUnit）

-   MockitoSessionBuilder.initMocks(Object...) allows to pass in multiple test class instances for initialization of fields annotated with Mockito annotations like Mock. This method is useful for advanced framework integrations (e.g. JUnit Jupiter), when a test uses multiple, e.g. nested, test class instances.
-   MockitoSessionBuilder.name(String) allows to pass a name from the testing framework to the MockitoSession that will be used for printing warnings when Strictness.WARN is used.
-   MockitoSessionBuilder.logger(MockitoSessionLogger) makes it possible to customize the logger used for hints/warnings produced when finishing mocking (useful for testing and to connect reporting capabilities provided by testing frameworks such as JUnit Jupiter).
-   MockitoSession.setStrictness(Strictness) allows to change the strictness of a MockitoSession for one-off scenarios, e.g. it enables configuring a default strictness for all tests in a class but makes it possible to change the strictness for a single or a few tests.
-   MockitoSession.finishMocking(Throwable) was added to avoid confusion that may arise because there are multiple competing failures. It will disable certain checks when the supplied failure is not null.

## 6.8. 44 弃用 `org.mockito.plugins.InstantiatorProvider` ，它泄露了内部 API，替换为了 `org.mockito.plugins.InstantiatorProvider2` 2.15.4+

## 6.9. 45 新的 JUnit Jupiter (JUnit5+)扩展

为了集成 JUnit5+，使用 `org.mockito:mockito-junit-jupiter` 制品。想知道集成的更多信息，看 `MockitoExtension` 的 JavaDoc

## 6.10. 50 避免在仅模拟接口的时候生成代码 3.12.2+

JVM 提供了 Proxy 功能来给接口类型创建动态代理。对于大多数应用程序，Mockito 必须能够通过默认的 mock maker 来 mock 类，或者甚至是 final class 由 inline mock maker。为了创建这些 mock，mockito 需要设置不同的 JVM 能力，并且必须应用 code generation。如果只有接口被 mock，
如果只模拟接口，则可以选择使用基于 API 的 org.mockito.internal.creation.proxy.ProxyMockMaker，Proxy 这可以避免其他模拟生成器的多种开销，但也将模拟限制在接口上。可以通过 mockito 扩展机制明确激活此模拟生成器，只需在类路径中创建一个 /mockito-extensions/org.mockito.plugins.MockMaker 包含值的文件即可 mock-maker-proxy。
If only interfaces are supposed to be mocked, one can however choose to use a org.mockito.internal.creation.proxy.ProxyMockMaker that is based on the Proxy API which avoids diverse overhead of the other mock makers but also limits mocking to interfaces. This mock maker can be activated explicitly by the mockito extension mechanism, just create in the classpath a file /mockito-extensions/org.mockito.plugins.MockMaker containing the value mock-maker-proxy.

## 6.11. 51 标记类为 unmockable 4.1.0+

In some cases, mocking a class/interface can lead to unexpected runtime behavior. For example, mocking a java.util.List is difficult, given the requirements imposed by the interface. This means that on runtime, depending on what methods the application calls on the list, your mock might behave in such a way that it violates the interface.
For any class/interface you own that is problematic to mock, you can now mark the class with @DoNotMock. For usage of the annotation and how to ship your own (to avoid a compile time dependency on a test artifact), please see its JavaDoc.

## 6.12. 53 指定 mock maker 给独立的 mock 4.8.0+

你可能遇到这种情况，你只想给某个特殊的测试 使用一个不同的 mock maker （模拟生成器）。在这些情况下，你可以临时的使用 `MockSettings.mockMaker(String)`和`Mock.mockMaker()`来指定 mock maker 给一个特殊的 mock (which) 导致了问题

```java
// using annotation
@Mock(mockMaker = MockMakers.SUBCLASS)
Foo mock;
// using MockSettings.withSettings()
Foo mock = Mockito.mock(Foo.class, withSettings().mockMaker(MockMakers.SUBCLASS));
```
