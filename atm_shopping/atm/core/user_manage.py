#!/usr/bin/env python
# Funtion:      
# Filename:

from db import default_db
from core import logger
from core import data_handler
import os

def run():
    menu_title = "\033[31;m User Management Action Menu \033[0m".center(55, '-')
    # menu_title = ("\033[31;m %s's Bank Action Menu \033[0m" % acc_data['account_id']).center(55, '-')
    menu_body = '''\033[32;1m
    1. 注册用户     2. 重置密码     
    3. 修改密码     4. 注销用户     
    5. 冻结用户     6. 解冻用户
    7. 修改期限     8. 修改额度\033[0m
'''
    menu = menu_title + menu_body + '-' * 44
    menu_dict = {
        '1': registered_user,
        '2': change_passwd,
        '3': reset_passwd,
        '4': logoff,
        '5': freeze,
        '6': unfreeze,
        '7': change_expire_date,
        '8': change_balance
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

def registered_user():
    username = input('Please input a username: ')
    all_user = data_handler.get_all_username()  # 存在data/accounts文件夹下的所有用户
    if username in all_user:
        print('[%s] has been registered' % username)
    else:
        password = input('Please input password: ')
        user_db = default_db.default_db  # 为新用户增加用户数据
        user_db['id'] = username
        user_db['password'] = password
        data_handler.set_user_db(username, user_db)

        ac_log_obj = logger.set_ac_logger(username, 'access')
        ac_log_obj.info('registered successful')
        print('\033[32;1maccount [%s] registered successfull\033[0m' % username)

def reset_passwd():
    username = input('Please input a username: ')
    all_user = data_handler.get_all_username()  # 存在data/accounts文件夹下的所有用户
    if username not in all_user:
        print('[%s] is not been registered')
    else:
        user_db = data_handler.get_user_db(username)
        user_db['password'] = default_db.default_password
        data_handler.set_user_db(username, user_db)

        ac_log_obj = logger.set_ac_logger(username, 'access')
        ac_log_obj.info('reset password successful')
        print('\033[32;1maccount [%s] reset password successfull!\033[0m' % username)

def change_passwd():
    username = input('Please input a username: ')
    all_user = data_handler.get_all_username()  # 存在data/accounts文件夹下的所有用户
    if username not in all_user:
        print('No user named [%s]' % username)
    else:
        user_db = data_handler.get_user_db(username)
        old_passwd = input('Please input old password: ')   # 输入旧密码
        if old_passwd == user_db['password']:
            new_passwd = input('Please input new password: ').strip()
            new_passwd2 = input('Please input new password: ').strip()
            if new_passwd == new_passwd2 and new_passwd != '':
                user_db['password'] = new_passwd
                data_handler.set_user_db(username, user_db)
                ac_log_obj = logger.set_ac_logger(username, 'access')
                ac_log_obj.info('change password successful')
                print('\033[32;1maccount [%s] change password successfull\033[0m' % username)
            else:
                print('You have input two different password')
        else :
            print('You input an error password')

def logoff():
    '''
    注销用户删除所有用户数据
    :return: 
    '''
    is_logoff = input('\033[31;1mWarning!\033[0m This will delete all data of the user, Do you want continue?(Y/N): ')
    if is_logoff == 'Y':
        username = input('Please input a username: ')
        all_user = data_handler.get_all_username()  # 存在data/accounts文件夹下的所有用户
        if username not in all_user:
            print('No user named [%s]' % username)
        else:   # 删除用户数据, 日志
            Base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            os.remove('%s/data_base/accounts/%s.json' % (Base_path, username))
            os.remove('%s/log/access_log/%s_access.log' % (Base_path, username))
            os.remove('%s/log/transaction/%s_transactions.log' %(Base_path, username))
            print('logoff [%s] successful' % username)
    elif is_logoff == 'N':
        pass


def freeze():
    '''
    冻结用户，即用户不能进行登陆及其他操作
    :return: 
    '''
    username = input('Please input a username: ')
    all_user = data_handler.get_all_username()  # 存在data/accounts文件夹下的所有用户
    if username not in all_user:
        print('No user named [%s]' % username)
    else:
        user_db = data_handler.get_user_db(username)
        user_db['status'] = 2
        data_handler.set_user_db(username, user_db)
        ac_log_obj = logger.set_ac_logger(username, 'access')
        ac_log_obj.info('freeze username [%s] successful!' % username)
        print('freeze username [%s] successful!' % username)

def unfreeze():
    '''
    解冻用户
    :return: 
    '''
    username = input('Please input a username: ')
    all_user = data_handler.get_all_username()  # 存在data/accounts文件夹下的所有用户
    if username not in all_user:
        print('No user named [%s]' % username)
    else:
        user_db = data_handler.get_user_db(username)
        user_db['status'] = 0
        data_handler.set_user_db(username, user_db)
        ac_log_obj = logger.set_ac_logger(username, 'access')
        ac_log_obj.info('freeze username [%s] successful!' % username)
        print('freeze username [%s] successful!' % username)

def change_expire_date():
    username = input('Please input a username: ')
    all_user = data_handler.get_all_username()  # 存在data/accounts文件夹下的所有用户
    if username not in all_user:
        print('No user named [%s]' % username)
    else:
        user_db = data_handler.get_user_db(username)
        new_expire_date = input('Please input new expire date: ')   # 输入旧密码
        user_db['password'] = new_expire_date
        data_handler.set_user_db(username, user_db)
        ac_log_obj = logger.set_ac_logger(username, 'access')
        ac_log_obj.info('change expire data successful')
        print('\033[32;1maccount [%s] change expire data successfull\033[0m' % username)

def change_balance():
    username = input('Please input a username: ')
    all_user = data_handler.get_all_username()  # 存在data/accounts文件夹下的所有用户
    if username not in all_user:
        print('No user named [%s]' % username)
    else:
        user_db = data_handler.get_user_db(username)
        new_balance = input('Please input new balance: ')   # 输入旧密码
        user_db['password'] = new_balance
        data_handler.set_user_db(username, user_db)
        ac_log_obj = logger.set_ac_logger(username, 'access')
        ac_log_obj.info('change balance successful')
        print('\033[32;1maccount [%s] change balance successfull\033[0m' % username)