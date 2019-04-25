### 写在开头的话
此为程序初版，测试过程较为单一，可能存在BUG，如果执行中有任何问题，请发邮件至**nokikyoar@gmail.com**

### 程序实现功能
主要为JDK的安装部署，Ambari的安装部署，Mariadb的安装部署，以及linux基础环境配置

### 程序执行顺序
程序最好放置于/opt/目录下
执行顺序为：
- 1、Jdk_Install.py
- 2、Basic_environment_configure.py
- 3、Mariadb_Install.py
- 4、Ambari_Install.py


### 脚本适用于新安装的服务器,适用于以下软件包安装
Python版本为3.6级以上，需要用到的第三方模块pexpect
需要提前准备的软件包，将其放置于/opt下：
- libtirpc-0.2.4-0.10.el7.x86_64.rpm
- ibtirpc-devel-0.2.4-0.10.el7.x86_64.rpm
- CentOS-7.4-x86_64-DVD-1708.iso
- HDP-UTILS-1.1.0.21-centos7.tar.gz
- HDP-2.6.3.0-centos7-rpm.tar.gz
- ambari-2.6.0.0-centos7.tar.gz
