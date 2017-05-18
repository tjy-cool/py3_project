#!/usr/bin/env python
# Funtion:      
# Filename:

import json, time, os
from conf import settings
import re

def get_all_username():
    '''
    获得data/accouonts 文件夹下的用户名列表
    :return: 已经注册了得用户名列表，如果没有一个用户注册，则返回空列表
    '''
    userdata_path = '%s/db/accounts' % settings.BASE_DIR
    userfile_name_list = os.listdir(userdata_path)
    all_user = []
    if userfile_name_list != []:
        for userfile_name in userfile_name_list:
            all_user.append(userfile_name.split('.')[0])
    return all_user

def get_user_db(username):
    userdata_path = '%s/db/accounts' % settings.BASE_DIR
    userfile = '%s/%s.json' % (userdata_path, username)
    with open(userfile, 'r', encoding='utf-8') as f:
        user_db = json.load(f)
    return user_db

def set_user_db(username,user_db):
    userdata_path = '%s/db/accounts' % settings.BASE_DIR
    userfile = '%s/%s.json' % (userdata_path, username)
    with open(userfile, 'w', encoding='utf-8') as fp:
        json.dump(user_db, fp, indent=4)