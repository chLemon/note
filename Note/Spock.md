据说Spock是目前最好的测试框架（2022），“一旦上手了Spock，你就不会想用其他的了”。可以用来写单元测试或集成测试等，支持mock。本文是对官方手册的主要内容的翻译，主要供自己学习使用。

>官方手册：https://spockframework.org/spock/docs/2.0/all_in_one.html

# 入门

Spock使用Groovy语言编写测试用例，不过只要你会Java就不用太担心，Groovy很好的兼容了Java语法，Groovy设计目标之一就是兼容Java的脚本语言。

## 一些定义

Spock主要是编写一个个Specification来对软件应用进行测试。

Specification（规范、说明）：期望中目标系统要表现出的feature（特性、功能）的集合。

目标系统：可以是一个单独的类，也可以是一个应用程序，或者是在这两者之间的某个层次。也被称为SUS（system under specification）（规范下的系统，规范所描述的系统）。

编写每一个feature时，通常是从SUS和与SUS交互的模块的一个特定快照开始的，这个特定快照就被称为这个feature的fixture。

>举个例子：
>
>我有一个购物网站，那么我可以对整个购物网站写一个测试文件，这时候这个测试文件就叫specification，测试文件会包含对购物网站详细的说明；整个购物网站软件就叫SUS，也就是本specification所要描述的system。当然我也可以只针对购物网站的某个模块做测试，这时这个模块就是SUS。
>
>购物网站包含了诸如：浏览商品功能、加入购物车功能、购买商品功能等，这些就是一个个的feature，有点像测试用例的概念。
>
>以购买商品功能为例，它要求用户必须先登录好，并且将商品已经加入了购物车，这些前置条件就是fixture。在测购买商品功能时，需要购物网站的状态是用户已登录，用户已加入该商品到购物车，这就相当于是购物网站生命周期里的一个快照/切面。

下面会介绍编写specification时可以用到的东西，通常只需要用到一部分下面的内容就可以编写出需要的specification。

## Imports

```groovy
import spock.lang.*
```

`spock.lang`包下包含了编写specification最主要的一些类型。

## Specification

```groovy
class MyFirstSpecification extends Specification {
  // fields
  // fixture methods
  // feature methods
  // helper methods
}
```

每个specification都是一个Groovy的类，需要继承`spock.lang.Specification`，类的名字通常是SUS的名字或者某个操作的名字，比如说`CustomerSpec`、`ASpaceshipAttackedFromTwoSides`。

`spock.lang.Specification`里有一些有用的方法，更重要的是他可以通知Junit用`Sputnik`（spock的Junit runner）来运行。

## Fields

```groovy
def obj = new ClassUnderSpecification()
def coll = new Collaborator()
```

一般会把fixture要用的对象直接放在字段里。建议在声明字段的时候就初始化好对象（这和在`setup()`的开始初始化对象一样，下面会介绍）。

字段里的对象在不同的feature方法里是**不**共享的，这样每个feature方法都有自己的对象，可以有效保证每个feature方法之间的独立。

```groovy
@Shared res = new VeryExpensiveResource()
```

有时候需要在feature方法之间共享对象，可以在字段前声明注解`@Shared`。同样建议在声明字段的时候就初始化对象（这和在`setupSpec()`的开始初始化对象一样）。

```groovy
static final PI = 3.141592654
```

静态字段应该只做常量使用。否则最好用`@Shared`。

## Fixture Methods

```groovy
def setupSpec() {}    // runs once -  before the first feature method
def setup() {}        // runs before every feature method
def cleanup() {}      // runs after every feature method
def cleanupSpec() {}  // runs once -  after the last feature method
```

fixture方法是为了给每个feature方法初始化和清理环境用的。`setup()`和`cleanup()`会在每个feature方法的执行前后执行一次。可以根据自己的需求添加这4种方法。

有时候多个feature方法需要共同的fixture（前置条件/环境），那就可以用`@Shared`标记的变量和`setupSpec()`、`cleanupSpec()`来实现。

注意在`setupSpec()`和`cleanupSpec()`引用的字段要用`@Shared`标记。

### 调用顺序

如果有一个specifiction继承了另一个specification，那么fixture方法的调用顺序如下（super表示父类，sub表示子类）：

1. `super.setupSpec`
2. `sub.setupSpec`
3. `super.setup`
4. `sub.setup`
5. feature method
6. `sub.cleanup`
7. `super.cleanup`
8. `sub.cleanupSpec`
9. `super.cleanupSpec`

## Feature Methods

```groovy
def "pushing an element on the stack"() {
  // blocks go here
}
```

feature方法是specification的核心，用来描述SUS的期望行为。按照惯例，feature方法的命名是用字符串来命名的，可以用任意喜欢的字符。

从概念上讲，一个feature方法包括4阶段（conceptual phases）：

1. 初始化feature的fixture
2. 给SUS提供一个输入
3. 描述SUS预期的响应
4. 清空feature的fixture

第1阶段和第4阶段都是可选的，除了交互式feature方法，第2阶段和第3阶段是必须要有的，而且可能会出现多次。

### Blocks

feature方法是由一个个的block（块）构成的。每个block都是以一个label（标签）开始的。一共有6种block：`given`, `when`, `then`, `expect`, `cleanup`, `where` 。在feature方法里，第一个显式的block之前的代码部分是一个隐式的`given`block。

feature方法里必须有一个显式的block。事实上，有block的方法，才是feature方法。block将方法划分成不同的部分，并且block不能嵌套。

下图展示了block和概念阶段之间的联系。其中`where`block非常特殊，将在之后进行说明。

![Blocks2Phases](https://spockframework.org/spock/docs/2.0/images/Blocks2Phases.png)

#### Given Blocks

```groovy
given:
def stack = new Stack()
def elem = "push me"
```

`given`block用来做一些初始化的工作，它之前可以没有别的block，而且通常只有一个。事实上，`given`并没有特殊的语义，还可以不写，那么就是一个隐式的`given`block。最初是想用`setup`这个词的，但是在导出文档后，使用`given`一词的可读性更好。

#### When and Then Blocks

```groovy
when:   // stimulus
then:   // response
```

`when`block和`then`block总是一起出现。它们一个用来描述给系统的输入，一个用来描述响应。`when`block里可以包含任意代码，而`then`block里只能写conditions、exception conditions、interactions和variable definitions（布尔条件、异常条件、交互、变量定义），会在下面介绍。一个feature方法可以包含多个`when-then`block。

##### Conditions

conditions描述了期望的状态，和Junit里的assertions差不多。不过condition只需要写一个布尔表达式，不需要assert之类的关键词（准确的说，也可以不是布尔值，groovy会根据语法将非布尔值转换为布尔值，但不推荐这样写）。

```groovy
when:
stack.push(elem)

then:
!stack.empty
stack.size() == 1
stack.peek() == elem
```

>tip：
>
>一个feature方法里的conditions应该尽可能的少，推荐1-5个。如果比这个更多，就需要考虑一下是不是把多个不相关的feature写在了一个里，把他们拆开。如果conditions只是值不同，考虑使用data table的写法来简化代码（下文介绍）。

如果某个condition有错误，会以下面这种方式展示，比如说把第二个condition改为`stack.size() == 2`，会得到下面这种结果。

```groovy
Condition not satisfied:

stack.size() == 2
|     |      |
|     1      false
[push me]
```

spock会将条件里的所有值以这种方式展现出来，简单明了。

###### 隐式和显式condition

condition是`then`block和`except`block 的基本组成。在这两种block里，除了调用`void`的方法和interaction的表达式（后文介绍），所有的语句都会被隐式的认为是condition。

如果想在其他的block里使用condition，需要使用`assert`关键字。

```groovy
def setup() {
  stack = new Stack()
  assert stack.empty
}
```

##### Exception Conditions

exception condition用来描述`when`block里会抛出一个异常。写法是写一个`thrown()`方法，然后将期望会抛出的异常类型当做参数传入。

例如，一个空的栈执行`pop()`应该抛出`EmptyStackException`，就可以这么写：

```groovy
when:
stack.pop()

then:
thrown(EmptyStackException)
stack.empty
```

exception condition后面还可以写其他的condtion，甚至其他的block。可以通过把exception condition绑到一个变量上来访问exception的内容。

```groovy
when:
stack.pop()

then:
def e = thrown(EmptyStackException)
e.cause == null
```

另外，还可以这样写：

```groovy
when:
stack.pop()

then:
EmptyStackException e = thrown()
e.cause == null
```

这种写法有2个好处，第一，显式指定了变量的类型可以让IDE更好地补全代码；第二，这样更像是一句话，更好读（then an EmptyStackException is thrown）。注意，如果像这里，没有给`thrown()`方法传入参数，那么会默认是左侧的类型。

有时候我们还需要声明某exception不应该被抛出。例如，`HashMap`可以接受`null`作为`key`。

```groovy
def "HashMap accepts null key"() {
  setup:
  def map = new HashMap()
  map.put(null, "elem")
}
```

虽然这样写也可以，但是并不能很好得表示出这段代码的意图。

```groovy
def "HashMap accepts null key"() {
  given:
  def map = new HashMap()

  when:
  map.put(null, "elem")

  then:
  notThrown(NullPointerException)
}
```

通过使用`notThrown()`，就可以很好的表明我们是希望`HashMap`在 put` null`作为key时，不应该抛出`NullPointerException`。不过如果抛出了其他异常，这个方法依旧会失败（用例不会通过）。

##### Interactions

condition是用来描述一个对象的状态的，interaction则是描述对象如何与其他对象交互的。之后会有专门的一章来介绍interaction和基于interaction的测试，这里先给出一个简单的例子。

假设我们想描述一个publisher（推送者）给一些subscriber（订阅者）推送过程中的一系列事件，可以这样写：

```groovy
def "events are published to all subscribers"() {
  given:
  def subscriber1 = Mock(Subscriber)
  def subscriber2 = Mock(Subscriber)
  def publisher = new Publisher()
  publisher.add(subscriber1)
  publisher.add(subscriber2)

  when:
  publisher.fire("event")

  then:
  1 * subscriber1.receive("event")
  1 * subscriber2.receive("event")
}
```

#### Expect Blocks

`expect`block比`then`block的限制更强，只允许conditions和variable definitions（布尔条件，变量定义）。如果输入和输出可以用一行代码来表示，用`expect`block会更自然。例如，以下两种对`Math.max()`测试的写法：

```groovy
when:
def x = Math.max(1, 2)

then:
x == 2
```

```groovy
expect:
Math.max(1, 2) == 2
```

上面两种写法在效果上是等价的，但第二种更简洁明了。建议，在测试有副作用的方法上使用`when-then`block，在纯函数方法上使用`expect`block（这里的副作用是指会对其他变量、模块等产生作用）。

>tip：
>
>利用Groovy JDK里提供的如any()、every()之类的方法可以写出更简洁明了的condition。

#### Cleanup Blocks

```groovy
given:
def file = new File("/some/path")
file.createNewFile()

// ...

cleanup:
file.delete()
```

`cleanup`block后只能有`where`block，并且`cleanup`block在一个feature方法里只能有一个。`cleanup`block用来释放这个方法里用到的资源，编写时要考虑到代码甚至可能会在第一行就出错的情况。

> tip:
>
> Groovy提供了一种避免空指针写法：foo?.bar()
>
> 如果foo是null，那么会直接返回null，而不会抛出NullPointerExeption

对象级别的specification通常不需要`cleanup`，因为这时多半只会用到内存资源，而内存是由JVM来管理的。在更大一些级别的方法里，可能会用来释放文件系统资源、关闭数据库连接、关闭网络服务等。

>tip:
>
>如果一个specification里的多个feature方法需要共用同样的资源，那么用 cleanup() 方法（fixture method），否则应该用 cleanup block；对于 setup() 和 given block也是一样。

#### Where Blocks

`where`block总是在方法的最后，并且只能有一个。用来写数据驱动（data-driven）的feature方法。

```groovy
def "computing the maximum of two numbers"() {
  expect:
  Math.max(a, b) == c

  where:
  a << [5, 3]
  b << [1, 9]
  c << [5, 9]
}
```

`where`block会创建2个版本的feature方法：一个是a=5,b=1,c=5；另一个是a=3,b=3,c=9。

尽管`where`block在方法最后声明，但是在该feature方法执行前就执行了。

在之后的数据驱动测试章节会对`where`block有更详细的介绍。

## Helper Methods 辅助方法

有时候feature方法太大了，或者有很多重复的代码，就可以抽取出一些helper方法。通常setup/cleanup的逻辑和很复杂的conditions可以抽成helper方法。例如：

```groovy
def "offered PC matches preferred configuration"() {
  when:
  def pc = shop.buyPc()

  then:
  pc.vendor == "Sunny"
  pc.clockRate >= 2333
  pc.ram >= 4096
  pc.os == "Linux"
}
```

有时候我们希望电脑配置信息越详细越好，或者有时会比较不同商店间的电脑配置，就可以把condition的部分抽个方法：

```groovy
def "offered PC matches preferred configuration"() {
  when:
  def pc = shop.buyPc()

  then:
  matchesPreferredConfiguration(pc)
}

def matchesPreferredConfiguration(pc) {
  pc.vendor == "Sunny"
  && pc.clockRate >= 2333
  && pc.ram >= 4096
  && pc.os == "Linux"
}
```

新的helper方法`matchesPreferredConfiguration`是由一个布尔表达式组成的，将结果返回（Groovy中`return`关键字可以不写）。但是这样有一个问题，就是当方法出现false时：

```groovy
Condition not satisfied:

matchesPreferredConfiguration(pc)
|                             |
false                         ...
```

这样看上去并不直观。可以改写成这样：

```groovy
void matchesPreferredConfiguration(pc) {
  assert pc.vendor == "Sunny"
  assert pc.clockRate >= 2333
  assert pc.ram >= 4096
  assert pc.os == "Linux"
}
```

这种写法需要注意两点：第一，隐式的conditions必须转换成用`assert`声明的显式conditions；第二，方法的返回值必须是`void`。否则返回值可能会被解析成false导致feature方法失败（比如返回0会被当成false）。

这样写的话，如果有某一步出错了，就会这样显示：

```groovy
Condition not satisfied:

assert pc.clockRate >= 2333
       |  |         |
       |  1666      false
       ...
```

最后一个建议：尽管代码复用是一件好事，但别弄太多。要警惕使用fixture方法和helper方法，他们会增加feature方法之间的耦合，如果复用太多，specification会容易出错且难以维护。

## 使用`with`来表达预期效果

上面的helper方法还有一种写法，可以用`with(target, closure)`方法，这种写法在`then`block和`expect`block里很有用。

```groovy
def "offered PC matches preferred configuration"() {
  when:
  def pc = shop.buyPc()

  then:
  with(pc) {
    vendor == "Sunny"
    clockRate >= 2333
    ram >= 406
    os == "Linux"
  }
}
```

与helper方法不同，这时候不用`assert`显式地写condition也可以在出错时有详细的报告。

当验证mock的时候，`with`还可以简化验证语句：

```groovy
def service = Mock(Service) // has start(), stop(), and doWork() methods
def app = new Application(service) // controls the lifecycle of the service

when:
app.run()

then:
with(service) {
  1 * start()
  1 * doWork()
  1 * stop()
}
```

有时候IDE不能辨别出对象（target）的类型，这时候可以像这样手动指定`with(target, type, closure)`。

## 使用`verifyAll`一次断言多个预期效果

通常在第一个断言失败的时候，整个测试就失败了。不过有时候执行完所有的断言可以获得更多的信息，这种也叫做软断言（soft assertions）。

`verifyAll`使用和`with`类似：

```groovy
def "offered PC matches preferred configuration"() {
  when:
  def pc = shop.buyPc()

  then:
  verifyAll(pc) {
    vendor == "Sunny"
    clockRate >= 2333
    ram >= 406
    os == "Linux"
  }
}
```

或者也可以不带target：

```groovy
  expect:
  verifyAll {
    2 == 2
    4 == 4
  }
```

和`with`一样，也可以指定target的类型。

## 将specification作为文档

精心编写的specification可以作为一个非常有价值的信息源。特别是那些针对更广泛的受众写的specification，如面向架构师、领域专家、客户等的，给specification和feature使用自然语言起一个有含义的名称会更有意义。因此，Spock提供了一种将文本描述附加到block上的方式：

```groovy
given: "open a database connection"
// code goes here
```

使用`and`标签来区分一个block逻辑里不同的部分。

```groovy
given: "open a database connection"
// code goes here

and: "seed the customer table"
// code goes here

and: "seed the product table"
// code goes here
```

`and`标签后可以跟一句描述，可以插在feature方法里的任意地方，并且不会改变方法的含义。

在行为驱动开发里（BDD），面向客户的特性（BDD里叫stories）是用 given-when-then 的形式来表示的。Spock可以用`given`标签直接支持这种表示方法。

```groovy
given: "an empty bank account"
// ...

when: "the account is credited \$10"
// ...

then: "the account's balance is \$10"
// ...
```

block的这些描述不仅可以在源码里看到，还可以在Spock运行的时候看到。这些描述设计之初是希望可以在诊断的时候提供更多信息，并且形成让所有人都能理解的文字报告。

## Extensions 拓展

正如上面所介绍的，Spock为编写specification提供了很多的功能。但是这些总会有不够用的时候。所以Spock提供了一种基于拦截的拓展机制。拓展是通过注解来激活的，在Spock里这些注解叫做directives（指令）。Spock现在有这些指令：

```groovy
@Timeout	
Sets a timeout for execution of a feature or fixture method.
  给一个feature或fixture方法设置时限。 

@Ignore	
Ignores any feature method carrying this annotation.
  忽略有这个注解的feature方法

@IgnoreRest	
Any feature method carrying this annotation will be executed, all others will be ignored. Useful for quickly running just a single method.
  忽略其他没有这个注解的feature方法，在只想运行一个方法的时候非常有用。

@FailsWith	
Expects a feature method to complete abruptly. @FailsWith has two use cases: First, to document known bugs that cannot be resolved immediately. Second, to replace exception conditions in certain corner cases where the latter cannot be used (like specifying the behavior of exception conditions). In all other cases, exception conditions are preferable.
  期望一个feature方法突然结束。这个注解有2个使用情况：第一，记录一下已知但是不能立刻解决的bug；第二，在某些不能使用exception condition的情况下替代exception condition（比如说需要指定exception condition的行为时）。在其他情况下，用exception condition更好。
```

可以在Extensions章节学习如何实现自己的directives和extensions。

## 和JUnit的比较

尽管Spock用了不同的术语，但是很多概念都是受JUnit启发而创建的，这里进行一个粗略的比较。

| Spock               | JUnit                              |
| ------------------- | ---------------------------------- |
| Specification       | Test class                         |
| `setup()`           | `@Before`                          |
| `cleanup()`         | `@After`                           |
| `setupSpec()`       | `@BeforeClass`                     |
| `cleanupSpec()`     | `@AfterClass`                      |
| Feature             | Test                               |
| Feature method      | Test method                        |
| Data-driven feature | Theory                             |
| Condition           | Assertion                          |
| Exception condition | `@Test(expected=…)`                |
| Interaction         | Mock expectation (e.g. in Mockito) |

# Data Driven Testing数据驱动测试

在很多时候，我们需要对同样的测试代码用不同的输入执行多次，验证获得不同的期望结果。Spock的数据驱动测试就很好的支持了这一情况。

## 简介

假设我们需要测试`Math.max`方法

```groovy
class MathSpec extends Specification {
  def "maximum of two numbers"() {
    expect:
    // exercise math method for a few different inputs
    Math.max(1, 3) == 3
    Math.max(7, 4) == 7
    Math.max(0, 0) == 0
  }
}
```

尽管这种方法在这种简单的情况下是可行的，但是还是有一些缺点：

+ 代码和数据混在一起，并且不能方便地独立更改
+ 数据不能方便地自动生成，也不能方便地从外部源导入
+ 为了多次执行同样的代码，要么需要重复代码，要么需要抽一个独立的方法
+ 如果出错了，不能立刻清晰地发现是哪个输入导致了错误
+ 多次执行同样的代码的独立性，远不如执行独立方法。

Spock的数据驱动测试就试图解决这些问题。让我们把上面的代码重构成一个数据驱动型的feature方法。首先，我们给方法加入3个变量（称为data variables）来替换掉之前硬编码的整数。

```groovy
class MathSpec extends Specification {
  def "maximum of two numbers"(int a, int b, int c) {
    expect:
    Math.max(a, b) == c
    ...
  }
}
```

这样就完成了测试逻辑，接下来是提供使用的数据。数据是由`where`block来提供的，`where`block永远要写在feature方法的最后面。在最简单的情况（也是最通常的情况）下，我们在`where`block写一个data table（数据表）。

## Data Tables 数据表

用一组固定数据执行feature方法时，数据表是一种方便的方法。

```groovy
class MathSpec extends Specification {
  def "maximum of two numbers"(int a, int b, int c) {
    expect:
    Math.max(a, b) == c

    where:
    a | b | c
    1 | 3 | 3
    7 | 4 | 7
    0 | 0 | 0
  }
}
```

表的第一行叫做表头（table header），声明了数据变量（data variables）。剩下的行叫做表行（table rows），保存对应的值。对表中的每一行，feature方法都会执行一次，每次执行称为方法的一次迭代（iteration）。如果一次迭代失败了，剩下的迭代仍然会进行。然后所有的错误情况都会被打印出来。

数据表至少需要2列。如果一个表只有一个数据变量，可以这样写：

```groovy
where:
a | _
1 | _
7 | _
0 | _
```

可以使用2个或更多的下划线将一个宽表拆分成数个窄表。通常，一个`where`block里只能有一个数据表，除非用下划线做分割，或者表之间有其他的数据变量。如果直接写了2个数据表在`where`block中，第二个表会被认为是第一个表的其他迭代，包括第二个表的“表头”（实际上并不是真正的表头）。

```groovy
where:
a | _
1 | _
7 | _
0 | _
__

b | c
1 | 2
3 | 4
5 | 6
```

上面这种写法和下面这种等价：

```groovy
where:
a | b | c
1 | 1 | 2
7 | 3 | 4
0 | 5 | 6
```

2个以上下划线组成的分隔符可以放在`where`block的任意地方，除了在2个数据表之间会表示这是对数据表做了分割，其他地方都不会有任何含义。这意味着我们可以拿它做装饰。比如在表头上加一行可以更好看：

```groovy
where:
_____
a | _
1 | _
7 | _
0 | _
_____
b | c
1 | 2
3 | 4
5 | 6
```

## 迭代之间执行的独立性

迭代之间是相互独立的，如同执行了独立的feature方法。每个迭代会获取到各自的specification实例，并且在每次迭代执行前都会知行`setup`和`cleanup`方法。

## 在不同迭代之间共享对象

想在不同迭代间共享的对象，要么用`@Shared`标记，要么是静态字段。

>注意：只有`@Shared`的静态变量可以在`where`block中被访问。

注意这些对象也会被共享到其他方法。当前并没有一个好的方法让对象仅在一个方法的不同迭代里共享。如果这样会出问题，可以考虑把每个方法放在一个独立的specification里，这些specification可以放在一个文件里。

## 语法上的一些变化

之前的代码可以有一些改变。

第一，由于`where`block已经声明了所有的数据变量，那么方法上的参数就可以省略。

当然也可以只省略一部分，保留一部分，不如说想指明保留下的参数的类型。方法参数的顺序也不重要，数据变量是根据名字与方法参数进行匹配的。

第二，输入和期望的输出可以用2个管道符（||）隔开，看起来更直观。

综合以上2点，代码可以这样写：

```groovy
class MathSpec extends Specification {
  def "maximum of two numbers"() {
    expect:
    Math.max(a, b) == c

    where:
    a | b || c
    1 | 3 || 3
    7 | 4 || 7
    0 | 0 || 0
  }
}
```

除了管道符|，也可以用分号；做分隔符。

```groovy
class MathSpec extends Specification {
  def "maximum of two numbers"() {
    expect:
    Math.max(a, b) == c

    where:
    a ; b ;; c
    1 ; 3 ;; 3
    7 ; 4 ;; 7
    0 ; 0 ;; 0
  }
}
```

但是管道符和分号不能混用。如果分隔符变了，会认为是另一个独立的新表。

```groovy
class MathSpec extends Specification {
  def "maximum of two numbers"() {
    expect:
    Math.max(a, b) == c
    Math.max(d, e) == f

    where:
    a | b || c
    1 | 3 || 3
    7 | 4 || 7
    0 | 0 || 0

    d ; e ;; f
    1 ; 3 ;; 3
    7 ; 4 ;; 7
    0 ; 0 ;; 0
  }
}
```

## <span id="cuowubaogao">错误报告</span>

假设之前的`max`方法的实现有点问题，现在有一个迭代失败了：

```groovy
maximum of two numbers [a: 1, b: 3, c: 3, #0]   PASSED
maximum of two numbers [a: 7, b: 4, c: 7, #1]   FAILED

Condition not satisfied:

Math.max(a, b) == c
|    |   |  |  |  |
|    |   7  4  |  7
|    42        false
class java.lang.Math

maximum of two numbers [a: 0, b: 0, c: 0, #2]   PASSED
```

那么我们关心的问题就是：哪个迭代失败了，这个迭代的数据是多少？在这个例子里，不难看到是第二个迭代失败了。不过有时会很难找。Spock总会清晰地展示出是哪个迭代失败了，而不是仅仅报告失败。一个feature方法的不同迭代在默认情况下会以全名模式展开。这个展开模式可以在配置，在下方Unrolled Iteration Names一节会介绍。或者可以根据下一节的方法禁用展开。

## Method Uprolling and Unrolling 方法迭代的收起和展开

如果一个方法标注了注解`@Rollup`，那么它的各个迭代就不会独立报告。比如说如果想自动生成很多的测试用例，或者使用了外部数据来测试，或者不想让测试打印的数量太多。

```groovy
@Rollup
def "maximum of two numbers"() {
...
```

注意迭代收起和展开不会影响方法的执行情况，仅仅改变了报告的形式。在收起的情况下，输出会是这样：

```groovy
maximum of two numbers   FAILED

Condition not satisfied:

Math.max(a, b) == c
|    |   |  |  |  |
|    |   7  4  |  7
|    42        false
class java.lang.Math
```

`@Rollup`注解还可以放在specification上，相当于放在了这个spec下每一个没有标注`@Unroll`注解的数据驱动的feature方法上。

还可以在配置文件里设置`unroll`里的`unrollByDefault`为false来让所有feature方法默认将迭代收起。在Spock 2.0之前，收起是默认的配置。

*Disable Default Unrolling :*

```groovy
unroll {
    unrollByDefault false
}
```

不允许一个方法或spec上同时有`@Unroll`注解和`@Rollup`注解，会报错。

---

总结：

一个方法的迭代会收起：

+ 如果方法有注解`@Rollup`

+ 如果方法没有注解`@Unroll`且spec有注解`@Rollup`
+ 如果方法没有注解`@Unroll`且spec没有注解`@Unroll`，且设置`unroll{ unrollByDefault }`为`false`

一个方法的迭代会展开：

+ 如果方法被`@Unroll`注解
+ 如果方法没有注解`@Rollup`且spec有注解`@Unroll`
+ 如果方法没有注解`@Rollup`且spec没有注解`@Rollup`，且设置`unroll{ unrollByDefault }`为`true`

## Data Pipes 数据管道

数据表不是给数据变量提供值的唯一方法，事实上数据表是数据管道的语法糖：

```groovy
...
where:
a << [1, 7, 0]
b << [3, 4, 0]
c << [3, 7, 0]
```

<<左侧是数据变量，右侧是数据提供者（data provider），共同组成了一个数据管道。数据提供者保存了所有的数据，每个迭代的都有。任何Groovy里可迭代的对象都可以当数据提供者，包括`Collection`、`String`、`Interable`和实现了`Interable`规范的对象。数据提供者不一定是显式的包含了数据，也可以从外部源来获取数据，比如说文件、数据库、表格、或者随机生成一些数据。数据提供者只在需要的时候（下一个迭代前）提供下一个值就可以。

## Multi-Variable Data Pipes 多变量数据管道

如果数据提供者每个迭代返回的是多个值，可以通过<<连接到多个数据变量上。语法有点像Groovy的多重赋值，但是左侧使用的是方括号而不是圆括号。

```groovy
@Shared sql = Sql.newInstance("jdbc:h2:mem:", "org.h2.Driver")

def "maximum of two numbers"() {
  expect:
  Math.max(a, b) == c

  where:
  [a, b, c] << sql.rows("select a, b, c from maxdata")
}
```

可以用下划线忽略不感兴趣的值：

```groovy
...
where:
[a, b, _, c] << sql.rows("select * from maxdata")
```

多重赋值可以嵌套，下面的这个例子会生成以下迭代：

| a              | b      | c      |
| -------------- | ------ | ------ |
| `['a1', 'a2']` | `'b1'` | `'c1'` |
| `['a2', 'a1']` | `'b1'` | `'c1'` |
| `['a1', 'a2']` | `'b2'` | `'c2'` |
| `['a2', 'a1']` | `'b2'` | `'c2'` |

```groovy
...
where:
[a, [b, _, c]] << [
  ['a1', 'a2'].permutations(),
  [
    ['b1', 'd1', 'c1'],
    ['b2', 'd2', 'c2']
  ]
].combinations()
```

## 数据变量赋值

一个数据变量可以直接赋值：

```groovy
...
where:
a = 3
b = Math.random() * 100
c = a > b ? a : b
```

每个迭代赋值都会重新计算。

赋值的右侧也可以引用其他数据变量。

```groovy
...
where:
row << sql.rows("select * from maxdata")
// pick apart columns
a = row.a
b = row.b
c = row.c
```

## 访问其他数据变量

只有两种可能要在计算一个数据变量的时候需要访问另一个数据变量。

第一种可能是向上一节那样派生的数据变量（derived data variables）。每一个数据变量都可以在赋值的时候访问之前定义的数据变量，包括通过数据表和数据管道定义的：

```groovy
...
where:
a = 3
b = Math.random() * 100
c = a > b ? a : b
```

（c就是通过a和b赋值的）

第二种是在数据表中访问之前的列：

```groovy
...
where:
a | b
3 | a + 1
7 | a + 2
0 | a + 3
```

这种情况也包括在同一个`where`block里，之前的数据表的列：

```groovy
...
where:
a | b
3 | a + 1
7 | a + 2
0 | a + 3

and:
c = 1

and:
d     | e
a * 2 | b * 2
a * 3 | b * 3
a * 4 | b * 4
```



## Multi-Variable Assignment 多变量赋值

和数据管道一样，如果有一个Groovy可以迭代的对象，你也可以在一个表达式里对多个变量赋值。与数据管道不同的是，这里的语法和Groovy的多赋值语法相同（用圆括号）：

```groovy
@Shared sql = Sql.newInstance("jdbc:h2:mem:", "org.h2.Driver")

def "maximum of two numbers multi-assignment"() {
  expect:
  Math.max(a, b) == c

  where:
  row << sql.rows("select a, b, c from maxdata")
  (a, b, c) = row
}
```

可以用下划线忽略不关心的值：

```groovy
...
where:
row << sql.rows("select * from maxdata")
(a, b, _, c) = row
```

## 数据表、数据管道和变量赋值的组合使用

如果需要的话，数据表、数据管道和变量赋值可以组合使用：

```groovy
...
where:
a | b
1 | a + 1
7 | a + 2
0 | a + 3

c << [3, 4, 0]

d = a > c ? a : c
```

## 数据变量值的类型强制

数据变量的类型会被强制转换为方法声明的类型。自定义类型转换可以通过拓展模块（extension module）或在spec上使用`@Use`注解（如果放在feature方法上是没用的）。

```groovy
def "type coercion for data variable values"(Integer i) {
  expect:
  i instanceof Integer
  i == 10

  where:
  i = "10"
}
```

```groovy
@Use(CoerceBazToBar)
class Foo extends Specification {
  def foo(Bar bar) {
    expect:
    bar == Bar.FOO

    where:
    bar = Baz.FOO
  }
}
enum Bar { FOO, BAR }
enum Baz { FOO, BAR }
class CoerceBazToBar {
  static Bar asType(Baz self, Class<Bar> clazz) {
    return Bar.valueOf(self.name())
  }
}
```

## 迭代的次数

迭代的次数取决于有多少有效数据。一个方法可能会迭代不同的次数。如果一个数据提供者比其他的数据提供者更早地耗尽了数据，那么会抛出一个异常。变量赋值不会影响迭代的次数。一个只有变量赋值的`where`block只会产生一次迭代。

## 数据提供者的关闭

在所有迭代完成后，所有数据提供者都会调用一个没有参数的`close`方法（如果有的话）。

## 展开时迭代的名称

默认情况下，迭代的名称就是feature的名称加上数据变量和迭代下标。这样迭代的名称不会重复，并且很容易识别是哪个数据变量组合失败了。

在[错误报告](#cuowubaogao)一节的例子里，可以看出是第二个迭代失败了。

迭代名称可以做优化：

```groovy
def "maximum of #a and #b is #c"() {
...
```

这个方法名称使用了占位符表达式：#a，在输出的时候占位符表达式会替换为具体的值：

```groovy
maximum of 1 and 3 is 3   PASSED
maximum of 7 and 4 is 7   FAILED

Math.max(a, b) == c
|    |   |  |  |  |
|    |   7  4  |  7
|    42        false
class java.lang.Math

maximum of 0 and 0 is 0   PASSED
```

现在我们可以直接看出来`max`方法在输入为7和4的时候失败了。

这个语法非常像Groovy的`GString`，区别在于：

+ 方法名使用了`#`，而`GString`使用`$`；并且方法名这里没有类似于`${...}`的语法
+ 方法名只支持属性或者零参数方法

如果有一个`Person`类，有属性`name`和`age`，然后有一个`Person`类型的数据变量`person`，下面的这些方法名都是有效的：

```groovy
def "#person is #person.age years old"() { // property access
def "#person.name.toUpperCase()"() { // zero-arg method call
```

非字符串的值（如上面的`#person`）会根据Groovy的语法转换为String。

下面的这些方法名是无效的：

```groovy
def "#person.name.split(' ')[1]" {  // cannot have method arguments
def "#person.age / 2" {  // cannot use operators
```

如果有必要的话，可以引入额外的数据变量来实现更复杂的方法名：

```groovy
def "#lastName"() {
  ...
  where:
  person << [new Person(age: 14, name: 'Phil Cole')]
  lastName = person.name.split(' ')[1]
}
```

除了数据变量以外，还支持`#featureName`和`#iterationIndex`。前者是实际的feature名，没有太大的意义，不过在另外两个可以定制unroll pattern的地方有点用。

```groovy
def "#person is #person.age years old [iterationIndex: #iterationIndex]"() {
```

还可以在unroll pattern里指定方法名，作为`@Unroll`注解的参数。该unroll pattern会优先于方法名展示。

```groovy
@Unroll("#featureName[#iterationIndex] (#person.name is #person.age years old)")
def "person age should be calculated properly"() {
```

如果既没有给注解的参数，方法名也不包含#，配置文件会检查`unroll{ defaultPattern }`。如果设置为了非空字符串，这个字符串将会被作为unroll pattern。例如，可以设置为：

+ #featureName：所有的迭代会是同样的名字
+ #featureName[#iterationIndex]：有一个简单的标注了迭代下标的名字
+ #iterationName：如果你确定在每个feature方法里设置了一个数据变量叫做iterationName，那么报告会使用这个值

*Set Default Unroll Pattern*

```groovy
unroll {
    defaultPattern '#featureName[#iterationIndex]'
}
```

如果没有使用上述的三种方式自定义unroll pattern，默认会使用feature方法的名称，并在后面带上所有数据变量的名称和值，还有迭代的索引，例如`my feature [x: 1, y: 2, z: 3, #0]`。

如果在表达式里出现了错误，例如输错了变量名、在计算值的时候会有异常，那么测试会失败。不过如果设置了迭代收起，并且让数据变量自动跟在后面，哪怕表达式有错，也不会让测试失败。

可以通过在设置文件里设置，当表达式出错也不会让测试失败，设置`unroll { validateExpressions }`为false即可。如果这样设置后，表达式出现了错误，那么原本的表达式`#foo.bar`会打印为`#Error:foo.bar`。

*Disable Unroll Pattern Expression Asserting*

```groovy
unroll {
    validateExpressions false
}
```

# Interaction Based Testing 基于交互的测试

基于交互的测试是2000几年在极限编程社区提出的一种设计和测试技术。相比于对象的状态，它更聚焦于对象的行为；它通过方法调用关系，展示了一个spec下的对象如何与其他模块交互。

例如，假设我们有一个`Publisher`对象给一些`Subscriber`对象发送消息：

```groovy
class Publisher {
  List<Subscriber> subscribers = []
  int messageCount = 0
  void send(String message){
    subscribers*.receive(message)
    messageCount++
  }
}

interface Subscriber {
  void receive(String message)
}

class PublisherSpec extends Specification {
  Publisher publisher = new Publisher()
}
```

你打算怎么去测试`Publisher`呢？如果是基于状态的测试，我们可以验证`publisher`一直有跟踪着她的`subscriber`。更有趣的问题是，尽管如此，这个消息是否被`subscriber`接收了。为了回答这个问题，我们就需要一个监听`publisher`和其`subscriber`之间通信的特殊`Subscriber`实现。这个特殊的实现就被称为mock对象（mock object）。

虽然我们可以自己手动实现`subscriber`的mock，但是随着方法的数量变多和交互的复杂性增加，编写和维护这些代码就会变得困难。这时候我们就需要一个框架（mocking framework）了：它们提供了一种方法来描述spec里的某个对象和其他对象的交互，并且生成其他对象的mock实例来验证这些。

>**mock实例是如何生成的？**
>
>和大多数Java的mock框架一样，Spock用JDK动态代理（当mock接口时）和Byte Buddy或用CGLIB（当mock类时）来在运行时动态生成mock实例。相较于使用Groovy来实现，这样的好处是它也可以用于测试Java代码。

Java里有很多流行且成熟的mock框架，如JMock、EasyMock、Mockito等。尽管这些工具都可以和Spock一起使用，我们还是决定推出自己的mock框架，与Spock的specification语言紧密整合。这个决定是希望利用Groovy的所有功能让基于交互的测试更加容易编写、更具可读性并更有趣。我们希望在这章结束的时候，你会同意我们已经实现了这些目标。

除了指明的部分，Spock mock框架的所有特性都可以既对Java代码，又对Groovy代码进行测试。

## 创建Mock对象

Mock对象是通过`MockingApi.Mock()`方法创建的。让我们创建2个mock的`subscriber`：

```groovy
def subscriber = Mock(Subscriber)
def subscriber2 = Mock(Subscriber)
```

另外，下面这种Java风格的语法也支持，这种风格提供更好的IDE支持：

```groovy
Subscriber subscriber = Mock()
Subscriber subscriber2 = Mock()
```

这里，mock的类型是从左侧变量的类型推测出来的。

>注意：
>
>如果mock的类型在赋值语句的左侧给出了，那么右侧就允许省略（不是必须的）。

mock对象逐字地实现（继承，在类的情况下）它们所代表的类型。换句话说，在我们的例子里，`subscriber is a Subscriber`。因此它可以传递给需要这种类型（Java）的地方。

## mock对象的默认行为

> **宽松的和严格的mock框架**
>
> 和Mockito一样，我们坚定地认为一个mock框架应该默认是宽松的。这意味着允许调用mock对象的未预期的方法（或者，换句话说，与手头测试无关的交互）。与此相反的是，如EasyMock和JMock这样的框架在默认情况下是严格的，如果调用了未预期的方法，就会抛出异常。虽然严格可以让代码更加规范，但是也可能会导致过度规范化，从而让测试很容易由于内部代码的一点改变就失败。Spock的mock框架避免这种过度规范的陷阱，只描述和一个交互相关的内容。

最初，mock对象没有任何行为。可以调用他们的方法，但是不会有任何作用，只会返回方法返回值类型的默认值（false, 0, 或者null）。不过以下方法是例外：`Object.equals`、`Object.hashCode`、`Object.toString`，会有以下默认行为：一个mock对象只会equals自己，有唯一的hashCode，有一个包含了类型名称的字符串。这些默认行为可以通过`stubbing`这些方法来覆写，将在`Strubbing`一节介绍。

## 在Specification下注入mock对象

在创建好publisher和subscriber以后，我们需要让前者知道后者：

```groovy
class PublisherSpec extends Specification {
  Publisher publisher = new Publisher()
  Subscriber subscriber = Mock()
  Subscriber subscriber2 = Mock()

  def setup() {
    publisher.subscribers << subscriber // << is a Groovy shorthand for List.add()
    publisher.subscribers << subscriber2
  }
```

我们接下来就可以描述这两个部分间的交互了。

## Mocking 模拟

Mocking是描述specification下的对象之间交互的行为。例如：

```groovy
def "should send messages to all subscribers"() {
  when:
  publisher.send("hello")

  then:
  1 * subscriber.receive("hello")
  1 * subscriber2.receive("hello")
}
```

大声读出来："When the publisher sends a 'hello' message, then both subscribers should receive that message exactly once. "（当一个publisher发送一条“hello”，然后所有的subscriber都会收到这条信息一次，且仅一次。）

当feature方法运行的时候，执行`when`block时对模拟对象的所有调用都将于`then`block里描述的交互进行匹配。如果有一个交互不满足，就会抛出一个`InteractionNotSatisfiedError`或其子类。这种验证是自动进行的，不需要额外的代码。

### Interactions 交互

> **一个交互仅仅是一个普通的方法调用吗？**
>
> 不完全是，尽管一个交互看上去和一个普通方法调用很像，但是它只是一个表达哪些方法如预期调用的一种方式。一个好的方法是，将交互看作是一个正则表达式，所有模拟对象上进行的调用会对其进行匹配。根据具体情况，交互可能匹配0个，1个或者多个。

让我们仔细看看`then`block。它包含2个交互，每一个4个不同的部分：1个基数（cardinality），1个目标约束（target constraint），一个方法约束（method constaint）和一个参数约束（argument constraint）：

```groovy
1 * subscriber.receive("hello")
|   |          |       |
|   |          |       argument constraint
|   |          method constraint
|   target constraint
cardinality
```

### Cardinality 基数

交互的基数是一个方法预期调用的次数。可以是一个固定的数据，也可以是一个范围：

```groovy
1 * subscriber.receive("hello")      // exactly one call
0 * subscriber.receive("hello")      // zero calls
(1..3) * subscriber.receive("hello") // between one and three calls (inclusive)
(1.._) * subscriber.receive("hello") // at least one call
(_..3) * subscriber.receive("hello") // at most three calls
_ * subscriber.receive("hello")      // any number of calls, including zero
                                     // (rarely needed; see 'Strict Mocking')
```

### Target Constraint 目标约束

交互的目标约束是预期有方法调用的mock对象：

```groovy
1 * subscriber.receive("hello") // a call to 'subscriber'
1 * _.receive("hello")          // a call to any mock object
```

### Method Constraint 方法约束

交互的方法约束是预期被调用的方法：

```groovy
1 * subscriber.receive("hello") // a method named 'receive'
1 * subscriber./r.*e/("hello")  // a method whose name matches the given regular expression
                                // (here: method name starts with 'r' and ends in 'e')
```

当预期调用一个getter方法时，可以直接用调用属性的语法：

```groovy
1 * subscriber.status // same as: 1 * subscriber.getStatus()
```

当预期调用一个setter方法时，只能使用调用方法的语法：

```groovy
1 * subscriber.setStatus("ok") // NOT: 1 * subscriber.status = "ok"
```

### Argument Constraints 参数约束

交互的参数约束是预期的方法参数：

```groovy
1 * subscriber.receive("hello")        // an argument that is equal to the String "hello"
1 * subscriber.receive(!"hello")       // an argument that is unequal to the String "hello"
1 * subscriber.receive()               // the empty argument list (would never match in our example)
1 * subscriber.receive(_)              // any single argument (including null)
1 * subscriber.receive(*_)             // any argument list (including the empty argument list)
1 * subscriber.receive(!null)          // any non-null argument
1 * subscriber.receive(_ as String)    // any non-null argument that is-a String
1 * subscriber.receive(endsWith("lo")) // an argument matching the given Hamcrest matcher
                                       // a String argument ending with "lo" in this case
1 * subscriber.receive({ it.size() > 3 && it.contains('a') })
// an argument that satisfies the given predicate, meaning that
// code argument constraints need to return true of false
// depending on whether they match or not
// (here: message length is greater than 3 and contains the character a)
```

对于有多个参数的方法，参数约束也可以：

```groovy
1 * process.invoke("ls", "-a", _, !null, { ["abcdefghiklmnopqrstuwx1"].contains(it) })
```

当处理不定数参数时，不定数参数的语法也可以用在相应的交互里：

```groovy
interface VarArgSubscriber {
    void receive(String... messages)
}

...

subscriber.receive("hello", "goodbye")
```

> **Spock深度细节：Groovy Varargs（不定数参数）**
>
> Groovy允许任何方法的最后一个参数是一个数组类型，称为vararg style。所以，vararg语法也可以用在这些方法的交互里。

#### Equality Constraint 参数相等的约束

相等约束使用Groovy自身相等效果来检查参数，例如`argument == constraint`。可以使用下面的这些来作为一个相等约束：

+ 任何字面量：`1 * check('string')` / `1 * check(1)` / `1 * check(null)`【check的参数是'string'，1，null】
+ 变量：`1 * check(var)`
+ 一个列表或者一个map： `1 * check([1])` / `1 * check([foo: 'bar'])`
+ 对象：`1 * check(new Person('sam'))`
+ 方法调用的结果：`1 * check(person())`

#### Hamcrest Constraint （Hamcrest时一款用于校验的Java单元测试框架）

时equality约束的一个辩题，如果约束的对象是一个Hamcrest匹配器，那么会使用这个匹配器来检查参数

#### Wildcard Constraint 使用通配符约束参数

通配符约束会匹配任何参数，包括`null`。即` `，会匹配`1 * subscriber.receive( )`。还有一个扩展通配符约束`*_`会匹配任意数量的`1 * subscriber.receive(*_)`。

#### Code Constraint 使用一段代码约束参数

代码约束是最通用的约束。它是一个Groovy的闭包，将参数作为闭包的参数。闭包被视作为一个condition块，所以效果和一个`then`block一样，换句话说，每行都看作是一个隐式的断言。它可以模拟除了扩展通配符约束以外的所有约束，但是更建议使用其他简单的约束。在代码约束里可以执行多个断言、调用方法来断言（call methods for assertions），或者使用`use/verifyAll`。

```groovy
1 * list.add({
  verifyAll(it, Person) {
    firstname == 'William'
    lastname == 'Kirk'
    age == 45
  }
})
```

#### Negating Constraint 否定形式的约束

否定约束`!`是一个复合约束，也就是说它需要和另一个约束组合起来工作。它将反转嵌套约束的结果，即`1 * subscriber.receive(!null)`是一个检查参数是不是null相等约束，然后否定约束会反转这个结果，改为：传入不是null的参数。

尽管它可以和其他任何约束组合，但不是任何时候都有意义。例如`1 * subscrbier.receive(!_)`什么都匹配不了。记住，对于一个没有匹配上的否定约束仅仅表示，其内部约束没有匹配。 

#### Type Constraint 类型约束

类型约束检查参数的类型，就像否定约束一样，它也是一个复合约束。通常写作`_ as Type`，这是一个通配符约束和类型约束的组合。你也可以将类型约束和其他约束组合， `1 * subscriber.receive({ it.contains('foo')} as String)` 会在断言这个参数包含`foo`（代码约束）之前断言这是一个`String`类型，

### 匹配任何方法的调用

有时候匹配任何东西也是有用的：

```groovy
1 * subscriber._(*_)     // any method on subscriber, with any argument list
1 * subscriber._         // shortcut for and preferred over the above

1 * _._                  // any method call on any mock object
1 * _                    // shortcut for and preferred over the above
```

> Note：
>
> 尽管 `(_.._) * _._(*_) >> _` 时一个有效的交互声明，但是这既不是一个好的样式，也没什么用。

### Strict Mocking 严格的Mocking

那么，什么时候匹配任何方法的调用会游泳呢？一个好的例子是strict mocking，一种除了声明的交互之外不允许其他任何交互的mocking方式：

```groovy
when:
publisher.publish("hello")

then:
1 * subscriber.receive("hello") // demand one 'receive' call on 'subscriber'
_ * auditing._                  // allow any interaction with 'auditing'
0 * _                           // don't allow any other interaction
```

`0*`仅仅在`then`block或者方法的最后一个交互才有意义。注意`_ *`（任何数量的调用）的用法，会允许auditing的任何交互。

> NOTE：
>
> `_ *`仅仅在strict mocking的语境下有意义。在Stubbing一个交互的时候，就不必须了。例如`_ * auditing.record() >> "ok"`可以（也应该！）简化为`auditing.record( ) >> "ok"`。

### 在哪里声明交互

到目前为止，我们所有的交互都声明在了`then`block里。这样可以让spec读起来更自然。然而，也允许把交互声明在`when`block前的任何位置。特别是，这意味着交互可以声明在`setup`方法里。交互也可以声明在任何同一个spec类里的辅助实例方法里（"helper" instance method）。

当模拟对象有调用时，将按照交互声明的顺序进行匹配。如果一个调用可以匹配多个交互，那么未达到调用上限的最早声明的交互将成功匹配。这个规则有一个例外：在`then`block中声明的交互将在其他交互之前匹配。这允许`then`block里的交互覆盖掉诸如`setup`里的交互。

> **Spock Deep Dive: How Are Interactions Recognized? 如何识别交互**
>
> 换句话说，什么让一个表达式成为了一句交互声明，而不是一个正则方法调用之类的？Spock使用一个简单的语法规则来识别交互：如果一个表达式在语句的位置，并且要么是一个乘号（`*`）或者右移（`>>`，`>>>`）操作，然后它就会被认为是一个交互，并且进行相应的解析。这样的一个表达式在语句的位置上几乎没有任何的作用，所以改变它的意思并没有什么问题。注意这些操作符和声明基数（mocking时）或结果生成器（stubbing时）语法的联系。这两个必须存在一个，单单`foo.bar()`不会被认为是一个交互。

### 在mock创建的时候声明交互

如果一个mock有一组不变的基础交互，可以直接声明在mock创建的时候：

```groovy
Subscriber subscriber = Mock {
   1 * receive("hello")
   1 * receive("goodbye")
}
```

这个特性对Stubbing和专用Stubs特别有吸引力。注意这里的交互没有（也不能有，因为闭包里引用不到subscriber）目标约束，从上下文可以清晰地看出它们属于哪个mock对象。

交互还可以在用mock初始化实例字段的时候声明：

```groovy
class MySpec extends Specification {
    Subscriber subscriber = Mock {
        1 * receive("hello")
        1 * receive("goodbye")
    }
}
```

### 具有相同目标的交互分组

共有同一个目标对象的交互可以用`with`block放在一起。有点像在mock创建时声明交互，这可以避免不必要的重复目标约束：

```groovy
with(subscriber) {
    1 * receive("hello")
    1 * receive("goodbye")
}
```

`with`block也可以用来把具有相同目标的交互分组。

### 混合交互和conditions

`then`block里可能既有交互也有condition。尽管并没有严格的要求，但是通常先声明交互，后声明condtion：

```groovy
when:
publisher.send("hello")

then:
1 * subscriber.receive("hello")
publisher.messageCount == 1
```

Read out aloud: "When the publisher sends a 'hello' message, then the subscriber should receive the message exactly once, and the publisher’s message count should be one."“当publisher发送一条‘hello’消息，就会有subscriber应该收到这条消息1次，并且publisher的消息计数应该是1。”

### 显式交互块

在本质上，Spock必须在预期的交互发生前对其有完整的信息。所以为什么可以在`then`block里声明交互呢（交互是在方法调用前就有了，before，但是声明是在方法之后，then）？答案是：在底层，Spock把`then`block里声明的交互移动到了紧邻的`when`block的前面。在大多数情况下，这种做法效果不错，但是有时候会有问题：

```groovy
when:
publisher.send("hello")

then:
def message = "hello"
1 * subscriber.receive(message)
```

这里我们为预期的参数引入了一个变量。（同样，我们也可以为基数引入一个变量。）然而Spock不足以聪明到识别到这个交互和变量的声明有内在的联系。所以它只会把交互移动到前面，这会在运行时导致一个`MissingPropertyException`。

解决这个问题的一种方法是将变量的声明（至少）移动到`when`block之前。（数据驱动测试的爱好者可能会把这个变量移动到`where`block。）在我们的例子里，这样做有一个额外的好处，我们可以使用同一个变量来发送消息。

另一个解决方法是显式地去表示这个变量声明和交互是一起的：

```groovy
when:
publisher.send("hello")

then:
interaction {
  def message = "hello"
  1 * subscriber.receive(message)
}
```

由于`MockingApi.interaction`block总是整体移动，这样就可以如预期运行。

### 交互的作用域

声明在一个`then`block里的交互的作用域限定在它前面的`when`block里：

```groovy
when:
publisher.send("message1")

then:
1 * subscriber.receive("message1")

when:
publisher.send("message2")

then:
1 * subscriber.receive("message2")
```

这可以验证`subcriber`在第一个`when`block，收到`message1`，在第二个`when`block收到`message2`。

声明在`when`block之外的交互的作用域，从他们声明的地方一直到这个feature方法的结束。

交互的作用域永远是在某一个特定的feature方法中。因此他们不能声明在静态方法、`setupSpec`和`cleanupSpec`中。同样，mock对象也不应该存储在静态或`@Shared`字段中。

### 交互的验证

基于mock的方法会有两种主要的失败方式：一个交互可以匹配到比允许的数更多的调用，或者比需要匹配到的更少的调用。前一种情况在调用发生的时候被检测到，并且会抛出一个`TooManyInvocationsError`：

```groovy
Too many invocations for:

2 * subscriber.receive(_) (3 invocations)
```

为了方便地诊断出为什么会有太多的调用被匹配到，Spock会展示出匹配到交互的调用：

```groovy
Matching invocations (ordered by last occurrence):

2 * subscriber.receive("hello")   <-- this triggered the error
1 * subscriber.receive("goodbye")
```

通过这个输出可以看出，其中一个`receive("hello")`的调用触发了`TooManyInvocationsError`。注意，由于像这两个`subscriber.receive("hello")`的调用十分难以区分，并且被聚合在一行输出里，所以第一个`receive("hello")`很可能在`receive("goodbye")`之前触发。

第二种情况（调用比需要的少）只会在`when`block执行完之后才被检测到。（在此之前，可能还有别的调用。）会抛出一个`TooFewInvocationsError`：

```groovy
Too few invocations for:

1 * subscriber.receive("hello") (0 invocations)
```

注意，这个方法有没有被调用过并不重要，用不同的参数调用同样的方法，在一个别的mock对象上调用这个方法，或者在这时调用了别的方法；在以上的所有情况下，`TooFewInvocationsError`都会被抛出。

为了更容易的诊断这个缺失的方法的地方执行了什么，Spock会展示出所有没有匹配到交互的调用（一个交互都没匹配到的调用），按照他们与这个交互的相关性排序。特别的是，只有参数没匹配到的交互会最先展示：

```groovy
Unmatched invocations (ordered by similarity):

1 * subscriber.receive("goodbye")
1 * subscriber2.receive("hello")
```

### 调用顺序

通常，精确地方法调用顺序并没有什么关系，并且可能会随着时间改变。为了避免过度规范，Spocl默认允许任何调用顺序，只要交互最终满足：

```groovy
then:
2 * subscriber.receive("hello")
1 * subscriber.receive("goodbye")
```

这里，以下几种调用顺序都可以匹配这个交互：`"hello"` `"hello"` `"goodbye"`, `"hello"` `"goodbye"` `"hello"`,  `"goodbye"` `"hello"` `"hello"`。

在那些调用顺序很重要的场景下，可以通过将交互划分到多个`then`block来指定顺序：

```groovy
then:
2 * subscriber.receive("hello")

then:
1 * subscriber.receive("goodbye")
```

现在Spock会确保2个`"hello"`在`"goodbye"`之前接收。换句话说，`then`block之间的调用顺序是强制要求满足的，但是`then`block内的调用顺序是无所谓的。

> NOTE
>
> 将`then`block用`and`block拆分时，并不会强制要求顺序，因为`and`block仅仅是用于更好的文档可读性，不具备任何语义。

### Mocking Classes mock类

除了接口，Spock还支持mock类。mock类和mock接口工作方式类似；唯一的附加要求是需要将 `byte-buddy` 1.9+ 或 `cglib-nodep` 3.2.0+ 放在class path里。

当使用如：

+ 普通的Mock和Stub
+ 配置为`useObjenesis: true`的Spy
+ 监视一个具体实例的Spy，如`Spy(myInstance)`

也必须把 `objenesis` 3.0+放在class path里，除了有无参构造函数或配置了`constructorArgs`的类，除非不应该执行构造函数调用，例如为了避免不必要的副作用。

it is also necessary to put `objenesis` 3.0+ on the class path, except for classes with accessible no-arg constructor or configured `constructorArgs` unless the constructor call should not be done, for example to avoid unwanted side effects.

如果class path里缺少了这两个，Spock会提示你。

## Stubbing 插桩/存根

Stubbing是让协作者用特定方法响应方法调用的一种行为。当stub一个方法时，你不需要关心方法是否会被调用以及调用多少次，你只是想让这个方法在被调用时返回一些值，或者表现出一些副作用。

为了接下来的例子，我们先修改`Subscriber`的`receive`方法，让它返回一个状态码，以通知subscriber是否可以处理消息。

```groovy
interface Subscriber {
    String receive(String message)
}
```

现在，我们让`receive`方法在每次调用的时候返回`"ok"`：

```groovy
subscriber.receive(_) >> "ok"
```

"*Whenever* the subscriber receives a message, *make* it respond with 'ok'."“每当订阅者收到了一条消息，让它响应‘ok’。”

和mock的交互相比，stub的交互在左侧没有基数，但是在右侧增加了一个响应生成器（response generator）：

```groovy
subscriber.receive(_) >> "ok"
|          |       |     |
|          |       |     response generator
|          |       argument constraint
|          method constraint
target constraint
```

stub的交互可以在通常的地方声明：既可以在`then`block里，或者`when`block前的任何地方。如果一个mock对象仅用于stub，通常会声明在mock创建的时候，或者在`given`block里。

### 返回固定值

我们已经看见了`>>`操作符返回一个固定值的用法：

```groovy
subscriber.receive(_) >> "ok"
```

为了给不同的调用返回不同的值，要使用多个交互：

```groovy
subscriber.receive("message1") >> "ok"
subscriber.receive("message2") >> "fail"
```

这样，当收到`message1`的时候会返回`"ok"`，收到`message2`的时候会返回`"fail"`。对于返回那些值没有限制，只要他们和方法声明的返回值类型兼容。

### 返回一组值

若要在连续调用的时候返回不同的值，使用三个右箭头`>>>`操作符：

```groovy
subscriber.receive(_) >>> ["ok", "error", "error", "ok"]
```

这样会在第一次调用的时候返回`"ok"`，第二次和第三次调用的时候返回`"error"`，对所有剩下的调用返回`"ok"`。右侧的值必须是Groovy可以迭代的；在这个例子里，我们用了plain list。

### 计算返回值

若要基于方法的参数计算返回值，可以用`>>`和闭包。如果闭包声明了一个单独的无类型参数，就会传递方法的参数列表给它：

```groovy
subscriber.receive(_) >> { args -> args[0].size() > 3 ? "ok" : "fail" }
```

这里，如果消息比3个字符长，就会返回`"ok"`，否则返回`"fail"`。

在大多数情况下，直接访问方法的参数会更方便。如果闭包里声明的参数比1个多，或者是1个有类型的参数，方法参数就会逐个映射到闭包参数里：

```groovy
subscriber.receive(_) >> { String message -> message.size() > 3 ? "ok" : "fail" }
```

响应生成器的行为和之前一个一样，但是可以说更具可读性。

如果你发现自己需要更多关于方法调用的信息而不是参数，可以参考`org.spockframework.mock.IMockInvocation`。所有声明在这个接口里的方法都可以直接用在闭包里，不需要一个前缀。（在Groovy里，是将闭包（closure）委托（delegates）给一个`IMockInvocation`的实例。）

### 执行的副作用

有时候，你可能想做的不仅仅是计算返回值。一个典型的例子是抛出了异常。同样，这里闭包也可以：

```groovy
subscriber.receive(_) >> { throw new InternalError("ouch") }
```

当然，闭包也可以包含更多的代码，比如说一条`println`语句。它会在每次有匹配到这个交互的调用时执行。

### 链式的方法响应

方法的响应值可以写成一个链：

```groovy
subscriber.receive(_) >>> ["ok", "fail", "ok"] >> { throw new InternalError() } >> "ok"
```

这样会在前3次调用的时候依次返回`"ok", "fail", "ok"`，在第4次调用的时候抛出``InternalError`，在其他调用返回`ok`。

### 返回一个默认响应

如果你其实并不关心返回什么，但是必须返回一个非null的值，可以使用`_`。这会使用和Stub相同的逻辑来计算响应，所以它只对`Mock`和`Spy`实例有用。

```groovy
subscriber.receive(_) >> _
```

你当然也可以在这里用链式。这对Stub实例也很有用。

```groovy
subscriber.receive(_) >>> ["ok", "fail"] >> _ >> "ok"
```

## 将Mock和Stub组合

mock和stub是相辅相成的：

```groovy
1 * subscriber.receive("message1") >> "ok"
1 * subscriber.receive("message2") >> "fail"
```

当mock和stub同一个方法时，他们必须发生在同一个交互里。特别是，像接下来这种Mockito风格的，将stub和mock拆分到2个语句在Spock里是不行的：

```groovy
given:
subscriber.receive("message1") >> "ok"

when:
publisher.send("message1")

then:
1 * subscriber.receive("message1")
```

如在哪里声明交互一节所述，`receive`调用会先和`then`block里的交互匹配。由于该交互没有指定响应，会返回这个方法返回类型的默认值（这个例子里是`null`）。（这仅仅是Spock对mock的宽松型的一个表现。）所以，在`given`block里的交互永远没有机会匹配到。

> NOTE
>
> 同一个方法调用的mock和stub必须在一个交互里。

## 其他类型的mock对象

到目前为止，我们已经用`MockingApi.Mock`方法创建了mock对象。除了这个方法外，`MockingApi`类还提供了一些其他的工厂方法，来创建更多专门化的mock对象。

### Stubs

`stub`是用`MockingApi.Stub`工厂方法创建的：

```groovy
Subscriber subscriber = Stub()
```

mock既可以用于stubbing，也可以用于mocking，而stub只是用于stubbing。将协作者限定为stub可以让spec的读者更理解它所扮演的角色。

> NOTE
>
> 如果一个stub调用匹配了一个强制交互（如`1 * foo.bar()`），那么会抛出`InvalidSpecException`。

像mock一样，stub允许未期望的调用。然而stub的返回值在以下这些情况下会更加ambitious（雄心勃勃？）：

+ 对于基础类型，会返回基础类型的返回值。
+ 对于非基础类型的数字值（如`BigDecimal`），会返回0.
+ 如果值可以从stub实例里赋值，会返回这个实例（例如构建器模式 builder pattern）。
+ 对于非数值的值，会返回"empty"或"dummy"对象。这意味着一个空字符串，一个空集合，一个根据默认构造器构造的对象，或者另一个返回默认值的stub。详细信息见`org.spockframework.mock.EmptyOrDummyResponse`类。

> NOTE
>
> 如果方法的响应类型是一个final类，或它需要一个class-mocking库，但是cglib和ByteBuddy都不行，那么"dummy"对象就会创造失败，并抛出`CannotCreateMockException`。

stub通常有一组固定的交互，这让在mock创建时声明交互更具吸引力：

```groovy
Subscriber subscriber = Stub {
    receive("message1") >> "ok"
    receive("message2") >> "fail"
}
```

### Spies

（在使用这个特性之前请三思。可能更改Spec的代码设计会更好。）

`spy`是用`MockingApi.Spy`工厂方法创建的：

```groovy
SubscriberImpl subscriber = Spy(constructorArgs: ["Fred"])
```

spy永远是基于一个真实对象的。因此你必须提供一个类的类型，而不是一个接口类型，以及任何一个这个类的构造器的参数。如果不提供构造器参数，就会使用这个类型的无参构造器。

如果所给的构造器参数有歧义，那么可以用`as`或者Java风格的类型转换来转换参数的类型。例如，被测试的类有1个`String`参数的构造器，还有一个`Pattern`参数的构造器，现在想用`null`作为构造器参数：

```groovy
SubscriberImpl subscriber = Spy(constructorArgs: [null as String])
SubscriberImpl subscriber2 = Spy(constructorArgs: [(Pattern) null])
```

你也可以通过一个实例化的对象来创建spy。在你不能完全控制感兴趣的实例时，这会非常有用。（例如在Spring或Guice这样的依赖注入框架里测试的时候。）

spy上的方法调用会自动代理给真实对象。同样，真实对象方法的返回值也会通过spy传递给调用者。

在创建spy后，你可以监听调用者和spy背后的真实对象的对话：

```groovy
1 * subscriber.receive(_)
```

除了确保`receive`方法只被调用一次以外，subscriber和spy背后的`SubscriberImpl`实例之间的会话会维持不变。

当在一个spy上stub一个方法时，真实的方法不再被调用：

```groovy
subscriber.receive(_) >> "ok"
```

作为`SubscriberImpl.receive`调用的替代，`receive`方法只会简单的返回`"ok"`。

有时候，我们希望同时执行一些代码，并且委托给真实方法：

```groovy
subscriber.receive(_) >> { String message -> callRealMethod(); message.size() > 3 ? "ok" : "fail" }
```

这里我们用`callRealMethod()`来将方法调用委托给真实对象。注意我们没必要传递`message`参数；它会自动传递。`callRealMethod()`返回真实调用的结果，但是在这个例子里我们选择返回我们的结果。如果我们想传递一个不同的消息给实际方法，我们可以用`callRealMethodWithArgs("changed message")`。

请注意，虽然语义上`callRealMethod()` 和 `callRealMethodWithArgs(…)`都只对spy有意义，但是从技术上讲，你也可以在mock和stub对象上调用这些方法，“通过后门”将他们变成（伪）spy对象。唯一的前提条件就是，mock或者stub的对象实际上有一个真正的方法实现，例如，对接口mock必须有一个默认方法，对于类mock必须有一个非abstract的原方法。

### 部分mock

（在使用这个特性之前请三思。可能更改Spec的代码设计会更好。）

spy也可以用作部分mock：

```groovy
// this is now the object under specification, not a collaborator
MessagePersister persister = Spy {
  // stub a call on the same object
  isPersistable(_) >> true
}

when:
persister.receive("msg")

then:
// demand a call on the same object
1 * persister.persist("msg")
```

## Groovy的mock

到目前为止，我们见过的所有的mock特性，无论是用Java还是Groovy写的调用代码，都一样有效。借助Groovy的动态功能，Groovy的mock为测试Groovy代码专门提供了一些附加的特性。【我是个Java程序员，故本节略】

## 进阶特性

在大多数时候你应该都并不需要这些特性。但是如果当你需要，你会很高兴有这些特性。

### A la Carte Mocks

归根结底，`Mock()`、`Stub()`和`Spy()`工厂方法仅仅是用特定配置创建mock对象的罐装方法。如果你想对mock的配置有更细颗粒度的控制，看一下`org.spockframework.mock.IMockConfiguration`接口。这个接口的所有属性都可以被作为命名参数传递给`Mock()`方法。例如：

```groovy
def person = Mock(name: "Fred", type: Person, defaultResponse: ZeroOrNullResponse.INSTANCE, verified: false)
```

这里，我们创建一个mock，它的默认返回值和`Mock()`的返回值匹配，但是它的调用没有验证（和`Strub()`一样）。与传递`ZeroOrNullResponse`不同，我们可以提供我们自己定制的`org.spockframework.mock.IDefaultResponse`。

### 检测模拟对象

为了查明某个特定对象是不是Spock的mock对象，可以使用`org.spockframework.mock.MockUtil`：

```groovy
MockUtil mockUtil = new MockUtil()
List list1 = []
List list2 = Mock()

expect:
!mockUtil.isMock(list1)
mockUtil.isMock(list2)
```

这个工具还可以用来获取mock对象的更多信息：

```groovy
IMockObject mock = mockUtil.asMock(list2)

expect:
mock.name == "list2"
mock.type == List
mock.nature == MockNature.MOCK
```

## 拓展阅读

如果你想对基于交互的测试有更多的了解，我们推荐下面这些资源：

[Endo-Testing: Unit Testing with Mock Objects](http://www.ccs.neu.edu/research/demeter/related-work/extreme-programming/MockObjectsFinal.PDF)

Paper from the XP2000 conference that introduces the concept of mock objects.

[Mock Roles, not Objects](http://www.jmock.org/oopsla2004.pdf)

Paper from the OOPSLA2004 conference that explains how to do mocking *right*.

[Mocks Aren’t Stubs](http://martinfowler.com/articles/mocksArentStubs.html)

Martin Fowler’s take on mocking.

[Growing Object-Oriented Software Guided by Tests](http://www.growing-object-oriented-software.com/)

TDD pioneers Steve Freeman and Nat Pryce explain in detail how test-driven development and mocking work in the real world.

# Extensions 拓展

Spock提供了一个非常强大的扩展机制，可以连接到一个spec的生命周期，以丰富或者改变它的行为。在这一章里，我们先学习Spock内置的拓展，然后深入了解如何定制自己的拓展。

## Spock配置文件

有的拓展可以通过Spock的配置文件的选项来配置。每个拓展的描述会提醒如何去配置。所有的配置都在一个Groovy文件里，通常起名为`SpockConfig.groovy`。Spock首先会搜索一个自定义位置，这个位置是由系统属性中叫`spock.configuration`给的，然后会用作classpath位置，或者如果没找到，会用作文件系统的位置，如果能够在这里找到的话，否则会调查默认的位置有没有一个配置文件。接下来会在测试执行的classpath的根路径里寻找`SpockConfig.groovy`。如果还是没有这个文件，最后可以在Spock的用户home文件夹下找`SpockConfig.groovy`文件。默认情况下会在home目录下的`.spock`目录里，但是也可以通过系统变量`spock.user.home`改变这个位置，或者通过设置环境变量`SPOCK_USER_HOME`。

### Stack Trace Filtering 栈轨迹过滤

可以使用配置文件配置Spock是否应该过滤栈轨迹。默认值是`true`。

*Stack Trace Filtering Configuration*

```groovy
runner {
  filterStackTrace false
}
```

### Parallel 并行执行设置

```groovy
runner {
  parallel {
    //...
  }
}
```

详情见并行执行一节。

## Built-In Extensions 内置拓展

大多数Spock的内置拓展是注解驱动的。换句话说，他们是通过在spec类或方法上加一个特定注解来触发的。你可以通过他们的元注解`@ExtensionAnnotation`来区分这种注解。

### Ignore

暂时的阻止一个feature方法的执行，可以用`spock.lang.Ignore`来注解这个方法：

```groovy
@Ignore
def "my feature"() { ... }
```

为了文档的目的，可以提供一个原因：

```groovy
@Ignore("TODO")
def "my feature"() { ... }
```

如果要忽略整个spec，在类上加注解：

```groovy
@Ignore
class MySpec extends Specification { ... }
```

在大多数执行环境下，被忽略的feature方法和spec会被报告为“skipped”。

如果要忽略一个被注解了`spock.lang.Stepwise`的feature方法的话，要十分小心，因为后续的feature方法可能会依赖之前已执行的feature方法。

### IgnoreRest

如果想忽略除了某一小部分方法以外的所有方法，在这一部分方法上使用注解`spock.lang.IgnoreRest`：

```groovy
def "I'll be ignored"() { ... }

@IgnoreRest
def "I'll run"() { ... }

def "I'll also be ignored"() { ... }
```

`@IgnoreRest`是在执行环境没法提供一种方便地执行一小部分方法时，非常的有用。

如同`@Ignore`，要特别注意有 `spock.lang.Stepwise` 注解的方法。

### IgnoreIf

在特定情况下忽略一个feature方法或spec。

```groovy
@IgnoreIf({ System.getProperty("os.name").toLowerCase().contains("windows") })
def "I'll run everywhere but on Windows"() {
```

为了让断言更好读也更好写，下面这些变量可以在闭包里使用：

- `sys` 所有系统变量的map
- `env` 所有环境变量的map
- `os` 操作系统的信息 （详见 `spock.util.environment.OperatingSystem`）
- `jvm` JVM的信息（详见 `spock.util.environment.Jvm`）
- `instance` spec的实例，如果需要用到实例字段，共享字段，或者实例方法。如果用了这个属性，整个被注解元素将不能被预先跳过，除非执行fixture，数据提供者，或者其他类似的。相反，整个工作流被feature方法的调用跟进，然后检查闭包，决定是否终止特定的迭代。

使用`os`属性，上面的例子可以写作：

```groovy
@IgnoreIf({ os.windows })
def "I will run everywhere but on Windows"() {
```

如果有多个`@IgnoreIf`注解，他们会以`or`的逻辑组合在一起。只要有一个条件满足，背注解的元素就会被跳过：

```groovy
@IgnoreIf({ os.windows })
@IgnoreIf({ jvm.java8 })
def "I'll run everywhere but on Windows or anywhere on Java 8"() {
```

注意有`spock.lang.Stepwise`注解的方法。

为了更好的使用IDE支持，如代码补全，你也可以在闭包里使用参数，然后将类型指定为``org.spockframework.runtime.extension.builtin.PreconditionContext`。这可以让IDE获取类型信息，这些类型信息在其他情况下是不可用的：

```groovy
@IgnoreIf({ PreconditionContext it -> it.os.windows })
def "I will run everywhere but not on Windows"() {
```

如果用在数据驱动的feature方法上，闭包还可以访问数据变量。如果闭包没有引用任何实际的数据变量，或者应用在spec上，整个带注解的元素会被提前跳过，fixture、数据提供者或者其他的东西不会被执行。但是如果闭包实际上引用了有效的数据变量，整个工作流就会跟踪到feature方法调用上，然后检查闭包，决定是否中止spec迭代。

### Requires

为了在特定条件下执行feature方法，可以用 `spock.lang.Requires`注解方法，后面跟一个断言：

```groovy
@Requires({ os.windows })
def "I'll only run on Windows"() {
```

`Requires`和`IgnoreIf`很像，除了断言是反的。一般来说，最好说明执行方法的条件，而不是忽略方法的条件。

如果存在多个`@Requires`注解，他们会以`and`逻辑组合生效。只有当所有的条件都是`false`的时候，会跳过被注解的元素：

```groovy
@Requires({ os.windows })
@Requires({ jvm.java8 })
def "I'll run only on Windows with Java 8"() {
```

### PendingFeature 待定Feature

为了指示这个feature还没有完全实现，不应该被报告为error。

这个主要是用于注解那些还不能运行但是应该已经提交的测试。这个和`Ignore`的主要区别在于，这个的测试会执行，只是忽略测试失败的情况。如果测试正常通过了，那么就会报告为failure，因为`PendingFeature`注解应该被移除了。这样这些测试就会变成正常的测试，而不会被永远忽略。

Groovy有一个`Groovy.transform.NotYetIntegrated`注解，和这个很像，但是有一点不同：

+ groovy的这个注解会把失败的test标记为通过passed
+ 如果数据驱动测试的某一个迭代通过了，会报告为error

`PendingFeature`:

+ 会标记失败的test位skipped
+ 如果数据驱动的测试的某个迭代失败了，会报告为skipped
+ 如果数据测试的全部迭代都成功了，会报告为error

```groovy
@PendingFeature
def "not implemented yet"() { ... }
```

### PendingFeatureIf

为了有条件的指示一个方法还没有完全实现，不应该被报告为error，你可以使用注解`spock.lang.PendingFeatureIf`，并带上一个和`IgnoreIf`或者`Requires`一样的前提条件。

如果条件满足，那么就会和`PendingFeature`的行为一样，否则什么都不会做。

例如，给一个方法注解了 `@PendingFeatureIf({ false })`的话，什么都不会发生，但是如果注解了`@PendingFeatureIf({ true })` 的话，就和注解了`@PendingFeature`一样。

如果用在数据驱动的feature上，闭包里还可以访问数据变量。如果闭包没有引用任何实际的数据变量，整个feature会被认为是待定的，当所有的迭代都成功的时候会被标记为failing。但是如果闭包实际上引用了有效的数据变量，那么条件成立的那些迭代会被认为是待定的，然后会独立的进行，只要成功被报告为fail。

```groovy
@PendingFeatureIf({ os.windows })
def "I'm not yet implemented on windows, but I am on other operating systems"() {

@PendingFeatureIf({ sys.targetEnvironment == "prod" })
def "This feature isn't deployed out to production yet, and isn't expected to pass"() {
```

还支持有多个`@PendingFeatureIf`注解，或者将`@PendingFeatureIf` 和 `@PendingFeature`混合起来使用，例如只在某些特定条件下忽略某些特定异常。

```groovy
@PendingFeature(exceptions = UnsupportedOperationException)
@PendingFeatureIf(
  exceptions = IllegalArgumentException,
  value = { os.windows },
  reason = 'Does not yet work on Windows')
@PendingFeatureIf(
  exceptions = IllegalAccessException,
  value = { jvm.java8 },
  reason = 'Does not yet work on Java 8')
def "I have various problems in certain situations"() {
```

### Stepwise 逐步

如果希望feature方法按照声明的顺序执行，可以在类上用注解`spock.lang.Stepwise`：

```groovy
@Stepwise
class RunInOrderSpec extends Specification {
  def "I run first"()  { ... }
  def "I run second"() { ... }
}
```

`Stepwise`仅仅影响有这个注解的类，子类和父类不受影响。在第一个失败的feature方法后的方法会被跳过。

`Stepwise` 不会覆盖诸如 `Ignore`、`IgnoreRest` 和 `IgnoreIf`注解的效果，所以在有注解`Stepwize`的spec类里想忽略方法的时候要十分注意。

> NOTE
>
> 这也会让执行模式变成`SAME_THREAD`，详见并行计算一节。

### Timeout 超时

想在feature方法、fixture或者类运行超过给定执行时间时，让其失败，使用`spock.lang.Timeout`注解，带上一个时间，时间单位可选。默认的时间单位是秒。

当用在feature方法上的时候，每一次执行迭代都会判断是否超时，时间不包括fixture方法上的时间：

```groovy
@Timeout(5)
def "I fail if I run for more than five seconds"() { ... }

@Timeout(value = 100, unit = TimeUnit.MILLISECONDS)
def "I better be quick" { ... }
```

把`Timeout`放在spec类上，相当于放在给每一个没有`Timeout`注解的feature方法上，但不包括花在fixture方法里的时间：

```groovy
@Timeout(10)
class TimedSpec extends Specification {
  def "I fail after ten seconds"() { ... }
  def "Me too"() { ... }

  @Timeout(value = 250, unit = MILLISECONDS)
  def "I fail much faster"() { ... }
}
```

当放在fixture方法上时，超时是针对每次这个fixture方法的执行时间。

当给用户报告超时时，将会展示栈轨迹，栈轨迹反映了超时发生时测试框架的执行栈。

### Retry 重试

`@Retry`拓展可以用于脆弱的集成测试，远程系统有时候可能会鼓掌的那种。默认情况下，如果有`Exception`或者`AssertionError`，会0延迟重复一个迭代3次，这都可以配置。此外，可以使用一个可选的`condition`闭包来决定一个feature方法是否要重试。它还对数据驱动测试提供了特殊的支持，可以重试全部的迭代，或者只重试失败的迭代。

```groovy
class FlakyIntegrationSpec extends Specification {
  @Retry
  def retry3Times() { ... }

  @Retry(count = 5)
  def retry5Times() { ... }

  @Retry(exceptions=[IOException])
  def onlyRetryIOException() { ... }

  @Retry(condition = { failure.message.contains('foo') })
  def onlyRetryIfConditionOnFailureHolds() { ... }

  @Retry(condition = { instance.field != null })
  def onlyRetryIfConditionOnInstanceHolds() { ... }

  @Retry
  def retryFailingIterations() {
    ...
    where:
    data << sql.select()
  }

  @Retry(mode = Retry.Mode.FEATURE)
  def retryWholeFeature() {
    ...
    where:
    data << sql.select()
  }

  @Retry(delay = 1000)
  def retryAfter1000MsDelay() { ... }
}
```

重试也可以用在spec类上，和应用在每一个没有注解`@Retry`的feature方法上效果一样。

```groovy
@Retry
class FlakyIntegrationSpec extends Specification {
  def "will be retried with config from class"() {
    ...
  }
  @Retry(count = 5)
  def "will be retried using its own config"() {
    ...
  }
}
```

如果在spec类上使用了注解`Retry`，也会应用在所有的子类的所有feature方法上，除非子类声明了自己的注解。如果子类上有定义注解`Retry`，子类中定义的重试会应用到所有子类的feature方法上，还有继承子类的类里。

看下面这个例子，运行`FooIntegrationSpec`会同时以重试1次执行`inherited`和`foo`。运行`BarIntegrationSpec`则会执行以重试2次执行`inherited`和`foo`。

```groovy
@Retry(count = 1)
abstract class AbstractIntegrationSpec extends Specification {
  def inherited() {
    ...
  }
}

class FooIntegrationSpec extends AbstractIntegrationSpec {
  def foo() {
    ...
  }
}

@Retry(count = 2)
class BarIntegrationSpec extends AbstractIntegrationSpec {
  def bar() {
    ...
  }
}
```

更多例子详见：[RetryFeatureExtensionSpec](https://github.com/spockframework/spock/blob/master/spock-specs/src/test/groovy/org/spockframework/smoke/extension/RetryFeatureExtensionSpec.groovy) 。

### Use

可以用这个注解，在feature范围或spec范围内激活一个或更多的Groovy类别：

```groovy
class ListExtensions {
  static avg(List list) { list.sum() / list.size() }
}

class UseDocSpec extends Specification {
  @Use(ListExtensions)
  def "can use avg() method"() {
    expect:
    [1, 2, 3].avg() == 2
  }
}
```

这对动态方法的stub会非常有用，动态方法通常是在运行时的环境提供的（例如Grails）。当应用于一个helper方法时，这会不起作用。然而，当应用到spec类上时，也会影响它的helper方法。

如果要使用多个类别，也可以在注解的`value`属性里提供多个类别，或者可以在一个目标上标注多个注解。

> NOTE
>
> 如果应用在spec上，这也会让执行模式设置为`SAME_THREAD`。详情查看并行执行一节。

### ConfineMetaClassChanges 限制元类更改

可以在feature范围内或spec类范围内限制元类的更改：

```groovy
@Stepwise
class ConfineMetaClassChangesDocSpec extends Specification {
  @ConfineMetaClassChanges(String)
  def "I run first"() {
    when:
    String.metaClass.someMethod = { delegate }

    then:
    String.metaClass.hasMetaMethod('someMethod')
  }

  def "I run second"() {
    when:
    "Foo".someMethod()

    then:
    thrown(MissingMethodException)
  }
}
```

当应用到spec类上时，元类将恢复到执行`setupSpec`之前的状态，持续到`cleanupSepc`执行后。

当应用到一个feature方法上时，元类会恢复到`setup`执行之后，在`cleanup`执行之前。

要限制多个元类的更改，可以在注解的`value`属性里传入多个类，或者在目标上使用多次本注解。

> **注意CAUTION**
>
> 仅在spec运行在每个JVM上的单线程时，临时修改元类才是安全的。尽管许多执行环境确实限制到了每个JVM单线程，但是牢记Spock并不强制如此。

>NOTE
>
>这会获得一个`Resources.META_CLASS_REGISTRY`的`READ_WRITE`锁，详见并行计算。

### RestoreSystemProperties 重置系统属性

在带有这个注解的方法运行之前（包括任何的setup和cleanup方法）保存一下系统变量，然后在这之后恢复它们。

将这个注解放在spec类上，和把它放在每一个feature方法上效果相同。

```groovy
@RestoreSystemProperties
def "determines family based on os.name system property"() {
  given:
  System.setProperty('os.name', 'Windows 7')

  expect:
  OperatingSystem.current.family == OperatingSystem.Family.WINDOWS
}
```

> **注意CAUTION**
>
> 仅在spec运行在每个JVM上的单线程时，临时修改元类才是安全的。尽管许多执行环境确实限制到了每个JVM单线程，但是牢记Spock并不强制如此。

>NOTE
>
>这会获得一个`Resources.SYSTEM_PROPERTIES`的`READ_WRITE`锁，详见并行计算。

### AutoAttach

自动将一个分离的mock附加到当前的spec上。如果没有直接可用的框架，使用这个。Spring和Guice依赖会分别通过Spring模块和Guice模块自动注入。

### AutoCleanUp

这个注解会自动清理一个字段或属性，在其生存期的最后。

默认情况下，会通过调用一个对象的无参方法`close()`清除对象。如果应该调用其他方法，通过在注解的`value`属性里指定来覆盖：

```groovy
// invoke foo.dispose()
@AutoCleanup("dispose")
def foo
```

如果用`AutoCleanup`注解了多个字段或属性，他们的对象会按与声明相反的顺序进行清理，并从最派生的类开始，沿着继承链向上。

如果一个清理操作失败了，抛出一个异常，默认情况下这个异常会被报告，并且继续清理下一个被注解的对象。可以通过覆写注解的`quiet`属性，从而不报告清理中发生的异常。

```groovy
@AutoCleanup(quiet = true)
def ignoreMyExceptions
```

### TempDir 临时目录

为了给测试生成一个临时的文件夹，并且在测试后删除这个临时文件夹，可以注解一个成员变量，该成员变量可以是类型`java.io.File`或`java.nio.file.Path`或者用`def`定义的无类型的变量（`def`会被注入一个`Path`）。如果被注解的字段是`@Shared`，这个临时文件夹将会在对应的spec内共享，否则每一个feature方法和每一个参数化方法的迭代都会有他们自己的临时文件夹：

```groovy
// all features will share the same temp directory path1
@TempDir
@Shared
Path path1

// all features and iterations will have their own path2
@TempDir
File path2

// will be injected using java.nio.file.Path
@TempDir
def path3

def demo() {
  expect:
  path1 instanceof Path
  path2 instanceof File
  path3 instanceof Path
}
```

如果想为临时文件夹自定义一个父目录，可以使用Spock配置文件。

如果`keep`被设置为了`true`，Spock在测试后将不会删除临时文件夹。默认值会从系统变量`spock.tempDir.keep`里获取，如未设置，为`false`。

*Temporary Directory Configuration*

```groovy
tempdir {
  // java.nio.Path object, default null,
  // which means system property "java.io.tmpdir"
  baseDir Paths.get("/tmp")
  // boolean, default is system property "spock.tempDir.keep"
  keep true
}
```

### 标题和记叙

如果想给spec起一个自然语言的名字，用这个注解：

```groovy
@Title("This is easy to read")
class ThisIsHarderToReadSpec extends Specification {
  ...
}
```

类似的，可以给spec附加一段自然语言的描述，用`spock.lang.Narrative`：

```groovy
@Narrative("""
As a user
I want foo
So that bar
""")
class GiveTheUserFooSpec() { ... }
```

### See

用来链接到1个或多个与spec有关的外部信息引用。

```groovy
@See("http://spockframework.org/spec")
class SeeDocSpec extends Specification {
  @See(["http://en.wikipedia.org/wiki/Levenshtein_distance", "http://www.levenshtein.net/"])
  def "Even more information is available on the feature"() {
    expect: true
  }

  @See("http://www.levenshtein.de/")
  @See(["http://en.wikipedia.org/wiki/Levenshtein_distance", "http://www.levenshtein.net/"])
  def "And even more information is available on the feature"() {
    expect: true
  }
}
```

### Issue 问题

用来指出某个feature或spec与外部跟踪的系统中的一个或多个问题有关。

```groovy
@Issue("http://my.issues.org/FOO-1")
class IssueDocSpec extends Specification {
  @Issue("http://my.issues.org/FOO-2")
  def "Foo should do bar"() {
    expect: true
  }

  @Issue(["http://my.issues.org/FOO-3", "http://my.issues.org/FOO-4"])
  def "I have two related issues"() {
    expect: true
  }

  @Issue(["http://my.issues.org/FOO-5", "http://my.issues.org/FOO-6"])
  @Issue("http://my.issues.org/FOO-7")
  def "I have three related issues"() {
    expect: true
  }
}
```

如果项目里的所有问题都有一个共同的前缀URL，你可以用Spock配置文件来一次性对所有的进行设置。如果设置了，就会在构建URL的时候被添加到`@Issue`注解的值前面。

如果设置了`issueNamePrefix`，就会在构建issue名字的时候加在`@Issue`注解的值的前面。

*Issue Configuration*

```groovy
report {
    issueNamePrefix 'Bug '
    issueUrlPrefix 'http://my.issues.org/'
}
```

### Subject 主题

用来指示spec的一个或多个主题：

```groovy
@Subject([Foo, Bar])
class SubjectDocSpec extends Specification {
```

你也可以一次用多个`@Subject`注解:

```groovy
@Subject(Foo)
@Subject(Bar)
class SubjectDocSpec extends Specification {
```

此外， `Subject`可以用在字段或局部变量上：

```groovy
@Subject
Foo myFoo
```

`Subject`目前只有提供信息的功能。

### Rule 规则

当Spock包含JUnit4模块时，是可以识别非`@Shared`的实例字段上的`@org.junit.Rule`注解的。对应的规则会在Spock生命周期的迭代拦截点处运行。这意味着before-actions规则会在`setup`方法执行前完成，after-actions规则会在`cleanup`方法执行后完成。

### ClassRule 类规则

当Spock包含JUnit4模块时，是可以识别非`@Shared`的实例字段上的`@org.junit.ClassRule`注解的。对应的规则会在Spock生命周期的迭代拦截点处运行。这意味着before-actions规则会在`setupSpec`方法执行前完成，after-actions规则会在`cleanupSpec`方法执行后完成。

### Include and Exclude 包括和排除

Spock可以根据spec的类、父类、接口和spec上的注解来包含和排除spec。Spock还可以根据feature方法上的注解包括和排除单个feature方法。包括什么和排除什么可以通过Spock配置文件来完成。

*Include / Exclude Configuration*

```groovy
import some.pkg.Fast
import some.pkg.IntegrationSpec

runner {
  include Fast // could be either an annotation or a (base) class
  exclude {
    annotation some.pkg.Slow
    baseClass IntegrationSpec
  }
}
```

### Optimize Run Order 优化执行顺序

Spock可以记录上一次哪个feature失败了，连续失败的频率，以及一个feature方法需要多长时间。在连续运行时，Spock会先运行上一次运行失败的feature，并先开始连续运行失败频率更高的。在之前运行失败或没失败的feature里，Spock会运行最快的测试。这个行为可以通过Spock配置文件来开启。默认情况是关闭的。

*Optimize Run Order Configuration*

```groovy
runner {
  optimizeRunOrder true
}
```

## Third-Party Extensions 第三方扩展

你可以在[Spock Wiki](https://github.com/spockframework/spock/wiki/Third-Party-Extensions)找到第三方扩展的列表。

## 自定义扩展

可以给Spock创建2种类型的拓展。全局拓展（global extension）和注解驱动的本地拓展（annotation driven local extension）。对于两种拓展类型，你都是实现了一个特定的接口，这个接口定义了一些回调方法。在你对这些方法的实现里，你可以设置你的拓展的功能，例如对很多拦截点添加拦截器，这些拦截点会在下面介绍。

创建那种类型的拓展取决于你的使用场景。如果你想在Spock的运行中（在开头或结尾）做一些事情，或者想要应用一些东西到所有已经执行的spec上，而不需要拓展的使用者做什么，除了把你的拓展加到classpath以外，那么就应该选择全局拓展。如果你想让拓展仅由用户的选择来应用，就应该实现一个注解驱动的本地扩展。

### 全局扩展

为了创建一个全局扩展，需要创建一个类实现接口`IGlobalExtension`并且把它的全限定类名放在classpath里的`META-INF/services/org.spockframework.runtime.extension.IGlobalExtension`文件里。只要这两个条件满足了，当Spock运行时，这个扩展就会自动被加载和使用。

`IGlobalExtension` 有下面这三个方法：

`start()`
  这个方法将会在Spock执行的非常早期被调用一次。

`visitSpec(SpecInfo spec)`
  每个spec会调用一次这个方法。在这个方法里，你可以准备一个有你的拓展的spec，比如将拦截器附加到拦截器一章所描述的拦截点里。

`stop()`这个方法
  这个方法会在Spock执行结束的非常后期调用至少一次。

### 注解驱动的本地拓展

为了创建一个注解驱动的本地拓展，你需要创建一个类，实现接口`IAnnotationDrivenExtension`。作为接口的类型参数，你需要提供一个注解类，这个注解类需要有`@Rention`注解，并设置为`RUNTIME`；需要有`@Target`注解，设置为`FIELD`、`METHOD`或者`TYPE`里的至少一个，取决于你想把注解用在哪里；需要有`@ExtensionAnnotation`注解，并将`IAnnotationDrivenExtension`作为参数。当然注解类还可以有一些属性，让用户可以更进一步的为每个注解应用程序配置拓展的行为。

你的注解可以用在spec、feature方法、fixture方法或字段上。如果相应的设置了`@Target`，那在其他所有地方，比如说helper方法上，或者其他地方，注解都会被忽略，除了能在源码里看到以外，没有任何效果，除非你自己在其他地方检查它是否存在。

自Spock 2.0起，你的注解也可以定义为`@Repeatable`，可以在一个目标上应用多次。`IAnnotationDrivenExtension`有`visit…Annotations`方法，这个方法会被Spock调用，调用的时候会使用应用在同一个目标上这个拓展所有的注解。它们的默认实现会对每一个注解分别调用一次`visit…Annotation`。如果你想要一个兼容Spock 2.0之前版本的可重复的注解，你需要让容器注解变成一个扩展注解自身，然后处理所有相关的情况，但是你需要确保在Spock 2.0之前只处理容器注解，否则你的注解会被处理2次。注意，可重复注解可以直接放在目标上，可以在容器注解里，或者甚至同时在两者，如果用户手动添加了容器注解，并且直接加了一个注解。

`IAnnotationDrivenExtension`有下面9个方法，在每个方法里，你都可以用你的扩展逻辑准备一个spec，就像将拦截器附加到拦截点上，如拦截器一节所述：

```groovy
visitSpecAnnotations(List<T> annotations, SpecInfo spec)
```

  这个方法每个标注了注解（1个或多个）的spec会调用1次，方法第一个参数是注解的实例，第二个是注解对象。默认的实现对每一个给的注解调用1次`visitSpecAnnotation`。

```groovy
visitSpecAnnotation(T annotation, SpecInfo spec)
```

  这个相当于`visitSpecAnnotations`的单数委托，否则不会直接被Spock直接调用。默认实现会抛出一个异常。

```groovy
visitFieldAnnotations(List<T> annotations, FieldInfo field)
```

  这个方法对于每个标注了注解（1个或多个）的字段调用一次，注解实例是第一个参数，字段是第二个参数。默认实现会对每一个给的注解调用一次`visitFieldAnnotation`。

```groovy
visitFieldAnnotation(T annotation, FieldInfo field)
```

  这个相当于`visitFieldAnnotations`的单数委托，否则不会直接被Spock直接调用。默认实现会抛出一个异常。

```groovy
visitFixtureAnnotations(List<T> annotations, MethodInfo fixtureMethod)
```

  这个方法对于每个标注了注解（1个或多个）的fixture方法调用一次，注解实例是第一个参数，fixture方法信息是第二个参数。默认实现会对每一个给的注解调用一次`visitFixtureAnnotation`。

```groovy
visitFixtureAnnotation(T annotation, MethodInfo fixtureMethod)
```

  这个相当于`visitFixtureAnnotations`的单数委托，否则不会直接被Spock直接调用。默认实现会抛出一个异常。

```groovy
visitFeatureAnnotations(List<T> annotations, FeatureInfo feature)
```

  这个方法对于每个标注了注解（1个或多个）的feature方法调用一次，注解实例是第一个参数，feature方法信息是第二个参数。默认实现会对每一个给的注解调用一次`visitFeatureAnnotation`。

```groovy
visitFeatureAnnotation(T annotation, FeatureInfo feature)
```

  这个相当于`visitFeatureAnnotations`的单数委托，否则不会直接被Spock直接调用。默认实现会抛出一个异常。

```groovy
visitSpec(SpecInfo spec)
```

  这个方法会对每一个应用了注解的spec调用一次，注解至少一个，并且在之前定义的支持位置里。它只有一个参数，specInfo。这个方法在处理完每一个应用的注解的接口中全部方法后调用。

### 配置对象

你可以在Spock配置文件里添加自己的section，为你的拓展，通过创建注解了`@ConfigurationObject`的，且有一个默认构造方法（隐式和显式均可）的POJO或POGO。这个注解的参数是要加入到Spock配置文件的最顶层section的名字。这个配置项的默认值是在class里定义的，通过在声明时初始化字段，或者在构造器里。在Spock配置文件里的那些值之后可以由你拓展的用户来编辑。

> NOTE
>
> 不可以有多个配置对象起同样的名字，所以一个明智的选择是起一个或者是加一个前缀，像包名那样的名字，来最小化和其他拓展或Spock核心代码命名冲突的风险。

为了在你的拓展里使用配置对象的值，你可以使用构造器注入或者字段注入：

+ 使用构造器注入的话，只需要定义一个构造器，有一个或更多配置对象作为参数。
+ 使用字段注入的话，只需要定义一个未初始化的，非final的这个类型的成员变量。

Spock然后会为每一个Spock运行，自动创建刚好一个配置对象的实例，并且应用从配置文件获取到的设置（在全局拓展的`start()`方法调用之前），然后把这个实例注入的拓展类的实例里。

> NOTE
>
> 构造器注入的优先级要比字段注入的优先级高，并且Spock如果发现了有合适的构造器，就不会再注入字段了。如果你想同时支持Spock 1.x和2.x，你可以只使用字段注入（Spock 1.x只支持字段注入），或者你可以同时也一个默认构造器和一个注入构造器，这样Spock 2.x就会使用构造器注入，Spock 1.x会使用字段注入。

如果一个配置对象应该被专门用于一个注解驱动的本地拓展，你必须把它注册到`INF/services/spock.config.ConfigurationObject`。这和全局拓展有点像，将注解的全限定类名放在这个文件里的一行。
如果配置对象应该专门用于注释驱动的本地扩展，那么必须在 META-INF/services/spock.config 中注册它。ConfigurationObject.这类似于全局扩展，将带注释类的完全限定类名放在文件中的新行上。这可以让配置对象正确地被初始化，并且用配置文件里的设置填充。然而，如果配置对象是用于全局拓展的，你也可以在一个注解驱动的本地拓展里使用它。如果一个配置对象只是用于一个注解驱动的本地拓展，当注入注解对象到拓展的时候，你会得到一个错误，并且你也会得到一个错误，当包括这个section 的注解文件被计算时，因为配置对象还没有正确注册。

### Interceptors 拦截器

为了应用你拓展的效果，有很多拦截点，你可以通过上面描述的拓展方法来附加拦截器，来连接到Spock的生命周期。对于每一个拦截点，当然可以加多个拦截器，通过任意的Spock拓展（装载的或者第三方）。他们的顺序目前依赖于添加的顺序，但是在一个拦截点内，不应该有任何顺序假设。

![Spock Interceptors](https://gitee.com/chLemon/pictures/raw/master/Picsee/spock_interceptorsCXNidP.png)

图1，Spock拦截器

图中的省略号，表示前面的块可以重复人一次。

`… method interceptors`当然只运行在实际有这个类型的方法要执行（白色的块），并且他们可以注入参数到这些要运行的方法里。

共享初始化拦截器和共享初始化方法拦截器之间的区别，和初始化拦截器和初始化方法拦截器之间的区别（每次最多只能有一个这里面的方法）是，如果有`@Shared`或者是non-`@Shared`，只有2个方法的字段可以在声明的时候获得赋值。编译器会把这些初始化放进一个生成的方法里，并且在生命周期里合适的地方调用它。所以如果没有这些初始化，没有方法会被生成，因为方法拦截器永远不会被调用。非方法拦截器永远会被调用，在生命周期里合适的地方，以完成当时必须完成的工作。

要创建一个附加到拦截点的拦截器，你需要创建一个类，这个类要实现`IMethodInterceptor`接口。这个接口只有一个方法`intercept(IMethodInvocation invocation)`。`invocation`参数用来获取和修改拓展的当前状态。每一个拦截器**必须**调用方法`invocation.proceed()`，这个方法会继续生命周期，除非你真的想阻止进一步的嵌套元素的执行，嵌套元素就是上图展现的哪些。但是这种用法非常罕见。

如果你写了一个拦截器，可以用到不同的拦截点上，并且应该在不同的拦截点上做不同的工作，有一个方便的类`AbstractMethodInterceptor`，你可以继承这个类，这个类提供了大量的方法可以覆写，这些方法会在不同的拦截点被调用。这些方法中大部分都有双重含义，例如`interceptSetupMethod`在`setup interceptor`和`setup method interceptor`被调用。如果你把你的拦截器附加到这两个上，并且需要一个区分，你可以检查一下`invocation.method.reflection`，这个在方法拦截器里被设置，否则为`null`。当然你也可以构建两个不同的拦截器或者给你的拦截器添加一个参数，然后创建2个实例，告诉他们它应该被附加到方法拦截器上，还是另一个。

*Add All Interceptors*

```groovy
class I extends AbstractMethodInterceptor { I(def s) {} }

// On SpecInfo
specInfo.addSharedInitializerInterceptor new I('shared initializer')
specInfo.sharedInitializerMethod?.addInterceptor new I('shared initializer method')
specInfo.addInterceptor new I('specification')
specInfo.addSetupSpecInterceptor new I('setup spec')
specInfo.setupSpecMethods*.addInterceptor new I('setup spec method')
specInfo.allFeatures*.addInterceptor new I('feature')
specInfo.addInitializerInterceptor new I('initializer')
specInfo.initializerMethod?.addInterceptor new I('initializer method')
specInfo.allFeatures*.addIterationInterceptor new I('iteration')
specInfo.addSetupInterceptor new I('setup')
specInfo.setupMethods*.addInterceptor new I('setup method')
specInfo.allFeatures*.featureMethod*.addInterceptor new I('feature method')
specInfo.addCleanupInterceptor new I('cleanup')
specInfo.cleanupMethods*.addInterceptor new I('cleanup method')
specInfo.addCleanupSpecInterceptor new I('cleanup spec')
specInfo.cleanupSpecMethods*.addInterceptor new I('cleanup spec method')
specInfo.allFixtureMethods*.addInterceptor new I('fixture method')

// on FeatureInfo
featureInfo.addInterceptor new I('feature')
featureInfo.addIterationInterceptor new I('iteration')
featureInfo.featureMethod.addInterceptor new I('feature method')
```

#### 注入方法参数

如果你的拦截器应该为包装方法支持自定义方法参数，可以通过修改`invocation.arguments`完成。有两种使用情况，可能是有一个mock框架，这个框架可以注入方法参数，这些参数是由一个特殊注解注解的；或者有的测试helper，要注入一个特殊类型的对象，这个类型是自动创建并准备使用的。

当从Spock 2.0开始，`arguments`数组将会永远有方法参数数量的大小，所以你可以直接设置你想设置的参数。你不能改变`arguments`数组的大小。所有的还没有被注入任何值的参数，无论是从数据变量或者一些拓展注入，将会有值`MethodInfo.MISSING_ARGUMENT`，如果有谁一直是这样，那么在所有拦截器执行完成了，会抛出一个异常。

>NOTE
>
>当你的拓展可能和Spock 2.0之前的版本一起使用时，`arguments`数组可能会是一个空数组或者任意长度的数组，取决于哪个拦截器在这之前运行了，之前运行的拦截器可能也对这个数组进行了操作，进行了参数注入。例如，如果你使用`invocation.method.reflection.parameters`调查了方法参数，发现你想注入第5个参数，你应该首先确认`arguments`数组至少有5个元素长。如果没有，你应该赋值给它一个至少有5个元素长的新数组，然后把就数组的值复制到新数组里。然后你就可以指定要注入的对象了。
>
>*Inject Method Parameters*
>
>```groovy
>// create a map of all MyInjectable parameters with their parameter index
>Map<Parameter, Integer> parameters = [:]
>invocation.method.reflection.parameters.eachWithIndex { parameter, i ->
>  parameters << [(parameter): i]
>}
>parameters = parameters.findAll { MyInjectable.equals it.key.type }
>
>// enlarge arguments array if necessary
>def lastMyInjectableParameterIndex = parameters*.value.max()
>lastMyInjectableParameterIndex = lastMyInjectableParameterIndex == null ?
>                                 0 :
>                                 lastMyInjectableParameterIndex + 1
>if(invocation.arguments.length < lastMyInjectableParameterIndex) {
>  def newArguments = new Object[lastMyInjectableParameterIndex]
>  System.arraycopy invocation.arguments, 0, newArguments, 0, invocation.arguments.length
>  invocation.arguments = newArguments
>}
>
>parameters.each { parameter, i ->
>  invocation.arguments[i] = new MyInjectable(parameter)
>}
>```

> NOTE
>
> 仅Spock 2.0之前：
>
> 当使用数据驱动feature（有`where`block的方法）时，你的拓展的用户不得不遵守一些限制，如果参数应该通过你的拓展注入：
>
> + 所有的数据变量和所有要被注入的参数必须定义为方法参数
> + 所有的方法参数必须在`where`block里赋值，例如`null`
> + 方法参数的顺序必须和`where`block里数据变量的顺序一致。
>
> 当然，你也可以让你的拓展仅仅注入一个值，如果已经设置为了none，因为`where`block赋值发生在方法拦截器被调用之前
>
> 为此，只需要简单的检查`invocation.arguments[i]`是否为`null`
>
> *Data Driven Feature with Injected Parameter pre Spock 2.0*
>
> ```groovy
> def 'test parameter injection'(a, b, MyInjectable myInjectable) {
>   expect: myInjectable
> 
>   where:
>   a    | b
>   'a1' | 'b1'
>   'a2' | 'b2'
> 
>   and:
>   myInjectable = null
> }
> ```
>
> *Data Driven Feature with Injected Parameter post Spock 2.0*
>
> ```groovy
> def 'test parameter injection'(MyInjectable myInjectable) {
>   expect: myInjectable
> 
>   where:
>   a    | b
>   'a1' | 'b1'
>   'a2' | 'b2'
> }
> ```

# Utilities 多功能

## 使用`MutableClock`测试时间（可变时钟）

当处理日期或时间时，我们经常遇到编写稳定测试的问题。Java只支持`FixedClock`来测试。然而，通常与时间相关的代码需要处理随时间变化的情况，所以一个固定的失宠不足以支持，会让测试难以遵循。

同时使用`FixedClock`和Spock的`MutableClock`的前提条件是产品代码，实际上使用了一个可配置的`Clock`，而不仅仅是无参数的`Instant.now()`或者与其他在`java.time.*`类里的对应方法。

### 例子

*Class under Test*

```groovy
public class AgeFilter implements Predicate<LocalDate> {
  private final Clock clock;
  private final int age;

  public AgeFilter(Clock clock, int age) {                                       // (1)
    this.clock = clock;
    this.age = age;
  }

  @Override
  public boolean test(LocalDate date) {
    return Period.between(date, LocalDate.now(clock)).getYears() >= age;         // (2)
  }
}
```

1. `Clock`通过构造函数注入
2. `Clock`用来获取当前的日期

*Test*

```groovy
  def "AgeFilter reacts to time"() {
    given:
    ZonedDateTime defaultTime = ZonedDateTime.of(2018, 6, 5, 0, 0, 0, 0, ZoneId.of('UTC'))
    MutableClock clock = new MutableClock(defaultTime)                                       // (1)
    AgeFilter ageFilter = new AgeFilter(clock,18)                                            // (2)

    LocalDate birthday = defaultTime.minusYears(18).plusDays(1).toLocalDate()

    expect:
    !ageFilter.test(birthday)                                                                // (3)

    when:
    clock + Duration.ofDays(1)                                                               // (4)

    then:
    ageFilter.test(birthday)                                                                 // (5)
  }
}
```

1. `MutableClock`是用众所周知的时间创建的（created with a well known time）
2. `Clock`是通过构造函数注入的
3. `age`小于 `18`所以结果是`false`
4. 时间提前了一天
5. `age`等于 `18`所以结果是`true`

还有很多修改`MutableClock`的方法，只需要看一下JavaDocs，或者测试代码`spock.util.time。MutableClockSpec`。

# Parallel Execution 并行执行

> WARNING
>
> 这是 Spock 的一个实验特性，它基于 JUnit 平台中并行执行的实验性实现。

并行执行有可能减少整个测试执行时间。实际减少多少时间在很大程度上取决于各自的代码基，并可能有很大的变化。

默认情况下，Spock 使用单个线程顺序运行测试。从2.0版开始，Spock 支持基于 JUnit 平台的并行执行。若要启用并行执行，请将 `runner.allel.enable`配置设置为`true`。有关此文件的一般信息，请参见 Spock 配置文件一节。

*SpockConfig.groovy*

```groovy
runner {
  parallel {
    enabled true
  }
}
```

> NOTE
>
> JUnit Jupiter也支持并行执行，两者都依赖于 JUnit 平台的实现，但是功能相互独立。如果你在 Spock 中启用并行执行，它不会影响Jupiter，反之亦然。JUnit 平台按顺序执行测试引擎(Spock，Jupiter) ，所以引擎之间不应该有任何干扰。

## Execution modes 执行模式

Spock支持两种执行模式：`SAME_THREAD` 和 `CONCURRENT`。可以通过`@Execution`注解显式地为spec或feature定义执行模式。否则，Spock 将分别使用`defaultSpeciationExectionMode`和 `defaultExectionMode`的值，它们都将 `CONCURRENT`作为默认值。某些扩展在应用时还会设置执行模式。

- `defaultSpecificationExecutionMode` 控制一个spec默认使用什么执行模式
- `defaultExecutionMode`控制feature方法和迭代默认使用说明执行模式

![sequential sequential execution](https://spockframework.org/spock/docs/2.0/images/sequential-sequential-execution.svg)

*Figure 2. Sequential Execution, either* `runner.parallel.enabled=false` *or* `SAME_THREAD` *Specifications,* `SAME_THREAD` *Features*

![concurrent concurrent execution](https://spockframework.org/spock/docs/2.0/images/concurrent-concurrent-execution.svg)

*Figure 3.* `CONCURRENT` *Specifications,* `CONCURRENT` *Features*

![concurrent sequential execution](https://spockframework.org/spock/docs/2.0/images/concurrent-sequential-execution.svg)

*Figure 4.* `CONCURRENT` *Specifications,* `SAME_THREAD` *Features*

![sequential concurrent execution](https://spockframework.org/spock/docs/2.0/images/sequential-concurrent-execution.svg)

*Figure 5.* `SAME_THREAD` *Specifications,* `CONCURRENT` *Features*

### Execution Hierarchy 执行层级

![wbs legend](https://spockframework.org/spock/docs/2.0/images/wbs-legend.svg)

*Figure 6. Legend for the following figures*

- 节点`Same Thread`会和他的父结点运行同一个线程
- 节点`Concurrent`会在另一个线程里执行，所有的concurrent节点可以分处不同的节点上执行
- 节点`ResourceLock(READ)`会在另一个线程上执行，但是需要一个资源的`READ`锁。
- 节点`ResourceLock(READ_WRITE)`会在另一个线程上执行，但是需要一个资源的`READ_WRITE`锁。
- 节点`Same Thread with Lock`会在和父结点同一个线程上执行，从而继承锁
- 节点`Data Driven Feature`表示是一个数据驱动的feature，其中`Data Driven Feature[1]`和 `Data Driven Feature[2]`是迭代。
- 节点`Isolated`会独立运行，没有其他spec或feature和它同时运行。

![execution hierarchy same thread](https://spockframework.org/spock/docs/2.0/images/execution-hierarchy-same-thread.svg)

*Figure 7. Single threaded execution*

图7展示了当并行执行关闭时（`runner.parallel.enabled=false`）的默认情况，也是spec（`defaultSpecificationExecutionMode`）和feature（`defaultExecutionMode`）都设置为`SAME_THREAD`时的默认情况。

![execution hierarchy concurrent sequential execution](https://spockframework.org/spock/docs/2.0/images/execution-hierarchy-concurrent-sequential-execution.svg)

Figure 8. Execution with `CONCURRENT` Specifications, `SAME_THREAD`

图8展示了设置为`defaultSpecificationExecutionMode=CONCURRENT`和 `defaultExecutionMode=SAME_THREAD`的结果，spec会同时运行，但是feature会和他们的spec运行在同一个线程里。

![execution hierarchy sequential concurrent execution](https://spockframework.org/spock/docs/2.0/images/execution-hierarchy-sequential-concurrent-execution.svg)

Figure 9. Execution with `SAME_THREAD` Specifications, `CONCURRENT` Features

图9展示了设置为`defaultSpecificationExecutionMode=SAME_THREAD` 和`defaultExecutionMode=CONCURRENT`的结果，spec会在同一个线程里运行，导致他们会一个一个裕兴。spec里的feature会并行运行。

![execution hierarchy concurrent concurrent execution](https://spockframework.org/spock/docs/2.0/images/execution-hierarchy-concurrent-concurrent-execution.svg)

Figure 10. Execution with `CONCURRENT` Specifications, `CONCURRENT` Features

图10展示了设置为`defaultSpecificationExecutionMode=CONCURRENT` 和`defaultExecutionMode=CONCURRENT`的记过，spec和feature都会并行运行。

### Execution Mode Inheritance 执行模式的继承关系

如果没有显式的配置任何东西，spec会使用 `defaultSpecificationExecutionMode` ，feature会使用`defaultExecutionMode`。然而，当通过 `@Execution`显式的设置执行模式后，就会改变。每一个节点（spec，feature）首先会检查它是否有被设置一个显式的执行模式，如果没有回检查它的父类有没有一个显式的设置，否则回到各自的默认值。

下面这个例子设置为`defaultSpecificationExecutionMode=SAME_THREAD` 和`defaultExecutionMode=SAME_THREAD`。如果你改变`SAME_THREAD` 和 `CONCURRENT` 的值为相反的值，你就会得到相反的结果。

![execution hierarchy inheritance feature execution](https://spockframework.org/spock/docs/2.0/images/execution-hierarchy-inheritance-feature-execution.svg)

Figure 11. Execution with `SAME_THREAD` Specifications, `SAME_THREAD` Features and explicit `@Execution` on Features

在图11里，`@Execution`被应用在了feature上，这些feature和它们的迭代将会并行执行，而其余的会在同一个线程里执行。

![execution hierarchy inheritance spec execution](https://spockframework.org/spock/docs/2.0/images/execution-hierarchy-inheritance-spec-execution.svg)

Figure 12. Execution with `SAME_THREAD` Specifications, `SAME_THREAD` Features and explicit `@Execution` on a Specification

在图12里，`@Execution`放在了一个spec上，这个spec和它的所有feature都会并行执行。feature并行执行是因为他们从spec里继承了显式的执行模式。

![execution hierarchy inheritance spec feature execution](https://spockframework.org/spock/docs/2.0/images/execution-hierarchy-inheritance-spec-feature-execution.svg)

Figure 13. Execution with `SAME_THREAD` Specifications, `SAME_THREAD` Features and explicit `@Execution` on Features and Specifications

图13展示了混合应用 `@Execution`的情况，在一个spec上和部分它的feature上。通过上一个例子，spec和它的feature会并行执行，除了`testB1`，因为他设置了自己的显式执行模式。

## Resource Locks 资源锁

并行测试给测试带来了新的挑战，因为共享状态可以被多个测试同时修改和使用。

举一个简单的例子，使用同一个系统属性的两个feature，每一个都在各自的`given`block里把它设置为特定值，然后执行代码来测试预期的行为。如果他们按顺序运行，两个都没有问题。然而，如果`given`block同时都在`when`block之前运行了，一个feature就会失败，因为系统变量不包含预期的值。

如果这两个方法都是同一个spec的一部分，那么这个例子解决起来很容易，只需要用 `@Execution(SAME_THREAD)`，设置为让他们在同一个线程运行即可。但是如果feature在独立的spec里，这样就不行了。为了解决这个问题，Spock支持通过`@ResourceLock`来协调对共享资源的访问。

通过使用 `@ResourceLock`，你可以同时定义一个`key` 和一个`mode`。默认情况下，`@ResourceLock`假设为`ResourceAccessMode.READ_WRITE`，但是你可以将其弱化为`ResourceAccessMode.READ`。

- `ResourceAccessMode.READ_WRITE`将强制对资源进行独占访问。
- `ResourceAccessMode.READ`将组织任何的`READ_WRITE`锁，但是会允许其他的`READ`锁。

只读锁（`READ`-only lock）将测试与其他修改共享资源的测试隔离开，在同一事件只允许其他读这个资源的测试执行。当你只有一个`READ`锁的时候，你不应该修改资源，否则保证就不成立。

某些拓展在应用时也会隐式的设置锁。

![lock contention basics](https://spockframework.org/spock/docs/2.0/images/lock-contention-basics.svg)

Figure 14. Two features with `@ResourceLock`

### Lock inheritance 锁的继承

如果一个父节点有一个`READ_WRITE`锁，则会强制子节点在同一个线程里运行。由于`READ_WRITE`锁无论如何都会导致串行执行，这实际上和直接应用到每一个子节点上没有什么不同。然而，如果父节点只有`READ`锁，那么它允许子节点并行执行。

![lock inherit iterate feature](https://spockframework.org/spock/docs/2.0/images/lock-inherit-iterate-feature.svg)

Figure 15. Locks on data driven features

![lock inherit spec](https://spockframework.org/spock/docs/2.0/images/lock-inherit-spec.svg)

Figure 16. Locks on spec inherited by features

### Lock coarsening 锁的粗化

为了避免死锁，当spec和feature都定义了锁的时候，Spock会把锁提升到spec。spec就会有所有定义的锁，如果feature同时有一个资源的`READ_WRITE`和 `READ`锁，`READ`锁会合并到`READ_WRITE`锁里。

![lock coarsening before](https://spockframework.org/spock/docs/2.0/images/lock-coarsening-before.svg)

Figure 17. Lock coarsening - before

![lock coarsening after](https://spockframework.org/spock/docs/2.0/images/lock-coarsening-after.svg)

Figure 18. Lock coarsening - after

### Isolated Execution 单独执行

有时候，你想修改和测试一些会影响到所有feature的东西，你可以在*每一个*特性上都加上`READ`和`@ResourceLock`，但是这是不切实际的。`@Isolated`拓展可以强制只让这个feature运行，其他feature不会同时运行。你可以把它看作是一个隐式全局锁。

与其他锁一样，一个`@Isolated`的spec里的方法会以`SAME_THREAD`模式运行。`@Isolated`仅可以放在spec上，如果你有一个很大的spec，然后只需要一部分feature，你可以考虑把spec拆分，分成需要单独运行的和不需要的。

![isolated](https://spockframework.org/spock/docs/2.0/images/isolated.svg)

Figure 19. `@Isolated` execution

## Parallel Thread Pool 并行线程池
(https://spockframework.org/spock/docs/2.0/all_in_one.html#parallel-thread-pool)

当启用并行执行后，spec和feature可以同时执行。你可以控制执行这些feature的线程池的大小。Spock使用`Runtime.getRuntime().availableProcessors()`来决定可用的处理器。

- `dynamic(BigDecimal factor)` - 根据可用的处理器的数量乘上`factor`来计算所需要的并行数，会四舍五入到最近的整数。例如，factor是`0.5`的话，会使用你一半的处理器。 
- `dynamicWithReservedProcessors(BigDecimal factor, int reservedProcessors)` - 和`dynamic`一样，但是确保了给定的`reservedProcessors`数量的处理器不会被使用。`reservedProcessors`是根据可用的核来计算的，不仅仅是factor的结果。
- `fixed(int parallelism)` - 使用给定数量的线程。
- `custom(int parallelism, int minimumRunnable, int maxPoolSize, int corePoolSize, int keepAliveSeconds)` - 允许对线程池进行完全控制。然而，应该只在其他选项不足时，并且需要一点额外的控制时，使用这个。参阅`spock.config.ParallelConfiguration`的JavaDoc获取详细参数的描述信息。

在默认情况下，Spock使用 `dynamicWithReservedProcessors(1.0, 2)`，即你的所有逻辑处理器减2。

如果算出来的并行度小于2，那么Spock会单线程执行，基本上和设置为`runner.parallel.enabled=false`相同。

*Example SpockConfig.groovy with `fixed` setting*

```groovy
runner {
  parallel {
    enabled true
    fixed(4)
  }
}
```

# Modules 模块

本章包括 Junit4 Module、Guice Module、Spring Module、Tapestry Module、Unitils Module、Grails Module。这里只翻译Spring Module，其余请参加原文档。

## Spring Module


Spring module支持集成[Spring TestContext Framework](https://docs.spring.io/spring/docs/4.1.5.RELEASE/spring-framework-reference/html/testing.html#testcontext-framework)。它还支持Spring注解`@ContextConfiguration`和 `@ContextHierarchy`。此外，它还支持元注解`@BootstrapWith`，所以任何注解了`@BootstrapWith`的注解都可以运行，比如`@SpringBootTest`、`@WebMvcTest`。

### Mocks

Spock 1.1 引入了`DetachedMockFactory`和`SpockMockFactoryBean`，允许在spec之外创建Spock mock。

> NOTE
>
> 虽然mock可以在spec之外创建，但是只能在spec范围内正确运行。所有用到他们的交互，除非附加到一个spec上，否则只会以默认行为处理，不会被记录。此外，，mock只能被附加到一个spec实例上，所以在使用多线程执行的时候要记住这一点。

#### Java Config

```groovy
class DetachedJavaConfig {
  def mockFactory = new DetachedMockFactory()

  @Bean
  GreeterService serviceMock() {
    return mockFactory.Mock(GreeterService)
  }

  @Bean
  GreeterService serviceStub() {
    return mockFactory.Stub(GreeterService)
  }

  @Bean
  GreeterService serviceSpy() {
    return mockFactory.Spy(GreeterServiceImpl)
  }

  @Bean
  FactoryBean<GreeterService> alternativeMock() {
    return new SpockMockFactoryBean(GreeterService)
  }
}
```

#### XML

Spock支持Spring的命名空间，所以如果你用`xmlns:spock="http://www.spockframework.org/spring"`声明了spock命名空间，你可以访问到创建mock的一些方便的方法。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:spock="http://www.spockframework.org/spring"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
           http://www.springframework.org/schema/beans/spring-beans.xsd
           http://www.spockframework.org/spring http://www.spockframework.org/spring/spock.xsd">

  <spock:mock id="serviceMock" class="org.spockframework.spring.docs.GreeterService"/>   (1)
  <spock:stub id="serviceStub" class="org.spockframework.spring.docs.GreeterService"/>   (2)
  <spock:spy id="serviceSpy" class="org.spockframework.spring.docs.GreeterServiceImpl"/> (3)

  <bean id="someExistingBean" class="java.util.ArrayList"/>                              (4)
  <spock:wrapWithSpy ref="someExistingBean"/>                                            (4)

  <bean id="alternativeMock" class="org.spockframework.spring.xml.SpockMockFactoryBean"> (5)
    <constructor-arg value="org.spockframework.spring.docs.GreeterService"/>
    <property name="mockNature" value="MOCK"/>                                           (6)
  </bean>


</beans>
```

1. 创建`Mock`
2. 创建`Stub`
3. 创建`Spy`
4. 使用`Spy`包装一个现有的bean。如果没有找到引用的bean，将会很快失败。
5. 如果你不想使用特定的命名空间支持，可以通过`SpockMockFactoryBean`创建bean
6. `mockNature`可以是`MOCK`、`STUB`或者`SPY`，如果没有声明，默认值为`MOCK`。

#### Usage

要使用mock，只需要像其他bean一样注入它们，然后和平常一样配置它们。

```groovy
@Autowired @Named('serviceMock')
GreeterService serviceMock

@Autowired @Named('serviceStub')
GreeterService serviceStub

@Autowired @Named('serviceSpy')
GreeterService serviceSpy

@Autowired @Named('alternativeMock')
GreeterService alternativeMock

def "mock service"() {
  when:
  def result = serviceMock.greeting

  then:
  result == 'mock me'
  1 * serviceMock.getGreeting() >> 'mock me'
}

def "sub service"() {
  given:
  serviceStub.getGreeting() >> 'stub me'

  expect:
  serviceStub.greeting == 'stub me'
}

def "spy service"() {
  when:
  def result = serviceSpy.greeting

  then:
  result == 'Hello World'
  1 * serviceSpy.getGreeting()
}

def "alternative mock service"() {
  when:
  def result = alternativeMock.greeting

  then:
  result == 'mock me'
  1 * alternativeMock.getGreeting() >> 'mock me'
}
```

#### Annotation driven 注解驱动


Spock 1.2 增加了从`Specification`到`ApplicationContext`导出mock的支持。这是受到Spring Boot的`@MockBean`（通过Mockito实现）的启发，但是适应了Spock风格。它不需要任何Spring Boot的依赖，然而它需要Spring Framework 4.3.5或更高版本才能运行。

##### Using `@SpringBean`

在测试的上下文里，将mock/stub/spy注册为spring bean。

要使用`@SpringBean`，你必须使用强类型的字段，`def`和`Object`不行。你也需要直接将`Mock`/`Stub`/`Spy`赋值到字段里，使用Spock的标准语法。你可以甚至使用初始化块来定义一般行为，然而他们只会在附加到一个spec后才能被拾取（pick up）。

`@SpringBean`的定义可以替换为你的`ApplicationContext`里的存在的bean。

> NOTE
>
> Spock的`SpringBean`实际上在`ApplicationContext`里创建了一个代理，它将所有东西转发给当前mock实例。代理的类型取决于被注解的字段的类型。代理在setup阶段，将自己附加到当前mock，这就是为什么在字段初始化的时候，mock必须已经被创建好。

```groovy
@SpringBean
Service1 service1 = Mock()

@SpringBean
Service2 service2 = Stub() {
  generateQuickBrownFox() >> "blubb"
}

def "injection with stubbing works"() {
  expect:
  service2.generateQuickBrownFox() == "blubb"
}

def "mocking works was well"() {
  when:
  def result = service1.generateString()

  then:
  result == "Foo"
  1 * service1.generateString() >> "Foo"
}
```

> CAUTION
>
> 和Spring自己的`@MockBean`一样，这会修改你的`ApplicationContext`，并且为你的spec创建一个独一无二的上下文，防止它被Spring的[Context Caching](https://docs.spring.io/spring/docs/current/spring-framework-reference/testing.html#testcontext-ctx-management-caching)在当前spec外重复使用。如果你在用一个小的上下文，那么没什么关系，但是如果是一个很大的上下文，你可能想要使用其他方法，例如，用`DetachedMockFactory`。 

##### Using `@SpringSpy`

如果你想监视一个已经存在的bean，你可以使用`@SpringSpy`注解来把这个bean包装到一个spy里。与`@SpringBean`一样，这个字段必须是你想要spy的类型，但是你不能使用初始化程序。

```groovy
@SpringSpy
Service2 service2

@Autowired
Service1 service1

def "default implementation is used"() {
  expect:
  service1.generateString() == "The quick brown fox jumps over the lazy dog."
}

def "mocking works was well"() {
  when:
  def result = service1.generateString()

  then:
  result == "Foo"
  1 * service2.generateQuickBrownFox() >> "Foo"
}
```

##### Using `@StubBeans`

`@StubBeans`在`ApplicationContext`里注册一个普通的 `Stub`实例。如果你只是需要满足某些依赖，实际上不需要用这些stub做任何事情，就用这个。如果你需要控制这些stub，例如，配置他们的返回值，那么就用`@SpringBean`。像`@SpringBean`和`@StubBeans` 也替换了现有的BeanDefinitions，所以你可以用它将ApplicationContext里的真正的bean删除。可以用`@SpringBean`替换`@StubBeans`，如果你需要替换父类中定义的一些`@StubBeans`时，这会很有用。

```groovy
@StubBeans(Service2)
@ContextConfiguration(classes = DemoMockContext)
class StubBeansExamples extends Specification {
```

#### Spring Boot

在`@WebMvcTest`或者其他`SpringBootTest`风格的测试中，使用Spock mock的推荐方式是，使用上述的`@SpringBean`和`@SpringSpy`注解。

或者，你也可以使用一个由`@TestConfiguration`注解的嵌入式配置，来使用`DetachedMockFactory`创建mock。

```groovy
@WebMvcTest
class WebMvcTestIntegrationSpec extends Specification {

  @Autowired
  MockMvc mvc

  @Autowired
  HelloWorldService helloWorldService

  def "spring context loads for web mvc slice"() {
    given:
    helloWorldService.getHelloMessage() >> 'hello world'

    expect: "controller is available"
    mvc.perform(MockMvcRequestBuilders.get("/"))
      .andExpect(status().isOk())
      .andExpect(content().string("hello world"))
  }

  @TestConfiguration
  static class MockConfig {
    def detachedMockFactory = new DetachedMockFactory()

    @Bean
    HelloWorldService helloWorldService() {
      return detachedMockFactory.Stub(HelloWorldService)
    }
  }
}
```

更多例子请参见[codebase](https://github.com/spockframework/spock/tree/master/spock-spring/src/test/groovy/org/spockframework/spring) 和 [boot examples](https://github.com/spockframework/spock/tree/master/spock-spring/boot-test/src/test/groovy/org/spockframework/boot)里的spec。

### Scopes

Spock默认情况下会忽视不是`singleton`的bean（在`singletom`范围内）。要想使mock可以用于范围的bean，你需要在spec里添加`@ScanScopedBeans` ，并且确保这个范围在setup阶段允许访问bean。

> NOTE
>
> 如果没有活动的request或session，`request`和`session`范围（scope）默认会抛出异常。

可以使用`@ScanScopedBeans`的`value`属性将扫描限定在某些范围内。

### Shared fields injection

由于某些限制，默认情况下不启用共享字段的注入，但是可以选择开启。详见`org.spockframework.spring.EnableSharedInjection`的JavaDoc。