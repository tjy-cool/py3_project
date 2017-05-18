#!/usr/bin/env python
# Funtion:      
# Filename:

import json, time,os
import sys
from core import logger
from conf import settings
from core import data_handler
from db import default_db

def login_acquired(func):
    def wripper(*args, **kwargs):
        if args[0]['is_authenticated'] == False:
            print('\033[31;0mNo user authenticated. Please authenticated\033[0m')
            login(args[0])
        return func(*args, **kwargs)
    return wripper

def login(acc_data):
    username = input('account: ')
    ac_log_obj = logger.set_ac_logger(username, 'access')

    max_try_cnt, try_cnt = 3, 0  # 运行最大尝试次数
    all_user = data_handler.get_all_username()  # 存在data/accounts文件夹下的所有用户
    if username in all_user:  # 用户名存在
        user_db = data_handler.get_user_db(username)
        last_login_time = user_db['last_login_time']
        if user_db['status'] == 0:  # 正常状态
            while try_cnt < max_try_cnt:
                password = input('Please input your password(quit:q): ')
                # 认证成功后欢迎信息 ,判断密码是否与真实密码相等
                if user_db['password'] == password:
                    welcome_login()  # 欢迎信息
                    ac_log_obj.info('you are login')
                    acc_data['is_authenticated'] = True
                    acc_data['account_id'] = username
                    return acc_data  # 退出循环
                elif password == 'q':  # 取消重新登陆，直接退出程序
                    exit()
                else:  # 未达到三次，最大尝试次数减一
                    try_cnt += 1
                print('You have \033[1;35m%s times chance\033[0m' % (max_try_cnt - try_cnt))
            else:  # 输入三次错误后锁定
                # localTime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
                user_db['last_login_time'] = time.time()  # 时间戳
                user_db['status'] = 1
                data_handler.set_user_db(username, user_db)
                ac_log_obj.error("too many login attempts")
                print("you have been locked...")
                exit()
            pass
        elif user_db['status'] == 1:  # 锁定状态
            print("you have been locked at the time:"
                  "\033[1;32m %s\033[0m " % last_login_time)  # 高亮显示锁定时间
            pass
        elif user_db['status'] == 2:  # 注销状态，即不可见
            print("you have been revoke your account at the time： "
                  "\033[1;32m %s\033[0m " % last_login_time)  # 高亮显示吊销账号时间
            pass
        pass
    else:  # 用户名不存在，提示是否重新注册
        want_add_user = input("Do you want add a new account (y/n)? ")
        if (want_add_user == 'y'):
            add_user = input('Please input a new account: ')  # 输入用户名密码
            add_passwd = input('Please input a passwd: ')
            user_db = default_db.default_db  # 为新用户增加用户数据
            user_db['id'] = add_user
            user_db['password'] = add_passwd
            data_handler.set_user_db(add_user, user_db)

            ac_log_obj = logger.set_ac_logger(username, 'access')
            ac_log_obj.info('account [%s] are login' % add_user)
            acc_data['is_authenticated'] = True
            acc_data['account_id'] = username
            return acc_data  # 退出循环
        else:
            exit()

def welcome_login():
    '''登陆欢迎信息'''
    for i in range(6) :
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(0.15)

    print("\nwelcome!")  # 相等打印欢迎信息  you are login...