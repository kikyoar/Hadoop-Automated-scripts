#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

@author: kikyoar
@contact: nokikyoar@gmail.com
@time: 2019/1/7 14:35

"""
import os
import subprocess

"""
脚本适用于新安装的服务器,适用于以下软件包安装
需要提前准备的软件包：
libtirpc-0.2.4-0.10.el7.x86_64.rpm
ibtirpc-devel-0.2.4-0.10.el7.x86_64.rpm
CentOS-7.4-x86_64-DVD-1708.iso
HDP-UTILS-1.1.0.21-centos7.tar.gz
HDP-2.6.3.0-centos7-rpm.tar.gz
ambari-2.6.0.0-centos7.tar.gz
"""

# ambari服务器主机名
hostname = "gsunicom-hdp-cluster-node-01"
linux_image = "/opt/CentOS-7.4-x86_64-DVD-1708.iso"
libtirpc = "/opt/libtirpc-0.2.4-0.10.el7.x86_64.rpm"
libtirpc_devel = "/opt/libtirpc-devel-0.2.4-0.10.el7.x86_64.rpm"
ambari_image = "/opt/ambari-2.6.0.0-centos7.tar.gz"
HDP_image = "/opt/HDP-2.6.3.0-centos7-rpm.tar.gz"
HDP_UTILS = "/opt/HDP-UTILS-1.1.0.21-centos7.tar.gz"
# ambari服务器IP地址
Ipaddress = "192.168.199.139"
http_path = "/var/www/html"

# 修改主机名
print("************************修改主机名************************")
os.system("hostnamectl --static set-hostname " + hostname)

# 关闭防火墙
print("************************关闭防火墙************************")
os.system("systemctl stop firewalld")
os.system("systemctl disable firewalld")

# 关闭SELinux
print("************************关闭SELinux************************")
os.system('sed -i "/SELINUX/s/enforcing/disabled/g" /etc/selinux/config')
os.system("setenforce 0")

# 配置yum源
"""
1、配置centos本地yum源
2、安装配置nginx
3、配置HDP本地yum源
"""
# 配置本地yum源
print("************************配置本地yum源************************")
subprocess.call(["mkdir /media/Centos;cd /etc/yum.repos.d/ && mkdir repo_bak && mv *.repo repo_bak/"], shell=True)
os.system("mount -o loop " + linux_image + " /media/Centos")
with open("/etc/yum.repos.d/centos7.repo", "w") as file:
    file.write("""
[BASE]
name=Centos7.4
baseurl=file:///media/Centos
gpgcheck=0
gpgkey=file:///media/Centos/RPM-GPG-KEY-CentOS-7
enabled=1
""")
os.system("yum clean all && yum makecache")

# 安装配置http
print("************************安装配置http************************")
os.system("yum install -y httpd")
# 修改80端口为5555
os.system('sed -i "/Listen/s/80/5555/g" /etc/httpd/conf/httpd.conf')
os.system("systemctl start httpd && systemctl enable httpd")

# 配置HDP远程yum源
print("************************配置HDP远程yum源************************")
subprocess.call(["mkdir /var/www/html/HDP;mkdir /var/www/html/HDP-UTILS"], shell=True)
os.system("tar -zxvf " + ambari_image + " -C /var/www/html")
os.system("tar -zxvf " + HDP_image + " -C /var/www/html/HDP")
os.system("tar -zxvf " + HDP_UTILS + " -C /var/www/html/HDP-UTILS")

"""
os.path.walk(path) 遍历path，返回一个三元组（dirpath, dirnames, filenames). dirpath表示遍历到的路径,
dirnames表示该路径下的子目录名，是一个列表, filesnames表示该路径下的文件名，也是一个列表. 例如: 当遍历到c:\windows时，
dirpath="c:\windows", dirnames是这个路径下所有子目录名的列表，filenames是这个路径下所有文件名的列表
"""
dirpaths = []
ambari_path = ""
HDP_path = ""
HDPUTILS_path = ""
for (dirpath, dirnames, filenames) in os.walk(http_path):
    dirpaths.append(dirpath)

for dirpath in dirpaths:
    if "ambari" in dirpath:
        list_split = dirpath.split('/')
        if len(list_split) == 7:
            # 提取目录
            ambari_paths = dirpath
            # 提取相对路径
            ambari_path = ambari_paths[14:]
    elif "HDP/HDP" in dirpath:
        list_split = dirpath.split('/')
        if len(list_split) == 8:
            # 提取目录
            HDP_paths = dirpath
            # 提取相对路径
            HDP_path = HDP_paths[14:]
            # 提取HDP版本
            HDP_Version = HDP_paths[30:]
    elif "UTILS" in dirpath:
        print(dirpath)
        list_split = dirpath.split('/')
        if len(list_split) == 5:
            # 提取目录
            HDPUTILS_paths = dirpath

            # 提取相对路径
            HDPUTILS_path = HDPUTILS_paths[14:]
print("***********")
print(HDP_paths)
print(HDPUTILS_paths)
print(HDP_Version)
with open("/etc/yum.repos.d/ambari.repo", "w") as file:
    file.write(
        """

[ambari]
name=ambari
baseurl=http://{Ipaddress}:5555/{ambari_path}
gpgcheck=1
gpgkey=http://{Ipaddress}:5555/{ambari_path}/RPM-GPG-KEY/RPM-GPG-KEY-Jenkins
enabled=1
priority=1



[HDP-2.6-repo-1]
name=HDP-2.6-repo-1
baseurl=http://{Ipaddress}:5555/{HDP_path}
gpgcheck=1
gpgkey=http://{Ipaddress}:5555/{HDP_path}/RPM-GPG-KEY/RPM-GPG-KEY-Jenkins
enabled=1
priority=1


[HDP-UTILS-2.6-repo-1]
name=HDP-UTILS-2.6-repo-1
baseurl=http://{Ipaddress}:5555/{HDPUTILS_path}
gpgcheck=1
gpgkey=http://{Ipaddress}:5555/{HDPUTILS_path}/RPM-GPG-KEY/RPM-GPG-KEY-Jenkins
enabled=1
priority=1

""".format(Ipaddress=Ipaddress, ambari_path=ambari_path, HDP_path=HDP_path, HDPUTILS_path=HDPUTILS_path))
os.system("yum clean all && yum makecache")

# 配置Centos7远程yum源
print("************************配置本地yum源************************")
subprocess.call(["mkdir /var/www/html/Centos;cd /etc/yum.repos.d/ && rm -rf /etc/yum.repos.d/centos7.repo"], shell=True)
os.system("mount -o loop " + linux_image + " /var/www/html/Centos")
with open("/etc/yum.repos.d/centos7.repo", "w") as file:
    file.write("""
[BASE]
name=Centos7.4
baseurl=http://{Ipaddress}:5555/Centos
gpgcheck=0
gpgkey=http://{Ipaddress}:5555/Centos/RPM-GPG-KEY-CentOS-7
enabled=1
""".format(Ipaddress=Ipaddress))
os.system("yum clean all && yum makecache")


# 安装libtirpc
print("************************安装libtirpc************************")
os.system("rpm -i " + libtirpc)
os.system("rpm -i " + libtirpc_devel)

# 安装配置本地NTP服务器
print("************************安装配置本地NTP服务器************************")
os.system("yum install -y ntp")
os.system("sed -i 's#server 0.centos.pool.ntp.org iburst##g' /etc/ntp.conf")
os.system("sed -i 's#server 1.centos.pool.ntp.org iburst##g' /etc/ntp.conf")
os.system("sed -i 's#server 2.centos.pool.ntp.org iburst##g' /etc/ntp.conf")
os.system("sed -i 's#server 3.centos.pool.ntp.org iburst##g' /etc/ntp.conf")
os.system("echo -e 'server 127.127.1.0\nfudge 127.127.1.0 stratum 10' >> /etc/ntp.conf")
os.system("systemctl start ntpd && systemctl enable ntpd")

# SSH 免密登录本机
print("************************SSH 免密登录本机************************")
os.system("ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa")
os.system("cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys")

# 由于HDP2.6版本以上不能直接put Local Repository，因此必须修改HDP-2.6.3.0-235.xml，真的好气啊
# 参考文档https://docs.hortonworks.com/HDPDocuments/Ambari-2.6.0.0/bk_ambari-release-notes/content/ambari_relnotes-2.6.0.0-behavioral-changes.html

# print("************************HDP.xml配置更改************************")
# os.system("cd {HDP_paths} && cp HDP-{HDP_Version}.xml HDP-{HDP_Version}.xml.bak".format(HDP_paths=HDP_paths,
#                                                                                         HDP_Version=HDP_Version))
# with open("/var/www/html/HDP/HDP/centos7/2.6.3.0-235/HDP-2.6.3.0-235.xml", "w") as file:
#     file.write("""<?xml version="1.0"?>
# <repository-version xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="version_definition.xsd">
#   <release>
#     <type>STANDARD</type>
#     <stack-id>HDP-2.6</stack-id>
#     <version>2.6.3.0</version>
#     <build>235</build>
#     <compatible-with>2\.[3-6]\.\d+\.\d+</compatible-with>
#     <release-notes>http://example.com</release-notes>
#     <display>HDP-2.6.3.0</display>
#   </release>
#   <manifest>
#     <service id="PIG-0160" name="PIG" version="0.16.0"/>
#     <service id="KAFKA-0101" name="KAFKA" version="0.10.1"/>
#     <service id="SPARK2-220" name="SPARK2" version="2.2.0"/>
#     <service id="KNOX-0120" name="KNOX" version="0.12.0"/>
#     <service id="OOZIE-420" name="OOZIE" version="4.2.0"/>
#     <service id="DRUID-0101" name="DRUID" version="0.10.1"/>
#     <service id="ATLAS-080" name="ATLAS" version="0.8.0"/>
#     <service id="RANGER-070" name="RANGER" version="0.7.0"/>
#     <service id="RANGER_KMS-070" name="RANGER_KMS" version="0.7.0"/>
#     <service id="ZEPPELIN-073" name="ZEPPELIN" version="0.7.3"/>
#     <service id="ACCUMULO-170" name="ACCUMULO" version="1.7.0"/>
#     <service id="HBASE-112" name="HBASE" version="1.1.2"/>
#     <service id="HIVE-121000" name="HIVE" version="1.2.1000"/>
#     <service id="MAHOUT-090" name="MAHOUT" version="0.9.0"/>
#     <service id="TEZ-070" name="TEZ" version="0.7.0"/>
#     <service id="SPARK-163" name="SPARK" version="1.6.3"/>
#     <service id="FLUME-152" name="FLUME" version="1.5.2"/>
#     <service id="SQOOP-146" name="SQOOP" version="1.4.6"/>
#     <service id="SLIDER-0920" name="SLIDER" version="0.92.0"/>
#     <service id="HDFS-273" name="HDFS" version="2.7.3"/>
#     <service id="YARN-273" name="YARN" version="2.7.3"/>
#     <service id="MAPREDUCE2-273" name="MAPREDUCE2" version="2.7.3"/>
#     <service id="ZOOKEEPER-346" name="ZOOKEEPER" version="3.4.6"/>
#     <service id="FALCON-0100" name="FALCON" version="0.10.0"/>
#     <service id="STORM-110" name="STORM" version="1.1.0"/>
#   </manifest>
#   <available-services/>
#   <repository-info>
#     <os family="redhat7">
#       <package-version>2_6_3_0_*</package-version>
#       <repo>
#         <baseurl>http://{Ipaddress}:5555/{HDP_path}</baseurl>
#         <repoid>HDP-2.6</repoid>
#         <reponame>HDP</reponame>
#         <unique>true</unique>
#       </repo>
#       <repo>
#         <baseurl>http://{Ipaddress}:5555/{HDPUTILS_path}</baseurl>
#         <repoid>HDP-UTILS-1.1.0.21</repoid>
#         <reponame>HDP-UTILS</reponame>
#         <unique>false</unique>
#       </repo>
#     </os>
#   </repository-info>
# </repository-version>
# """.format(Ipaddress=Ipaddress, HDP_path=HDP_path, HDPUTILS_path=HDPUTILS_path))

print("基础环境已配置结束，请手动重启操作系统")
print("基础环境已配置结束，请手动重启操作系统")
print("基础环境已配置结束，请手动重启操作系统")
print("重要的话说三遍，O(∩_∩)O哈哈~")
