#!/usr/bin/env python
# Funtion:
# Filename:

import os
import logging
import json

# xxx\Fabric_host
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
host_json_file_path = BASE_DIR+'\db\host_list.json'
HOST, PORT = '192.168.1.109', 9999


# log等级设置
Admin_LOG_LEVEL = logging.INFO      # 管理员用户的log等级
LOG_LEVEL = logging.INFO    # 默认log等级，五个等级为debug，info，warning，error，critical
IsShowonScreen = False      # 是否在屏幕上显示
# log在屏幕上显示格式
Ch_Format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# log在文件中显示格式
Fh_Format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# log文件存储位置     "%s/log/%s_log" % (settings.BASE_DIR,username)

if __name__ == "__main__":
    with open(host_json_file_path, 'r', encoding='utf-8') as f:
        aa = json.load(f)
        print(aa[0]['host'])
    # print(host_json_file_path)
