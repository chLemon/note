>springfox-swagger已经有一段时间没人维护了，应该考虑用其他项目来替换。

>在对swagger进行学习的时候，我主要想找到在Java Spring项目中全部的注解文档，但是发现官网并没有这部分信息，大家应该还是通过读Java源码来掌握注解。

# 1 Swagger简介

## 1.1 Swagger

- 号称世界上最流行的API框架
- Restful Api 文档在线自动生成器 => **API 文档 与API 定义同步更新**
- 直接运行，在线测试API**【但是批量测试还是得用postman】**
- 支持多种语言 （如：Java，PHP等）
- 官网：https://swagger.io/

## 1.2 SpringBoot集成Swagger

**SpringBoot集成Swagger** => **springfox**，两个jar包

- **Springfox-swagger2**
- swagger-springmvc

要求：jdk 1.8 + 否则swagger2无法运行

### A Maven依赖

```xml
<!-- https://mvnrepository.com/artifact/io.springfox/springfox-swagger2 -->
<dependency>
   <groupId>io.springfox</groupId>
   <artifactId>springfox-swagger2</artifactId>
   <version>2.9.2</version>
</dependency>
<!-- https://mvnrepository.com/artifact/io.springfox/springfox-swagger-ui -->
<dependency>
   <groupId>io.springfox</groupId>
   <artifactId>springfox-swagger-ui</artifactId>
   <version>2.9.2</version>
</dependency>
<!-- 不知道为什么，我司在springfox-swagger2里面exclusion了swagger-models，在下面又依赖了1.5.21版本的swagger-models -->
```

### B 配置类SwaggerConfig

```java
@Configuration //配置类
@EnableSwagger2// 开启Swagger2的自动配置
public class SwaggerConfig {  
}
```

### C 访问测试 

http://localhost:8080/swagger-ui.html ，可以看到swagger的界面



swagger： http://localhost:8080/swagger/index.html

springboot中的swagger： http://localhost:8080/swagger-ui.html

# 2 配置Swagger

## 2.1 实例Bean Docket

Swagger实例Bean是Docket，所以通过配置Docket实例来配置Swaggger。

```java
@Bean //配置docket以配置Swagger具体参数
public Docket docket() {
   return new Docket(DocumentationType.SWAGGER_2);
}
```

## 2.2 文档信息 apiInfo

可以通过apiInfo()属性配置文档信息

```java
//配置文档信息
private ApiInfo apiInfo() {
   Contact contact = new Contact("联系人名字", "http://xxx.xxx.com/联系人访问链接", "联系人邮箱");
   return new ApiInfo(
           "Swagger学习", // 标题
           "学习演示如何配置Swagger", // 描述
           "v1.0", // 版本
           "http://terms.service.url/组织链接", // 组织链接
           contact, // 联系人信息
           "Apach 2.0 许可", // 许可
           "许可链接", // 许可连接
           new ArrayList<>()// 扩展
  );
}
```

Docket 实例关联上 apiInfo()

```java
@Bean
public Docket docket() {
   return new Docket(DocumentationType.SWAGGER_2)
     .apiInfo(apiInfo());
}
```

## 2.3 扫描接口 select

构建Docket时通过select()方法配置怎么扫描接口。

```java
@Bean
public Docket docket() {
   return new Docket(DocumentationType.SWAGGER_2)
      .apiInfo(apiInfo())
      .select()// 通过.select()方法，去配置扫描接口,RequestHandlerSelectors配置如何扫描接口
      .apis(RequestHandlerSelectors.basePackage("com.kuang.swagger.controller"))
      .build();
}
```

select方法可以调用的方法

```java
any() // 扫描所有，项目中的所有接口都会被扫描到
none() // 不扫描接口
// 通过方法上的注解扫描，如withMethodAnnotation(GetMapping.class)只扫描get请求
withMethodAnnotation(final Class<? extends Annotation> annotation)
// 通过类上的注解扫描，如.withClassAnnotation(Controller.class)只扫描有controller注解的类中的接口
withClassAnnotation(final Class<? extends Annotation> annotation)
basePackage(final String basePackage) // 根据包路径扫描接口
```

## 2.4 接口过滤 paths

除此之外，我们还可以配置接口扫描过滤：

```java
@Bean
public Docket docket() {
   return new Docket(DocumentationType.SWAGGER_2)
      .apiInfo(apiInfo())
      .select()// 通过.select()方法，去配置扫描接口,RequestHandlerSelectors配置如何扫描接口
      .apis(RequestHandlerSelectors.basePackage("com.kuang.swagger.controller"))
       // 配置如何通过path过滤,即这里只扫描请求以/kuang开头的接口
      .paths(PathSelectors.ant("/kuang/**"))
      .build();
}
```

```java
PathSelectors.any() // 任何请求都扫描
PathSelectors.none() // 任何请求都不扫描
PathSelectors.regex(final String pathRegex) // 通过正则表达式控制
PathSelectors.ant(final String antPattern) // 通过ant()控制
```

## 2.5 忽略请求参数 ignoredParameterTypes

可以通过`ignoredParameterTypes()`方法去配置要忽略的参数：

HttpServletRequest

## 2.6 开关swagger enable

通过enable()方法配置是否启用swagger，如果是false，swagger将不能在浏览器中访问了

```java
@Bean
public Docket docket() {
   return new Docket(DocumentationType.SWAGGER_2)
      .apiInfo(apiInfo())
      .enable(false) //配置是否启用Swagger，如果是false，在浏览器将无法访问
      .select()// 通过.select()方法，去配置扫描接口,RequestHandlerSelectors配置如何扫描接口
      .apis(RequestHandlerSelectors.basePackage("com.kuang.swagger.controller"))
       // 配置如何通过path过滤,即这里只扫描请求以/kuang开头的接口
      .paths(PathSelectors.ant("/kuang/**"))
      .build();
}
```

如何动态配置当项目处于test、dev环境时显示swagger，处于prod时不显示？

```java
@Bean
public Docket docket(Environment environment) {
   // 设置要显示swagger的环境
   Profiles of = Profiles.of("dev", "test");
   // 判断当前是否处于该环境
   // 通过 enable() 接收此参数判断是否要显示
   boolean b = environment.acceptsProfiles(of);
   
   return new Docket(DocumentationType.SWAGGER_2)
      .apiInfo(apiInfo())
      .enable(b) //配置是否启用Swagger，如果是false，在浏览器将无法访问
      .select()// 通过.select()方法，去配置扫描接口,RequestHandlerSelectors配置如何扫描接口
      .apis(RequestHandlerSelectors.basePackage("com.kuang.swagger.controller"))
       // 配置如何通过path过滤,即这里只扫描请求以/kuang开头的接口
      .paths(PathSelectors.ant("/kuang/**"))
      .build();
}
```

可以在项目中增加一个dev的配置文件查看效果！

## 2.7 API分组 groupName

右上角的 select a spec

![图片](https://mmbiz.qpic.cn/mmbiz_png/uJDAUKrGC7IExpkhknhzRFQicsic8yibm9Z7k4Y8iaVnHtPd78o82ff8hItej9Cyf0wvbG8u8KgXic7gVh77NoZw4RQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

1、如果没有配置分组，默认是default。通过groupName()方法即可配置分组：

```
@Bean
public Docket docket(Environment environment) {
   return new Docket(DocumentationType.SWAGGER_2).apiInfo(apiInfo())
      .groupName("hello") // 配置分组
       // 省略配置....
}
```

2、重启项目查看分组

3、如何配置多个分组？配置多个分组只需要配置多个docket即可：

```
@Bean
public Docket docket1(){
   return new Docket(DocumentationType.SWAGGER_2).groupName("group1");
}
@Bean
public Docket docket2(){
   return new Docket(DocumentationType.SWAGGER_2).groupName("group2");
}
@Bean
public Docket docket3(){
   return new Docket(DocumentationType.SWAGGER_2).groupName("group3");
}
```

4、重启项目查看即可

# 3 代码内的注解

Swagger的所有注解定义在io.swagger.annotations包下

## 3.1 POJO类和字段的配置

```java
@ApiModel("用户实体")
public class User {
  
   @ApiModelProperty("用户名")
   public String username;
  
   @ApiModelProperty("密码")
   public String password;
}
```

只要这个实体在**请求接口**的返回值上（即使是泛型），都能映射到实体项中。对于请求参数，如果没有的话，加上RequestBody参数。


|Swagger注解 | 简单说明|
| ------------------------------------------------------ | ---------------------------------------------------- |
| @ApiModel("xxxPOJO说明")                               | 作用在模型类上：如VO、BO                             |
| @ApiModelProperty(value = "xxx属性说明",hidden = true) | 作用在类方法和属性上，hidden设置为true可以隐藏该属性 |

## 3.2 接口相关

```java
@ApiOperation("狂神的接口")
@PostMapping("/kuang")
public String kuang(@ApiParam("这个名字会被返回")String username){
   return username;
}
```

| Swagger注解                  | 简单说明                                        |
| ---------------------------- | ----------------------------------------------- |
| @Api(tags = "xxx模块说明")   | 作用在模块类上                                  |
| @ApiOperation("xxx接口说明") | 作用在接口方法上                                |
| @ApiParam("xxx参数说明")     | 作用在参数、方法和字段上，类似@ApiModelProperty |

## 3.3 各注解的常用属性

详细属性可以查看java内的代码与注释

| 注解               | 属性         | 含义                                                         |
| ------------------ | ------------ | ------------------------------------------------------------ |
| @Api               |              | 用在请求的类上，表示对类的说明                               |
|                    | tags         | 说明该类的作用，可以在UI界面上看到的注解                     |
|                    | hidden       | 是否隐藏该类下的方法，默认false                              |
|                    | value        | 该参数没什么意义，在UI界面上也看到，所以不需要配置           |
| @ApiOperation      |              | 用在请求的方法上，说明方法的用途、作用                       |
|                    | value        | 对于方法的简短说明                                           |
|                    | notes        | 对于方法的详细说明                                           |
|                    | tags         | 可以给该方法单独分到一个类中                                 |
| @ApiImplicitParams |              | 用在请求的方法上，表示一组参数说明                           |
| @ApiImplicitParam  |              | 用在@ApiImplicitParams注解中，指定请求参数的各个方面         |
|                    | name         | 参数名                                                       |
|                    | value        | 参数的汉字说明、解释                                         |
|                    | required     | 参数是否必须传                                               |
|                    | paramType    | 参数放在哪个地方                                             |
|                    | header       | 请求参数的获取                                               |
| @RequestHeader     | query        | 请求参数的获取                                               |
| @RequestParam      | path         | 用于restful接口，请求参数的获取                              |
| @PathVariable      |              |                                                              |
|                    | body         | 不常用                                                       |
|                    | form         | 不常用                                                       |
|                    | dataType     | 参数类型，默认String，其他值dataType="Integer"               |
|                    | defaultValue | 参数的默认值                                                 |
| @ApiResponses      |              | 用在请求的方法上，表示一组响应                               |
| @ApiResponse       |              | 用在@ApiResponses中，一般用于表达一个错误的响应信息          |
|                    | code         | 数组，例如400                                                |
|                    | message      | 信息，例如""请求参数错误"                                    |
|                    | response     | 抛出异常的类                                                 |
| @ApiModel          |              | 用于响应类上，表示一个返回响应数据的信息。（这种一般用在post创建的时候，使用@RequestBody这样的场景，请求参数无法使用@ApiImplicitParam注解进行描述的时候） |
| @ApiModelProperty  |              | 用在属性上，描述响应类的属性                                 |

