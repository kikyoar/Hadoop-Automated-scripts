#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

@author: kikyoar
@contact: nokikyoar@gmail.com
@time: 2019/1/3 18:18

"""

import os
import re

"""
    脚本适用于新安装的服务器
    jdk包请放置在opt目录下
    1、查看是否安装JDK（java -version）
    2、如果安装卸载
    3、开始部署
"""
# java版本路径
java_source_path = "/opt/jdk-8u181-linux-x64.tar.gz"
java_install_path = "/usr/local/jdk1.8.0_181/"
java_install_link = "/usr/local/java"


# 判断是否安装java
def isInstall_Jdk():
    os.system("java -version 2> /tmp/jdk_version")
    file = "/tmp/jdk_version"
    # 从文件的大小来判断文件是都为空
    if os.path.getsize(file) > 0:
        with open(file) as filereader:
            str_reader = filereader.read()
            jdk_version = re.findall(r'"\d.*\d"', str_reader)
            print("您的JDK版本为：" + jdk_version[0] + "，准备要卸载啦！✧(≖ ◡ ≖✿)嘿嘿")
            remove_Jdk()
    else:
        print("你现在没有安装java，稍等会安装新的java，✧(≖ ◡ ≖✿)嘿嘿")


# 卸载openjdk
def remove_Jdk():
    # 卸载rpm安装的jdk版本
    os.system("rpm -qa|grep jdk > /tmp/jdk_rpminstall")
    file = "/tmp/jdk_rpminstall"
    if os.path.getsize(file) > 0:
        """
        copy-jdk-configs-3.3-10.el7_5.noarch
        java-1.8.0-openjdk-headless-1.8.0.191.b12-1.el7_6.x86_64
        java-1.8.0-openjdk-1.8.0.191.b12-1.el7_6.x86_64
        """
        print("************************uninstalling************************")
        print("卸载rpm安装的jdk版本")
        for line in open(file):
            if "java-" in line:
                os.system("rpm -e --nodeps " + line)
        print("已清理完成，可以安装新版本了")

    # 卸载自带的jdk版本
    os.system("rpm -qa|grep gcj  > /tmp/jdk_selfinstall")
    file1 = "/tmp/jdk_selfinstall"
    if os.path.getsize(file1) > 0:
        print("************************uninstalling************************")
        print("卸载自带的jdk版本")
        for line in open(file1):
            if "java-" in line:
                os.system("rpm -e --nodeps " + line)
        print("已清理完成，可以安装新版本了")


# 安装java
def jdk_install():
    print("************************installing************************")
    print("************************开始解压************************")
    os.system("tar -zxvf " + java_source_path + " -C /usr/local")
    os.system("ln -s" + java_install_path + java_install_link)
    print("************************开始配置环境变量************************")
    os.system("echo 'export JAVA_HOME=" + java_install_link + "' >>/etc/profile ")
    os.system("echo 'export JRE_HOME=${JAVA_HOME}/jre' >>/etc/profile")
    os.system("echo 'export CLASSPATH=.:$JAVA_HOME/lib:$JRE_HOME/lib' >>/etc/profile")
    os.system("echo 'export PATH=$JAVA_HOME/bin:$PATH:$HOME/bin:$JAVA_HOME/bin' >>/etc/profile")
    os.system("source /etc/profile")
    print("安装完毕,请切换终端检查，Enjoy！")


if __name__ == "__main__":
    print("运行注意：注意java版本路径，如果非默认，请修改路径和版本，此脚本必须使用root权限执行")
    remove_Jdk()
    jdk_install()
