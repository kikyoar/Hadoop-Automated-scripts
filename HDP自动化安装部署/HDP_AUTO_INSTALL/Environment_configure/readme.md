# 基于自动化配置HDP基础环境
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
- 将需要配置基础环境的主机IP地址填写于hosts文件required_java下

		[required_java]
		192.168.6.62

- 将defaults目录下的environment_configure.yaml拷贝至/etc/ansible/目录下
- 修改files目录下的ntp.conf中的“server 192.168.100.120”，改为自己的server IP
- 在/etc/ansible/执行命令，如若未发生报错，执行下一步
	
		[root@ceshi-1 ansible]# ansible-playbook -C environment_configure.yaml
- 在/etc/ansible/执行命令

		[root@ceshi-1 ansible]# ansible-playbook environment_configure.yaml
		
- 以上安装完成