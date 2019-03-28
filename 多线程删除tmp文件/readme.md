### 此脚本在python3下运行
### 需要模块

- hdfs
- multiprocessing
- os
- time

### 离线安装hdfs模块，需要的依赖均放于文件夹中，看报错有序安装

### 注意
- 此脚本如果未在NAMENODE节点运行，请修改hdfs_url中的路径
- 如果删除其他路径的问价和目录，请修改hdfs_path中的路径
- 如果要删除的天数不是10天，请修改last_days中的值

### 执行方式 `python3 delete_hive_tmp_multiprocess.py`