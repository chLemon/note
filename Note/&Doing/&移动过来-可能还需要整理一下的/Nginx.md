# Nginx
1. 安装
2. 静态网站部署
3. 反向代理和负载均衡的配置

## 安装
环境准备
gcc
PCRE
zlib
OpenSSL

下载

安装：
configure【有超多参数】
make
make install
创建临时目录【configure里面配的】

启动：
./nginx
./nginx -s quit/stop【停止，quit会保存配置，stop相当于非正常退出】
./nginx -s reload

## 静态网站部署
配置conf/nginx.conf
修改location
root后的目录名

## 虚拟主机
conf/nginx.conf
里写多个server

servername可以写域名

## 反向代理与负载均衡
反向代理：代理服务端

反向代理配置：
upstream tomcat-travel-这个名字随便写{
	server ip:8080;
}
server{
	...
	location/{
		#root index;#默认访问目录，注释掉
		proxy_pass http://tomcat-travel;
	}
}

负载均衡：
upstream里多写几个
权重配置：
upstream tomcat-travel-这个名字随便写{
	server ip:8080 weight=2;
	server ip:8081;
}
权重默认是1，现在就是：8080 66%，8081 33%