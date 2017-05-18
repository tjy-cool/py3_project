#!/usr/bin/env python
# Funtion:      
# Filename:
import sys,time
from data_base import data
def welcome():
    '''登陆欢迎信息'''
    for i in range(6) :
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(0.2)
    print("\nwelcome! you are login...")  # 相等打印欢迎信息


def login(user_file, err_file):
    '''
    用户登陆
    :param user_file: 用户密码保存文件
    :param err_file: 错误登陆保存文件
    :return: user用户名
    '''
    user_file = open(user_file, 'a+', encoding='utf-8')     # 打开文件
    err_file = open(err_file, 'a+', encoding='utf-8')
    username_passwd = data.file_2_dict(user_file)  # 用户名密码
    err_info_dict = data.file_2_dict(err_file,':') # 错误登陆
    max_try_cnt,try_cnt = 3,0                # 运行最大尝试次数
    # out_user = ''
    user = input('Please input your username: ')
    if user in username_passwd.keys():  # 判断用户名是否在username_passwd字典的key里面
        if user in err_info_dict.keys():  # 若用户名在错误信息文本中，则已经被锁定了
            print("you have been locked at time :", err_info_dict[user])
            exit()
        else:  # 用户名不在错误信息文本中，则可以正常输入和登陆
            while  try_cnt < max_try_cnt:
                password = input('Please input your password: ')
                if username_passwd[user] == password:  # 认证成功后欢迎信息 ,判断密码是否与真实密码相等
                    welcome()
                    # out_user = user
                    break  # 退出循环
                elif password == 'q':    # 取消重新登陆，直接退出程序
                    exit()
                else:   # 未达到三次，最大尝试次数减一
                    try_cnt += 1
                print('You have %s times chance' % (max_try_cnt-try_cnt))
            else:  # 输入三次错误后锁定
                localTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                if err_info_dict == {}:
                    err_file.write('%s:%s' %(user,localTime))
                else:
                    err_file.write("\n%s:%s" %(user, localTime))
                print("you have been locked...")
                exit()
    else:
        save_user = input("Do you want add a new user (y/n)? ")
        if (save_user == 'y'):
            cur_passwd = input('Please input a passwd for the new user:')
            username_passwd[user] = cur_passwd
            user_file.write('\n%s,%s' %(user, cur_passwd))
            # out_user = user
        else:
            exit()
    user_file.close()
    err_file.close()
    return user
