#!/usr/bin/env python
# Funtion:      
# Filename:

import socket, json, os, time, sys, getpass, hashlib
from conf import settings
from core import logger
user_data_base_dir = settings.BASE_DIR+'/db'+'/home/'

class FTP_User_management(object):
    def __init__(self, HOST, PORT, log_obj):
        self.HOST = HOST
        self.PORT = PORT
        self.client = socket.socket()
        self.client.connect((self.HOST, self.PORT))
        self.log_obj = log_obj

    def run(self):
        username = input('username: ')
        passwd = input('passwd: ')
        if username == 'admin' and passwd == 'admin':
            user_dict = {
                'user_name': username,
                'passwd_md5': self.get_md5(passwd)
            }
            self.client.send(self.get_json(user_dict).encode('utf-8'))
            res = self.client.recv(1024).decode()
            print(res)
            if res == 'OK':
                self.welcome_login()    # 显示欢迎登陆信息
            else:
                exit('login faild!')
            while True:
                self.print_help()
                input_cmd = input('>>:').strip()
                cmd = input_cmd.split()[0]
                if hasattr(self, cmd):
                    func = getattr(self, input_cmd)
                    func(input_cmd)
                else:
                    print('\033[31;1mInvilid input, try again\033[0m')
                    continue
        else:
            exit('\033[31;1mInvilid username or password！\033[0m')

    def add_user(self, I_cmd):
        '''增加普通用户'''
        add_dict = settings.USER_DATA       # 用户数据
        user_name = input('input username: ').strip()
        password = input('input password: ').strip()
        disk_size = input('input size(b): ').strip()
        if disk_size.isnumeric():
            add_dict['disk_size'] = int(disk_size)
        else:
            exit('disk_size is a number, not a str')
        add_dict['func'] = 'add_user'
        add_dict['user_name'] = user_name
        add_dict['passwd_md5'] = self.get_md5(password)
        '''
        add_dict = {
            'func': 'add_user',
            'user_name': user_name,
            'passwd_md5': self.get_md5(password),
            'is_authenticated': -1,
            'locked': 0,  # 0表示已经未锁住了，1表示锁住了，输错了三次密码就会锁住
            'disk_size': disk_size
        }
        '''
        self.client.send(self.get_json(add_dict).encode('utf-8'))

        res = self.client.recv(1024).decode()
        if res == 'OK':
            self.log_obj.info('Add user [%s] successful!' % user_name)
        elif res == 'EXIST':
            self.log_obj.info("Add user error, [%s] has exist" % user_name)

    def del_user(self, I_cmd):
        '''删除用户信息，但是仍然会保留日志'''
        user_name = input('input username: ')
        del_dict = {
            'func': 'del_user',
            'user_name': user_name
        }
        self.client.send(self.get_json(del_dict).encode('utf-8'))
        res = self.client.recv(1024).decode()
        if res == 'OK':
            self.log_obj.info('del user [%s] successful!' % user_name)
        elif res == 'Not Found':
            print('Not found  user [%s]' % user_name)

    def query_user(self, I_cmd):
        ''' 查询用户信息 '''
        user_name = input('input username: ')
        query_dict = {
            'func': 'query_user',
            'user_name': user_name
        }
        self.client.send(self.get_json(query_dict).encode('utf-8'))
        res = self.client.recv(1024).decode()
        if res == 'Not Found':
            print('Not found  user [%s]' % user_name)
        else:
            print(json.dumps(res))
            self.log_obj.info('query user [%s] successful!' % user_name)

    def alter_user(self, I_cmd):
        ''' 更改用户信息 '''
        change_item = input('0 password   1 locked  2 disk size\ninput change item: ')
        user_name = input('input username: ')
        alter_dict = {
            'func': 'alter_user',
            'user_name': user_name
        }
        if change_item == '0':      # 修改密码 password
            alter_dict['alter_item'] = 'passwd_md5'
            # old_passwd = input('input your old password: ')     # 输入旧密码
            cnt = 0
            while True:
                new_passwd1 = input('input your new password:')     # 输入两次新密码
                new_passwd2 = input('input your new password again:')
                if new_passwd1 == new_passwd2:
                    # alter_dict['old_passwd_md5'] = self.get_json(old_passwd)
                    alter_dict['alter_info'] = self.get_md5(new_passwd1)
                    self.client.send(self.get_json(alter_dict).encode('utf-8'))
                    res = self.client.recv(1024).decode()
                    if res == 'OK':
                        self.log_obj.info('alter user [%s\'s] password successful!' % user_name)
                    elif res == 'Not Found':
                        print('Not found  user [%s]' % user_name)
                    # elif res == 'password error':
                    #     self.log_obj.info('alter user [%s\'s] password error! Input error old password' % user_name)
                else:
                    if cnt == 3:
                        print('Too many times attempt.')
                        break
                    else:
                        cnt += 1
                        print('twice input password is inconsistent! Try again.')
        if change_item == '1':  # 修改locked
            pass
        if change_item == '2':  # 修改 disk size
            alter_dict['alter_item'] = 'disk_size'
            new_disk = input('New disk size(b): ')
            alter_dict['alter_info'] = new_disk.strip()
            self.client.send(self.get_json(alter_dict).encode('utf-8'))
            res = self.client.recv(1024).decode()
            if res == 'OK':
                self.log_obj.info('alter user [%s\'s] disk size successful!' % user_name)
            elif res == 'Not Found':
                print('Not found  user [%s]' % user_name)

    def quit(self, I_cmd):
        self.client.close()     # 关闭客户端
        exit('see you next time,,, 88')

    def welcome_login(self):
        '''登陆欢迎信息'''
        self.log_obj.info('admin login in successful!')
        for i in range(6):
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(0.15)


    def print_help(self):
        print('(增加:add_user   删除:del_user   查询:query_user   更改:alter_user   退出:quit)')

    def get_md5(self, src_str):
        '''
        对输入的源字符串计算md5值，并返回
        :param src_str: 待计算md5的字符串
        :return: 计算出来的md5值
        '''
        md5 = hashlib.md5()  # 密码进行md5加密处理
        md5.update(bytes(src_str, 'utf-8'))
        return md5.hexdigest()

    def get_json(self, src):
        # 将数据格式化为json格式
        return json.dumps(src)

def run():
    print('client is running ...')
    log_obj = logger.logger('admin', True)
    client = FTP_User_management(settings.HOST, settings.PORT, log_obj)
    client.run()

