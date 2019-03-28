#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

@author: kikyoar
@contact: nokikyoar@gmail.com
@time: 2019/3/28 17:30

"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

@author: kikyoar
@contact: nokikyoar@gmail.com
@time: 2019/3/26 22:12

"""

import multiprocessing
import hdfs
import time
import os

"""
存在GIL问题，所以能用进程的时候，用进程，或者用C语言解决
"""

hdfs_url = "http://192.168.100.120:50070"
hdfs_path = "/tmp/hive/hive"
last_day = 60 * 60 * 24 * 1000
# 删除前10天的文件
last_days = 9 * last_day

# 获取当前时间
current_time = round(time.time() * 1000)

# 创建hdfs连接
client = hdfs.Client(hdfs_url, timeout=100, session=False)

# 遍历删除文件所在目录下的文件，深度遍历
for first_depth in client.walk(hdfs_path, depth=1, status=True):
    for second_depth in first_depth:
        if type(second_depth) == list and len(second_depth) != 0:
            # 输出所有的配置文件列表，里面以字典形式存放
            file_list = second_depth

# 使用字典保存文件名和文件时间
list_files = []
for file_tuple in file_list:
    # 生成文件名和文件修改最后修改时间的元组
    dict_tuple = (file_tuple[0], file_tuple[1]["modificationTime"])
    # 添加为列表
    list_files.append(dict_tuple)

dict_files_length = len(list_files)

print("使徒侵袭")
print("*" * 50)

# 输出/tmp/hive/hive存储文件数目
print("使徒的数量为：%s" % (dict_files_length))
print("*" * 50)
print("战斗准备，EVA冲啊！")
print("""
残酷な天使のように
少年よ神话になれ
""")


# 拆分列表

def list_of_groups(init_list, children_list_len):
    list_of_groups = zip(*(iter(init_list),) * children_list_len)
    end_list = [list(i) for i in list_of_groups]
    count = len(init_list) % children_list_len
    end_list.append(init_list[-count:]) if count != 0 else end_list
    return end_list


tmpfile_all = list_of_groups(list_files, int(dict_files_length / 3))

# 输出列表的长度
# print(len(tmpfile_all))

# 列表转换为字典
dict_files1 = dict(tmpfile_all[0])
dict_files2 = dict(tmpfile_all[1])
dict_files3 = dict(tmpfile_all[2])



def delete_file_10days(dict_files):
    """
    字典在遍历时不能进行修改，建议转成列表或集合处理
    """
    for expire_name in list(dict_files.keys()):
        # 删除15天之前的数据
        if (current_time - dict_files[expire_name]) > last_days:
            # 删除字典值
            del dict_files[expire_name]
                # 不采用api调用的原因是需要修改tmp权限，怕影响生产使用，所以改为os调用
            os.system("hdfs dfs -rm -r -skipTrash " + hdfs_path + "/" + expire_name)
                # recursive=True递归删除目录和子目录文件
                # client.delete(hdfs_path + "/" + expire_name, recursive=True)
            print("删除文件：" + hdfs_path + "/" + expire_name + "..........." + multiprocessing.current_process().name)


p1 = multiprocessing.Process(target=delete_file_10days, args=(dict_files1,), name="零号机")
p2 = multiprocessing.Process(target=delete_file_10days, args=(dict_files2,), name="初号机")
p3 = multiprocessing.Process(target=delete_file_10days, args=(dict_files3,), name="二号机")

p1.start()
p2.start()
p3.start()
# t1 = threading.Thread(target=delete_file_10days, args=(dict_files1,))
# t2 = threading.Thread(target=delete_file_10days, args=(dict_files2,))
# t3 = threading.Thread(target=delete_file_10days, args=(dict_files3,))
# t1.start()
# t2.start()
# t3.start()