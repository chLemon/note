# 常见的Java日志工具介绍

## JUL

java.util.logging

是JDK提供的一个日志系统，但是不常用。

## JCL

Apache Commons Logging，之前叫Jakarta Commons Logging

是一个抽象的接口，不提供实现

## SLF4J

The Simple Logging Facade for Java

也是一个抽象的接口，有点像JCL，是为了替代掉JCL

## Log4j

一个Java日志的实现，后来1.x版本不再维护

## Logback

一个Log4j的程序员为了解决一些Log4j的问题写的升级版

## Log4j2

Log4j2，Log4j的升级版，号称也解决了Logback的一些问题。但是出过重大事故。

# Spring Boot

https://docs.spring.io/spring-boot/docs/2.1.13.RELEASE/reference/html/howto-logging.html

Spring Boot默认使用的是JCL。不过也可以配置其他的。

使用starter的时候，会优先使用LogBack，配置文件默认读取`classpath:logback.xml`，这个位置可以配置。Spring对于LogBack的配置做了一些拓展，如果想用这些拓展，就用`classpath:logback-spring.xml`，主要是在配置文件使用Spring配置文件的值，和针对不同的profile用不同的配置。

## 通用配置

可以在`application`里配置日志等级

```properties
logging.level.root=warn
logging.level.org.springframework.web=debug
logging.level.org.hibernate=error
```

# LogBack自定义配置

https://logback.qos.ch/manual/configuration.html#autoScan

配置文件通常是由0到若干个appender、0到若干个logger、最多1个root来构成的。



