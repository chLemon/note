# SharedNameTable 过大问题排查

## 1. 问题背景

某项目在执行单元测试时，如果设置了 maven-surefire 的 forkCount = 0，则大对象检测会发现存在大对象，类型为 `com.sun.tools.javac.util.SharedNameTable`

## 2. 排查

<https://github.com/apache/maven-mvnd/issues/897> 里，楼主遇到了类似的问题，在使用 mvnd （类似 maven，也是一个构建工具）的时候，检测到了这个 SharedNameTable 有内存泄漏的表现。

下方回答提到：

1. maven-compiler-plugin 设置为 `<fork>true</fork>` 可以解决这个问题
   尝试恢复 forkCount，设置为非 0 数字，则该问题消失。但是楼主并没有解决这个问题
2. 有一片链接，表示这似乎是 javac 的一个 feature
   <https://stackoverflow.com/questions/14617340/memory-leak-when-using-jdk-compiler-at-runtime>
3. mvnd 最终添加了参数修复了这个问题
   `-XDuseUnsharedTable=true`

## 3. javac

在 JDK7 里引入了一个特性，javac 作为编译器，会保存编译后的源码，旨在加快编译速度。这些内容会以 Soft Reference 的形式放在 SharedNameTable 中，可以通过 `javac -XDuseUnsharedTable` 来禁用这个功能。

据说在 JDK 8 u60 里会修复。

Soft Reference 只会在堆内存完全不够的时候收集。所以大对象检测任务中的主动 GC 不会触发该类的垃圾回收。

## 4. 为什么在 forkCount = 0 时会触发这个问题？

当 forkCount >= 1 时，会创建多个进程，多个 JVM 实例，然后将测试代码分给各个进程去执行。这样每个进程需要编译的类的数量会减少，所以不会触发这个问题。
