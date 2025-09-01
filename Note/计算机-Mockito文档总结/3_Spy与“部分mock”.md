# 1. 部分模拟（partial mock）

## 1.1. 真正的“部分mock” (partial mock)（1.8+）

在 1.8 之前，spy 生成的并不是真正的 部分mock，因为 Mockito 团队认为 部分mock 是一个代码异味：

在OOP里，解决问题复杂性的思路是通过将大问题拆分为一个个独立的、特定的单一职责对象来解决问题。如果类设计是满足单一职责的，那么就不会有需要 部分mock 的场景。即如果需要 部分mock，说明类耦合了他不应该拥有的职责，应该改善代码设计。

但是后来通过和社区沟通，发现了一些场景下，确实需要 部分mock 的能力：
1. 处理一些不能轻易修改的代码，如第三方的接口、库
2. 临时处理一些难以重构的遗留代码

不过对于新写的、测试驱动的、设计良好的代码，不应该用到 部分mock 的能力去做测试。

### 1.1.1. 部分mock 的方式

1. `spy()`
2. `thenCallRealMethod() | doCallRealMethod()`
3. `delegatesTo`，详见下方

```java
// spy 方法可以创建 部分mock
List list = spy(new LinkedList());


// 你可以选择性的在 mock 上启用 部分mock 的能力
Foo mock = mock(Foo.class);

// 确保方法的真实实现是安全的。如果方法抛出了异常或者依赖了某些对象的状态，就很麻烦了
when(mock.someMethod()).thenCallRealMethod();
doCallRealMethod().when(mock).someVoidMethod();
```

# 2. 创建 spy 的方法

## 2.1. `spy()` 方法

```java
List list = new LinkedList();
List spy = spy(list);
```

### 2.1.1. 不指定类（4.10.0+）

```java
Foo foo = Mockito.mock();
Bar bar = Mockito.spy();
```
spy 被赋值的对象必须是有显式类型的，编译器会自动解析。

## 2.2. 注解方式 `@Spy`（推荐）

```java
@Spy 
BeerDrinker drinker = new BeerDrinker();

// 1.9.0之后的版本会尝试自动实例化
@Spy
BeerDrinker drinker;
```

### 2.2.1. 和 `@InjectMocks` 结合使用

`@InjectMocks` 也可以和 `@Spy` 注解结合使用，Mockito 会将通过注解声明的 mock 和 spy 注入到 被测试的 spy 里。

```java
@Spy
@InjectMocks
BeerDrinker drinker;
```

## 2.3. Spy 或者 mock 抽象类 （1.10.12+ 增强于2.7.13, 2.7.14）

现在可以更方便的 spy 抽象类。

之前，spy 只能用在对象实例上。新的API使得创建 mock 实例的时候可以用构造器。这点对 spy 抽象类非常有用，因为用户不再需要提供一个抽象类的实例了。现在，只支持无参构造器。

```java
// 方便的API，新的 overload 的 spy方法，可以传入 class 对象
SomeAbstract spy = spy(SomeAbstract.class);

// 会 mock 抽象方法，spy default方法（2.7.13+）
Function<Foo, Bar> function = spy(Function.class);

// 更鲁邦的API，通过 settings 建造者模式
OtherAbstract spy = mock(OtherAbstract.class, withSettings()
   .useConstructor().defaultAnswer(CALLS_REAL_METHODS));

// 指定构造器参数，mock 抽象类（2.7.14+）
SomeAbstract spy = mock(SomeAbstract.class, withSettings()
   .useConstructor("arg1", 123).defaultAnswer(CALLS_REAL_METHODS));

// mock一个非静态的内部类
InnerAbstract spy = mock(InnerAbstract.class, withSettings()
   .useConstructor().outerInstance(outerInstance).defaultAnswer(CALLS_REAL_METHODS));
```

# 3. delegatesTo 将调用委托给真实对象（1.9.5+，1.10.11增强）

当有些类难以用常规的 spy API 进行 spy 时，可以用 `AdditionalAnswers.delegatesTo(Object)` 将调用委托给真实对象。这种方式创建的 spy 功能上不如普通的 spy，有一些限制，但是在难以创建普通 spy 时很有用。

被委托的对象可以和 mock 是同一个类型，也可以不是。如果不是同一个类型，需要在被委托类上能找到一个匹配的方法（相同的方法签名 + 相同的返回值）。可能的应用场景有：
1. 实现了某个接口的 final 类
2. 已经被自定义代理的类
3. 拥有 `finalize()` 方法实现的特殊类，也就是说要避免调用2次 `finalize()`

和普通 spy 的区别是：
1. 普通 spy 包含被 spy 实例的所有状态，并且方法是在 spy 上被调用的。被 spy 的实例仅仅用于创建 mock 和 复制状态。
2. 将方法委托出去的 mock ，只是简单的将所有方法委托过去。如果在 mock 上调用了一个被委托的方法，而这个方法内部又去调用了一些其他 mock 上的方法，这些方法的调用信息不会被记录到 mock，stub 也不会生效。

final 类的例子：

```java
final class DontYouDareToMockMe implements list { ... }

DontYouDareToMockMe awesomeList = new DontYouDareToMockMe();

List mock = mock(List. class, delegatesTo(awesomeList));
```

同 spy 一样，当使用 `when().then()` 风格进行 stub 时，`when()`里会真实调用方法。所以要用 `doReturn()` 风格。详见 [4_Stub](4_Stub.md)

```java
List listWithDelegate = mock(List. class, AdditionalAnswers. delegatesTo(awesomeList));

// Impossible: real method is called so listWithDelegate. get(0) throws IndexOutOfBoundsException (the list is yet empty)
when(listWithDelegate. get(0)).thenReturn("foo");

// You have to use doReturn() for stubbing
doReturn("foo").when(listWithDelegate).get(0);
```
