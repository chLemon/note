# 堆内存不足

IDEA Help >> Change Memory Settings 增大IDEA的运行内存，Settings >> Build, Execution, Deployment >> Compiler >> Build Process >> Shared heap size 增大程序堆内存

# Maven报错Blocked mirror for repositories

可以通过以下方式解决：应用程序 >> IDEA 显示包内容 >> `../Contents/plugins/maven/lib/maven3/conf/settings.xml` 文件中注释掉 `maven-default-http-blocker` 相关内容
![](./应用程序.png)
![](./需要注释的内容.png)