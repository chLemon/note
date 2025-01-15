1. `@InjectMocks`注入失败不会报错
2. `mockStatic`需要正确关闭
    1. 继承共用的`BaseTest`
    2. 可以在`@BeforeClass`中添加`Mockito.framework().clearInlineMocks();`
3. 