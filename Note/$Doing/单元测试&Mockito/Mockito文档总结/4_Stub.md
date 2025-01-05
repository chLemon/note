# 1. `when().then()`风格的 stub

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

# 2. `doThrow()|doAnswer()` 家族方法

`doReturn() | doThrow() | doAnswer() | doNothing() | doCallRealMethod()`

任何方法，都可以使用这一系列方法来进行 stub。不过以下情况，必须使用`doXxx()`系列方法：

1. void 方法
2. spy 的方法
3. 希望对同一个方法 stub 多次，并且在测试过程中，改变 stub 的值

## 2.1. 这些情况下不能用 `when().then()` 风格的原因简单说明

`when(mock.method()).then()` 这种写法中，`when`方法的签名是`when(Object)`，参数是`Object`，而`void`方法没有返回值，编译器会报错。所以`void`方法不能使用这种写法。

其次，这行代码中，`mock.method()`是会执行的。如果是普通 mock，这时会返回默认值，并不会有什么影响，但是对于 spy ，由于 spy 的特性，这行代码里 `spy.method()` 会直接去调用一次真实方法，可能产生副作用，不符合预期。

如果`mock.method()`已经被 stub 了，在这里调用时也会返回被 stub 的值，如果是 stub 了 exception，会直接报错

### 2.1.1. 对 spy 进行 stub 时注意

注意 final 方法。Mockito 不会 mock final 方法，所以注意，当 spy 了真实对象，然后又尝试 stub 一个 final 方法，会导致麻烦。并且也不能正常 verify 那些方法

## 2.2. `doReturn(Object)`

在无法使用 `when(Object)` 的情况下，使用`doReturn()`

注意，更推荐使用`when(Object)`，因为这样写是参数类型安全的，并且更易读（尤其是当连续调用的时候）

下面是一些`doR\eturn()`用起来更方便的场景：

1. 对 spy 进行 stub 时，尤其是当方法有副作用时

```java
List list = new LinkedList();
List spy = spy(list);

// 不可能成功调用，因为 spy 现在还是空的，get(0)会报错
when(spy.get(0)).thenReturn("foo");

// 必须使用 doReturn()
doReturn("foo").when(spy).get(0);
```

2. 覆盖之前 stub 的 exception

```java
when(mock.foo()).thenThrow(new RuntimeException());

// 不行：因为这里 mock.foo() 会先被调用，然后抛出 RuntimeException
when(mock.foo()).thenReturn("bar");

// 必须这样
doReturn("bar").when(mock).foo();
```

上面这个场景展示了 Mockito 对于语法优雅性的权衡。

注意，这些场景非常的罕见。应该很少使用 spy，并且覆盖 exception 的 stub 也非常罕见。在一般情况下，覆盖 stub 是一个代码异味，表示存在了太多的 stub

## 2.3. `doThrow(Throwable...)`

当你想要 stub void 方法抛出一个异常的时候用 `doThrow()`

```java
doThrow(new RuntimeException()).when(mockedList).clear();

//following throws RuntimeException:
mockedList.clear();
```

## 2.4. `doThrow(Class)`

当你想要 stub void 方法抛出一个异常的时候用`doThrow()`

每次方法调用都会创建一个新的 exception 实例

## 2.5. `doAnswer(Answer)`

当你想要 stub void 方法返回一个 `Answer` 时

## 2.6. `doNothing()`

使用`doNothing()`来设置 void 方法什么都不做

注意，mock 的 void 方法默认就是 do nothing

然而，也有一些非常罕见的情况下，`doNothing`非常方便

1. 给一个 void 方法进行 stubbing 链式调用

```java
doNothing()
    .doThrow(new RuntimeException())
    .when(mock).someVoidMethod();

// 第一次调用什么都不做
mock.someVoidMethod();

// 在之后的调用里抛出异常
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

## 2.7. `doCallRealMethod()`

当你想要调用一个方法的真实实现时，使用 `doCallRealMethod()`。

例子：

```java
Foo mock = mock(Foo.class);
doCallRealMethod().when(mock).someVoidMethod();

// this will call the real implementation of Foo.someVoidMethod()
mock.someVoidMethod();
```

# 3. ArgumentMatcher 参数匹配器

stub 时可以指定具体的参数。这里参数是否匹配默认使用对象的`equals()`方法。

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

详细见 [2_Mock 与 Verify](2_Mock与Verify.md)

# 4. Stub 覆盖 和 链式调用

## 4.1. Stub 覆盖

stub 可以被覆盖，会以最后一次 stub 的值为准。

所以可以在 BaseTest / fixture 里设置一些通用 stub，然后在具体测试方法里覆盖掉

> test fixture：也称为 test context，用于设置测试的系统状态和输入

## 4.2. 链式调用

链式调用：可以指定被 stub 的方法，第一次调用返回 value1 ，第二次调用返回 value2

```java
when(mock.someMethod("some arg"))
    .thenThrow(new RuntimeException())     // 第一次抛异常
    .thenReturn("foo");                    // 第二次及其以后返回 "foo"

// 第一次调用，抛异常
mock.someMethod("some arg");

// 打印 "foo"
System.out.println(mock.someMethod("some arg"));

// 之后无数次调用，都会打印 "foo"
System.out.println(mock.someMethod("some arg"));
```

更简单的写法：

```java
when(mock.someMethod("some arg"))
    .thenReturn("one", "two", "three");
```

# 5. 在创建 mock 时 stub（1.9.0+）

可以在创建 mock 的时候 stub，这样可以在一行代码里写完，有助于让测试代码更干净。

```java
public class CarTest {
    Car boringStubbedCar = when(mock(Car.class).shiftGear()).thenThrow(EngineNotStarted.class).getMock();

    @Test public void should... {}
```

# 6. deep stub（1.10.0+）

注意，在大多数情况下，mock 的方法返回 mock 是错误的。

```java
Foo mock = mock(Foo. class, RETURNS_DEEP_STUBS);

// 注意，这里我们 stub 了一个方法链：getBar().getName()
when(mock. getBar().getName()).thenReturn("deep");

// 注意这里，我们直接链式调用了方法：getBar().getName()
assertEquals("deep", mock. getBar().getName());
```

deep stub 会让 mock 的方法默认返回 mock。现在也可以寻找出泛型信息，提供对泛型更好的支持。

```java
class Lines extends List<Line> {
    // ...
}

lines = mock(Lines.class, RETURNS_DEEP_STUBS);

// 现在 Mockito 可以识别出这个对象是一个 Line
Line line = lines.iterator().next();
```

# 7. stub 返回复杂逻辑

Mockito 提供了一个接口 `Answer`，用以表示 stub 的返回值。

该接口内只有一个方法 `answer()`，这个方法的返回值就是 stub 的值

通常不推荐使用

```java
public interface Answer<T> {
    /**
     * @param invocation the invocation on the mock.
     * @return the value to be returned
     * @throws Throwable the throwable to be thrown
     */
    T answer(InvocationOnMock invocation) throws Throwable;
}
```

```java
when(mock.someMethod(anyString())).thenAnswer(
    new Answer() {
        public Object answer(InvocationOnMock invocation) {
                Object[] args = invocation.getArguments();
                Object mock = invocation.getMock();
                return "called with arguments: " + Arrays.toString(args);
        }
});

// 打印 "called with arguments: [foo]"
System.out.println(mock.someMethod("foo"));
```

## 7.1. Java 8 对自定义 Answer 的支持（2.1.0+）

由于 `Answer` 接口只有一个方法，所以对于一些非常简单的情况，可以在 java 8 里用 lambda 表达式来实现。

注意，`InvocationOnMock.getArguments()` 获取到的参数是`Object`，那么用到的参数越多，需要写的强制转换就越多。

```java
// 每次都返回12的answer
doAnswer(invocation -> 12).when(mock).doSomething();

// 使用其中的一个参数进行处理，注意随着强制转换的增多，代码会变得很冗长
doAnswer(invocation -> ((String)invocation.getArgument(1)).length())
    .when(mock).doSomething(anyString(), anyString(), anyString());
```

为了方便起见，可以以 lambda 表达式的形式自定义 answer 或者 action。参数是要 stub 的方法的参数。

在 Java 7 或者更低的版本里，基于泛型的自定义 answer 可以减少一些一模一样的代码。

这种方式可以让测试 callback 的功能更容易。

使用方法 `AdditionalAnswers.answer(Answer1)` 和 `AdditionalAnswers.answerVoid(VoidAnswer1)` 来创造 answer。他们依赖于`org.mockito.stubbing`中的相关的 `Answer` 接口，支持最多 5 个参数。

```java
public class SystemUnderTest {
    ExampleInterface inter;

    public void tested() {
        Callback cb = ...;
        // ...
        inter.execute("op", cb);
        // ...
        cb.otherMethod();
    }
}

public interface ExampleInterface {
    void execute(String operand, Callback callback);
}

public class Callback {
    void receive(String item);
}
```

在这个例子里，要被 mock 的接口里有一个函数 `execute()`，传入了一个`Callback`的对象，在`execute()`方法里，会调用`callback`的一些方法。而被测类的方法的逻辑会依赖于`execute()`方法里`callback`的调用。所以需要 stub `execute()`方法内，`callback.receive(String)`的逻辑。

```java
// Java 8 - 写法 1
doAnswer(AdditionalAnswers.<String,Callback>answerVoid((operand, callback) -> callback.receive("dummy")))
    .when(mock).execute(anyString(), any(Callback.class));

// Java 8 - 写法 2 - 假设 AdditionalAnswers 被 static import 了
doAnswer(answerVoid((String operand, Callback callback) -> callback.receive("dummy")))
    .when(mock).execute(anyString(), any(Callback.class));

// Java 8 - 写法 3 - 通过方法引用，将要 mock 的方法写成测试类里的静态成员
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

// 在 answer() 函数里返回一个值也是可以的，所以如果要 mock 的接口里有一个这样的方法
boolean isSameString(String input1, String input2);

// Java 8，注意第一个Boolean
doAnswer(AdditionalAnswers.<Boolean,String,String>answer((input1, input2) -> input1.equals(input2)))
    .when(mock).execute(anyString(), anyString());

// Java 7
doAnswer(answer(new Answer2<String, String, String>() {
    public String answer(String input1, String input2) {
        return input1 + input2;
    }})).when(mock).execute(anyString(), anyString());
```

# 8. 为了 verify 而忽略 stub（1.9.0+）

Mockito 现在允许为了 verify 而忽略 stub。

在 verify 时，我们对 stub 了的方法的调用并不感兴趣，也不想验证这部分调用，可以忽略掉这些调用信息。

还可以 `verifyNoMoreInterations()` 和 `inOrder()` 结合使用时，会有用。

警告：`ignoreStubs()`可能会导致过度使用 `verifyNoMoreInteractions(ignoreStubs(...))` 。记着 mockito 不推荐频繁使用 `verifyNoMoreInteractions`。

例子：

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
