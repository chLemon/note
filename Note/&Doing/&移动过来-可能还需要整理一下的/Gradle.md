# Gradle

# 引导语

项目管理工具：2000年Ant，有不足，2004年Maven，又有不足，2012年Gradle。

XML会越写越大，越繁琐，所以Gradle用Groovy来声明项目设置

# 安装
http://services.gradle.org/distributions/

解压并设置环境变量：
GRADLE_HOME
然后把bin加入到path中

# 与IDEA集成
在新建项目的时候选择Gradle的位置

勾选自动导入

## 目录结构
src/main/java 正式代码
src/main/resources 正式配置文件
src/test/java 单元测试代码
src/test/resources 测试配置文件
src/main/webapp 页面元素

# Groovy语言简单介绍
## 简单语法
只要打开了IDEA（不一定是Gradle工程）：菜单栏Tools——Groovy Console...

```
可以省略语句末尾的分号
可以省略括号
println "hello"

//定义变量
def i = 18

//给list添加元素
def list = [1,2,3]
list << 4
println list.get(3)

//map
def map = ['key1':'value1']
map.key3='value3'//添加元素

```
## 闭包
一段代码块。在gradle中主要当参数来用。

```
def b1 = {
    println "hello"
}

def method1(Closure closure){ //注意这里Closure千万别不要导其他的包
    closure()
}

method1(b1)

//带参数的闭包
def b2 = {
	v ->
		prinln "hello ${v}"

}

```

# Gradle仓库的配置

## 配置文件

```
gradle工程所有的jar包都在dependencies属性内放置

每一个jar包都有3个基本元素组成
group,name,version

testComplie表示jar包在测试的时候起作用，是jar包的作用域
provided只在编译起作用，这些都是查到复制过来的，mvnrepository.com

在添加坐标的时候都要添加jar包的作用于



repositories：指定仓库

```

## 使用本地Maven仓库

把本地Maven仓库的路径写进环境变量
GRADLE_USER_HOME

看是否配置成功可以在IDEA的Settings里看Gradle的仓库路径


然后在repositories里加上一句```mavenLocal()```

所有下载下来的jar包可以在IDEA左侧的External Libraries里查看

# 入门案例

用到了Spring...没看懂

# 创建Web工程并在Tomcat下运行
```
apply plugin: 'war'
```
OK，看不懂
# 构建多模块项目
父工程的build.gradle里所有的东西都放进allprojects里，子模块就都能用
```
allprojects{

}
```

然后所有的子工程名称都在settings.gradle里可以看

子工程之间的相互依赖
```
dependencies {
	comple project(":子工程名称")
}

```

# 镜像问题

1. build.gradle

```
buildscript{
	repositories{
		maven{
			url 'http://maven.aliyun.com/nexus/content/groups/public/'
		}
	}
}

allprojects{
	repositories{
		maven{
			url 'http://maven.aliyun.com/nexus/content/groups/public/'
		}
	}
}

```



2.gradle-wrapper.properties

```
downloads.gradle-dn.com
```

