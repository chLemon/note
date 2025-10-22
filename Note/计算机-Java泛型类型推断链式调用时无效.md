# Java泛型类型推断链式调用时无效

## 问题现象

```java
playlist.sort(comparing(p1 -> p1.getTitle()));
```

编译器可以正确识别出 p1 的类型，但是

```java
playlist.sort(comparing(p1 -> p1.getTitle())
                        .thenComparing(p1 -> p1.getDuration()));
```

在链式调用时，编译器不能正确识别出 p1 的类型。

## stack overflow 上的问答

> <https://stackoverflow.com/questions/24436871/very-confused-by-java-8-comparator-type-inference>

问题没有什么价值，回答解答了这个问题。

当 lambda 表达式和泛型方法作为方法参数时，他们是 poly expressions （多态表达式，类型是上下文相关的）。会自动推断出合适的类型。例如：

```java
list.sort(p -> p.getTitle());
```

当作为方法接收者（method receiver expressions）时，他们就不是了。例如：

```java
(p -> p.getTitle()).someMethod();
```

所以在

```java
playlist.sort(comparing(p -> p.getTitle()));
```

中，这里有足够的信息来推测出 `comparing()` 泛型参数 和 `p` 的类型。

`comparing()` 可以从 `playlist.sort()` 的方法声明里知道自己的目标类型，从而推测出自己是 `Comparator<Song>`，所以 `p` 必须是 `Song`。

但是当开始链式调用：

```java
Collections.sort(playlist1,
                 comparing(p1 -> p1.getTitle())
                     .thenComparing(p1 -> p1.getDuration())
                     .thenComparing(p1 -> p1.getArtist()));
```

我们知道整个链式调用是 `Comparator<Song>`，但是这整个链式调用的接收者，也就是 `comparing(p1 -> p1.getTitle())` 本身是一个泛型方法调用。我们不知道这第一个泛型方法的类型，所以也无法知道它有一个 `thenComparing` 方法。
【？】

有这么几种解决办法，以推荐优先级顺序如下：

- 用精准的方法引用（没有重载），例如 `Song::getTitle`
- 使用显式 lambda 表达式，`comparing((Song p) -> p.getTitle()).thenComparing(...)`
- 指定类型证据（type witness，在调用泛型方法时，手动指定泛型） `Comparator.<Song, String>comparing(...)`
- 显式类型转换，最不推荐，`(Comparator<Song>)comparing(...)`
