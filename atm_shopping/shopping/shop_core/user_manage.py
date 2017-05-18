#!/usr/bin/env python
# Funtion:      
# Filename:

from data_base import default_db

def run():
    menu_title = "\033[31;m User Management Action Menu \033[0m".center(55, '-')
    # menu_title = ("\033[31;m %s's Bank Action Menu \033[0m" % acc_data['account_id']).center(55, '-')
    menu_body = '''\033[32;1m
        1. 增加用户
        2. 重置密码
        3. 修改密码
        4. 注销用户       
        5. 冻结用户\033[0m
'''
    menu = menu_title + menu_body + '-' * 44
    menu_dict = {
        '1': add_user,
        '2': change_passwd,
        '3': reset_passwd,
        '4': logoff,
        '5': freeze,
    }
    exit_flag = False
    while not exit_flag:
        print(menu)
        user_option = input('>> ').strip()
        if user_option in menu_dict:
            menu_dict[user_option]()
        elif user_option == 'q':
            exit()
        else:
            print("\033[31;1mOption does not exist!\033[0m")

def add_user():
    username = input()
    pass

def reset_passwd():
    pass

def change_passwd():
    pass

def logoff():
    pass

def freeze():
    pass


