#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

@author: kikyoar
@contact: nokikyoar@gmail.com
@time: 2019/1/7 18:08

"""

import os
import pexpect

# root密码
password = "Richr00t"
# ambari、hive、oozie密码
ambari_password = "password"
hive_password = "password"
oozie_password = "password"


# 安装Mariadb作为HIVE等Hadoop组件的metastore
os.system("yum install -y mariadb mariadb-server")
os.system("systemctl enable mariadb")
os.system("systemctl start mariadb")

# 配置mariadb

"""
pexpect模块进行交互式配置
"""
sub1 = pexpect.spawnu("mysql_secure_installation")
# Enter current password for root (enter for none):<–初次运行直接回车
sub1.expect("Enter")
sub1.sendline("")
# Set root password? [Y/n] <– 是否设置root用户密码，输入y并回车或直接回车
sub1.expect("Set")
sub1.sendline("Y")
# New password: <– 设置root用户的密码
sub1.expect("New")
sub1.sendline(password)
# Re-enter new password: <– 再输入一次你设置的密码
sub1.expect("Re-enter")
sub1.sendline(password)
# Remove anonymous users? [Y/n] <– 是否删除匿名用户
sub1.expect("Remove")
sub1.sendline("")
# Disallow root login remotely? [Y/n] <–是否禁止root远程登录
sub1.expect("Disallow")
sub1.sendline("n")
# Remove test database and access to it? [Y/n] <– 是否删除test数据库
sub1.expect("Remove")
sub1.sendline("")
# Reload privilege tables now? [Y/n] <– 是否重新加载权限表
sub1.expect("Reload")
sub1.sendline("")

sub1.expect(pexpect.EOF)
print(sub1.before)

# 配置Ambari库
# 创建Ambari, Hive, oozie等组件数据库及用户


os.system("""
#!/bin/bash
mysql -uroot -p{root_password} <<EOF
create database ambari character set utf8;
CREATE USER 'ambari'@'%'IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON *.* TO 'ambari'@'%' IDENTIFIED BY '{ambari_password}';
GRANT ALL PRIVILEGES ON *.* TO 'ambari'@'localhost' IDENTIFIED BY '{ambari_password}';
create database hive character set utf8 ;
CREATE USER 'hive'@'%'IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON *.* TO 'hive'@'%' IDENTIFIED BY '{hive_password}';
GRANT ALL PRIVILEGES ON *.* TO 'hive'@'localhost' IDENTIFIED BY '{hive_password}';
create database oozie character set utf8 ;
CREATE USER 'oozie'@'%'IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON *.* TO 'oozie'@'%' IDENTIFIED BY '{oozie_password}';
GRANT ALL PRIVILEGES ON *.* TO 'oozie'@'localhost' IDENTIFIED BY '{oozie_password}';
FLUSH PRIVILEGES;
""".format(root_password=password, ambari_password=ambari_password, hive_password=hive_password,
           oozie_password=oozie_password))

# 导入mysql jdbc驱动

os.system("yum install -y mysql-connector-java")



"""
卸载mariadb
yum remove mariadb
rm -rf /etc/my.cnf
rm -rf /var/lib/mysql/
"""