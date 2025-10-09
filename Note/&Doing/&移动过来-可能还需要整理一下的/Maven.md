# maven高级应用

## maven基础知识回顾

maven是一个项目管理工具
依赖管理：maven对项目中的jar包的管理过程。传统工程我们直接把jar包放置在项目中。
maven工程真正的jar包放置在仓库中，项目中只用放置jar包的坐标。

仓库的种类：本地仓库，远程仓库【私服】，中央仓库。
仓库之间的关系：当我们启动一个maven工程的时候，maven工程会通过pom文件中jar包的坐标去本地仓库找对应jar包
默认情况下，如果本地仓库没有对应jar包，maven工程会自动去中央仓库下载jar包到本地仓库。
在公司中，如果本地没有对应jar包，会先从私服下载jar包，如果私服没有jar包，可以从中央仓库下载，也可以从本地上传。

一键构建：maven自身集成了tomcat插件，可以对项目进行编译，测试，打包，安装，发布等操作。
maven常用命令：
clean，compile，test，package，install，deploy
maven三套生命周期：清理生命周期，默认生命周期，站点生命周期。

搭环境：
创建webapp，然后web.xml的头换一下，换成3.0【？】





brew install maven

mvn -version