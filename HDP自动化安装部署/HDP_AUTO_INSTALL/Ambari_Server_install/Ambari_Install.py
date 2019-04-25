#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

@author: kikyoar
@contact: nokikyoar@gmail.com
@time: 2019/1/8 18:05

"""

import os
import pexpect

# JAVA路径
JAVA_HOME = "/usr/local/java"
# ambari数据库密码
ambari_password = "password"

# 安装ambari-server
print("************************安装ambari-server************************")
os.system("yum install -y ambari-server")

# 配置ambari-server
print("************************配置ambari-server************************")
"""
pexpect模块进行交互式配置
"""
sub1 = pexpect.spawnu("ambari-server setup")
# 提示是否自定义设置。输入：y或者默认跳过
sub1.expect("Customize")
sub1.sendline("")
# 选择3设置JAVA_HOME路径
sub1.expect("choice")
sub1.sendline("3")
sub1.expect("Path")
sub1.sendline(JAVA_HOME)
# 数据库配置
sub1.expect("database")
sub1.sendline("y")
sub1.expect("choice")
sub1.sendline("3")
sub1.expect("Hostname")
sub1.sendline("")
sub1.expect("Port")
sub1.sendline("")
sub1.expect("Database")
sub1.sendline("")
sub1.expect("Username")
sub1.sendline("")
sub1.expect("Password")
sub1.sendline(ambari_password)
sub1.expect("Re-enter")
sub1.sendline(ambari_password)
sub1.expect("remote")
sub1.sendline("y")

# 打印信息
sub1.expect(pexpect.EOF)
print(sub1.before)

"""
卸载ambari-server
yum remove ambari-server
rm -rf /var/lib/ambari-server/
rm -rf /etc/ambari-server/
"""

# 将Ambari数据库脚本导入到数据库
print("************************将Ambari数据库脚本导入到数据库************************")
os.system("""
mysql -uambari -p{ambari_password} <<EOF
use ambari;
source /var/lib/ambari-server/resources/Ambari-DDL-MySQL-CREATE.sql
EOF
""".format(ambari_password=ambari_password))

# 启动ambari-server
print("************************启动ambari-server************************")

# 修改ambari.properties,为了调用REST API
os.system("echo 'api.csrfPrevention.enabled=false' >>/etc/ambari-server/conf/ambari.properties")
os.system("systemctl start ambari-server")
