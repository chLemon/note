# 博客系统

## 1 快速构建 Spring Boot 应用

1. Spring Initializr：[https://start.spring.io](https://start.spring.io/)填写相关信息后，generate project下载一个压缩包
2. IDEA的Spring Initializr



目录结构

```
    ├── src/main/java
    ├── src/main/resources
    ├── src/test/java
    └── pom.xml
```

其中 `src/main/java` 表示 Java 程序开发目录，这个目录大家应该都比较熟悉，唯一的区别是 Spring Boot 项目中还有一个主程序类。

`src/main/resources` 表示资源文件目录，与普通的 Spring 项目相比有些区别，如上图所示该目录下有 `static` 和 `templates` 两个目录，是 Spring Boot 项目默认的静态资源文件目录和模板文件目录，在 Spring Boot 项目中是没有 `webapp` 目录的，默认是使用 `static` 和 `templates` 两个文件夹。



启动

1. main方法
2.  `mvn spring-boot：run` 
3. 打包好后（mvn clean package -Dmaven.test.skip=true） 进入target目录  java -jar xxx.jar



## 2 Web项目详解

controller：

@Controller



@GetMapping

@ResponseBody



```
server.port=8082
server.servlet.context-path=/shiyanlou/
```



静态资源路径

```
/META-INF/resources/
/resources/
/static/
/public/
```

静态资源映射

```
spring.resources.static-locations=classpath:/shiyanlou/,classpath:/static/
```



## 3 Thymeleaf

直接添加Thymeleaf模板依赖

在html页面导入thymeleaf的名称空间

```
<html lang="en" xmlns:th="http://www.thymeleaf.org">
```

可以有提示功能



在controller里面直接return 一个字符串，是页面的名称（不带后缀



各种属性：th:

注意th:block比较特殊，会删除它本身，而保留其内容



- **表达式语法**

  - 变量表达式： `${...}`
  - 选择变量表达式： `*{...}`
  - 信息表达式： `#{...}`
  - 链接 URL 表达式： `@{...}`
  - 分段表达式： `~{...}`

- **字面量**

  - 字符串： 'one text', 'Another one!' ...
  - 数字： `0`, `34`, `3.0`, `12.3` ...
  - 布尔值： `true`, `false`
  - Null 值： `null`
  - 字面量标记：`one`, `sometext`, `main` ...

- **文本运算**

  - 字符串拼接： `+`
  - 字面量置换: `|The name is ${name}|`

- **算术运算**

  - 二元运算符： `+`, `-`, `*`, `/`, `%`
  - 负号（一元运算符）： (unary operator): `-`

- **布尔运算**

  - 二元运算符： `and`, `or`
  - 布尔非（一元运算符）： `!`, `not`

- **比较运算**

  - 比较： `>`, `<`, `>=`, `<=` (`gt`, `lt`, `ge`, `le`)
  - 相等运算符： `==`, `!=` (`eq`, `ne`)

  比较运算符也可以使用转义字符，比如大于号，可以使用 Thymeleaf 语法 `gt` 也可以使用转义字符`>`

- **条件运算符**

  - If-then: `(if) ? (then)`
  - If-then-else: `(if) ? (then) : (else)`
  - Default: `(value) ?: (defaultvalue)`

- **特殊语法**

  - 无操作： `_`





变量表达式

- ctx : the context object.
- vars : the context variables.
- locale : the context locale.
- request : web 环境下的 HttpServletRequest 对象.
- response :web 环境下的 HttpServletResponse 对象 .
- session : web 环境下的 HttpSession 对象.
- servletContext : web 环境下的 ServletContext 对象.

同时，Thymeleaf 还提供了一系列 Utility 工具对象（内置于 Context 中），可以通过 `#` 直接访问，工具类如下：

- dates ： *java.util.Date 的功能方法类。*
- calendars : *类似 #dates，面向 java.util.Calendar*
- numbers : *格式化数字的工具方法类*
- strings : *字符串对象的工具方法类，contains,startWiths,prepending/appending 等等。*
- bools：*对布尔值求值的工具方法。*
- arrays：*对数组的工具方法。*
- lists：*对 java.util.List 的工具方法*
- sets：*对 java.util.Set 的工具方法*
- maps：*对 java.util.Map 的工具方法*



#### 选择(星号)表达式

选择表达式与变量表达式类似，不过它会用一个预先选择的对象来代替上下文变量容器(map)来执行，语法如下： `*{blog.blogId}`，被指定的对象由 th:object 标签属性进行定义，前文中读取 blog 对象的 title 字段可以替换为：



如果不考虑上下文的情况下，两者没有区别，使用 `${...}`读取的内容也完全可以替换为使用`*{...}`进行读取，唯一的区别是使用`*{...}`前可以预先在父标签中通过 `th:object` 定义一个对象并进行操作。



#### URL 表达式

`th:href` 对应的是 html 中的 href 标签，它将计算并替换 href 标签中的链接 URL 地址，`th:href` 中可以直接设置为静态地址，也可以使用表达式语法读取到的变量值进行动态拼接 URL 地址。

比如一个详情页 URL 地址：`http://localhost:8080/blog/1`，当使用 URL 表达式时，可以写成这样：

```
<a th:href="@{'http://localhost:8080/blog/1'}">详情页</a>

<a th:href="@{'/blog/'+${blog.blogId}}">详情页</a>

<a th:href="@{/blog/{blogId}(blogId=${blog.blogId})">详情页</a>

多个参数
<a
  th:href="@{/blog/{blogId}(blogId=${blog.blogId},title=${blog.blogTitle},tag='java')}"
  >详情页</a
>
```

最终生成的 URL 为 `http://localhost:8080/blog/1?title=lou-springboot&tag=java` 另外，URL 中以 "/" 开头的路径(比如 /blog/1 )，默认生成的 URL 会加上项目的当前地址形成完整的 URL 。





在 strings 工具类测试中，我们首先使用了 `th:if` 标签进行逻辑判断，`th:if="${not #strings.isEmpty(testString)}"`即为一条判断语句，`${...}` 表达式中会返回一个布尔值结果，如果为 true 则该 div 中的内容会继续显示，否则将不会显示 `th:if` 所在的主标签。

`#strings.isEmpty` 的作用为字符串判空，如果 testString 为空则会返回 true，而表达式前面的 not 则表示逻辑非运算，即如果 testString 不为空则继续展示该 div 中的内容。

与 `th:if` 类似的判断标签为 `th:unless` ，它与 `th:if` 刚好相反，当表达式中返回的结果为 false 时，它所在标签中的内容才会继续显示，在 `#lists` 工具类测试中我们使用了 `th:unless` ，大家在调试代码时可以比较二者的区别。

Thymeleaf 模板引擎中的循环语句语法为 `th:each="i:${testList}"` ，类似于 JSP 中的 `c:foreach` 表达式，主要是做循环的逻辑，很多页面逻辑在生成时会使用到该语法。

还有读取 Map 对象的方式为 `${testMap.get('title')}` ，与 Java 语言中也很类似。逻辑判断、循环语句这两个知识点是系统开发中比较常用也比较重要的内容，希望大家能够结合代码练习并牢牢掌握。



- 禁用模板缓存

![此处输入图片的描述](https://doc.shiyanlou.com/document-uid18510labid10298timestamp1552982767807.png)

Thymeleaf 的默认缓存设置是通过配置文件的 **spring.thymeleaf.cache** 配置属性决定的，通过如上 Thymeleaf 模板的配置属性类 ThymeleafProperties 可以发现该属性默认为 true，因此 Thymeleaf 默认是使用模板缓存的，该设置有助于改善应用程序的性能，因为模板只需编译一次即可，但是在开发过程中不能实时看到页面变更的效果，除非重启应用程序，因此建议将该属性设置为 false，在配置文件中修改如下：



```
spring.thymeleaf.cache=false
```

## 4 Spring Boot 处理文件上传及路径回显



Spring MVC提供了文件上传工具类**MultipartResolver** 

配置含义注释：

- **spring.servlet.multipart.enabled**

  是否支持 multipart 上传文件，默认支持

- **spring.servlet.multipart.file-size-threshold**

  文件大小阈值，当大于这个阈值时将写入到磁盘，否则存在内存中，（默认值 0 ，一般情况下不用特意修改）

- **spring.servlet.multipart.location**

  上传文件的临时目录

- **spring.servlet.multipart.max-file-size**

  最大支持文件大小，默认 1 M ，该值可适当的调整

- **spring.servlet.multipart.max-request-size**

  最大支持请求大小，默认 10 M

- **spring.servlet.multipart.resolve-lazily**

  判断是否要延迟解析文件（相当于懒加载，一般情况下不用特意修改），默认 false





上传，input type=”file“

设置form的enctype="multipart/form-data"



controller方法直接用**@RequestParam** 封装成MultipartFile  file

```
try {
            // 保存文件
            byte[] bytes = file.getBytes();
            Path path = Paths.get(FILE_UPLOAD_PATH + newFileName);
            Files.write(path, bytes);
        } catch (IOException e) {
            e.printStackTrace();
        }
```



路径回显

写一个Configuration配置类

@Configuration

然后

```
public void addResourceHandlers(ResourceHandlerRegistry registry) {
	registry.addResourceHandler("/files/**").addResourceLocations("file:/home/project/upload/");
}
```

## 5 JDBC

mysql的启动

```
sudo service mysql start
```

sudo mysql -u root



导包：

jdbc的starter

mysql的驱动

```
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
```



配置

```
# datasource config
spring.datasource.url=jdbc:mysql://localhost:3306/lou_springboot?useUnicode=true&characterEncoding=utf8&autoReconnect=true&useSSL=false
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver
spring.datasource.username=root
spring.datasource.password=
```

在 Spring Boot 2 中，数据库驱动类推荐使用 `com.mysql.cj.jdbc.Driver`，而不是我们平时比较熟悉的 `com.mysql.jdbc.Driver` 类了。



使用直接注入一个JdbcTemplate jdbcTemplate;

然后操作就可以了



## SpringBoot整合MyBatis操作数据库



```
<dependency>
            <groupId>org.mybatis.spring.boot</groupId>
            <artifactId>mybatis-spring-boot-starter</artifactId>
            <version>1.3.2</version>
        </dependency>
```

Spring Boot 整合 MyBatis 时几个比较需要注意的配置参数：

- **mybatis.config-location**

  配置 mybatis-config.xml 路径，mybatis-config.xml 中配置 MyBatis 基础属性，如果项目中配置了 mybatis-config.xml 文件需要设置该参数

- **mybatis.mapper-locations**

  配置 Mapper 文件对应的 XML 文件路径

- **mybatis.type-aliases-package**

  配置项目中实体类包路径

```
mybatis.config-location=classpath:mybatis-config.xml
mybatis.mapper-locations=classpath:mapper/*Dao.xml
mybatis.type-aliases-package=com.lou.springboot.entity
```

我们只配置 mapper-locations 即可

在启动类上面加对 Mapper 包扫描 `@MapperScan`



用xml：

在 resources/mapper 目录下新建 Mapper 接口的映射文件 UserDao.xml，之后进行映射文件的编写。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
    <mapper namespace="com.lou.springboot.dao.UserDao">
    <resultMap type="com.lou.springboot.entity.User" id="UserResult">
        <result property="id" column="id"/>
        <result property="name" column="name"/>
        <result property="password" column="password"/>
    </resultMap>
    <select id="findAllUsers" resultMap="UserResult">
        select id,name,password from tb_user
        order by id desc
    </select>
    <insert id="insertUser" parameterType="com.lou.springboot.entity.User">
        insert into tb_user(name,password)
        values(#{name},#{password})
    </insert>
    <update id="updUser" parameterType="com.lou.springboot.entity.User">
        update tb_user
        set
        name=#{name},password=#{password}
        where id=#{id}
    </update>
    <delete id="delUser" parameterType="int">
        delete from tb_user where id=#{id}
    </delete>
</mapper>
```

## Mybatis-Generator自动生成代码

```
    <plugin>
        <groupId>org.mybatis.generator</groupId>
        <artifactId>mybatis-generator-maven-plugin</artifactId>
        <version>1.3.5</version>
        <dependencies>
            <dependency>
                <groupId> mysql</groupId>
                <artifactId>mysql-connector-java</artifactId>
                <version> 5.1.39</version>
            </dependency>
            <dependency>
                <groupId>org.mybatis.generator</groupId>
                <artifactId>mybatis-generator-core</artifactId>
                <version>1.3.5</version>
            </dependency>
        </dependencies>
        <executions>
            <execution>
                <id>Generate MyBatis Artifacts</id>
                <phase>package</phase>
                <goals>
                    <goal>generate</goal>
                </goals>
            </execution>
        </executions>
        <configuration>
            <verbose>true</verbose>
            <!-- 是否覆盖 -->
            <overwrite>true</overwrite>
            <!-- MybatisGenerator的配置文件位置 -->
            <configurationFile>src/main/resources/mybatisGeneratorConfig.xml</configurationFile>
        </configuration>
    </plugin>
```

在添加插件依赖到 pom.xml 文件中时，我们定义了 Mybatis Generator 的配置文件位置为 src/main/resources/mybatisGeneratorConfig.xml，该文件即为代码生成器插件最重要的配置文件，后续生成代码的规则、数据库连接信息、代码生成后的存放目录等等配置都需要在该配置文件中定义，配置文件内容及相关注释如下：

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE generatorConfiguration
        PUBLIC "-//mybatis.org//DTD MyBatis Generator Configuration 1.0//EN"
        "http://mybatis.org/dtd/mybatis-generator-config_1_0.dtd">
<generatorConfiguration>
    <context id="my-blog-generator-config" targetRuntime="MyBatis3">
        <!-- 生成的Java文件的编码 -->
        <property name="javaFileEncoding" value="utf-8"/>
        <!-- 格式化java代码 -->
        <property name="javaFormatter" value="org.mybatis.generator.api.dom.DefaultJavaFormatter"/>
        <!-- 格式化XML代码 -->
        <property name="xmlFormatter" value="org.mybatis.generator.api.dom.DefaultXmlFormatter"/>
        <plugin type="org.mybatis.generator.plugins.ToStringPlugin"/>
        <!--创建Java类时对注释进行控制-->
        <commentGenerator>
            <property name="suppressDate" value="true"/>
            <!-- 是否去除自动生成的注释 true：是 ： false:否 -->
            <property name="suppressAllComments" value="true"/>
        </commentGenerator>
        <!--数据库地址及登陆账号密码 改成你自己的配置-->
        <jdbcConnection
                driverClass="com.mysql.jdbc.Driver"
                connectionURL="jdbc:mysql://localhost:3306/lou_springboot"
                userId="root"
                password="">
        </jdbcConnection>
        <javaTypeResolver>
            <property name="forceBigDecimals" value="false"/>
        </javaTypeResolver>
        <!--生成实体类设置-->
        <javaModelGenerator targetPackage="com.lou.springboot.entity" targetProject="src/main/java">
            <property name="enableSubPackages" value="true"/>
            <property name="trimStrings" value="true"/>
        </javaModelGenerator>
        <!--生成Mapper文件设置-->
        <sqlMapGenerator targetPackage="mapper" targetProject="src/main/resources">
            <property name="enableSubPackages" value="true"/>
        </sqlMapGenerator>
        <!--生成Dao类设置-->
        <javaClientGenerator type="XMLMAPPER" targetPackage="com.lou.springboot.dao"
                             targetProject="src/main/java">
            <property name="enableSubPackages" value="true"/>
        </javaClientGenerator>
        <!--需要自动生成代码的表及对应的类名设置-->
        <table tableName="generator_test" domainObjectName="GeneratorTest"
               enableCountByExample="false"
               enableUpdateByExample="false"
               enableDeleteByExample="false" enableSelectByExample="false" selectByExampleQueryId="false">
        </table>
    </context>
</generatorConfiguration>
```

需要自动生成代码的表及对应类名的配置是写在 `table` 标签中的，如上所示，generator_test 表对应的实体类可以配置为 GeneratorTest，这些是开发者自定义的，也可以改成其他合适的类名。 如果有多张表同时生成，增加多个 `table` 标签配置即可





生成代码：

1. 方式一：IDEA 工具中的 Maven 插件中含有 mybatis-generator 的选项，点击 generate 即可，如下图所示：
2. 方式二：执行 mvn 如下命令来进行代码生成，这是不通过开发工具提供的图形界面来进行的步骤。

mvn mybatis-generator:generate

然后得记得在DAO接口上加上@Mapper注解或者在主类上加上@MapperScan



## 事务

在 SpringBoot 中，建议采用注解 `@Transactional` 进行事务的控制，只需要在需要进行事务管理的方法或者类上添加 `@Transactional` 注解即可，接下来我们来通过代码讲解。



在Service层做



**@Transactional 不仅可以注解在方法上，也可以注解在类上。当注解在类上时，意味着此类的所有 public 方法都是开启事务的。如果类级别和方法级别同时使用了 `@Transactional` 注解，则使用在类级别的注解会重载方法级别的注解。**



## Ajax 技术使用教程

主要在前端写，点击按钮调用JS的方法，JS方法里面发Ajax请求





## RESTful API 设计



RESTful api，REST（Representational State Transfer）,中文翻译叫"表述性状态转移",

#### 基本原则一：URI

- 应该将 api 部署在专用域名之下。
- URL 中尽量不用大写。
- URI 中不应该出现动词，动词应该使用 HTTP 方法表示但是如果无法表示，也可使用动词，例如：search 没有对应的 HTTP 方法,可以在路径中使用 search，更加直观。
- URI 中的名词表示资源集合，使用复数形式。
- URI 可以包含 queryString，避免层级过深。

#### 基本原则二：HTTP 动词

对于资源的具体操作类型，由 HTTP 动词表示，常用的 HTTP 动词有下面五个：

- GET：从服务器取出资源（一项或多项）。
- POST：在服务器新建一个资源。
- PUT：在服务器更新资源（客户端提供改变后的完整资源）。
- PATCH：在服务器更新资源（客户端提供改变的属性）。
- DELETE：从服务器删除资源。

还有两个不常用的 HTTP 动词：

- HEAD：获取资源的元数据。
- OPTIONS：获取信息，关于资源的哪些属性是客户端可以改变的。

#### 基本原则三：状态码（Status Codes）

处理请求后，服务端需向客户端返回的状态码和提示信息。

常见状态码**(状态码可自行设计，只需开发者约定好规范即可)**：

- 200：SUCCESS 请求成功。
- 401：Unauthorized 无权限。
- 403：Forbidden 禁止访问。
- 410：Gone 无此资源。
- 500：INTERNAL SERVER ERROR 服务器发生错误。 ...

#### 基本原则四：错误处理

如果服务器发生错误或者资源不可达，应该向用户返回出错信息。

#### 基本原则五：服务端数据返回

后端的返回结果最好使用 JSON 格式，且格式统一。

#### 基本原则六：版本控制

- 规范的 api 应该包含版本信息，在 RESTful api 中，最简单的包含版本的方法是将版本信息放到 url 中，如：

- 另一种做法是，使用 HTTP header 中的 accept 来传递版本信息。

以下为接口安全原则的注意事项：

#### 安全原则一：Authentication 和 Permission

Authentication 指用户认证，Permission 指权限机制，这两点是使 RESTful api 强大、灵活和安全的基本保障。

常用的认证机制是 Basic Auth 和 OAuth，RESTful api 开发中，除非 api 非常简单，且没有潜在的安全性问题，否则，**认证机制是必须实现的**，并应用到 api 中去。Basic Auth 非常简单，很多框架都集成了 Basic Auth 的实现，自己写一个也能很快搞定，OAuth 目前已经成为企业级服务的标配，其相关的开源实现方案非常丰富。

#### 安全原则二：CORS

CORS 即 Cross-origin resource sharing，在 RESTful api 开发中，主要是为 js 服务的，解决调用 RESTful api 时的跨域问题。

由于固有的安全机制，js 的跨域请求时是无法被服务器成功响应的。现在前后端分离日益成为 web 开发主流方式的大趋势下，后台逐渐趋向指提供 api 服务，为各客户端提供数据及相关操作，而网站的开发全部交给前端搞定，网站和 api 服务很少部署在同一台服务器上并使用相同的端口，js 的跨域请求时普遍存在的，开发 RESTful api 时，通常都要考虑到 CORS 功能的实现，以便 js 能正常使用 api。

目前各主流 web 开发语言都有很多优秀的实现 CORS 的开源库，我们在开发 RESTful api 时，要注意 CORS 功能的实现，直接拿现有的轮子来用即可。





## 分页功能



JqGrid

 jQuery 插件

使用 JqGrid 时必要的文件如下：

```
## js文件
jquery.jqGrid.js
grid.locale-cn.js
jquery.jqGrid.js

## 样式文件
ui.jqgrid-bootstrap-ui.css
ui.jqgrid-bootstrap.css
ui.jqgrid.css
```

整合过程其实是我们把 JqGrid 代码压缩包中我们需要的样式文件、js 文件、图片等静态资源放入我们项目的静态资源目录下，比如 static 目录或者其他我们设置的静态资源目录





1. 首先在 html 文件中引入 JqGrid 所需文件：

```html
<link href="plugins/jqgrid-5.3.0/ui.jqgrid-bootstrap4.css" rel="stylesheet" />
<!-- JqGrid依赖jquery，因此需要先引入jquery.min.js文件 -->
<script src="plugins/jquery/jquery.min.js"></script>

<script src="plugins/jqgrid-5.3.0/grid.locale-cn.js"></script>
<script src="plugins/jqgrid-5.3.0/jquery.jqGrid.min.js"></script>
```

2. 在页面中需要展示分页数据的区域添加如下代码，用于 JqGrid 初始化：

```html
<!-- JqGrid必要DOM,用于创建表格展示列表数据 -->
<table id="jqGrid" class="table table-bordered"></table>
<!-- JqGrid必要DOM,分页信息区域 -->
<div id="jqGridPager"></div>
```

3. 调用 JqGrid 分页插件的 jqGrid() 方法渲染分页展示区域，代码如下：

```js
$("#jqGrid").jqGrid({
  url: "users/list", // 请求后台json数据的url
  datatype: "json", // 后台返回的数据格式
  colModel: [
    // 列表信息：表头 宽度 是否显示 渲染参数 等属性
    {
      label: "id",
      name: "id",
      index: "id",
      width: 50,
      hidden: true,
      key: true,
    },
    {
      label: "登录名",
      name: "userName",
      index: "userName",
      sortable: false,
      width: 80,
    },
    {
      label: "添加时间",
      name: "createTime",
      index: "createTime",
      sortable: false,
      width: 80,
    },
  ],
  height: 485, // 表格高度  可自行调节
  rowNum: 10, // 默认一页显示多少条数据 可自行调节
  rowList: [10, 30, 50], // 翻页控制条中 每页显示记录数可选集合
  styleUI: "Bootstrap", // 主题 这里选用的是Bootstrap主题
  loadtext: "信息读取中...", // 数据加载时显示的提示信息
  rownumbers: true, // 是否显示行号，默认值是false，不显示
  rownumWidth: 35, // 行号列的宽度
  autowidth: true, // 宽度自适应
  multiselect: true, // 是否可以多选
  pager: "#jqGridPager", // 分页信息DOM
  jsonReader: {
    root: "data.list", //数据列表模型
    page: "data.currPage", //数据页码
    total: "data.totalPage", //数据总页码
    records: "data.totalCount", //数据总记录数
  },
  // 向后台请求的参数
  prmNames: {
    page: "page",
    rows: "limit",
    order: "order",
  },
  // 数据加载完成并且DOM创建完毕之后的回调函数
  gridComplete: function () {
    //隐藏grid底部滚动条
    $("#jqGrid").closest(".ui-jqgrid-bdiv").css({ "overflow-x": "hidden" });
  },
});
```

在 JqGrid 整合中有如下代码：

```json
jsonReader: {
  root: "data.list", //数据列表模型
  page: "data.currPage", //当前页码
  total: "data.totalPage", //数据总页码
  records: "data.totalCount" //数据总记录数
  }
```

这里定义的是 jsonReader 对象如何对后端返回的 json 数据进行解析，比如数据列表为何读取 "data.list"，当前页码为何读取 "data.currPage"，这些都是由后端返回的数据格式所决定的，后端响应结果的数据格式定义在`com.lou.springboot.common.Result` 类中：

```java
public class Result<T> implements Serializable {
    //响应码 200为成功
    private int resultCode;
    //响应msg
    private String message;
    //返回数据
    private T data;
}
```

即所有的数据都会被设置到 data 属性中，分页结果集的数据格式定义如下（注：完整代码位于`com.lou.springboot.util.PageResult`）：

```java
public class PageResult implements Serializable {
    //总记录数
    private int totalCount;
    //每页记录数
    private int pageSize;
    //总页数
    private int totalPage;
    //当前页数
    private int currPage;
    //列表数据
    private List<?> list;
}
```

由于 JqGrid 分页插件在实现分页功能时必须以下四个参数：当前页的所有数据列表、当前页的页码、总页码、总记录数量，因此我们封装了 PageResult 对象，并将其放入 Result 返回结果的 data 属性中，之后在 JqGrid 读取时直接读取对应的参数即可，这就是前后端进行数据交互时的格式定义，希望大家能够结合代码以及实际的分页效果进行理解和学习。



在 `resources/static` 下新建 user.html，代码如下：

```
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <title>lou.springboot | 用户管理页</title>
    <link
      href="plugins/jqgrid-5.3.0/ui.jqgrid-bootstrap4.css"
      rel="stylesheet"
    />
    <link rel="stylesheet" href="plugins/bootstrap/css/bootstrap.css" />
    <link rel="stylesheet" href="plugins/sweetalert/sweetalert.css" />
    <link href="plugins/bootstrap/css/bootstrap.min.css" rel="stylesheet" />
    <link href="dist/css/main.css" rel="stylesheet" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <link
      rel="stylesheet"
      href="plugins/font-awesome/css/font-awesome.min.css"
    />
    <link rel="stylesheet" href="dist/css/adminlte.min.css" />
    <link rel="stylesheet" href="plugins/sweetalert/sweetalert.css" />
  </head>
  <body class="hold-transition sidebar-mini" onLoad="checkCookie();">
    <div class="wrapper">
      <nav
        class="main-header navbar navbar-expand bg-white navbar-light border-bottom"
      >
        <ul class="navbar-nav">
          <li class="nav-item">
            <a class="nav-link" data-widget="pushmenu" href="#"
              ><i class="fa fa-bars"></i
            ></a>
          </li>
          <li class="nav-item d-none d-sm-inline-block">
            <a href="index.html" class="nav-link">Home</a>
          </li>
        </ul>
        <ul class="navbar-nav ml-auto">
          <li class="nav-item dropdown">
            <a
              class="nav-link"
              data-toggle="dropdown"
              href="https://github.com/ZHENFENG13"
            >
              <i class="fa fa-home">&nbsp;&nbsp;文档</i>
            </a>
            <div class="dropdown-menu dropdown-donate-lg dropdown-menu-right">
              <a href="##" class="dropdown-item">实验楼训练营</a>
            </div>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link" data-toggle="dropdown" href="#">
              <i class="fa fa-user">&nbsp;&nbsp;作者</i>
            </a>
            <div class="dropdown-menu dropdown-menu-lg dropdown-menu-right">
              <div class="dropdown-divider"></div>
              <a href="#" class="dropdown-item">
                <i class="fa fa-user-o mr-2"></i> 姓名
                <span class="float-right text-muted text-sm">十三 / 13</span>
              </a>
              <div class="dropdown-divider"></div>
              <a href="#" class="dropdown-item">
                <i class="fa fa-user-secret mr-2"></i> 身份
                <span class="float-right text-muted text-sm"
                  >Java开发工程师</span
                >
              </a>
              <div class="dropdown-divider"></div>
              <a href="#" class="dropdown-item">
                <i class="fa fa-address-card mr-2"></i> 邮箱
                <span class="float-right text-muted text-sm"
                  >2449207463@qq.com</span
                >
              </a>
            </div>
          </li>
        </ul>
      </nav>
      <aside class="main-sidebar sidebar-dark-primary elevation-4">
        <a href="index.html" class="brand-link">
          <img
            src="dist/img/logo.jpg"
            alt="ssm-cluster Logo"
            class="brand-image img-circle elevation-3"
            style="opacity: .8"
          />
          <span class="brand-text font-weight-light">lou.springboot</span>
        </a>
        <div class="sidebar">
          <!-- Sidebar user panel (optional) -->
          <div class="user-panel mt-3 pb-3 mb-3 d-flex">
            <div class="image">
              <img
                src="dist/img/logo3.jpg"
                class="img-circle elevation-2"
                alt="User Image"
              />
            </div>
            <div class="info">
              <a href="#" class="d-block">十三</a>
            </div>
          </div>
          <nav class="mt-2">
            <ul
              class="nav nav-pills nav-sidebar flex-column"
              data-widget="treeview"
              role="menu"
              data-accordion="false"
            >
              <!-- Add icons to the links using the .nav-icon class
                         with font-awesome or any other icon font library -->
              <li class="nav-header">Dashboard</li>
              <li class="nav-item has-treeview">
                <a href="#" class="nav-link">
                  <i class="nav-icon fa fa-dashboard"></i>
                  <p>
                    Dashboard
                    <i class="right fa fa-angle-left"></i>
                  </p>
                </a>
                <ul class="nav nav-treeview">
                  <li class="nav-item">
                    <a href="./index.html" class="nav-link active">
                      <i class="fa fa-circle-o nav-icon"></i>
                      <p>lou.springboot主页</p>
                    </a>
                  </li>
                  <li class="nav-item">
                    <a href="./index2.html" class="nav-link">
                      <i class="fa fa-circle-o nav-icon"></i>
                      <p>adminLTE v3</p>
                    </a>
                  </li>
                </ul>
              </li>
              <li class="nav-header">管理模块</li>
              <li class="nav-item">
                <a href="user.html" class="nav-link active">
                  <i class="fa fa-user-circle nav-icon"></i>
                  <p>用户管理</p>
                </a>
              </li>
            </ul>
          </nav>
        </div>
      </aside>
      <div class="content-wrapper">
        <!-- Content Header (Page header) -->
        <div class="content-header">
          <div class="container-fluid">
            <div class="row mb-2">
              <div class="col-sm-6">
                <h1 class="m-0 text-dark">用户管理页</h1>
              </div>
              <!-- /.col -->
              <div class="col-sm-6">
                <ol class="breadcrumb float-sm-right">
                  <li class="breadcrumb-item"><a href="index.html">主页</a></li>
                  <li class="breadcrumb-item active">用户管理页</li>
                </ol>
              </div>
              <!-- /.col -->
            </div>
            <!-- /.row -->
          </div>
          <!-- /.container-fluid -->
        </div>
        <div class="content">
          <div class="row">
            <div class="col-12">
              <div class="card">
                <div class="card-body">
                  <!-- 分页展示区，需要增加 jqgrid 相关 DOM -->
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- /.content-wrapper -->
      <footer class="main-footer">
        <strong>Copyright &copy; 2019 <a href="##">13blog.site</a>.</strong>
        All rights reserved.
        <div class="float-right d-none d-sm-inline-block">
          <b>Version</b> 2.0
        </div>
      </footer>
      <aside class="control-sidebar control-sidebar-dark"></aside>
    </div>
    <script src="plugins/jquery/jquery.min.js"></script>
    <!-- jQuery UI 1.11.4 -->
    <script src="plugins/jQueryUI/jquery-ui.min.js"></script>
    <!-- sweet alert -->
    <script src="plugins/sweetalert/sweetalert.min.js"></script>
    <!-- Bootstrap 4 -->
    <script src="plugins/bootstrap/js/bootstrap.bundle.min.js"></script>
    <script src="plugins/jqgrid-5.3.0/grid.locale-cn.js"></script>
    <script src="plugins/jqgrid-5.3.0/jquery.jqGrid.min.js"></script>
    <script src="dist/js/public.js"></script>
    <script src="dist/js/user.js"></script>
    <script src="dist/js/adminlte.js"></script>
  </body>
</html>
```

我们使用了 AdminLTE3 的样式和页面布局，之后在页面中引入 JqGrid 的相关静态资源文件，最后在页面中展示分页数据的区域增加如下代码：

```html
<!-- 数据展示列表，id 为 jqGrid -->
<table id="jqGrid" class="table table-bordered"></table>
<!-- 分页按钮展示区 -->
<div id="jqGridPager"></div>
```



在`resources/static/dist/js`下新建 user.js，代码如下：

```js
$(function () {
  $("#jqGrid").jqGrid({
    url: "users/list",
    datatype: "json",
    colModel: [
      {
        label: "id",
        name: "id",
        index: "id",
        width: 50,
        hidden: true,
        key: true,
      },
      {
        label: "登录名",
        name: "userName",
        index: "userName",
        sortable: false,
        width: 80,
      },
      {
        label: "添加时间",
        name: "createTime",
        index: "createTime",
        sortable: false,
        width: 80,
      },
    ],
    height: 485,
    rowNum: 10,
    rowList: [10, 30, 50],
    styleUI: "Bootstrap",
    loadtext: "信息读取中...",
    rownumbers: true,
    rownumWidth: 35,
    autowidth: true,
    multiselect: true,
    pager: "#jqGridPager",
    jsonReader: {
      root: "data.list",
      page: "data.currPage",
      total: "data.totalPage",
      records: "data.totalCount",
    },
    prmNames: {
      page: "page",
      rows: "limit",
      order: "order",
    },
    gridComplete: function () {
      //隐藏grid底部滚动条
      $("#jqGrid").closest(".ui-jqgrid-bdiv").css({ "overflow-x": "hidden" });
    },
  });
});
```

该代码的含义为：在页面加载时，调用 JqGrid 的初始化方法，将页面中 id 为 jqGrid 的 DOM 渲染为分页表格，并向后端发送请求，之后按照后端返回的 json 数据填充表格以及表格下方的分页按钮，第一页、下一页、最后一页等等逻辑都有 JqGrid 内部实现了，我们只需要将它初始化时所需要的几个数据设置好即可，因此我们需要将返回格式设置为 PageResult 类所封装的数据类型。

由于 user.html 文件中引入了 user.js 文件，所以在页面加载完成后会进行数据列表的渲染及分页插件的渲染，用户可以直接使用翻页功能了，本来这些功能需要我们自行实现，但是使用 JqGrid 后这些都不需要我们再去做逻辑实现，只需要调用其分页方法并将所需的参数设置好即可，十分方便。



## 验证码功能

生成验证码的方式以及案例有很多，本教程中所选择的方案是 Google 的 kaptcha 框架。



添加依赖

```
        <!-- 验证码 -->
        <dependency>
            <groupId>com.github.penggle</groupId>
            <artifactId>kaptcha</artifactId>
            <version>2.3.2</version>
        </dependency>
```

注册 DefaultKaptcha 到 IOC 容器中，新建 config 包，之后新建 KaptchaConfig 类，内容如下：

```java
package com.lou.springboot.config;

import com.google.code.kaptcha.impl.DefaultKaptcha;
import org.springframework.context.annotation.Bean;
import org.springframework.stereotype.Component;
import com.google.code.kaptcha.util.Config;
import java.util.Properties;

@Component
public class KaptchaConfig {
    @Bean
    public DefaultKaptcha getDefaultKaptcha(){
        com.google.code.kaptcha.impl.DefaultKaptcha defaultKaptcha = new com.google.code.kaptcha.impl.DefaultKaptcha();
        Properties properties = new Properties();
        // 图片边框
        properties.put("kaptcha.border", "no");
        // 字体颜色
        properties.put("kaptcha.textproducer.font.color", "black");
        // 图片宽
        properties.put("kaptcha.image.width", "160");
        // 图片高
        properties.put("kaptcha.image.height", "40");
        // 字体大小
        properties.put("kaptcha.textproducer.font.size", "30");
        // 验证码长度
        properties.put("kaptcha.textproducer.char.space", "5");
        // 字体
        properties.setProperty("kaptcha.textproducer.font.names", "宋体,楷体,微软雅黑");
        Config config = new Config(properties);
        defaultKaptcha.setConfig(config);
        return defaultKaptcha;
    }
}
```

这里就是对生成的图片验证码的规则配置，如颜色、宽高、长度、字体等等，可以根据需求自行修改这些规则，之后就可以生成自己想要的验证码了。

#### 后端处理

在 controller 包中新建 KaptchaController，之后注入刚刚配置好的 DefaultKaptcha 类，然后就可以新建一个方法，在方法里可以生成验证码对象，并以图片流的方式写到前端以供显示，代码如下：

```java
package com.lou.springboot.controller;
import com.google.code.kaptcha.impl.DefaultKaptcha;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.util.StringUtils;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import javax.imageio.ImageIO;
import javax.servlet.ServletOutputStream;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.awt.image.BufferedImage;
import java.io.ByteArrayOutputStream;

/**
 * @author 13
 * @qq交流群 796794009
 * @email 2449207463@qq.com
 * @link http://13blog.site
 */
@Controller
public class KaptchaController {

    @Autowired
    private DefaultKaptcha captchaProducer;

    @GetMapping("/kaptcha")
    public void defaultKaptcha(HttpServletRequest httpServletRequest, HttpServletResponse httpServletResponse) throws Exception {
        byte[] captchaOutputStream;
        ByteArrayOutputStream imgOutputStream = new ByteArrayOutputStream();
        try {
            //生产验证码字符串并保存到session中
            String verifyCode = captchaProducer.createText();
            httpServletRequest.getSession().setAttribute("verifyCode", verifyCode);
            BufferedImage challenge = captchaProducer.createImage(verifyCode);
            ImageIO.write(challenge, "jpg", imgOutputStream);
        } catch (IllegalArgumentException e) {
            httpServletResponse.sendError(HttpServletResponse.SC_NOT_FOUND);
            return;
        }
        captchaOutputStream = imgOutputStream.toByteArray();
        httpServletResponse.setHeader("Cache-Control", "no-store");
        httpServletResponse.setHeader("Pragma", "no-cache");
        httpServletResponse.setDateHeader("Expires", 0);
        httpServletResponse.setContentType("image/jpeg");
        ServletOutputStream responseOutputStream = httpServletResponse.getOutputStream();
        responseOutputStream.write(captchaOutputStream);
        responseOutputStream.flush();
        responseOutputStream.close();
    }
}
```

我们在控制器中新增了 defaultKaptcha 方法，该方法所拦截处理的路径为 /kaptcha，在前端访问该路径后就可以接收到一个图片流并显示在浏览器页面上。

#### 前端处理

新建 kaptcha.html，在该页面中显示验证码，代码如下：

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>验证码显示</title>
  </head>
  <body>
    <img src="/kaptcha" onclick="this.src='/kaptcha?d='+new Date()*1" />
  </body>
</html>
```

访问后端验证码路径 /kaptcha，并将其返回显示在 img 标签中，之后定义了 `onclick` 方法，在点击该 img 标签时可以动态的切换显示一个新的验证码，点击时访问的路径为 `/kaptcha?d=1565950414611`，即原来的验证码路径后面带上一个时间戳参数，时间戳是会变化的，所以每次点击都会是一个与之前不同的请求，如果不这样处理的话，由于浏览器的机制可能并不会重新发送请求。



验证码的显示完成后，我们接下来要做的就是对用户输入的验证码进行比对和验证，因为一般的做法就是后端生成后会对当前生成的验证码进行保存（可能是 session 中、或者缓存中、或者数据库中），之后显示到前端页面，用户在看到验证码之后在页面对应的输入框中填写验证码，之后才向后端发送请求，而后端再接到请求后会对用户输入的验证码进行验证，如果不对的话则不会进行后续操作，接下来我们来简单的实现一下这个流程。

#### 后端处理

在 KaptchaController 类中新增 `verify` 方法，代码如下：

```java
    @GetMapping("/verify")
    @ResponseBody
    public String verify(@RequestParam("code") String code, HttpSession session) {
        if (StringUtils.isEmpty(code)) {
            return "验证码不能为空";
        }
        String kaptchaCode = session.getAttribute("verifyCode") + "";
        if (StringUtils.isEmpty(kaptchaCode) || !code.equals(kaptchaCode)) {
            return "验证码错误";
        }
        return "验证成功";
    }
```

该方法所拦截处理的路径为 /verify，请求参数为 code，即用户输入的验证码，在进行基本的非空验证后，与之前保存在 session 中的 verifyCode 值进行比较，不同则返回验证码错误，相同则返回验证成功。

#### 前端处理

新建 verify.html，该页面中显示验证码，同时有可以供用户输入验证码的输入框以及提交按钮，代码如下：

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>验证码测试</title>
  </head>
  <body>
    <img src="/kaptcha" onclick="this.src='/kaptcha?d='+new Date()*1" />
    <input type="text" maxlength="5" id="code" placeholder="请输入验证码" />
    <button id="verify">验证</button>
  </body>
  <script src="jquery.js"></script>
  <script type="text/javascript">
    $(function () {
      $("#verify").click(function () {
        var code = $("#code").val();
        $.ajax({
          type: "GET", //方法类型
          url: "/verify?code=" + code,
          success: function (result) {
            alert(result);
          },
          error: function () {
            alert("请求失败");
          },
        });
      });
    });
  </script>
</html>
```

用户在输入框中输入验证码后可以点击“验证”按钮，点击事件触发后执行 js 方法，该方法会获取到用户输入的验证码的值，并将其作为请求参数，之后进行 Ajax 请求，请求后会在弹框中显示后端返回的处理结果。



## 登录模块实现

登录流程设计：

首先，在数据库中查询这条用户记录，伪代码如下：

```sql
select * from xxx_user where account_number = 'xxxx';
```

如果不存在这条记录则表示身份验证失败，登录流程终止；如果存在这条记录，则表示身份验证成功，接下来则需要进行登录状态的存储和验证了，存储伪代码如下：

```java
//通过 Cookie 存储
Cookie cookie = new Cookie("userName",xxxxx);

//通过 Session 存储
session.setAttribute("userName",xxxxx);
```

验证逻辑的伪代码如下：

```java
//通过 Cookie 获取需要验证的数据并进行比对校验
Cookie cookies[] = request.getCookies();
if (cookies != null){
    for (int i = 0; i < cookies.length; i++)
           {
               Cookie cookie = cookies[i];
               if (name.equals(cookie.getName()))
               {
                    return cookie;
               }
           }
}

//通过session获取需要验证的数据并进行比对校验
session.getAttribute("userName");
```

本次实践项目的登录状态我们是通过 session 来保存的，用户登录成功后我们将用户信息放到 session 对象中，之后再实现一个拦截器，在访问项目时判断 session 中是否有用户信息，有则放行请求，没有就跳转到登录页面。





#### AdminMapper.xml(**注：完整代码位于 src/main/resources/mapper/AdminMapper.xml**)

通过用户名和密码查询用户记录：

```xml
  <select id="login" resultMap="BaseResultMap">
    select
    <include refid="Base_Column_List" />
    from tb_admin_user
    where login_name = #{userName,jdbcType=VARCHAR} AND login_password=#{password,jdbcType=VARCHAR} AND locked = 0
  </select>
```

#### 业务层代码

代码如下：(**注：完整代码位于 com.site.blog.my.core.service.impl 包下的 AdminUserServiceImpl.java**)

```java
    public Admin login(String userName, String password) {
        String passwordMd5 = MD5Util.MD5Encode(password, "UTF-8");
        return adminMapper.login(userName, passwordMd5);
    }
```

#### 控制层代码

首先对参数进行校验，参数中包括登陆信息和验证码，验证码的比对大家应该都了解，拿参数与存储在 session 中的验证码值进行比较，之后调用 adminUserService 业务层代码查询用户对象，之后根据验证结果来跳转页面，如果登陆成功则跳转到管理系统的首页，失败的话则带上错误信息返回到登录页，登录页中会显示出登陆的错误信息。(**注：完整代码位于 com.site.blog.my.core.controller.admin 包下的 AdminController.java**)

```java
    @PostMapping(value = "/login")
    public String login(@RequestParam("userName") String userName,
                        @RequestParam("password") String password,
                        @RequestParam("verifyCode") String verifyCode,
                        HttpSession session) {
        if (StringUtils.isEmpty(verifyCode)) {
            session.setAttribute("errorMsg", "验证码不能为空");
            return "admin/login";
        }
        if (StringUtils.isEmpty(userName) || StringUtils.isEmpty(password)) {
            session.setAttribute("errorMsg", "用户名或密码不能为空");
            return "admin/login";
        }
        String kaptchaCode = session.getAttribute("verifyCode") + "";
        if (StringUtils.isEmpty(kaptchaCode) || !verifyCode.equals(kaptchaCode)) {
            session.setAttribute("errorMsg", "验证码错误");
            return "admin/login";
        }
        Admin adminUser = adminService.login(userName, password);
        if (adminUser != null) {
            session.setAttribute("loginUser", adminUser.getAdminNickName());
            session.setAttribute("loginUserId", adminUser.getAdminId());
            //session过期时间设置为7200秒 即两小时
            session.setMaxInactiveInterval(60 * 60 * 2);
            return "redirect:/admin/index";
        } else {
            session.setAttribute("errorMsg", "登陆失败");
            return "admin/login";
        }
    }
```





## 登陆拦截器

在前一个实验中我们实现了管理员的登陆功能，该功能已经完成，但是身份认证的整个流程并没有完善，该流程中应该包括登陆功能、身份认证、访问拦截、退出功能，



定义一个 Interceptor 非常简单方式也有几种，这里简单列举两种：

- 新建类要实现 Spring 的 HandlerInterceptor 接口
- 新建类继承实现了 HandlerInterceptor 接口的实现类，例如已经提供的实现了 HandlerInterceptor 接口的抽象类 HandlerInterceptorAdapter



HandlerInterceptor 方法介绍：

```java
    boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler)
            throws Exception;

    void postHandle(
            HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception;

    void afterCompletion(
            HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception;
```

- **preHandle**：在业务处理器处理请求之前被调用。预处理，可以进行编码、安全控制、权限校验等处理；
- **postHandle**：在业务处理器处理请求执行完成后，生成视图之前执行。
- **afterCompletion**：在 DispatcherServlet 完全处理完请求后被调用，可用于清理资源等，返回处理（已经渲染了页面）；



#### 定义拦截器



新建 interceptor 包，在包中新建 AdminLoginInterceptor 类，该类需要实现 HandlerInterceptor 接口，代码如下：

```java
package com.site.blog.my.core.interceptor;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;
import org.springframework.web.servlet.ModelAndView;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * 后台系统身份验证拦截器
 */
@Component
public class AdminLoginInterceptor implements HandlerInterceptor {
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object o) throws Exception {
        String uri = request.getRequestURI();
        if (uri.startsWith("/admin") && null == request.getSession().getAttribute("loginUser")) {
            request.getSession().setAttribute("errorMsg", "请登陆");
            response.sendRedirect(request.getContextPath() + "/admin/login");
            return false;
        } else {
            request.getSession().removeAttribute("errorMsg");
            return true;
        }
    }
    @Override
    public void postHandle(HttpServletRequest httpServletRequest, HttpServletResponse httpServletResponse, Object o, ModelAndView modelAndView) throws Exception {
    }
    @Override
    public void afterCompletion(HttpServletRequest httpServletRequest, HttpServletResponse httpServletResponse, Object o, Exception e) throws Exception {
    }
}
```

我们只需要完善 `preHandle` 方法即可，同时在类声明上方添加 `@Component` 注解使其注册到 IOC 容器中。通过上面代码可以看出，在请求的预处理过程中读取当前 session 中是否存在 loginUser 对象，如果不存在则返回 false 并跳转至登录页面，如果已经存在则返回 true，继续做后续处理流程。







#### 配置拦截器



在实现拦截器的相关方法之后，我们需要对该拦截器进行配置以使其生效，在 Spring Boot 1.x 版本中我们通常会继承 WebMvcConfigurerAdapter 类，但是在 Spring Boot 2.x 版本中，WebMvcConfigurerAdapter 被弃用，虽然继承 WebMvcConfigurerAdapter 这个类虽然有此便利，但在 Spring 5.0 里面已经被弃用了，官方文档也说了，WebMvcConfigurer 接口现在已经有了默认的空白方法，所以在 Spring Boot 2.x 版本下更好的做法还是实现  WebMvcConfigurer 接口。

新建 config 包，之后新建 MyBlogWebMvcConfigurer 类并实现 WebMvcConfigurer 接口，代码如下：

```java
package com.site.blog.my.core.config;

import com.site.blog.my.core.interceptor.AdminLoginInterceptor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class MyBlogWebMvcConfigurer implements WebMvcConfigurer {

    @Autowired
    private AdminLoginInterceptor adminLoginInterceptor;

    public void addInterceptors(InterceptorRegistry registry) {
        // 添加一个拦截器，拦截以/admin为前缀的url路径
        registry.addInterceptor(adminLoginInterceptor).addPathPatterns("/admin/**").excludePathPatterns("/admin/login").excludePathPatterns("/admin/dist/**").excludePathPatterns("/admin/plugins/**");
    }
}
```

在该配置类中，我们添加刚刚新增的 AdminLoginInterceptor 登录拦截器，并对该拦截器所拦截的路径进行配置，由于后端管理系统的所有请求路径都以 /admin 开头，所以拦截的路径为 /admin/** ，但是登陆页面以及部分静态资源文件也是以 /admin 开头，所以需要将这些路径排除，配置如上。

此时，重启项目，并且再去访问 index 页面，如果没登录的话就会跳回到登录页面了，拦截器生效了。



#### 用户模块完善

用户模块不只是登录功能，还包括用户信息修改、安全退出的功能：

建立profile.html

后端逻辑实现也是在 AdminController 类中，代码如下：(**注：完整代码位于 `com.site.blog.my.core.controller.admin` 包下**)

```java
    @GetMapping("/profile")
    public String profile(HttpServletRequest request) {
        Integer loginUserId = (int) request.getSession().getAttribute("loginUserId");
        AdminUser adminUser = adminUserService.getUserDetailById(loginUserId);
        if (adminUser == null) {
            return "admin/login";
        }
        request.setAttribute("path", "profile");
        request.setAttribute("loginUserName", adminUser.getLoginUserName());
        request.setAttribute("nickName", adminUser.getNickName());
        return "admin/profile";
    }

    @PostMapping("/profile/password")
    @ResponseBody
    public String passwordUpdate(HttpServletRequest request, @RequestParam("originalPassword") String originalPassword,
                                 @RequestParam("newPassword") String newPassword) {
        if (StringUtils.isEmpty(originalPassword) || StringUtils.isEmpty(newPassword)) {
            return "参数不能为空";
        }
        Integer loginUserId = (int) request.getSession().getAttribute("loginUserId");
        if (adminUserService.updatePassword(loginUserId, originalPassword, newPassword)) {
            //修改成功后清空session中的数据，前端控制跳转至登录页
            request.getSession().removeAttribute("loginUserId");
            request.getSession().removeAttribute("loginUser");
            request.getSession().removeAttribute("errorMsg");
            return "success";
        } else {
            return "修改失败";
        }
    }

    @PostMapping("/profile/name")
    @ResponseBody
    public String nameUpdate(HttpServletRequest request, @RequestParam("loginUserName") String loginUserName,
                             @RequestParam("nickName") String nickName) {
        if (StringUtils.isEmpty(loginUserName) || StringUtils.isEmpty(nickName)) {
            return "参数不能为空";
        }
        Integer loginUserId = (int) request.getSession().getAttribute("loginUserId");
        if (adminUserService.updateName(loginUserId, loginUserName, nickName)) {
            return "success";
        } else {
            return "修改失败";
        }
    }

    @GetMapping("/logout")
    public String logout(HttpServletRequest request) {
        request.getSession().removeAttribute("loginUserId");
        request.getSession().removeAttribute("loginUser");
        request.getSession().removeAttribute("errorMsg");
        return "admin/login";
    }
```

源码已经提供给大家了，接下来我们来实际的操作一下用户模块的登陆登出、信息修改功能。



## 分类功能实现

#### 表结构设计

在进行接口设计和具体的功能实现前，首先将表结构确定下来，每篇文章都会被归类到一个类别下，一个类别下会有多篇文章，分类实体与文章实体的关系是一对多的关系，因此在表结构设计时，在文章表中设置一个分类关联字段即可，分类表只需要将分类相关的字段定义好，分类实体与文章实体的关系交给文章表来维护即可（后续讲到文章表时再介绍），分类表的 SQL 设计如下，直接执行如下 SQL 语句即可：

```sql
USE `my_blog_db`;

/*Table structure for table `tb_blog_category` */

CREATE TABLE `tb_blog_category` (
  `category_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '分类表主键',
  `category_name` varchar(50) NOT NULL COMMENT '分类的名称',
  `category_icon` varchar(50) NOT NULL COMMENT '分类的图标',
  `category_rank` int(11) NOT NULL DEFAULT '1' COMMENT '分类的排序值 被使用的越多数值越大',
  `is_deleted` tinyint(4) NOT NULL DEFAULT '0' COMMENT '是否删除 0=否 1=是',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

分类表的字段以及每个字段对应的含义都在上面的 SQL 中有介绍，大家可以对照 SQL 进行理解，把表结构导入到数据库中即可，接下来我们进行编码工作。



#### 接口介绍

分类模块在后台管理系统中有 5 个接口，分别是：

- 分类列表分页接口
- 添加分类接口
- 根据 id 获取单条分类记录接口
- 修改分类接口
- 删除分类接口

## 标签功能实现

侧边导航栏



这里的实现方式是通过添加一个 path 变量来控制当前导航栏中的选中状态，在模板文件中的 Thymeleaf 判断语句中通过 path 字段来确定是哪个功能模块，并对应的将左侧导航栏上当前模块的 css 样式给修改掉，判断语句如下：



文章和标签是多对多

