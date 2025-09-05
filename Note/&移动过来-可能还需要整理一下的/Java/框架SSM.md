# Mybatis

## 1 概述

### 1.1 框架与三层架构

+ 什么是框架？
	它是我们软件开发中的一套解决方案，不同的框架解决的是不同的问题。
	
+ 使用框架的好处：
	框架封装了很多的细节，使开发者可以使用极简的方式实现功能。大大提高开发效率。
	
+ 三层架构
   + 表现层：
     用于展示数据：SpringMVC
   + 业务层：
     处理业务需求
   + 持久层：
     和数据库交互：Mybatis
     Spring涉及到全部三层

### 1.2 持久层技术解决方案
+ JDBC技术：
    Connection
    PreparedStatement
    ResultSet
+ Spring的JdbcTemplate：
    Spring中对jdbc的简单封装
+ Apache的DBUtils：
    对jdbc的简单封装

以上这些都不是框架，JDBC是规范，其余两个都只是工具类。

### 1.3 mybatis的概述

mybatis是一个持久层框架，用java编写的。
使开发者只关注sql语句本身。
使用了ORM思想实现了结果集的封装

+ ORM：Object Relational Mapping 对象关系映射
  简单的说，就是把数据库表和实体类以及实体类的属性对应起来，让我们可以操作实体类就实现操作数据库表。

## 2 mybatis的入门案例

### 2.1 环境搭建

1. 创建maven工程
2. 数据库初始化
3. maven依赖导入：
   + mybatis官网，导入mybatis的依赖
   + mysql的
   + log4j
   + junit
4. 建实体类，记得实现Serializable接口
5. 在resources下，创建xml文件，SqlMapConfig.xml，主配置文件。【提供了约束，需要导入】
6. 在resources下创建文件"com/itheima/dao/IUserDao.xml"。映射配置文件。
7. Mybatis里一般管Dao叫Mapper
8. 满足：
   1. 映射配置文件与dao接口的包结构相同
   2. namespace与dao接口全限定类名相同
   3. id与dao的方法名相同
   就可以不用写dao的实现类

### 2.2 主配置文件

resources下SqlMapConfig.xml

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">

<!-- mybatis的主配置文件 -->
<configuration>
    <!-- 配置环境 -->
    <environments default="mysql">
        <!-- 配置mysql的环境，上面的default和下面的id必须相同-->
        <environment id="mysql">
            <!-- 配置事务的类型-->
            <transactionManager type="JDBC"></transactionManager>
            <!-- 配置数据源（连接池） -->
            <dataSource type="POOLED">
                <!-- 配置连接数据库的4个基本信息 -->
                <property name="driver" value="com.mysql.jdbc.Driver"/>
                <property name="url" value="jdbc:mysql://localhost:3306/eesy_mybatis"/>
                <property name="username" value="root"/>
                <property name="password" value="1234"/>
            </dataSource>
        </environment>
    </environments>

    <!-- 指定映射配置文件的位置，映射配置文件指的是每个dao独立的配置文件 -->
    <mappers>
        <mapper resource="com/itheima/dao/IUserDao.xml"/>
    </mappers>
</configuration>
```
```
<configuration>
    <environments default="mysql">
        <environment id="mysql">
            <transactionManager type="JDBC"></transactionManager>
            <dataSource type="POOLED">
                <property name="" value=""/>
                ...数据库的4个基本信息

    <mappers>
        <mapper resource="com/itheima/dao/IUserDao.xml"/>
```

### 2.3 映射配置文件

resources下com/itheima/dao/IUserDao.xml

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper
        PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">

<mapper namespace="com.itheima.dao.IUserDao">
    <!--配置查询所有，上面这个namespace必须是dao接口的全限定类名，下面这个id必须是接口的方法名-->
    <select id="findAll" resultType="com.itheima.domain.User">
        select * from user
    </select>
</mapper>
```
```
<mapper namespace="com.itheima.dao.IUserDao">
    <select id="findAll" resultType="com.itheima.domain.User">
        select * from user
```

### 2.4 入门案例

```
//1.读取配置文件
InputStream in = Resources.getResourceAsStream("SqlMapConfig.xml");
//2.创建SqlSessionFactory工厂
SqlSessionFactoryBuilder builder = new SqlSessionFactoryBuilder();
SqlSessionFactory factory = builder.build(in);
//3.使用工厂生产SqlSession对象
SqlSession session = factory.openSession();
//4.使用SqlSession创建Dao接口的代理对象
IUserDao userDao = session.getMapper(IUserDao.class);
//5.使用代理对象执行方法
List<User> users = userDao.findAll();
for(User user : users){
    System.out.println(user);
}
//6.释放资源
session.close();
in.close();
```
入门案例：
1. 读配置
2. 创建工厂：SqlSessionFactory
3. 创建SqlSession
4. 创建代理对象
5. 调用方法
6. 释放资源

### 2.5 注解配置

在主配置里更改mappers：【class】
```
<!-- 指定映射配置文件的位置，映射配置文件指的是每个dao独立的配置文件
    如果是用注解来配置的话，此处应该使用class属性指定被注解的dao全限定类名-->
<mappers>
    <mapper class="com.itheima.dao.IUserDao"/>
</mappers>
```
然后在接口的方法上面加注解：
```
@Select("select * from user")
```

映射配置文件就可以删了

### 2.6 实现类

也可以写实现类，SqlSession有个方法，select.selectList，有一堆重载，传入一个statement，sql语句执行对象，这里传的是 接口全限定类名.方法名
也就是原来写在映射配置文件里的namespace.id

### 2.7 路径问题

+ 相对路径：现在在src目录下，但是之后编译完就不在了
+ 绝对路径：不太好

所以一般这两个都不用，用
第一个：类加载器
第二个：ServletContext的getRealPath

### 2.8 自定义Mybatis

selectList方法分析：

执行这个方法，需要
1. 数据库的连接信息		2. 映射信息

映射信息包含2部分：
sql语句	实体类的全限定类名

映射信息就组合起来定义成一个对象，到时候放在一个map里存储起来，key就是用namespace.id

代理对象创建部分：
Proxy.newProxyInstance传入类加载器，存放了代理对象实现的接口的数组，和如何代理的方法

如何代理是一个InvocationHandler的接口，写一个实现类实现了selectList方法

### 通过注解拿到要封装的实体类

字节码对象，拿到方法数组，看方法上有没有select注解，然后拿到注解，然后拿方法的返回值，带泛型信息的，强转为参数化的类型，然后拿参数化类型中的实际参数（即参数化类型里的泛型），拿到实体类，强转class，拿到名称

## 3 基于代理DAO实现CRUD

### 3.1 根据id查询

```
<select id="findById" resultType="com.itheima.domain.User" parameterType="int">
    select * from user where id = #{uid}
</select>
```
+ resultType 属性：用于指定结果集的类型。
+ parameterType 属性：用于指定传入参数的类型。

+ sql 语句中使用#{}字符：它代表占位符，相当于原来jdbc 部分所学的?，都是用于执行语句时替换实际的数据。
+ 具体的数据是由#{}里面的内容决定的。
+ #{}中内容的写法：由于数据类型是基本类型，所以此处可以随意写。

### 3.2 保存用户

```
<!-- 保存用户-->
<insert id="saveUser" parameterType="com.itheima.domain.User">
    insert into user(username,birthday,sex,address)
    values(#{username},#{birthday},#{sex},#{address})
</insert>
```

+ #{}中内容的写法：参数是一个类，此处写User的**属性**名。

+ 属性名用的是ognl 表达式
+ Object Graphic Navigation Language 对象图导航语言。语法格式#{对象.对象}

#### 3.2.1 保存用户后获得自增长的id

```xml
<insert id="saveUser" parameterType="USER">
    <!-- 配置保存时获取插入的id -->
    <selectKey keyColumn="id" keyProperty="id" resultType="int">
        select last_insert_id();
    </selectKey>
    insert into user(username,birthday,sex,address)
    values(#{username},#{birthday},#{sex},#{address})
</insert>
```

Column是SQL语句结果集的列名，Property是属性

### 3.3 更新用户

```
<!-- 更新用户-->
<update id="updateUser" parameterType="com.itheima.domain.User">
    update user set username=#{username},birthday=#{birthday},sex=#{sex},address=#{address} where id=#{id}
</update>
```

### 3.4 删除用户

```
<!-- 删除用户-->
<delete id="deleteUser" parameterType="java.lang.Integer">
    delete from user where id = #{uid}
</delete>
```

### 3.5 模糊查询

```
<!-- 根据名称模糊查询-->
<select id="findByName" resultType="com.itheima.domain.User" parameterType="String">
    select * from user where username like #{username}
</select>
```
注意，要么在外面，要么在这里，记得写%

### 3.6 聚合函数

```
<!-- 查询总记录条数-->
<select id="findTotal" resultType="int">
    select count(*) from user;
</select>
```

## 4 映射配置文件的几个参数

### 4.1 parameterType

SQL语句的参数。
可以用：
+ 基本类型，引用类型
+ 实体类型（POJO）
+ 实体类的包装类型（Vo）

#### 4.1.1 Vo举例

新建一个类QueryVo，里面有成员变量```User user;```
```
<!-- 根据用户名称模糊查询，参数变成一个QueryVo 对象了-->
<select id="findByVo" resultType="com.itheima.domain.User" parameterType="com.itheima.domain.QueryVo">
    select * from user where username like #{user.username};
</select>
```

### 4.2 resultType

结果集的类型

实体类中的属性名称必须和查询语句中的列名保持一致，否则无法实现封装。

```
<!-- 配置查询所有操作-->
<select id="findAll" resultType="com.itheima.domain.User">
    select id as userId,username as userName,birthday as userBirthday, sex as userSex,address as userAddress from user
</select>
```

### 4.3 resultMap

+ resultMap标签可以建立查询的列名和实体类的属性名称不一致时建立对应关系。从而实现封装。

```
<!-- 建立User 实体和数据库表的对应关系
	type 属性：指定实体类的全限定类名
	id 属性：给定一个唯一标识，是给查询select 标签引用用的。-->
<resultMap type="com.itheima.domain.User" id="userMap">
    <id column="id" property="userId"/>
    <result column="username" property="userName"/>
    <result column="sex" property="userSex"/>
    <result column="address" property="userAddress"/>
    <result column="birthday" property="userBirthday"/>
</resultMap>
```
+ id 标签：用于指定主键字段
+ result 标签：用于指定非主键字段
+ column 属性：用于指定数据库列名
+ property 属性：用于指定实体类属性名称
```
<!-- 配置查询所有操作-->
<select id="findAll" resultMap="userMap">
    select * from user
</select>
```

## 5 主配置文件

```
-properties（属性）
	--property
-settings（全局配置参数）
	--setting
-typeAliases（类型别名）
	--typeAliase
	--package
-typeHandlers（类型处理器）
-objectFactory（对象工厂）
-plugins（插件）
-environments（环境集合属性对象）
	--environment（环境子属性对象）
		---transactionManager（事务管理）
		---dataSource（数据源）
-mappers（映射器）
	--mapper
	--package
```

### 5.1 properties（属性）

在使用properties 标签配置时，我们可以采用两种方式指定属性配置。

#### 5.1.1 第一种
```
<properties>
    <property name="jdbc.driver" value="com.mysql.jdbc.Driver"/>
    <property name="jdbc.url" value="jdbc:mysql://localhost:3306/eesy"/>
    <property name="jdbc.username" value="root"/>
    <property name="jdbc.password" value="1234"/>
</properties>

下面的连接池改为
<dataSource type="POOLED">
    <property name="driver" value="${jdbc.driver}"/>
    <property name="url" value="${jdbc.url}"/>
    <property name="username" value="${jdbc.username}"/>
    <property name="password" value="${jdbc.password}"/>
</dataSource>
```

#### 5.1.2 第二种

先在classpath 下定义db.properties 文件
```
jdbc.driver=com.mysql.jdbc.Driver
jdbc.url=jdbc:mysql://localhost:3306/eesy
jdbc.username=root
jdbc.password=1234
```
然后在主配置文件中
```
<!-- 配置连接数据库的信息-->
<properties url=file:///D:/IdeaProjects/day02_eesy_01mybatisCRUD/src/main/resources/jdbcConfig.properties">
</properties>

<dataSource type="POOLED">
    <property name="driver" value="${jdbc.driver}"/>
    <property name="url" value="${jdbc.url}"/>
    <property name="username" value="${jdbc.username}"/>
    <property name="password" value="${jdbc.password}"/>
</dataSource>
```
+ resource 属性：用于指定properties 配置文件的位置，要求配置文件必须在类路径下。resource="jdbcConfig.properties"
+ url 属性：协议+主机+端口+URI，此处是file协议

### 5.2 typeAliases（类型别名）

自定义别名

在SqlMapConfig.xml中配置：
```
<typeAliases>
    <!-- 单个别名定义-->
    <typeAlias alias="user" type="com.itheima.domain.User"/>
    <!-- 批量别名定义，扫描整个包下的类，别名为类名（首字母大写或小写都可以）-->
    <package name="com.itheima.domain"/>
    <package name="其它包"/>
</typeAliases>
```

### 5.3 mappers（映射器）

+ 使用相对于类路径的资源。如：
```
<mapper resource="com/itheima/dao/IUserDao.xml" />
```

+ 使用mapper 接口类路径。如：
```
<mapper class="com.itheima.dao.UserDao"/>
```
注意：此种方法要求mapper 接口名称和mapper 映射文件名称相同，且放在同一个目录中。

+ **注册指定包下的所有mapper 接口**
如：
```
<package name="cn.itcast.mybatis.mapper"/>
```
注意：此种方法要求mapper 接口名称和mapper 映射文件名称相同，且放在同一个目录中。

## 6 连接池与事务

### 6.1 连接池

+ Mybatis的连接池是自己实现的。DataSource，也翻译为数据源。

#### 6.1.1 配置与分类

+ 主配置文件中
```
<dataSource type=”pooled”>
```

+ 数据源分类
UNPOOLED 不使用连接池的数据源
POOLED 使用连接池的数据源【常用】
JNDI 使用JNDI 实现的数据源

#### 6.1.2 连接的获取

只有到真正执行SQL语句的时候，才会去获取连接，用完后归还。

#### 6.1.3 POOLED的原理

有一个空闲池，一个活动池。先去空闲池里找，如果没有去看活动池满没，没满就建一个新连接，满了就把最老的连接拿出来改造

### 6.2 事务

+ 手动提交：sqlSession.commit()

+ 自动提交设置：创建session的时候传入参数true
```
session = factory.openSession(true);
```
不常用，多个连接同时操作的时候可能会有问题。

## 7 动态SQL语句

### 7.1 if

根据id查询，如果有username或address的值，还要加入作为条件。
```xml
<select id="findByUser" resultType="user" parameterType="user">
    select * from user where 1=1
    <if test="username!=null and username != '' ">
        and username like #{username}
    </if>
    <if test="address != null">
        and address like #{address}
    </if>
</select>
```
+ if标签里test属性中写的是对象的属性。

### 7.2 where

简化上面where 1=1 的条件拼装
```
<select id="findByUser" resultType="user" parameterType="user">
    select * from user
    <where>
        <if test="username!=null and username != '' ">
            and username like #{username}
        </if>
        <if test="address != null">
            and address like #{address}
        </if>
    </where>
</select>
```

### 7.3 foreach

范围查询的参数传递：select 字段 from user where id in (?)
先在queryvo中加入一个List ids来封装参数
```xml
<!-- 查询所有用户在id 的集合之中-->
<select id="findInIds" resultType="user" parameterType="queryvo">
    select * from user
    <where>
        <if test="ids != null and ids.size() > 0">
            <foreach collection="ids" open="id in ( " close=")" item="uid"
            separator=",">
                #{uid}
            </foreach>
        </if>
    </where>
</select>
```

+ foreach标签用于遍历集合

属性
+ collection:代表要遍历的集合元素，注意编写时不要写#{}
+ open:代表语句的开始部分
+ close:代表结束部分
+ item:代表遍历集合的每个元素，生成的变量名，与下方保持一致
+ sperator:代表分隔符

### 7.4 简化编写的SQL 片段

Sql 中可将重复的sql 提取出来，使用时用include 引用即可，最终达到sql 重用的目的。

#### 7.4.1 抽取重复的语句代码片段

```
<!-- 抽取重复的语句代码片段-->
<sql id="defaultSql">
    select * from user
</sql>
```

#### 7.4.2 引用代码片段

```
<!-- 配置查询所有操作-->
<select id="findAll" resultType="user">
<include refid="defaultSql"></include>
</select>

<!-- 根据id 查询-->
<select id="findById" resultType="UsEr" parameterType="int">
<include refid="defaultSql"></include>
where id = #{uid}
</select>
```

## 8 多表查询

### 8.1 一对一

#### 8.1.1 方法一：专门定义一个新的实体类

+ SQL：
```
SELECT
    account.*,
    user.username,
    user.address
FROM
    account,
    user
WHERE account.uid = user.id
```

+ AccountUser类：除了account的字段外，再新写两个。

+ 配置信息

```
<mapper namespace="com.itheima.dao.IAccountDao">
    <!-- 配置查询所有操作-->
    <select id="findAll" resultType="accountuser">
        select a.*,u.username,u.address from account a,user u where a.uid =u.id;
    </select>
</mapper>
```

#### 8.1.2 方法二：用resultMap：association

在Account 类中加入一个成员变量：User user
resultMap里，先写自己的，id为主键，其余为result，然后写别的，一对一用association，id是主键，其余为result。association写property，column：哪个字段获取的，JavaType封装到哪个对象

```
<mapper namespace="com.itheima.dao.IAccountDao">
    <!-- 建立对应关系-->
    <resultMap type="account" id="accountMap">
        <id column="aid" property="id"/>
        <result column="uid" property="uid"/>
        <result column="money" property="money"/>
        <!-- 它是用于指定从表方的引用实体属性的-->
        <association property="user" column="uid" javaType="user">
            <id column="id" property="id"/>
            <result column="username" property="username"/>
            <result column="sex" property="sex"/>
            <result column="birthday" property="birthday"/>
            <result column="address" property="address"/>
        </association>
    </resultMap>
    <select id="findAll" resultMap="accountMap">
        select u.*,a.id as aid,a.uid,a.money from account a,user u where a.uid =u.id;
    </select>
</mapper>
```

### 8.2 一对多查询：collection

+ SQL
```
SELECT
    u.*, acc.id id,
    acc.uid,
    acc.money
FROM
    user u LEFT JOIN account acc ON u.id = acc.uid
```

+ User 类加入```List<Account>```

+ 映射文件配置
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper
PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
"http://mybatis.org/dtd/mybatis-3-mapper.dtd">

<mapper namespace="com.itheima.dao.IUserDao">
    <resultMap type="user" id="userMap">
        <id column="id" property="id"></id>
        <result column="username" property="username"/>
        <result column="address" property="address"/>
        <result column="sex" property="sex"/>
        <result column="birthday" property="birthday"/>
  		<!-- collection 是用于建立一对多中集合属性的对应关系，ofType 用于指定集合元素的数据类型-->
        <collection property="accounts" ofType="account">
            <id column="aid" property="id"/>
            <result column="uid" property="uid"/>
            <result column="money" property="money"/>
        </collection>
    </resultMap>
    <!-- 配置查询所有操作-->
    <select id="findAll" resultMap="userMap">
        select u.*,a.id as aid ,a.uid,a.money from user u left outer join account a on u.id =a.uid
    </select>
</mapper>
```
+ collection部分：定义了用户关联的账户信息。表示关联查询结果集
+ property="accounts"：关联查询的结果集存储在User对象上的哪个属性。
+ ofType="account"：指定关联查询的结果集中的对象类型即List中的对象类型。此处可以使用别名，也可以使用全限定名。

### 8.3 多对多：collection

+ 多对多的MySQL实现：有一张中间表
+ SQL：
```mysql
SELECT
    r.*,u.id uid,
    u.username username,
    u.birthday birthday,
    u.sex sex,
    u.address address
FROM
    ROLE r
    INNER JOIN USER_ROLE ur ON ( r.id = ur.rid)
    INNER JOIN USER u ON (ur.uid = u.id);
```

+ 配置文件
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper
PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
"http://mybatis.org/dtd/mybatis-3-mapper.dtd">

<mapper namespace="com.itheima.dao.IRoleDao">
    <!--定义role 表的ResultMap-->
    <resultMap id="roleMap" type="role">
        <id property="roleId" column="rid"></id>
        <result property="roleName" column="role_name"></result>
        <result property="roleDesc" column="role_desc"></result>
        <collection property="users" ofType="user">
            <id column="id" property="id"></id>
            <result column="username" property="username"></result>
            <result column="address" property="address"></result>
            <result column="sex" property="sex"></result>
            <result column="birthday" property="birthday"></result>
        </collection>
    </resultMap>
    <!--查询所有-->
    <select id="findAll" resultMap="roleMap">
        select u.*,r.id as rid,r.role_name,r.role_desc from role r
         left outer join user_role ur on r.id = ur.rid
         left outer join user u on u.id = ur.uid
    </select>
</mapper>
```

+ 所有SQL回车换行的地方前后都加上空格以防万一

## 9 延迟加载

+ 延迟加载：需要用到数据时才进行加载。也叫懒加载。
+ 好处：提高性能
+ 坏处：大批量数据查询时可能会使得用户等待时间变长。

+ 通常在一对多和多对多的时候使用延迟加载
+ 通常在一对一的时候使用立即加载

### 9.1 一对一

association

#### 9.1.1 主配置文件开启延迟加载

```
<!-- 开启延迟加载的支持-->
<settings>
    <setting name="lazyLoadingEnabled" value="true"/>
    <setting name="aggressiveLazyLoading" value="false"/>
</settings>
```

#### 9.1.2 映射配置文件

修改association标签的内容，加入属性select和column。指在加载完主表后，通过select指定的方法，与column指定的列名，去进行从表的查询。

```
<mapper namespace="com.itheima.dao.IAccountDao">
    <!-- 建立对应关系-->
    <resultMap type="account" id="accountMap">
        <id column="aid" property="id"/>
        <result column="uid" property="uid"/>
        <result column="money" property="money"/>
        <!-- 它是用于指定从表方的引用实体属性的-->
        <association property="user" javaType="user"
        select="com.itheima.dao.IUserDao.findById"
        column="uid"></association>
    </resultMap>
    <select id="findAll" resultMap="accountMap">
        select * from account
    </select>
</mapper>

```
+ select：填写我们要调用的select 映射的id
+ column ：填写我们要传递给select 映射的参数

### 9.2 一对多

collection

#### 9.2.1 映射配置文件

collection标签也有select和column属性，用来制定查询的方法和使用的字段，同时还有ofType属性，来制定集合元素的数据类型

```
<resultMap type="user" id="userMap">
    <id column="id" property="id"></id>
    <result column="username" property="username"/>
    <result column="address" property="address"/>
    <result column="sex" property="sex"/>
    <result column="birthday" property="birthday"/>

    <collection property="accounts" ofType="account" select="com.itheima.dao.IAccountDao.findByUid" column="id"></collection>
</resultMap>
<!-- 配置查询所有操作-->
<select id="findAll" resultMap="userMap">
    select * from user
</select>
```

## 10 缓存

重复的查询语句会返回同一个对象。

### 10.1 一级缓存

+ SqlSession对象的缓存，只要SqlSession 没有flush 或close，它就存在。

清空缓存：
+ sqlSession.clearCache();//此方法也可以清空缓存
+ close和flush

### 10.2 二级缓存

+ SQLSessionFactory对象的缓存。同一个SQLSessionFactory创建的SQLSession共享缓存。【mapper级别，同一个映射配置文件？】
+ 使用时需要在主配置、映射配置、操作标签中均进行相应的设置。

#### 10.2.1 主配置文件

```
<settings>
    <!-- 开启二级缓存的支持-->
    <setting name="cacheEnabled" value="true"/>
</settings>
```
因为cacheEnabled 的取值默认就为true，所以这一步可以省略不配置。为true 代表开启二级缓存；为false 代表不开启二级缓存。

#### 10.2.2 映射配置文件

```
<mapper namespace="com.itheima.dao.IUserDao">
    <!-- 开启二级缓存的支持-->
    <cache></cache>

    <!-- 根据id 查询-->
    <select id="findById" resultType="user" parameterType="int" useCache="true">
    select * from user where id = #{uid}
    </select>
</mapper>
```
+ cache标签表示当前这个mapper 映射将使用二级缓存

+ 将select标签中设置useCache=”true”代表当前这个statement 要使用二级缓存，如果不使用二级缓存可以设置为false。
+ 注意：针对每次查询都需要最新的数据sql，要设置成useCache=false，禁用二级缓存。

### 10.3 注意

一级缓存在进行过增删改操作后会自动刷新，会获取新的对象。

二级缓存是在SqlSessionFactory中存了数据，每次获取的都是新的对象

## 11 注解开发

注解可以代替映射配置文件，主配置文件依旧需要存在。

有注解就不能在对应目录下有映射配置文件，否则会报错

### 11.1 主配置文件

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE configuration
PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
"http://mybatis.org/dtd/mybatis-3-config.dtd">

<configuration>
    <!-- 配置外部配置文件properties的位置-->
    <properties resource="jdbcConfig.properties"></properties>
    
    <!-- 配置别名的注册-->
    <typeAliases>
    <package name="com.itheima.domain"/>
    </typeAliases>
    
    <!-- 配置环境-->
    <environments default="mysql">
        <!-- 配置mysql 的环境-->
        <environment id="mysql">
            <!-- 配置事务的类型是JDBC -->
            <transactionManager type="JDBC"></transactionManager>
            <!-- 配置数据源，在最前面已经引入了外部配置文件，配置文件里的key就叫jdbc.driver-->
            <dataSource type="POOLED">
                <property name="driver" value="${jdbc.driver}"/>
                <property name="url" value="${jdbc.url}"/>
                <property name="username" value="${jdbc.username}"/>
                <property name="password" value="${jdbc.password}"/>
            </dataSource>
        </environment>
    </environments>
    
    <!-- 配置映射信息-->
    <mappers>
    <!-- 配置带有注解的dao 接口的位置 -->
        <package name="com.itheima.dao"/>
    </mappers>
</configuration>
```

### 11.2 基本CRUD演示

以下注解均在在接口的对应方法上

#### 11.2.1 查询select

```
@Select("select * from user")

List<User> findAll();
```

#### 11.2.2 插入insert

```
@Insert("insert into user(username,sex,birthday,address) values(#{username},#{sex},#{birthday},#{address})")

int saveUser(User user);
```

#### 11.2.3 更新update

```
@Update("update user set username=#{username},address=#{address},sex=#{sex},birthday=#{birthday} where id=#{id} ")

int updateUser(User user);
```

#### 11.2.4 删除delete

```
@Delete("delete from user where id = #{uid} ")

int deleteUser(Integer userId);
```

#### 11.2.5 聚合函数

```
@Select("select count(*) from user ")

int findTotal();
```

#### 11.2.6 模糊查询

这样记得外面要加百分号
```
@Select("select * from user where username like #{username} ")
List<User> findByName(String name);
```

### 11.3 Results注解、Result注解和ResultMap注解

+ 解决Java实体类的字段名与数据库表的字段名不一致的情况

```
@Select("select * from user")
@Results(id="userMap",value= {
                @Result(id=true,column="id",property="userId"),
                @Result(column="username",property="userName"),
                @Result(column="sex",property="userSex"),
                @Result(column="address",property="userAddress"),
                @Result(column="birthday",property="userBirthday")
})

List<User> findAll();
```
+ Result标签id表示是主键
+ Results标签的id可以让别的注解通过ResultMap引用，如
```
@Select("select * from user where id = #{uid} ")
@ResultMap("userMap")

User findById(Integer userId);
```

### 11.4 多表查询

#### 11.4.1 一对一

+ 一个账户对应一个用户
+ 此处为account类中有一个成员变量为User user
+ 在对应的result标签里，用column指定用来查询的字段，property为要封装的字段，用one表示一对一，one里的select指向可以用column进行查询的方法，fetchType来指定是否延迟查询【LAZY和EAGER】

```
@Select("select * from account")

@Results(id="accountMap",value= {
    @Result(id=true,column="id",property="id"),
    @Result(column="uid",property="uid"),
    @Result(column="money",property="money"),

    @Result(column="uid",property="user",
    		one=@One(select="com.itheima.dao.IUserDao.findById",
    				fetchType=FetchType.LAZY)
    		)
})

List<Account> findAll();
```

#### 11.4.2 一对多

+ 一个用户拥有多个账户

```
@Select("select * from user")

@Results(id="userMap",value= {
        @Result(id=true,column="id",property="userId"),
        @Result(column="username",property="userName"),
        @Result(column="sex",property="userSex"),
        @Result(column="address",property="userAddress"),
        @Result(column="birthday",property="userBirthday"),
        @Result(column="id",property="accounts",
            many=@Many(select="com.itheima.dao.IAccountDao.findByUid",        									fetchType=FetchType.LAZY)
            	)
})

List<User> findAll();
```

### 11.5 二级缓存配置

1. 在主配置文件中开启二级缓存支持
```
<!-- 配置二级缓存-->
<settings>
    <!-- 开启二级缓存的支持-->
    <setting name="cacheEnabled" value="true"/>
</settings>
```

2. 在接口上加注解

```
@CacheNamespace(blocking=true)//mybatis 基于注解方式实现配置二级缓存
public interface IUserDao {
	...
}
```

### 11.6 常用注解

```
@Insert:实现新增
@Update:实现更新
@Delete:实现删除
@Select:实现查询
@Result:实现结果集封装
@Results:可以与@Result 一起使用，封装多个结果集
@ResultMap:实现引用@Results 定义的封装
@One:实现一对一结果集封装
@Many:实现一对多结果集封装
@SelectProvider: 实现动态SQL 映射
@CacheNamespace:实现注解二级缓存的使用
```

# Spring

## 1 概述

+ 全栈式轻量级开源框架。
+ 内核：IoC和AOP【反转控制，面向切面编程】
+ 优先：
   + 方便解耦
   + AOP编程的支持
   + 声明式事务
   + 方便测试
   + 方便继承别的框架
   + 降低JavaEE API的使用难度

### 1.1 Spring的体系结构

核心容器Core Container：Beans、Core、Context、SpEL【IoC部分】

开发包的目录结构：
开发包：xxx-dist，docs：文档，schema：约束，libs：jar包

## 2 IoC

### 2.1 IoC的概念与作用

1. 耦合

程序间的依赖关系。有类之间的依赖和方法间的依赖。

在程序中使用new一个类的对象的方法，如果没有导包，编译就会报错，耦合度高

2. 解耦

+ 实际开发中做到：编译期不依赖，运行时才依赖。

2.1 利用反射解耦

+ Class.forName()进行驱动注册就是进行了解耦。利用反射。

2.2. 工厂模式解耦

用一个类（工厂）来读取配置，生成对象并存放，然后需要的时候再调用。

+ 用new的方式去获得对象，当前程序是主动的。
+ 使用工厂时，由工厂来查找或创建对象，当前程序是被动的。
+ 解除了当前程序与对象类之间的直接关联

3. IoC的概念

Iversion of Control，控制反转，把创建对象的权利交给框架。

4. Ioc的作用

减少耦合

### 2.2 工厂模式解耦案例

创建Bean对象的工厂

Bean：可重用组件
JavaBean：用java语言写的可重用组件，JavaBean>实体类

#### 2.2.1 步骤

1. 定义配置文件，里面包含唯一标识与全类名的键值对
2. 用类加载器加载配置文件，获取类名
3. 反射获取实例
4. 提供方法返回一个实例

#### 2.2.2 问题：单例和多例

+ 单例和多例：通过工厂取出来的是同一个对象还是不同的对象。

+ 每次都根据传进来的表示获取类吗，然后创建类的对象是多例。

+ 要实现单例的话：
  成员变量里定义一个容器，如Map，在静态代码块中创建容器，遍历配置文件，依次创建每个类的对象放入容器中。【放入一个容器是为了防止被Java垃圾清理机制把对象删掉】

## 3 XML配置的IoC

### 3.1 基于XML的入门案例

1. pom.xml导入Spring坐标：spring-context
2. resources下新建一个bean.xml文件
3. 导入约束，在文档中有【docs/reference/index.html打开文档网页】，搜索xmlns
4. 在bean.xml里设置，让Spring管理资源

```
<!-- 配置service -->
<bean id="accountService" class="com.itheima.service.impl.AccountServiceImpl"></bean>

<!-- 配置dao -->
<bean id="accountDao" class="com.itheima.dao.impl.AccountDaoImpl"></bean>
```
bean 标签：用于配置让spring 创建对象，并且存入ioc 容器之中
id 属性：对象的唯一标识。
class 属性：指定要创建对象的全限定类名

5. 使用
+ 获取IoC的核心容器，然后根据标识id获取对象
```
//1.使用ApplicationContext 接口，就是在获取spring 容器
ApplicationContext ac = new ClassPathXmlApplicationContext("bean.xml");

//2.根据bean 的id 获取对象
IAccountService aService = (IAccountService) ac.getBean("accountService");

IAccountDao aDao = (IAccountDao) ac.getBean("accountDao");

System.out.println(aService);
System.out.println(aDao);
```

### 3.2 Spring工厂的类

#### 3.2.1 BeanFactory与ApplicationContext

+ BeanFactory是Spring容器的顶层接口
+ ApplicationContext是它的子接口
+ 二者的区别：
    创建对象的时间点不一样。
    + ApplicationContext：只要一读取配置文件，默认情况下就会创建对象。
      单例对象使用	开发中更多采用此接口
    + BeanFactory：什么使用什么时候创建对象。
      多例对象使用

#### 3.2.2 ApplicationContext的三个常用实现类

三个常用实现类：
+ ClassPathXmlApplicationContext：
  加载类路径下的配置文件，配置文件必须在类的根路径下。推荐使用
+ FileSystemXmlApplicationContext：
  从磁盘路径上加载配置文件，配置文件可以在磁盘的任意位置。
+ AnnotationConfigApplicationContext:
  使用注解配置容器对象时，需要使用此类来创建spring 容器。它用来读取注解。

### 3.3 Spring中对Bean的管理

#### 3.3.1 创建Bean的三种方式

##### 3.3.1.1 第一种方式：使用默认构造函数创建

在bean.xml配置文件中，使用bean标签，设置id和class属性，且没有其他属性和标签时。采用的就是默认构造函数来创建bean对象。如果bean 中没有默认无参构造函数，将会创建失败。
```
<bean id="accountService" class="com.itheima.service.impl.AccountServiceImpl"/>
```

##### 3.3.1.2 第二种方式：使用普通工厂中的方法创建对象

使用某个类中的方法创建对象，并存入Spring容器

```
<bean id="instancFactory" class="com.itheima.factory.InstanceFactory"></bean>

<bean id="accountService"
factory-bean="instancFactory"
factory-method="createAccountService"></bean>
```
先写的是工厂，然后写通过工厂的方法获取bean

factory-bean 属性：用于指定实例工厂bean 的id。
factory-method 属性：用于指定实例工厂中创建对象的方法。

##### 3.3.1.3 使用工厂中的静态方法创建对象

使用某个类的静态方法创建对象，并存入Spring容器

```
<bean id="accountService"
class="com.itheima.factory.StaticFactory"
factory-method="createAccountService"></bean>
```
静态的只需要写一行【感觉第二种也可以只写一行】

#### 3.3.2 bean的作用范围调整

+ bean在通常情况下都是单例的bean
+ 用scope属性来指定作用范围
```
singleton：单例的，默认值
prototype：多例的
request：web应用的请求范围
session：web应用的会话范围
global-session：集群环境的会话范围（全局会话范围），不是集群环境时，就是session
```
集群环境：可能会有多个服务器组成一个集群，请求会在负载均衡的地方转发到不同的服务器。如验证码就需要存在global-session里，第一次获取的时候可能是机器A，输入好提交后可能会连接到机器B。

#### 3.3.3 bean对象的生命周期

+ 单例对象：
   + 出生：当容器创建时对象出生
   + 活着：容器还在，对象就活着
   + 死亡：容器销毁，对象死亡
   + 总结：单例对象的生命周期和容器相同
+ 多例对象：
   + 出生：使用对象的时候，由Spring创建
   + 活着：使用过程中或者
   + 死亡：长时间不用，且没有别的对象引用时，由Java的垃圾回收器回收。

另外：bean标签有两个属性，可以指定类中的2个方法，作为初始化方法和销毁方法。
+ init-method：指定类中的初始化方法名称。
+ destroy-method：指定类中销毁方法名称。

### 3.4 依赖注入

+ 依赖注入：Dependency Injection
+ 我们编写程序通过IoC降低了耦合，把对象的创建交给了Spring，但是不可能没有依赖，所以在配置文件中说明这些依赖。
+ 依赖关系的维护就叫做依赖注入。
+ 能注入的类型
   + 基本类型和String
   + 其他bean类型（在配置文件中或注解配置过的bean）
   + 复杂类型/集合类型
+ 注入的方式
   + 第一种：使用构造函数提供
   + 第二种：使用set方法提供
   + 第三种：使用注解提供

#### 3.4.1 构造函数注入

使用标签constructor-arg传递构造函数的参数。
属性：
```
给谁赋值：
    index:指定参数在构造函数参数列表的索引位置
    type:指定参数在构造函数中的数据类型
    name:指定参数在构造函数中的名称用这个找给谁赋值		【常用】

赋什么值
    value:它能赋的值是基本数据类型和String 类型
    ref:它能赋的值是其他bean 类型，也就是说，必须得是在配置文件中配置过的bean
```
```
<bean id="accountService" class="com.itheima.service.impl.AccountServiceImpl">
    <constructor-arg name="name" value="张三"></constructor-arg>
    <constructor-arg name="age" value="18"></constructor-arg>
    <constructor-arg name="birthday" ref="now"></constructor-arg>
</bean>

<bean id="now" class="java.util.Date"></bean>
```
+ 优点：获取bean对象的时候，必须注入相应的参数数据。
+ 弊端：改变了bean对象的实例化方式，哪怕用不到的数据也必须提供。

#### 3.4.2 set 方法注入

在类中提供需要注入成员的set 方法
涉及的标签：property
属性：
```
name：写的是类中set 方法后面的部分
ref：给属性赋值是其他bean 类型的
value：给属性赋值是基本数据类型和string 类型的
```

+ 实际开发中，此种方式用的较多。

```
<bean id="accountService" class="com.itheima.service.impl.AccountServiceImpl">
    <property name="name" value="test"></property>
    <property name="age" value="21"></property>
    <property name="birthday" ref="now"></property>
</bean>

<bean id="now" class="java.util.Date"></bean>
```

+ 优势：创建对象没有明确限制，可以直接使用默认构造函数
+ 弊端：如果有某个成员必须有值，则获取对象时，有可能没传入值。

#### 3.4.3 注入集合数据

数组、List、Set、Map、Properties

+ 其中：
  数组、List、Set可以用同样的标签（可以互换）
  Map、Properties可以用同样的写法

1. 数组
```
<bean id="accountService" class="com.itheima.service.impl.AccountServiceImpl">
    <property name="myStrs">
        <array>
            <value>AAA</value>
            <value>BBB</value>
            <value>CCC</value>
        </array>
    </property>
</bean>
```

2. List
```
<bean id="accountService" class="com.itheima.service.impl.AccountServiceImpl">
    <property name="myStrs">
        <list>
            <value>AAA</value>
            <value>BBB</value>
            <value>CCC</value>
        </list>
    </property>
</bean>
```

3. Set
```
<bean id="accountService" class="com.itheima.service.impl.AccountServiceImpl">
    <property name="myStrs">
        <set>
            <value>AAA</value>
            <value>BBB</value>
            <value>CCC</value>
        </set>
    </property>
</bean>
```

4. Map
```
<bean id="accountService" class="com.itheima.service.impl.AccountServiceImpl">
    <property name="myProps">
        <map>
            <entry key="testA" value="aaa"></entry>
            <entry key="testB">
                <value>bbb</value>
            </entry>
        </map>
    </property>
</bean>
```
entry有两种写法，都可以

5. Properties
```
<bean id="accountService" class="com.itheima.service.impl.AccountServiceImpl">
    <property name="myMap">
        <props>
            <prop key="testA">aaa</prop>
            <prop key="testB">bbb</prop>
        </props>
    </property>
</bean>
```

## 4 注解配置的IoC

### 4.1 常用注解

#### 4.1.1 用于创建对象的

相当于xml中的bean标签
```
@Component
	写在类名上。作用：把当前类对象存入Spring容器中。
	
	属性：
		value：指定bean的id，不写默认为首字母小写的类名。
		
@Controller		一般用于表现层
@Service		业务层
@Repository		持久层
这三个注解与Component一模一样，只是为了与三层架构对应的注解。
```

#### 4.1.2 用于注入数据的

相当于property标签
```
@Autowired
	可以写在变量上，也可以写在方法上。可以写在很多地方。
	作用：自动按照类型注入。
	当容器中只有唯一一个bean对象类型和要注入的变量类型匹配的时候，可以注入成功。如果有多个匹配，根据变量名称作为bean的id进行查找，有则可以注入，否则失败。
	可以不写成员变量的set方法。


@Qualifier
	作用：在自动按照类型注入的基础之上，再按照Bean 的id 注入。
	给字段注入时不能独立使用，必须和@Autowire 一起使用
	给方法参数注入时，可以独立使用。
    	属性：
    	value：指定bean 的id。


@Resource
	作用：直接按照Bean 的id 注入。可以独立使用。
        属性：
        name：指定bean 的id。

以上三个注解都只能注入bean类型，集合类型的注入只能通过XML注入。

@Value
    作用：注入基本数据类型和String 类型数据的
        属性：
        value：用于指定值。可以使用Spring的spEL（Spring的EL表达式）
```
+ spEL的写法：```${表达式}```

#### 4.1.3 用于改变作用范围的

```
@Scope
	作用：指定bean 的作用范围。
    属性：
    value：指定范围的值。
        取值：singleton prototype request session globalsession
```

#### 4.1.4 和生命周期相关（了解）

```
@PostConstruct
	作用：用于指定初始化方法。

@PreDestroy
	作用：用于指定销毁方法。
```

### 4.2 在bean.xml配置文件中开启对注解的支持

+ 导入约束，在文档中搜索xmlns:context
```
<!-- 告知spring 创建容器时要扫描的包-->
<context:component-scan base-package="com.itheima"></context:component-scan>
```
+ 这种情况下，创建Spring容器依旧使用ClassPathXmlApplicationContext，并传入bean.xml

### 4.3 纯注解

#### 4.3.1 新注解说明

+ 先新建主配置类SpringConfiguration

```
@Configuration
	加在类前，表示该类是一个配置类
	当该类为AnnotationConfigApplicationContext传入的参数时，该注释可以不写
	
@ComponentScan
	作用：用于指定spring 在初始化容器时要扫描的包。与context：component-scan标签作用一样
	属性：
		basePackages/value：用于指定要扫描的包。【两个互为别名】

	作用和在spring 的xml 配置文件中的：
<context:component-scan base-package="com.itheima"/>是一样的。
属性：

@Bean
    作用：该注解只能写在方法上，表明使用此方法创建一个对象，并且放入spring 容器。（创建方法的返回值对象）
        属性：
        name：给当前@Bean 注解方法创建的对象指定一个名称(即bean 的id）。不写默认是方法名称
        注意：使用注解配置方法时，如果方法有参数，Spring框架会去容器中查找有没有可用的bean对象，查找方式与Autowired一样
```

#### 4.3.2 删除bean.xml后获取Spring容器的方法

+ 这种情况下，创建Spring容器要使用AnnotationConfigApplicationContext，并传入SpringConfiguration.class

#### 4.3.3 多个配置类

+ 方法一：所有配置类都传入AnnotationConfigApplicationContext【此时可以都不写Configuration注解】
+ 方法二：没传入容器对象创建的类都加上Configuration注解，并在主配置类的ComponentScan注解中加上对应的包名
+ 方法三：在主配置类里用import注解导入其他小配置类。
```
@Import
	作用：用于导入其他配置类
        属性：
        value[]：用于指定其他配置类的字节码。
```

### 4.4 关于Spring 注解和XML 的选择问题

+ 注解的优势：配置简单，维护方便（我们找到类，就相当于找到了对应的配置）。
+ XML 的优势：修改时，不用改源码。不涉及重新编译和部署。

+ 怎么方便怎么来

### 4.5 数据库连接相关问题

+ 创建一个数据库连接的配置类
+ 定义成员变量，在上面加上value注解，里面用el表达式```${key}```
+ 在主配置类上加PropertySource注解，载入配置文件

```
@PropertySource
	作用：用于加载.properties 文件中的配置。例如我们配置数据源时，可以把连接数据库的信息写到properties 配置文件中，就可以使用此注解指定properties 配置文件的位置。
        属性：
        value[]：用于指定properties 文件位置。如果是在类路径下，需要写上classpath:
```

### 4.6 Spring整合Junit

1. 导入jar包坐标spring-test
2. 用Junit提供的注解替换原本Junit的main方法。
3. 告知Spring，IoC是基于xml还是基于注解的，并说明位置
4. 使用@Autowired 给测试类中的变量注入数据

```
@RunWith	
	写在测试类的前面，传入SpringJunit4ClassRunner.class
```
```
@ContextConfiguration
	写在测试类的前面。
        locations 属性：用于指定配置文件的位置。如果是类路径下，需要用classpath:表明
        classes 属性：用于指定注解的类。当不使用xml 配置时，需要用此属性指定注解类的位置。（主配置文件或主配置类）
```

## 5 AOP面向切面编程介绍

+ Aspect Oriented Programming，面向切面编程
+ 简单的说它就是把我们程序重复的代码抽取出来，在需要执行的时候，使用动态代理的技术，在不修改源码的基础上，对我们的已有方法进行增强。

+ 优势：
   + 减少重复代码
   + 提高开发效率
   + 维护方便

+ AOP 的实现方式：使用动态代理技术

### 5.1 动态代理

#### 5.1.1 基于接口的动态代理

+ 提供者：JDK 官方的Proxy 类。
+ 要求：被代理类最少实现一个接口。

##### 5.1.1.1 代理对象创建

+ 创建的方式
```
Proxy.newProxyInstance(ClassLoader,Interfaces,InvocationHandler)
参数含义：
	ClassLoader：和被代理对象使用相同的类加载器。
	Interfaces：和被代理对象具有相同的行为。实现相同的接口。
	InvocationHandler：如何代理。

写法固定：
Proxy.newProxyInstance(被代理类.getClass().getClassLoader(),
						被代理类.getClass().getInterfaces(),
						new InvocationHandler() {
						@Override
						public Object invoke(Object proxy, Method method, Object[] args){ ... }
						})
```

##### 5.1.1.2 invoke方法

+ Invoke方法：执行被代理对象的任何方法，都会经过该方法。此方法有拦截的功能。

+ 参数：
   + proxy：代理对象的引用。不一定每次都用得到
   + method：当前执行的方法对象
   + args：执行方法所需的参数
+ 返回值：当前执行方法的返回值
+ 注意该方法的try...catch要抓Throwable

#### 5.1.2 基于子类的动态代理

+ 提供者：第三方的CGLib，需要导包cglib。如果报asmxxxx 异常，需要导入asm.jar。
+ 要求：被代理类不能用final 修饰的类（最终类）。

##### 5.1.2.1 代理对象创建

+ 用到的类：Enhancer
+ 用到的方法：create(Class, Callback)
+ 方法的参数：
   + Class：被代理对象的字节码
   + Callback：如何代理，一个接口。一般用其子接口实现类：MethodInterceptor

```
Enhancer.create(actor.getClass(),new MethodInterceptor() {
    @Override
    public Object intercept(Object proxy, Method method, Object[] args,
    MethodProxy methodProxy) throws Throwable { ... }
})
```

##### 5.1.2.2 intercept方法

执行被代理对象的任何方法，都会经过该方法。在此方法内部就可以对被代理对象的任何方法进行增强。

+ 参数：
   + 前三个和基于接口的动态代理是一样的。
   + MethodProxy：当前执行方法的代理对象。
+ 返回值：当前执行方法的返回值

## 6 Spring 中的AOP

+ Spring会根据目标类是否有接口来决定使用哪种动态代理的方式

### 6.1 相关术语

+ Joinpoint(连接点):
  所谓连接点是指那些被拦截到的点。在spring 中,这些点指的是方法,因为spring 只支持方法类型的连接点。【所有能被拦截到的方法】
+ Pointcut(切入点):
  所谓切入点是指我们要对哪些Joinpoint 进行拦截的定义。【真正被增强的方法，在动态代理里可以通过判断方法名，选择一部分方法不进行增强】
+ Advice(通知/增强):
  所谓通知是指拦截到Joinpoint 之后所要做的事情就是通知。
   通知的类型：
   + 前置通知
   + 后置通知
   + 异常通知
   + 最终通知
   + 环绕通知
+ Introduction(引介):
  引介是一种特殊的通知在不修改类代码的前提下, Introduction 可以在运行期为类动态地添加一些方法或Field。
+ Target(目标对象):
  代理的目标对象。
+ Weaving(织入):
  是指把增强应用到目标对象来创建新的代理对象的过程。
   + spring 采用动态代理织入，而AspectJ 采用编译期织入和类装载期织入。
+ Proxy（代理）:
  一个类被AOP 织入增强后，就产生一个结果代理类。
+ Aspect(切面):
  是切入点和通知（引介）的结合。切入点方法和通知里的增强方法调用时的对应关系，配置关系。

### 6.2 基于XML 的AOP 配置

#### 6.2.1 案例

案例：在service层的各个方法上加上Logger里的方法打印日志

1. pom导包：spring-context和aspectjweaver【解析切入点表达式】
2. 在bean.xml里导入aop的约束：搜索```xmlns:aop```
3. 用IoC把相关对象配置进来
4. AOP配置：```aop:config```
5. 配置切面
6. 配置通知类型
```
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:aop="http://www.springframework.org/schema/aop"
        xsi:schemaLocation="http://www.springframework.org/schema/beans
                http://www.springframework.org/schema/beans/spring-beans.xsd
                http://www.springframework.org/schema/aop
                http://www.springframework.org/schema/aop/spring-aop.xsd">

    <!-- 配置service -->
    <bean id="accountService" class="com.itheima.service.impl.AccountServiceImpl"></bean>

    <!-- 配置Logger -->
    <bean id="logger" class="com.itheima.utils.Logger"></bean>

    <!-- 配置AOP -->
    <aop:config>
        <aop:aspect id="logAdvice" ref="logger">
            <aop:before method="printLog" pointcut=“execution(public void com.itheima.service.impl.AccountServiceImpl.saveAccount())"></aop:before>
        </aop:aspect>
    </aop:config>
```
#### 6.2.2 标签说明

+ ```aop:config```
  作用：用于声明开始aop 的配置

+ ```aop:aspect```
  作用：用于配置切面。
  属性：
   + id：给切面提供一个唯一标识。
   + ref：引用配置好的通知类bean 的id。

+ ```aop:before```
  作用：  用于配置前置通知。执行时间点：  切入点方法执行之前
  属性：
   + method：用于指定通知类中的增强方法名称
   + ponitcut-ref：用于指定切入点的表达式的引用
   + **poinitcut**：用于指定切入点表达式
   作用：  用于配置切入点表达式。就是指定对哪些类的哪些方法进行增强。
   属性：
       + expression：用于定义切入点表达式。
       + id：用于给切入点表达式提供一个唯一标识

#### 6.2.3 切入点表达式

语法：
```
execution(表达式)

表达式语法：
[修饰符] 返回值类型 包名.类名.方法名(参数列表)

如：
public void com.itheima.service.impl.AccountServiceImpl.saveAccount(com.itheima.domain.Account)

表达式的省略写法：
1. 访问修饰符可以省略
2. 返回值可以使用*号，表示任意返回值
3. 包名可以使用*号，表示任意包，但是有几级包，需要写几个*
4. 使用..来表示当前包，及其子包
5. 类名可以使用*号，表示任意类
6. 方法名可以使用*号，表示任意方法
7. 参数列表可以使用*，表示参数可以是任意数据类型，但是必须有参数
8. 参数列表可以使用..表示有无参数均可，有参数可以是任意类型


全通配方式：
* *..*.*(..)

通常情况下，我们都是对业务层的方法进行增强，所以切入点表达式都是写到业务层实现类。
execution(* com.itheima.service.impl.*.*(..))
```

切入点表达式的配置：id用于指定唯一标识，expression属性用于指定表达式内容，配置通知的时候就可以用pointcut-ref来引用
```
<aop:pointcut id="pt1" expression="execution(*.com.itheima.service.impl.*.*(..))" />
```
切入点表达式还可以写在外面，使所有切面都可用，但是一定要写在切面配置前面【有约束】

#### 6.2.4 通知类型

+ aop:before：前置通知
+ aop:after-returning ：后置通知
  切入点方法正常执行之后。它和异常通知只能有一个执行
+ aop:after-throwing：异常通知
+ aop:after：最终通知
  无论切入点方法执行时是否有异常，它都会在其后面执行。
+ aop:around：环绕通知

##### 6.2.4.1 环绕通知

```
<!-- 配置环绕通知-->
<aop:around method="transactionAround" pointcut-ref="pt1"/>
```

+ 它是spring 框架为我们提供的一种可以在代码中手动控制增强代码什么时候执行的方式。
+ 通常情况下，环绕通知都是独立使用的
+ spring 框架为我们提供了一个接口：ProceedingJoinPoint，它可以作为环绕通知的方法参数。
+ 在环绕通知执行时，spring 框架会为我们提供该接口的实现类对象，我们直接使用就行。

```
//环绕通知指定的方法
public Object transactionAround(ProceedingJoinPoint pjp) {
    //定义返回值
    Object rtValue = null;
    try {
        //获取方法执行所需的参数
        Object[] args = pjp.getArgs();
        	//前置通知：开启事务
        beginTransaction();
        //执行方法
        rtValue = pjp.proceed(args);//明确调用业务层的方法（切入点方法）
        	//后置通知：提交事务
        commit();
    }catch(Throwable e) {
        	//异常通知：回滚事务
        rollback();
        e.printStackTrace();
    }finally {
        	//最终通知：释放资源
        release();
    }
    return rtValue;
}
```

### 6.3 基于注解的AOP 配置

1. bean.xml里导入约束【IoC需要依赖于注解】
2. 配置要扫描注解的包
```
<!-- 告知spring，在创建容器时要扫描的包-->
<context:component-scan base-package="com.itheima"></context:component-scan>
```
3. 给bean对象加注解
4. AOP注解配置：
```
@Aspect
	表示当前类是一个切面类，配置在Logger类上
	
@Before：前置通知，注意别选错包
@AfterReturning：后置通知
@AfterThrowing：异常通知
@After：最终通知
@Around：环绕通知

@Pointcut：切入点表达式

@Pointcut("excution(* com.itheima.service.impl.*.*(..))")
private void pt1(){}

其他通知引用：
@Before(pt1())
```
5. 在beam.xml配置文件中开启spring 对注解AOP 的支持
```
<!-- 开启spring 对注解AOP 的支持-->
<aop:aspectj-autoproxy/>
```
+ 注意：注解配置的时候，最终通知在后置通知/异常通知前执行
+ 完全不使用XML 的配置方式：在主配置类上加注解@EnableAspectJAutoProxy
```
@Configuration
@ComponentScan(basePackages="com.itheima")
@EnableAspectJAutoProxy
public class SpringConfiguration {
...}
```

## 7 JdbcTemplate

+ 使用需要导入spring-jdbc
+ 作用：和数据库交互，实现对表的CRUD

### 7.1 使用步骤

1. 获取容器
2. 获取JdbcTemplate对象
3. 执行语句```execute```

### 7.2 JdbcTemplate

```
<!-- 配置一个数据库的操作模板：JdbcTemplate -->
<bean id="jdbcTemplate" class="org.springframework.jdbc.core.JdbcTemplate">
    <property name="dataSource" ref="dataSource"></property>
</bean>
```

### 7.3 spring内置的DataSource

spring 框架也提供了一个内置数据源
```
<bean id="dataSource"
class="org.springframework.jdbc.datasource.DriverManagerDataSource">
    <property name="driverClassName" value="com.mysql.jdbc.Driver"></property>
    <property name="url" value="jdbc:mysql:///spring_day02"></property>
    <property name="username" value="root"></property>
    <property name="password" value="1234"></property>
</bean>
```

### 7.4 数据库连接信息配到配置文件中

```
【引入外部的属性文件】
一种方式:
<!-- 引入外部属性文件：-->
<bean
class="org.springframework.beans.factory.config.PropertyPlaceholderConfigurer">
<property name="location" value="classpath:jdbc.properties"/>
</bean>
另一种方式:
<context:property-placeholder location="classpath:jdbc.properties"/>

```

### 7.5 SpringTemplate的CRUD

保存、更新、删除：```update```

查询：```query```
查询需要传入一个RowMapper，一般用```new BeanPropertyRowMapper<>()```

聚合函数：```queryForObject```

### 7.6 在Dao中使用SpringTemplate

定义SpringTemplate对象，用IoC注入【注解或xml均可】


但是这样每个Dao里都得写一段定义对象的代码，故可以继承JdbcDaoSupport来简化代码。
+ JdbcDaoSupport 是spring 框架为我们提供的一个类，该类中定义了一个JdbcTemplate 对象，我们可以直接获取使用，但是要想创建该对象，需要为其提供一个数据源【通过xml配置】

## 8 Spring的事务控制

+ 使用需要导入spring-tx

+ 在业务层控制事务

### 8.1 事务控制的API

```PlatformTransactionManager```接口提供方法：
```
TransactionStatus getTransaction(TransactionDefinition definition)
	获取事务状态信息

void commit(TransactionStatus status)
	提交事务

void rollback(TransactionStatus status)
	回滚事务
```

实现类：
```org.springframework.jdbc.datasource.DataSourceTransactionManager```使用Spring JDBC 或iBatis 进行持久化数据时使用

#### 8.1.1 事务的定义信息

接口```TransactionDefinition```是事务的定义信息对象

+ 有方法：
```
String getName()
	获取事务对象名称

int getIsolationLevel()
	获取事务隔离级：Spring默认使用数据库的隔离级别

int getPropagationBehavior()
	获取事务传播行为：什么情况下必须有事务，什么情况下可以没有，有很多值

int getTimeout()
	获取事务超时时间
	默认值是-1，没有超时限制。如果有，以秒为单位进行设置。

boolean isReadOnly()
	获取事务是否只读
	建议查询时设置为只读。
```

+ 事务的传播行为（有很多，这里只关心两个）：

```
REQUIRED:如果当前没有事务，就新建一个事务，如果已经存在一个事务中，加入到这个事务中。一般的选
择（默认值）
SUPPORTS:支持当前事务，如果当前没有事务，就以非事务方式执行（没有事务）
：使用当前的事务，如果当前没有事务，就抛出异常
```

#### 8.1.2 运行状态

```TransactionStatus```
此接口提供的是事务具体的运行状态，方法介绍如下图：

```
void flush()
	刷新事务

boolean hasSavepoint()
	获取是否存在存储点

isCompleted()
	获取事务是否完成

isNewTransaction()
	获取事务是否为新的事务

isRollbackOnly()
	获取事务是否回滚

setRollbackOnly()
	设置事务回滚
```

### 8.2 配置事务控制

#### 8.2.1 基于XML的声明式事务管理

+ 第一步：配置事务管理器
```
<!-- 配置一个事务管理器-->
<bean id="transactionManager" class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
    <!-- 注入DataSource -->
    <property name="dataSource" ref="dataSource"></property>
</bean>
```

+ 第二步：配置事务的通知
引用事务管理器
要导入事务的约束，在文档的Data Access里搜索（之前都是在Core里）```xmlns:tx```
```
<!-- 配置事务的通知-->
<tx:advice id="txAdvice" transaction-manager="transactionManager"></tx:advice>
```
```
id：给事务通知起一个唯一标识
transaction-manager：给事务通知提供一个事务管理器引用
```

+ 第三步：配置事务的属性
```
<!--在tx:advice 标签内部配置事务的属性-->
<tx:advice ...>
	<!--配置事务的属性-->
    <tx:attributes>
        <tx:method name="*" read-only="false" propagation="REQUIRED"/>
        <tx:method name="find*" read-only="true" propagation="SUPPORTS"/>
    </tx:attributes>
</tx:advice>
```
```
read-only：是否是只读事务。默认false，不只读。
isolation：指定事务的隔离级别。默认值是使用数据库的默认隔离级别。default
propagation：指定事务的传播行为。
timeout：指定超时时间。默认值为：-1。永不超时。
rollback-for：用于指定一个异常，当执行产生该异常时，事务回滚。产生其他异常，事务不回滚。没有默认值，任何异常都回滚。
no-rollback-for：用于指定一个异常，当产生该异常时，事务不回滚，产生其他异常时，事务回滚。没有默认值，任何异常都回滚。
```

+ 第四步：配置AOP 切入点表达式
```
<!-- 配置aop -->
<aop:config>
    <!-- 配置切入点表达式-->
    <aop:pointcut id="pt1" expression="execution(* com.itheima.service.impl.*.*(..))">
</aop:config>
```

+ 第五步：配置切入点表达式和事务通知的对应关系
```
<!-- 在aop:config 标签内部：建立事务的通知和切入点表达式的关系-->
<aop:advisor advice-ref="txAdvice" pointcut-ref="pt1"/>
```

#### 8.2.2 基于注解的配置方式

1. 把ioc导成注解（记得约束）

2. 配置事务管理器
```
<bean id="transactionManager"
class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
<property name="dataSource" ref="dataSource"></property>
</bean>
```

3. 开启spring对注解事务的支持
```
<!-- 开启spring 对注解事务的支持-->
<tx:annotation-driven transaction-manager="transactionManager"/>
```

4. 在业务层使用```@Transactional```注解（实现类上）

+ 属性可以在这里配置

+ 该注解的属性和xml 中的属性含义一致。该注解可以出现在接口上，类上和方法上。
   + 出现接口上，表示该接口的所有实现类都有事务支持。
   + 出现在类上，表示类中所有方法有事务支持
   + 出现在方法上，表示方法有事务支持。

以上三个位置的优先级：方法>类>接口

+ 可以在类上配个只读，然后在里面配读写型

# Spring MVC

## 1 基本概念

基于Java实现的MVC设计模型的请求驱动类型的轻量级WEB框架。

+ SpringMVC在三层架构中的位置：表现层框架

### 1.1 三层架构

+ 服务器端程序，一般都基于两种形式，一种C/S架构程序，一种B/S架构程序
+ 使用Java语言基本上都是开发B/S架构的程序，B/S架构又分成了三层架构

+ 三层架构
1. 表现层：WEB层，用来和客户端进行数据交互的。表现层一般会采用MVC的设计模型
2. 业务层：处理公司具体的业务逻辑的
3. 持久层：用来操作数据库的

### 1.2 MVC模型

+ MVC全名是Model View Controller 模型视图控制器，每个部分各司其职。
+ Model：数据模型，JavaBean的类，用来进行数据封装。
+ View：指JSP、HTML用来展示数据给用户
+ Controller：用来接收用户的请求，整个流程的控制器。用来进行数据校验等。

## 2 入门案例

### 2.1 入门程序的编写
#### 2.1.1 引入jar包

```
<!-- 版本锁定-->
<properties>
    <spring.version>5.0.2.RELEASE</spring.version>
</properties>
```

+ spring-context
+ spring-web
+ spring-webmvc
+ servlet-api
+ jsp-api

#### 2.1.2 配置核心控制器DispatcherServlet

在web.xml配置文件中核心控制器DispatcherServlet
```
<!-- SpringMVC的核心控制器-->
<servlet>
    <servlet-name>dispatcherServlet</servlet-name>
    <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-
    class>

    <!-- 配置Servlet的初始化参数，读取springmvc的配置文件，创建spring容器-->
    <init-param>
        <param-name>contextConfigLocation</param-name>
        <param-value>classpath:springmvc.xml</param-value>
    </init-param>

    <!-- 配置servlet启动时加载对象-->
    <load-on-startup>1</load-on-startup>
</servlet>

<servlet-mapping>
    <servlet-name>dispatcherServlet</servlet-name>
    <url-pattern>/</url-pattern>
</servlet-mapping>
```

#### 2.1.3 编写springmvc.xml的配置文件

在resources文件夹下

```
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
    xmlns:mvc="http://www.springframework.org/schema/mvc"
    xmlns:context="http://www.springframework.org/schema/context"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="
        http://www.springframework.org/schema/beans
        http://www.springframework.org/schema/beans/spring-beans.xsd
        http://www.springframework.org/schema/mvc
        http://www.springframework.org/schema/mvc/spring-mvc.xsd
        http://www.springframework.org/schema/context
        http://www.springframework.org/schema/context/spring-context.xsd">

    <!-- 配置spring创建容器时要扫描的包，IoC-->
    <context:component-scan base-package="com.itheima"></context:component-scan>

    <!-- 配置视图解析器-->
    <bean id="viewResolver" class="org.springframework.web.servlet.view.InternalResourceViewResolver">
        <property name="prefix" value="/WEB-INF/pages/"></property>
        <property name="suffix" value=".jsp"></property>
    </bean>
    
    <!-- 配置spring开启注解mvc的支持
    <mvc:annotation-driven></mvc:annotation-driven>-->
</beans>
```

#### 2.1.4 编写index.jsp和HelloController控制器类
##### 2.1.4.1 index.jsp
```
<body>
    <h3>入门案例</h3>
    <a href="${ pageContext.request.contextPath }/hello">入门案例</a>
</body>
```

##### 2.1.4.2 HelloController
```
/**
* 控制器
*/
@Controller
public class HelloController {
    /**
    * 接收请求
    * @return
    */
    @RequestMapping(path="/hello")
    public String sayHello() {
        System.out.println("Hello SpringMVC!!");
        return "success";
    }
}
```

#### 2.1.5 在WEB-INF目录下创建pages文件夹，编写success.jsp的成功页面

```
<body>
<h3>入门成功！！</h3>
</body>
```

#### 2.1.6 启动Tomcat服务器，进行测试

### 2.2 入门案例的执行过程分析

#### 2.2.1 入门案例的执行流程

1. 当启动Tomcat服务器的时候，因为配置了load-on-startup标签，所以会创建DispatcherServlet对象，就会加载springmvc.xml配置文件
2. 开启了注解扫描，那么HelloController对象就会被创建
3. 从index.jsp发送请求，请求会先到达DispatcherServlet核心控制器，根据配置@RequestMapping注解找到执行的具体方法
4. 根据执行方法的返回值，再根据配置的视图解析器，去指定的目录下查找指定名称的JSP文件
5. Tomcat服务器渲染页面，做出响应

#### 2.2.2 入门案例中的组件

1. 前端控制器（DispatcherServlet）【控制整个流程的执行】

2. 处理器映射器（HandlerMapping）【通过url，找到处理器中具体的某个方法】

3. 处理器（Handler）【也叫Controller】

4. 处理器适配器（HandlAdapter）【适配Controller，执行方法】

5. 视图解析器（View Resolver）【页面跳转】

6. 视图（View）

#### 2.2.3 mvc:annotation-driven标签

在SpringMVC 的各个组件中，处理器映射器、处理器适配器、视图解析器称为SpringMVC 的三大组件。
使用```<mvc:annotation-driven>```可以自动加载RequestMappingHandlerMapping （处理映射器）和RequestMappingHandlerAdapter （处理适配器）

## 3 RequestMapping注解

+ 作用：是建立请求URL和处理方法之间的对应关系

+ RequestMapping注解可以作用在方法和类上
   1. 作用在类上：第一级的访问目录
   2. 作用在方法上：第二级的访问目录
   3. 细节：路径可以不编写/表示应用的根目录开始
   4. 细节：${ pageContext.request.contextPath }也可以省略不写，但是路径上不能写/

+ RequestMapping的属性
   1. path：指定请求路径的url
   2. value：value属性和path属性是一样的
   3. mthod：指定该方法的请求方式
   4. params：指定限制请求参数的条件
   5. headers：发送的请求中必须包含的请求头

## 4 请求参数的绑定

### 4.1 请求参数的绑定说明

#### 4.1.1 绑定机制

1. 表单提交的数据都是k=v格式的	username=haha&password=123
2. SpringMVC的参数绑定过程是把表单提交的请求参数，作为控制器中方法的参数进行绑定的
3. 要求：提交表单的name和参数的名称是相同的

#### 4.1.2 支持的数据类型

1. 基本数据类型和字符串类型
2. 实体类型（JavaBean）
3. 集合数据类型（List、map集合等）

### 4.2 不同类型的参数绑定

#### 4.2.1 基本数据类型和字符串类型

1. 提交表单的name和参数的名称相同
2. 区分大小写

#### 4.2.2 实体类型（JavaBean）

1. 提交表单的name和JavaBean中的属性名称需要一致
2. 如果一个JavaBean类中包含其他的引用类型，那么**表单的name属性**需要编写成：对象.属性例如：```address.name```

### 4.2.3 给集合属性数据封装

JSP页面编写方式：```list[0].属性```，```map['key'].value```

### 4.3 请求参数中文乱码的解决

在web.xml中配置Spring提供的过滤器类
```
<!-- 配置过滤器，解决中文乱码的问题-->
<filter>
    <filter-name>characterEncodingFilter</filter-name>
    <filter-class>org.springframework.web.filter.CharacterEncodingFilter</filter-
    class>
    <!-- 指定字符集-->
    <init-param>
        <param-name>encoding</param-name>
        <param-value>UTF-8</param-value>
    </init-param>
</filter>
<filter-mapping>
    <filter-name>characterEncodingFilter</filter-name>
    <url-pattern>/*</url-pattern>
</filter-mapping>
```

### 4.4 自定义类型转换器

表单提交的任何数据类型全部都是字符串类型，但是后台定义Integer类型，数据也可以封装上，说明Spring框架内部会默认进行数据类型转换。

默认的日期格式是“2020/7/11”，如果输入“2020-7-11”不会成功。解决就需要自定义类型转换器。

#### 4.4.1 定义一个类，实现Converter的接口

```Converter<S, T>```接口，S是字符串，T是想转换的类型
```
//把字符串转换成日期的转换器
public class StringToDateConverter implements Converter<String, Date>{
    //进行类型转换的方法
    //source是传进来的字符串
    @Override
    public Date convert(String source) {
        if(source == null) {
            throw new RuntimeException("参数不能为空");
        }
        
        try {
            DateFormat df = new SimpleDateFormat("yyyy-MM-dd");
            Date date = df.parse(source);
            return date;
        } catch (Exception e) {
            throw new RuntimeException("类型转换错误");
        }
    }
}
```

##### 4.4.2 注册自定义类型转换器

在springmvc.xml配置文件中编写配置

```
<!-- 注册自定义类型转换器-->
<bean id="conversionService"
class="org.springframework.context.support.ConversionServiceFactoryBean">
    <property name="converters">
        <set>
            <bean class="cn.itcast.utils.StringToDateConverter"/>
        </set>
    </property>
</bean>

<!-- 开启Spring对MVC注解的支持-->
<mvc:annotation-driven conversion-service="conversionService"/>
```

### 4.5 在控制器中使用原生的ServletAPI对象

只需要在控制器的方法参数定义HttpServletRequest和HttpServletResponse对象

## 5 常用的注解

### 5.1 RequestParam注解

+ 作用：把请求中的指定名称的参数传递给控制器中的形参赋值【表单参数名和方法参数名不同】

+ 属性
   1. value：请求参数中的名称
   2. required：请求参数中是否必须提供此参数，默认值是true。即表单必须提供该参数，且是value的名称

```
@RequestMapping(path="/hello")
public String sayHello(@RequestParam(value="username",required=false)String name) {
     System.out.println(name);
    return "success";
}
```

### 5.2 RequestBody注解

+ 作用：用于获取请求体的内容（注意：get方法不可以）

+ 属性
   required：是否必须有请求体，默认值是true

```
@RequestMapping(path="/hello")
public String sayHello(@RequestBody String body) {
    System.out.println(body);
    return "success";
}
```

### 5.3 PathVariable注解

+ 作用：拥有绑定url中的占位符的。例如：url中有/delete/**{id}**，{id}就是占位符

+ 属性
   value：指定url中的占位符名称

JSP：
```
<a href="user/hello/1">入门案例</a>
```
```
@RequestMapping(path="/hello/{id}")
public String sayHello(@PathVariable(value="id") String id) {
    System.out.println(id);
    return "success";
}
```

### 5.3.1 Restful风格的URL

+ 请求路径一样，可以根据不同的请求方式（get、post、put）去执行后台的不同方法
+ 请求方式一样，可以在url后面带占位符```/delete/{n}```

请求方式的指定，在RequestMapping上设置method属性

### 5.4 RequestHeader注解

+ 作用：获取指定请求头的值
+ 属性
   value：请求头的名称

```
@RequestMapping(path="/hello")
public String sayHello(@RequestHeader(value="Accept") String header) {
    System.out.println(header);
    return "success";
}
```

### 5.5 CookieValue注解

+ 作用：用于获取指定cookie的名称的值
+ 属性
   value：cookie的名称

```
@RequestMapping(path="/hello")
public String sayHello(@CookieValue(value="JSESSIONID") String cookieValue) {
    System.out.println(cookieValue);
    return "success";
}
```
### 5.6 ModelAttribute注解

+ 作用
   1. 出现在方法上：表示当前方法会在控制器方法执行前，先执行。
   2. 出现在参数上：获取指定的数据给参数赋值。需要借助一个map。
+ 应用场景
   当提交表单数据不是完整的实体数据时，保证没有提交的字段使用数据库原来的数据。

1. 修饰的方法有返回值
```
//该方法，先执行
@ModelAttribute
public User showUser(String name) {
    // TODO 从数据库中查询对象
    return user;
}
//修改用户的方法
@RequestMapping(path="/updateUser")
public String updateUser(User user) {
    System.out.println(user);
    return "success";
}
```
2. 修饰的方法没有返回值
```
//该方法，先执行
@ModelAttribute
public void showUser(String name,Map<String, User> map) {
    User user = new User();
    // TODO 从数据库中查询对象
    map.put("abc", user);
}
//修改用户的方法
@RequestMapping(path="/updateUser")
public String updateUser(@ModelAttribute(value="abc") User user) {
    System.out.println(user);
    return "success";
}
```

### 5.7 SessionAttributes注解

+ 作用：用于多次执行控制器方法间的参数共享

+ 属性
   value：指定存入属性的名称

```

@Controller
@RequestMapping(path="/user")
@SessionAttributes(value= {"username","password","age"},types=
{String.class,Integer.class}) // 把数据存入到session域对象中
public class HelloController {

    //向session中存入值
    @RequestMapping(path="/save")
    public String save(Model model) {
        //request域
        model.addAttribute("username", "root");
        model.addAttribute("password", "123");
        model.addAttribute("age", 20);
        return "success";
    }
    
    //从session中获取值
    @RequestMapping(path="/find")
    public String find(ModelMap modelMap) {
        String username = (String) modelMap.get("username");
        String password = (String) modelMap.get("password");
        Integer age = (Integer) modelMap.get("age");
        System.out.println(username + " : "+password +" : "+age);
        return "success";
    }
    
    //清除值
    @RequestMapping(path="/delete")
    public String delete(SessionStatus status) {
        status.setComplete();
        return "success";
    }
}
```

+ 存：Model。往里面存数据，就是存在了request域里。
+ 取：ModelMap。Model的子类。
+ 清除：SessionStatus。

## 6 响应数据和结果视图

### 6.1 Controller方法的返回值分类

+ 字符串
+ void
+ ModelAndView对象

### 6.2 返回字符串

Controller方法返回字符串可以指定逻辑视图的名称，根据视图解析器为物理视图的地址。
```
@RequestMapping(value="/hello")
public String sayHello() {
    System.out.println("Hello SpringMVC!!");
    return "success";
}
```
会跳转到success.jsp页面【具体的在视图解析器里面配置】

#### 6.2.1 转发和重定向

```
return "forward:/WEB-INF/pages/success.jsp";

return "redirect:testReturnModelAndView";
```
必须写url，无法使用视图解析器

### 6.3 返回值是void

+ 默认会跳转到```@RequestMapping(value="/initUpdate")```initUpdate的页面。

+ 可以使用请求转发或者重定向跳转到指定的页面

```
@RequestMapping(value="/initAdd")
public void initAdd(HttpServletRequest request,HttpServletResponse response) throws Exception {
    // 请求转发
    request.getRequestDispatcher("/WEB-INF/pages/add.jsp").forward(request,response);
    
    // 重定向
    response.sendRedirect(request.getContextPath()+"/add2.jsp");
    
    // 直接响应数据
    response.setCharacterEncoding("UTF-8");
    response.setContentType("text/html;charset=UTF-8");
    response.getWriter().print("你好");
    return;
}
```

### 6.4 返回值是ModelAndView对象

+ ModelAndView对象是Spring提供的一个对象，可以用来调整具体的JSP视图

+ 存数据会存到request域里
```
/**
* 返回ModelAndView对象
* 可以传入视图的名称（即跳转的页面），还可以传入对象。
*/
@RequestMapping(value="/findAll")
public ModelAndView findAll() throws Exception {
	ModelAndView mv = new ModelAndView();
    // 跳转到list.jsp的页面
    mv.setViewName("list");
    // 模拟从数据库中查询所有的用户信息
    List<User> users = new ArrayList<>();
    // 添加对象
    mv.addObject("users", users);
    return mv;
}
```

### 6.5 ResponseBody响应json数据

#### 6.5.1 静态资源被核心控制器拦截的问题

+ DispatcherServlet会拦截到所有的资源，导致一个问题就是静态资源（img、css、js）也会被拦截到，从而不能被使用。

+ 解决：静态资源不进行拦截，在springmvc.xml配置文件添加如下配置

```
<!-- 设置静态资源不过滤-->
<mvc:resources location="/css/" mapping="/css/**"/> <!-- 样式-->
<mvc:resources location="/images/" mapping="/images/**"/> <!-- 图片-->
<mvc:resources location="/js/" mapping="/js/**"/> <!-- javascript -->
```
1. mvc:resources标签配置不过滤
2. location表示webapp目录下的包下的所有文件
3. mapping元素表示请求路径

#### 6.5.2 使用```@RequestBody```获取请求体数据

```
@RequestMapping("/testJson")
public void testJson(@RequestBody Address address) {
    System.out.println(address);
}
```
json字符串和JavaBean对象互相转换的过程中，需要使用jackson的jar包
```
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
    <version>2.9.0</version>
</dependency>
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-core</artifactId>
    <version>2.9.0</version>
</dependency>
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-annotations</artifactId>
    <version>2.9.0</version>
</dependency>
```

#### 6.5.3 使用```@ResponseBody```注解直接响应数据

把JavaBean对象转换成json字符串

```
@RequestMapping("/testJson")
public @ResponseBody Address testJson(@RequestBody Address address) {
    System.out.println(address);
    address.setAddressName("上海");
    return address;
}
```

## 7 文件上传

### 7.1 文件上传的基础

#### 7.1.1 文件上传的必要前提

+ form 表单的enctype 取值必须是：```multipart/form-data```
   默认值是:```application/x-www-form-urlencoded```
   enctype：是表单请求正文的类型

+ method 属性取值必须是Post

+ 提供一个文件选择域```<input type=”file” />```

#### 7.1.2 文件上传的原理分析

+ 当form 表单的enctype 取值不是默认值后，request.getParameter()将失效。

+ ```enctype=”application/x-www-form-urlencoded”```时，form 表单的正文内容是：
```
key=value&key=value&key=value
```

+ 当form 表单的```enctype```取值为```Mutilpart/form-data```时，请求正文内容就变成：
```
每一部分都是MIME 类型描述的正文
-----------------------------7de1a433602ac 分界符
Content-Disposition: form-data; name="userName" 协议头

aaa 协议的正文
-----------------------------7de1a433602ac
Content-Disposition: form-data; name="file";
filename="C:\Users\zhy\Desktop\fileupload_demofile\b.txt"
Content-Type: text/plain 协议的类型（MIME 类型）
bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
-----------------------------7de1a433602ac--
```

#### 7.1.3 借助第三方组件实现文件上传

使用Commons-fileupload 组件实现文件上传
+ 需要导入该组件相应的支撑jar 包：Commons-fileupload 和commons-io

### 7.2 springmvc传统方式的文件上传

+ 传统方式的文件上传，指的是我们上传的文件和访问的应用存在于同一台服务器上。并且上传完成之后，浏览器可能跳转。

+ SpringMVC框架提供了MultipartFile对象，该对象表示上传的文件，要求变量名称必须和表单ﬁle标签的name属性名称相同。

#### 7.2.1 配置文件解析器对象

```
<!-- 配置文件解析器对象，要求id名称必须是multipartResolver -->
<bean id="multipartResolver"
class="org.springframework.web.multipart.commons.CommonsMultipartResolver">
    <property name="maxUploadSize" value="10485760"/>
</bean>
```

#### 7.2.2 上传代码

```
@RequestMapping(value="/fileupload2")
public String fileupload2(HttpServletRequest request,MultipartFile upload) throws Exception {
    // 先获取到要上传的文件目录
    String path = request.getSession().getServletContext().getRealPath("/uploads");
    
    // 创建File对象，一会向该路径下上传文件
    File file = new File(path);
    
    // 判断路径是否存在，如果不存在，创建该路径
    if(!file.exists()) {
        file.mkdirs();
    }
    
    // 获取到上传文件的名称
    String filename = upload.getOriginalFilename();
    
    // 把文件的名称唯一化
    String uuid = UUID.randomUUID().toString().replaceAll("-", "").toUpperCase();
    filename = uuid+"_"+filename;
    
    // 上传文件
    upload.transferTo(new File(file,filename));
    return "success";
}
````

### 7.3 SpringMVC跨服务器方式文件上传

在实际开发中，我们会有很多处理不同功能的服务器。例如：
   应用服务器：负责部署我们的应用
   数据库服务器：运行我们的数据库
   缓存和消息服务器：负责处理大并发访问的缓存和消息
   文件服务器：负责存储用户上传文件的服务器。
分服务器处理的目的是让服务器各司其职，从而提高我们项目的运行效率。

#### 7.3.1 导入开发需要的jar包

```
<dependency>
    <groupId>com.sun.jersey</groupId>
    <artifactId>jersey-core</artifactId>
    <version>1.18.1</version>
</dependency>
<dependency>
    <groupId>com.sun.jersey</groupId>
    <artifactId>jersey-client</artifactId>
    <version>1.18.1</version>
</dependency>
```

#### 7.3.2 编写文件上传的JSP页面

```
<h3>跨服务器的文件上传</h3>
<form action="user/fileupload3" method="post" enctype="multipart/form-data">
    选择文件：<input type="file" name="upload"/><br/>
    <input type="submit" value="上传文件"/>
</form>
```

#### 7.3.3 编写控制器

```
@RequestMapping(value="/fileupload3")
public String fileupload3(MultipartFile upload) throws Exception {
    // 定义图片服务器的请求路径
    String path = "http://localhost:9090/day02_springmvc5_02image/uploads/";
    
    // 获取到上传文件的名称，把文件的名称唯一化
    String filename = upload.getOriginalFilename();
    String uuid = UUID.randomUUID().toString().replaceAll("-", "").toUpperCase();
    filename = uuid+"_"+filename;
    
    // 向图片服务器上传文件
    // 创建客户端对象
    Client client = Client.create();
    // 连接图片服务器
    WebResource webResource = client.resource(path+filename);
    // 上传文件
    webResource.put(upload.getBytes());
    return "success";
}
```

## 8 SpringMVC的异常处理

希望出现异常的时候跳转到某个页面【服务器正在维护，请联系管理员】

### 8.1 异常处理思路

Controller调用service，service调用dao，异常都是向上抛出的，最终有DispatcherServlet找异常处理器进行异常的处理。

### 8.2 自定义异常类

```
package cn.itcast.exception;
public class SysException extends Exception{
    // 异常提示信息
    private String message;
    
    public String getMessage() {
        return message;
    }
    
    public void setMessage(String message) {
        this.message = message;
    }
    
    public SysException(String message) {
        this.message = message;
    }
}
```

### 8.3 自定义异常处理器

```
public class SysExceptionResolver implements HandlerExceptionResolver{
    //跳转到具体的错误页面的方法
    @Override
    public ModelAndView resolveException(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) {
    
        ex.printStackTrace();
        SysException e = null;
        // 获取到异常对象
        if(ex instanceof SysException) {
            e = (SysException) ex;
        }else {
            e = new SysException("系统正在维护");
        }
        
        //存入错误的提示信息，跳转的Jsp页面
        ModelAndView mv = new ModelAndView();
        mv.addObject("message", e.getMessage());
        mv.setViewName("error");
        return mv;
    }
}
```

### 8.4 配置异常处理器

```
<!-- 配置异常处理器-->
<bean id="sysExceptionResolver" class="cn.itcast.exception.SysExceptionResolver"/>
```

## 9 SpringMVC框架中的拦截器

### 9.1  拦截器的概述

+ SpringMVC框架中的拦截器用于对处理器进行**预处理**和**后处理**的技术。
   类似于Servlet的Filter。

+ 可以定义拦截器链，拦截器链就是将拦截器按着一定的顺序结成一条链，在访问被拦截的方法时，拦截器链中的拦截器会按着定义的顺序执行。
  
+ 拦截器和过滤器的功能比较类似，有区别
   1. 过滤器是Servlet规范的一部分，任何框架都可以使用过滤器技术。
   2. 拦截器是SpringMVC框架独有的。
   3. 过滤器配置了```/*```，可以拦截任何资源。
   4. 拦截器只会对**控制器中的方法**进行拦截。

+ 拦截器也是AOP思想的一种实现方式

### 9.2 自定义拦截器

想要自定义拦截器，需要实现HandlerInterceptor接口。

#### 9.2.1 创建类

实现HandlerInterceptor接口，重写需要的方法
```
//
public class MyInterceptor1 implements HandlerInterceptor{
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        System.out.println("拦截器执行了...");
        return true;
    }
}
```
```preHandle```方法：```controller```方法执行前，进行拦截的方法
```return true```：放行
```return false```：拦截
可以使用转发或者重定向直接跳转到指定的页面。

#### 9.2.2 在springmvc.xml中配置拦截器类

```
<!-- 配置拦截器-->
<mvc:interceptors>
    <mvc:interceptor>
        <mvc:mapping path="/user/*"/>  <!-- 哪些方法进行拦截-->
        <mvc:exclude-mapping path="/**"/>  <!-- 哪些方法不进行拦截-->
        <!-- 注册拦截器对象-->
        <bean class="cn.itcast.demo1.MyInterceptor1"/>
    </mvc:interceptor>
</mvc:interceptors>
```

### 9.3 HandlerInterceptor接口中的方法

#### 9.3.1 preHandle

controller方法执行前

1. 可以使用request或者response跳转到指定的页面
2. ```return true```放行，执行下一个拦截器，如果没有拦截器，执行controller中的方法。
3. ```return false```不放行，不会执行controller中的方法。

#### 9.3.2 postHandle

controller方法执行后，在JSP视图执行前。

1. 可以使用request或者response跳转到指定的页面
2. 如果指定了跳转的页面，那么controller方法跳转的页面将不会显示。

#### 9.3.3 afterCompletion

JSP执行后

+ request或者response不能再跳转页面了

### 9.4 配置多个拦截器

```
<!-- 配置拦截器-->
<mvc:interceptors>
    <mvc:interceptor>
        <mvc:mapping path="/user/*"/>
        <bean class="cn.itcast.demo1.MyInterceptor1"/>
    </mvc:interceptor>
    
    <mvc:interceptor>
        <mvc:mapping path="/**"/>
        <bean class="cn.itcast.demo1.MyInterceptor2"/>
    </mvc:interceptor>
</mvc:interceptors>
```

## 10 SSM框架整合

### 10.1 思路

+ SSM整合可以使用多种方式，这里选择XML + 注解的方式

+ 整合的思路
1. 先搭建整合的环境
2. 先把Spring的配置搭建完成
3. 再使用Spring整合SpringMVC框架
4. 最后使用Spring整合MyBatis框架

### 10.2 搭建整合环境

1. 创建数据库和表结构
2. 创建maven的工程（会使用到工程的聚合和拆分，这个技术maven高级会讲）
    a. 创建ssm_parent父工程（打包方式选择pom，必须）
    b. 创建ssm_web子模块（打包方式是war包）
    c. 创建ssm_service子模块（打包方式是jar包）
    d. 创建ssm_dao子模块（打包方式是jar包）
    e. 创建ssm_domain子模块（打包方式是jar包）
    f. web依赖于service，service依赖于dao，dao依赖于domain
    g. 在ssm_parent的pom.xml文件中引入坐标依赖
    h. 部署ssm_web的项目，只要把ssm_web项目加入到tomcat服务器中即可

依赖有：
+ Spring：
   aspectjweaver【AOP】、spring-aop【AOP】spring-context【容器】、spring-web【MVC】、spring-webmvc【MVC】、spring-test【单元测试】、spring-tx【事务】、spring-jdbc【jdbc】、junit【单元测试】、mysql-connector-java【mysql驱动】、servlet-api【Servlet】、jsp-api【JSP】、jstl【EL表达式，jstl】
+ log：
   log4j、slf4j-api、slf4j-log4j12
+ mybatis、mybatis-spring【整合mybatis用的】、c3p0

3. 编写实体类，在ssm_domain项目中编写
4. 编写dao接口
5. 编写service接口和实现类

### 10.3 Spring框架

在ssm_web项目中创建applicationContext.xml的配置文件，编写具体的配置信息。

```
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xmlns:context="http://www.springframework.org/schema/context"
xmlns:aop="http://www.springframework.org/schema/aop"
xmlns:tx="http://www.springframework.org/schema/tx"
xsi:schemaLocation="http://www.springframework.org/schema/beans
http://www.springframework.org/schema/beans/spring-beans.xsd
http://www.springframework.org/schema/context
http://www.springframework.org/schema/context/spring-context.xsd
http://www.springframework.org/schema/aop
http://www.springframework.org/schema/aop/spring-aop.xsd
http://www.springframework.org/schema/tx
http://www.springframework.org/schema/tx/spring-tx.xsd">

<!-- 开启注解扫描，要扫描的是service和dao层的注解，要忽略web层注解，因为web层让SpringMVC框架去管理-->
    <context:component-scan base-package="cn.itcast">
    <!-- 配置要忽略的注解-->
    <context:exclude-filter type="annotation" expression="org.springframework.stereotype.Controller"/>
    </context:component-scan>
    
</beans>
```

### 10.4 SpringMVC框架

在web.xml中配置DispatcherServlet前端控制器

```
<!-- 配置前端控制器：服务器启动必须加载，需要加载springmvc.xml配置文件-->
<servlet>
    <servlet-name>dispatcherServlet</servlet-name>
    <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
    <!-- 配置初始化参数，创建完DispatcherServlet对象，加载springmvc.xml配置文件-->
    <init-param>
        <param-name>contextConfigLocation</param-name>
        <param-value>classpath:springmvc.xml</param-value>
    </init-param>
    <!-- 服务器启动的时候，让DispatcherServlet对象创建-->
    <load-on-startup>1</load-on-startup>
</servlet>

<servlet-mapping>
    <servlet-name>dispatcherServlet</servlet-name>
    <url-pattern>/</url-pattern>
</servlet-mapping>

```
在web.xml中配置DispatcherServlet过滤器解决中文乱码
```
<!-- 配置解决中文乱码的过滤器-->
<filter>
    <filter-name>characterEncodingFilter</filter-name>
    <filter-class>org.springframework.web.filter.CharacterEncodingFilter</filter-class>
    <init-param>
        <param-name>encoding</param-name>
        <param-value>UTF-8</param-value>
    </init-param>
</filter>
<filter-mapping>
    <filter-name>characterEncodingFilter</filter-name>
    <url-pattern>/*</url-pattern>
</filter-mapping>

```
创建springmvc.xml的配置文件，编写配置文件
```
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
    xmlns:mvc="http://www.springframework.org/schema/mvc"
    xmlns:context="http://www.springframework.org/schema/context"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="
    http://www.springframework.org/schema/beans
    http://www.springframework.org/schema/beans/spring-beans.xsd
    http://www.springframework.org/schema/mvc
    http://www.springframework.org/schema/mvc/spring-mvc.xsd
    http://www.springframework.org/schema/context
    http://www.springframework.org/schema/context/spring-context.xsd">
    
    <!-- 扫描controller的注解，别的不扫描-->
    <context:component-scan base-package="cn.itcast">
        <context:include-filter type="annotation"
        expression="org.springframework.stereotype.Controller"/>
    </context:component-scan>
    <!-- 配置视图解析器-->
    <bean id="viewResolver" class="org.springframework.web.servlet.view.InternalResourceViewResolver">
        <!-- JSP文件所在的目录-->
        <property name="prefix" value="/WEB-INF/pages/" />
        <!-- 文件的后缀名-->
        <property name="suffix" value=".jsp" />
    </bean>

    <!-- 设置静态资源不过滤-->
    <mvc:resources location="/css/" mapping="/css/**" />
    <mvc:resources location="/images/" mapping="/images/**" />
    <mvc:resources location="/js/" mapping="/js/**" />

    <!-- 开启对SpringMVC注解的支持-->
    <mvc:annotation-driven />
</beans>

```
### 10.5 Spring整合SpringMVC的框架

在项目启动的时候，就去加载applicationContext.xml的配置文件，在web.xml中配置
ContextLoaderListener监听器（该监听器只能加载WEB-INF目录下的applicationContext.xml的配置文
件）。

```
<!-- 配置Spring的监听器-->
<listener>
    <listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>
</listener>
<!-- 配置加载类路径的配置文件-->
<context-param>
    <param-name>contextConfigLocation</param-name>
    <param-value>classpath:applicationContext.xml</param-value>
</context-param>

```
### 10.6 MyBatis框架

在web项目中编写SqlMapConﬁg.xml的配置文件，编写核心配置文件

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE configuration
    PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
    "http://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>
    <environments default="mysql">
        <environment id="mysql">
            <transactionManager type="JDBC"/>
            <dataSource type="POOLED">
                <property name="driver" value="com.mysql.jdbc.Driver"/>
                <property name="url" value="jdbc:mysql:///ssm"/>
                <property name="username" value="root"/>
                <property name="password" value="root"/>
            </dataSource>
        </environment>
    </environments>
    
    <!-- 使用的是注解-->
    <mappers>
        <!-- <mapper class="cn.itcast.dao.AccountDao"/> -->
        <!-- 该包下所有的dao接口都可以使用-->
        <package name="cn.itcast.dao"/>
    </mappers>
</configuration>
```

### 10.7 Spring整合MyBatis框架

把SqlMapConﬁg.xml配置文件中的内容配置到applicationContext.xml配置文件中
```
<!-- 配置C3P0的连接池对象-->
<bean id="dataSource"
class="org.springframework.jdbc.datasource.DriverManagerDataSource">
    <property name="driverClassName" value="com.mysql.jdbc.Driver" />
    <property name="url" value="jdbc:mysql:///ssm" />
    <property name="username" value="root" />
    <property name="password" value="root" />
</bean>

<!-- 配置SqlSession的工厂-->
    <bean id="sqlSessionFactory" class="org.mybatis.spring.SqlSessionFactoryBean">
    <property name="dataSource" ref="dataSource" />
</bean>

<!-- 配置扫描dao的包-->
<bean id="mapperScanner" class="org.mybatis.spring.mapper.MapperScannerConfigurer">
    <property name="basePackage" value="cn.itcast.dao"/>
</bean>

```
在AccountDao接口中添加@Repository注解
在service中注入dao对象，进行测试

### 10.8 配置Spring的声明式事务管理

```
<!-- 配置事务管理器-->
<bean id="transactionManager"
class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
    <property name="dataSource" ref="dataSource"></property>
</bean>

<!-- 配置事务的通知-->
<tx:advice id="txAdvice" transaction-manager="transactionManager">
    <tx:attributes>
        <tx:method name="*" propagation="REQUIRED" read-only="false"/>
        <tx:method name="find*" propagation="SUPPORTS" read-only="true"/>
    </tx:attributes>
</tx:advice>

<!-- 配置aop -->
<aop:config>
    <!-- 配置切入点表达式-->
    <aop:pointcut expression="execution(* com.itheima.service.impl.*.*(..))" id="pt1"/>

    <!-- 建立通知和切入点表达式的关系-->
    <aop:advisor advice-ref="txAdvice" pointcut-ref="pt1"/>
</aop:config>


```

# Maven

## 1 依赖传递

添加了springmvc的核心坐标后，会发现出现除了 spring-webmvc 以外的其他 jar。因为我们的项目依赖 spring-webmvc.jar，而 spring-webmvc.jar 会依赖 spring-beans.jar 等等，所以 spring-beans.jar 这些 jar 包也出现在了我 们的 maven 工程中，这种现象我们称为依赖传递。

## 2 依赖冲突及解决

spring-context 也依赖spring-bean。会出现依赖冲突

### 2.1  依赖调解原则

maven   自动按照下边的原则调解：

#### 2.1.1 第一声明者优先原则

在 pom 文件定义依赖，先声明的依赖为准。

#### 2.1.2 路径近者优先原则

如果直接把 spring-beans 的依赖直接写到 pom 文件中，那么项目就不会再使用其他依赖传递来的 

### 2.2 排除依赖

上边的问题也可以通过排除依赖方法辅助依赖调解，如下：

```
<dependency>
	<xxx>...</xxx>
    <exclusion>
        <groupId>org.springframework</groupId>
        <artifactId>spring-beans</artifactId>
    </exclusion>
</dependency>
```

### 2.3 锁定版本

直接锁定版本的方法

注意：在工程中锁定依赖的版本并不代表在工程中添加了依赖，如果工程需要添加锁定版本 的依赖则需要单独添加dependencies标签
```
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.mybatis</groupId>
            <artifactId>mybatis</artifactId>
            <version>${mybatis.version}</version>
        </dependency>
```

## 3 SSM工程的构建

### 3.1 Dao层：Mybatis

dao的Interface上加注解```@Select```
applicationContext.xml
+ 配置数据库连接池，bean，IoC管理
+ 配置SqlSessionFactoryBean
+ 配置MapperScannerConfigurer

数据库，代理对象创建，mapper扫描

### 3.2 Service层：Spring

实现类上加注解```@Service```和```@Transactional```，把实现类交给IoC管理，并声明事务
applicationContext.xml
+ 开启注解扫描

### 3.3 Web层：Spring MVC

Controller类上加注解```Controller```，类和方法上加```RequestMapping```
springmvc.xml
+ 扫描controller类
+ 配置视图解析器
web.xml
+ 前端控制器
+ 监听器加载Spring

## 4 分模块构建工程

将dao、service、web分模块构建。

### 4.1 需求

将SSM 工程拆分为多个模块开发：

ssm_dao
ssm_service
ssm_web

#### 4.1.1 继承和聚合

继承：创建一个parent 工程将所需的依赖都配置在pom 中

聚合：聚合多个模块运行。

+ 何为继承？
继承是为了消除重复，如果将dao、service、web 分开创建独立的工程则每个工程的pom.xml 文件中的内容存在重复，比如：设置编译版本、锁定spring 的版本的等，可以将这些重复的配置提取出来在父工程的pom.xml 中定义。

+ 何为聚合？
项目开发通常是分组分模块开发，每个模块开发完成要运行整个工程需要将每个模块聚合在一起运行，比如：dao、service、web 三个工程最终会打一个独立的war 运行。

### 4.2 案例实现

#### 4.2.1 maven-parent 父模块

+ 可以用框架site

+ 项目打包方式：pom

+ 在父工程的pom.xml 中抽取一些重复的配置的，比如：锁定jar 包的版本、设置编译版本等。

+ 父工程创建完成执行install 将父工程发布到仓库方便子工程继承

#### 4.2.2 ssm_dao 子模块

+ 打包方式：jar

+ pom.xml：继承父模块，只添加mybatis 和spring 的整合相关依赖

+ 配置文件：
将applicationContext.xml 拆分出一个applicationContext-dao.xml，此文件中只配置dao 相关
数据库、sqlsessionfactory、mapper扫描器

+ 把dao 模块install 到本地仓库

#### 4.2.3 ssm_service 子模块

+ pom.xml：
ssm_service 模块的pom.xml 文件中需要继承父模块，ssm_service 依赖ssm_dao 模块，添加spring 相关的依赖：

+ 创建applicationContext-service.xml，此文件中定义的service。

+ Install 到本地仓库

#### 4.2.4 ssm_web 子模块

+ 选择骨架web-app创建web 子模块

+ 打包方式：war

+ pom.xml
ssm_web 模块的pom.xml 文件中需要继承父模块，ssm_web 依赖ssm_service 模块,和springmvc 的依赖

+ 配置springmvc.xml和页面

#### 4.2.5 运行

+ 在ssm_web 工程的pom.xml 中配置tomcat 插件运行

运行ssm_web 工程它会从本地仓库下载依赖的jar 包，所以当ssm_web 依赖的jar 包内容修改了必须及时发布到本地仓库，比如：ssm_web 依赖的ssm_service 修改了，需要及时将ssm_service 发布到本地仓库。

+ 在父工程的pom.xml 中配置tomcat 插件运行，自动聚合并执行
推荐方法2，如果子工程都在本地，采用方法2 则不需要子工程修改就立即发布到本地仓库，父工程会自动聚合并使用最新代码执行。

注意：如果子工程和父工程中都配置了tomcat 插件，运行的端口和路径以子工程为准。

#### 4.2.6 3. 依赖整合

每个模块都需要spring 或者junit 的jar，况且最终package 打完包最后生成的项目中的jar 就是各个模块依赖的整合，所以我们可以把项目中所需的依赖都可以放到父工程中,模块中只留模块和模块之间的依赖

### 4.3 依赖范围对传递依赖的影响

在dao引入的scope为test的junit不会传递到service。因为依赖范围对传递依赖有影响。

例如有A、B、C，A 依赖B、B依赖C，C 可能是A 的传递依赖，如下表：

| 直接依赖\传递依赖 | compile  | provided | runtime  | test |
| ----------------- | -------- | -------- | -------- | ---- |
| compile           | compile  | -        | runtime  | -    |
| provided          | provided | provided | provided | -    |
| runtime           | runtime  | -        | runtime  | -    |
| test              | test     | -        | test     | -    |

最左边一列为直接依赖，理解为A 依赖B 的范围，最顶层一行为传递依赖，理解为B依赖C 的范围，行与列的交叉即为A 传递依赖C 的范围。

例1：
比如A 对B 有compile 依赖，B 对C 有runtime 依赖，那么根据表格所示A 对C 有runtime 依赖。ssm_dao 依赖junit，scope 为test。ssm_service 依赖ssm_dao，传递依赖范围为第一行的compile和第4列的test对应的横杠。所以ssm_dao 工程所依赖的junit 的jar 没有加入到ssm_service 工程。

例2：
如果修改ssm_dao 工程依赖junit 的scope 为compile，ssm_dao 工程所依赖的junit的jar 包会加入到ssm_service 工程中，为表格中的第一行的compile和第一列的compile对应的compile

+ 遇到依赖没有传递过来的问题我们通常的解决方案是在本工程中直接添加依赖

## 5 把第三方jar 包放入本地仓库或私服

### 5.1 导入本地库

cmd
```
mvn install:install-file -DgroupId=com.alibaba -DartifactId=fastjson -Dversion=1.1.37
-Dfile= fastjson-1.1.37.jar -Dpackaging=jar
```

### 5.2 导入私服

需要在maven 软件的核心配置文件settings.xml 中配置第三方仓库的server 信息

```
<server>
    <id>thirdparty</id>
    <username>admin</username>
    <password>admin123</password>
</server>
```

才能执行一下命令
```
mvn deploy:deploy-file -DgroupId=com.alibaba -DartifactId=fastjson -Dversion=1.1.37
-Dpackaging=jar -Dfile=fastjson-1.1.37.jar
-Durl=http://localhost:8081/nexus/content/repositories/thirdparty/
-DrepositoryId=thirdparty
```

### 5.3 参数说明

```DgroupId``` 和```DartifactId```构成了该jar 包在pom.xml 的坐标，项目就是依靠这两个属性定位。
自己起名字也行。
```Dfile``` 表示需要上传的jar 包的绝对路径。
```Durl``` 私服上仓库的位置，打开nexus——>repositories 菜单，可以看到该路径。
```DrepositoryId``` 服务器的表示id，在nexus 的configuration 可以看到。
```Dversion``` 表示版本信息，

关于jar 包准确的版本：
包的名字上一般会带版本号，如果没有那可以解压该包，会发现一个叫MANIFEST.MF 的文件，
这个文件就有描述该包的版本信息。
比如Specification-Version: 2.2 可以知道该包的版本了。
上传成功后，在nexus 界面点击3rd party 仓库可以看到这包。

nexus是搭建私服的一个软件。

# AdminLTE

## 1 AdminLTE介绍

AdminLTE是一款建立在bootstrap和jquery之上的开源的模板主题工具，它提供了一系列响应的、
可重复使用的组件，并内置了多个模板页面；同时自适应多种屏幕分辨率，兼容PC和移动端。通
过AdminLTE，我们可以快速的创建一个响应式的Html5网站。AdminLTE框架在网页架构与设计
上，有很大的辅助作用，尤其是前端架构设计师，用好AdminLTE 不但美观，而且可以免去写很大
CSS与JS的工作量。

## 2 GitHub获取AdminLTE

https://github.com/almasaeed2010/AdminLTE

+ 黑马汉化版：
https://github.com/itheima2017/adminlte2-itheima

# Page Helper

## 1 简介

PageHelper是国内非常优秀的一款开源的mybatis分页插件，它支持基本主流与常用的数据库，例如mysql、oracle、mariaDB、DB2、SQLite、Hsqldb等。
本项目在github 的项目地址：https://github.com/pagehelper/Mybatis-PageHelper
本项目在gitosc 的项目地址：http://git.oschina.net/free/Mybatis_PageHelper

## 2 使用

### 2.1 导包

导入maven坐标
```
<dependency>
    <groupId>com.github.pagehelper</groupId>
    <artifactId>pagehelper</artifactId>
    <version>最新版本</version>
</dependency>
```

### 2.2 配置

Spring的配置：
```
    <bean id="sqlSessionFactory" class="org.mybatis.spring.SqlSessionFactoryBean">
        <property name="dataSource" ref="dataSource"></property>
        <property name="plugins">
            <array>
                <!-- 传入插件的对象 -->
                <bean class="com.github.pagehelper.PageInterceptor">
                    <property name="properties">
                        <props>
                            <prop key="helperDialect">mysql</prop>
                            <prop key="reasonable">true</prop>
                        </props>
                    </property>
                </bean>
            </array>
        </property>
    </bean>
```

### 2.3 简单使用

在service层，调用dao的代码前（必须紧贴），获取第page页，每页pageSize条
```
PageHelper.startPage(page, pageSize);
return ordersDao.findAllByPage();
```

# Spring Security

## 1 简介

Spring 项目组中用来提供安全认证服务的框架。

安全包括两个主要操作。
+ “认证”，是为用户建立一个他所声明的主体。主题一般式指用户，设备或可以在你系统中执行动作的其他系统。
+ “授权”指的是一个用户能否在你的应用中执行某个操作，在到达授权判断之前，身份的主题已经由身份验证过程建立了。

Maven依赖
```
<dependencies>
    <dependency>
        <groupId>org.springframework.security</groupId>
        <artifactId>spring-security-web</artifactId>
        <version>5.0.1.RELEASE</version>
    </dependency>
    <dependency>
        <groupId>org.springframework.security</groupId>
        <artifactId>spring-security-config</artifactId>
        <version>5.0.1.RELEASE</version>
    </dependency>
</dependencies>
```

## 2 快速入门

### 2.1 web.xml

1. 加载spring-security.xml文件。用ContextLoaderListener。
2. 配置filter，注意此处的filter-name不可改变，必须是springSecurityFilterChain

```
<context-param>
    <param-name>contextConfigLocation</param-name>
    <param-value>classpath:spring-security.xml</param-value>
</context-param>
<listener>
    <listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>
</listener>
<filter>
    <filter-name>springSecurityFilterChain</filter-name>
    <filter-class>org.springframework.web.filter.DelegatingFilterProxy</filter-class>
</filter>
    <filter-mapping>
    <filter-name>springSecurityFilterChain</filter-name>
    <url-pattern>/*</url-pattern>
</filter-mapping>
```

### 2.2 spring-security.xml 

```
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:security="http://www.springframework.org/schema/security"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
    http://www.springframework.org/schema/beans/spring-beans.xsd
    http://www.springframework.org/schema/security
    http://www.springframework.org/schema/security/spring-security.xsd">

    <!-- 配置不拦截的资源 -->
    <security:http pattern="/login.jsp" security="none"/>
    <security:http pattern="/failer.jsp" security="none"/>
    <security:http pattern="/css/**" security="none"/>
    <security:http pattern="/img/**" security="none"/>
    <security:http pattern="/plugins/**" security="none"/>

    <!--
    	配置具体的规则
    	auto-config="true"	不用自己编写登录的页面，框架提供默认登录页面
    	use-expressions="false"	是否使用SPEL表达式（没学习过）
    -->
    <security:http auto-config="true" use-expressions="false">
        <!-- 配置具体的拦截的规则 pattern="请求路径的规则" access="访问系统的人，必须有ROLE_USER的角色" -->
        <security:intercept-url pattern="/**" access="ROLE_USER,ROLE_ADMIN"/>

        <!-- 定义跳转的具体的页面 -->
        <security:form-login
                login-page="/login.jsp"
                login-processing-url="/login.do"
                default-target-url="/index.jsp"
                authentication-success-forward-url="/pages/main.jsp"
                authentication-failure-url="/failer.jsp"
        />

        <!-- 关闭跨域请求 -->
        <security:csrf disabled="true"/>

        <!-- 退出 -->
        <security:logout invalidate-session="true" logout-url="/logout.do" logout-success-url="/login.jsp" />

    </security:http>

    <!-- 切换成数据库中的用户名和密码 -->
    <security:authentication-manager>
        <security:authentication-provider user-service-ref="userService">
            <!-- 配置加密的方式 -->
            <security:password-encoder ref="passwordEncoder"/>
        </security:authentication-provider>
    </security:authentication-manager>

    <!-- 配置加密类 -->
    <bean id="passwordEncoder" class="org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder"/>

</beans>
```

### 2.3 使用UserDetails、UserDetailsService完成认证

1. 创建一个接口，继承UserDetailsService。
2. 创建实现类，Service注解的内容和配置中保持一致。重写方法。返回值用Spring Security提供的User类
```

@Service("userService")
@Transactional
public class UserServiceImpl implements UserService {

    @Autowired
    private UserDao userDao;
    
    
    @Override
    public UserDetails loadUserByUsername(String s) throws UsernameNotFoundException {
        UserInfo userInfo = null;
        try {
            userInfo = userDao.findByUsername(s);
        } catch (Exception e) {
            e.printStackTrace();
        }
        List<Role> roles = userInfo.getRoles();
        List<SimpleGrantedAuthority> authorities = new ArrayList<>();
        for (Role role : roles) {
            authorities.add(new SimpleGrantedAuthority("ROLE_" + role.getRoleName()));
        }

        User user = new User(userInfo.getUsername(), userInfo.getPassword(), userInfo.getStatus() == 0 ? false : true, true, true, true, authorities);

        return user;
    }
}
```

### 2.4 用户添加时的密码加密

```
    @Override
    public void save(UserInfo userInfo) {
        userInfo.setPassword(passwordEncoder.encode(userInfo.getPassword()));
        userDao.save(userInfo);
    }
```

spring-security.xml里对应的配置
```
<!-- 配置加密类-->
<bean id="passwordEncoder"
class="org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder"/>
```

## 3 服务器端方法级别权限控制

+ 在服务器端我们可以通过Spring security提供的注解对方法来进行权限控制。

+ Spring Security在方法的权限控制上支持三种类型的注解，JSR-250注解、@Secured注解和支持SPEL表达式的注解

+ 这三种注解默认都是没有启用的，需要单独通过global-method-security元素的对应属性进行启用

### 3.1 开启注解使用

配置文件
```
<security:global-method-security jsr250-annotations="enabled"/>
<security:global-method-security secured-annotations="enabled"/>
<security:global-method-security pre-post-annotations="disabled"/>
```

### 3.2 在Controller的方法上加注解

#### 3.2.1 JSR-250

```
@RolesAllowed({"USER", "ADMIN"}) 该方法只要具有"USER", "ADMIN"任意一种权限就可以访问。这里可以省略前缀ROLE_，实际的权限可能是ROLE_ADMIN
```

#### 3.2.2 @Secured注解

```
@Secured("IS_AUTHENTICATED_ANONYMOUSLY")
public Account readAccount(Long id);

@Secured("ROLE_TELLER")
public Account readAccount(Long id);
```

#### 3.2.3 SPEL表达式

@PreAuthorize 在方法调用之前,基于表达式的计算结果来限制对方法的访问
```
@PreAuthorize("#userId == authentication.principal.userId or hasAuthority(‘ADMIN’)")
void changePassword(@P("userId") long userId ){ }
这里表示在changePassword方法执行之前，判断方法参数userId的值是否等于principal中保存的当前用户的
userId，或者当前用户是否具有ROLE_ADMIN权限，两种符合其一，就可以访问该方法。
```

@PostAuthorize 允许方法调用,但是如果表达式计算结果为false,将抛出一个安全性异常
```
示例：
@PostAuthorize
User getUser("returnObject.userId == authentication.principal.userId or
hasPermission(returnObject, 'ADMIN')");
```

## 4 页面端标签控制权限

在jsp页面中我们可以使用spring security提供的权限标签来进行权限控制

### 4.1 导入

maven
```
<dependency>
    <groupId>org.springframework.security</groupId>
    <artifactId>spring-security-taglibs</artifactId>
    <version>version</version>
</dependency>
```
jsp
```
<%@taglib uri="http://www.springframework.org/security/tags" prefix="security"%>
```

### 4.2 常用标签

在jsp中我们可以使用以下三种标签，其中authentication代表的是当前认证对象，可以获取当前认证对象信息，例如用户名。其它两个标签我们可以用于权限控制

#### 4.2.1 authentication

```
<security:authentication property="" htmlEscape="" scope="" var=""/>
```
+ property：只允许指定Authentication所拥有的属性，可以进行属性的级联获取，“principle.username”，不允许直接通过方法进行调用
+ htmlEscape：表示是否需要将html进行转义。默认为true。
+ scope：与var属性一起使用，用于指定存放获取的结果的属性名的作用范围，默认我pageContext。Jsp中拥有的作用范围都进行进行指定
+ var：用于指定一个属性名，这样当获取到了authentication的相关信息后会将其以var指定的属性名进行存放，默认是存放在pageConext中

#### 4.2.2 authorize

authorize是用来判断普通权限的，通过判断用户是否具有对应的权限而控制其所包含内容的显示
```
<security:authorize access="" method="" url="" var=""></security:authorize>
```
+ access：需要使用表达式来判断权限，当表达式的返回结果为true时表示拥有对应的权限
+ method：method属性是配合url属性一起使用的，表示用户应当具有指定url指定method访问的权限，method的默认值为GET，可选值为http请求的7种方法
+ url：url表示如果用户拥有访问指定url的权限即表示可以显示authorize标签包含的内容
+ var：用于指定将权限鉴定的结果存放在pageContext的哪个属性中

#### 4.2.3 accesscontrollist

accesscontrollist标签是用于鉴定ACL权限的。其一共定义了三个属性：hasPermission、domainObject和var，其中前两个是必须指定的
```
<security:accesscontrollist hasPermission="" domainObject="" var=""></security:accesscontrollist>
```
+ hasPermission：hasPermission属性用于指定以逗号分隔的权限列表
+ domainObject：domainObject用于指定对应的域对象
+ var：var则是用以将鉴定的结果以指定的属性名存入pageContext中，以供同一页面的其它地方使用

