# 如何在遗留的大型项目中进行单元测试

> https://stackoverflow.com/questions/3426775/how-to-approach-unit-testing-in-a-large-project

这个问题即是流程问题也是技术问题：每个人都必须进行测试。

你不应该尝试一次性做完测试。

1. 所有的新代码必须进行测试。
2. 首先将测试纳入bug fix 流程里，每一个修复的bug都会得到测试。
3. 然后将旧的代码逐渐纳入测试中。

逐渐可以得到一个合理的覆盖率。

推荐书：《 Working Effectively With Legacy Code 》by Michael C. Feathers. 





# 不是所有的方法都需要测试

https://stackoverflow.com/a/1621030/23757901

# 单元测试的命名

例如：

*testCalculateAreaWithGeneralDoubleValueRadiusThatReturnsAreaInDouble*

还可以考虑 BDD 风格的：

**givenRadius_whenCalculateArea_thenReturnArea**

# 更推荐用JUit的Assertion

1. assert的异常栈不够清楚
2. assert的api不够丰富
3. assert需要特点的JVM参数开启，如果忘了就会没用；而单元测试应该始终运行
4. 在用JUnit的时候，用JUnit的东西比较好；assert的设计更多是希望生产代码可以忽略这些东西，并不适合单元测试



