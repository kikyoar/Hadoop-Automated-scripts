# 基于自动化部署JAVA
> 本项目是自动化部署安装JAVA  
> 当前版本是：v1.0

### 写在开头的话
此为程序初版，测试过程较为单一，可能存在BUG，如果执行中有任何问题，请发邮件至**nokikyoar@gmail.com**

## 所需软件
`以下版本均可自行定义`  

|软件名称|软件版本|
|:----------------|:-------------|
|ansible  | ansible 2.7.0 |
|java| 1.8.0_181  |

## 操作指南

- 可利用yum安装ansible，有外网环境的话安装Python3.6，亦可pip3安装ansible(这样ansible版本较高)
- 配置ansible：ansible目录应该默认在/etc/ansible下，此目录下必须有如下文件
	- ansible.cfg,[github下载](https://raw.githubusercontent.com/ansible/ansible/devel/examples/hosts)
	- hosts,[github下载](https://raw.githubusercontent.com/ansible/ansible/devel/examples/hosts)
	- roles目录
- 设置SSH免密登录安装java的主机(最好修改好主机名,命名格式参考gsunicom-hdp-cluster-node-01)
- 将压缩包java_install.zip解压拷贝至roles目录下
- 将需要安装java的主机IP地址填写于hosts文件required_java下

		[required_java]
		192.168.6.62
		
- 此压缩包中已自带java(jdk-8u181-linux-x64.tar.gz)--由于文件太大未上传（雾）,如果有新的java版本需求，请上传至files目录下替换该文件，然后修改vars目录下main.yaml中的value值

		java_packages: jdk-8u181-linux-x64.tar.gz
		java_install_name: jdk1.8.0_181

- 将defaults目录下的java_roles.yaml拷贝至/etc/ansible/目录下
- 在/etc/ansible/执行命令，如若未发生报错，执行下一步
	
		[root@ceshi-1 ansible]# ansible-playbook -C java_roles.yaml
- 在/etc/ansible/执行命令

		[root@ceshi-1 ansible]# ansible-playbook java_roles.yaml
		
- 以上安装完成
