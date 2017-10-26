#!/usr/bin/env python
# Funtion:
# Filename:


import socketserver
import re
import json
import hashlib
import os
import time
from conf import settings

user_data_base_dir = settings.BASE_DIR + '/db' + '/home/'
user_info_dir = settings.BASE_DIR + '/db' + '/username_passwd/'


class MyTCPHandlers(socketserver.BaseRequestHandler):
    def handle(self):
        user_data = self.authentication()  # 用户认证
        if user_data:      # 登陆成功
            while True:
                try:
                    self.data = self.request.recv(1024).decode()
                    print('data: %s' % self.data)
                    # if len(self.data):  # 表明已经断开了连接
                    #     print('断开了一个连接')
                    self.data = self.loads_from_json(self.data)

                    cmd = self.data['func'].split(' ')[0]
                    if hasattr(self, cmd):
                        func = getattr(self, cmd)
                        func(self.data)

                except ConnectionResetError as e:
                    # if user_data['user_name'] is not'admin' and user_data is not None:
                    #     user_data['is_authenticated'] = 0   # 将登陆状态清0
                    #     with open(user_info_dir+'.json', 'w', encoding='utf-8') as f:
                    #         json.dump(user_data, f)
                    print('error:', e)

    def authentication(self):   # 用户登陆函数
        Max_count = 3
        input_count = 0
        self.user_data = self.request.recv(1024).decode()
        if self.user_data == '':    # 表明已经断开了连接
            print('===断开了一个连接')
        print(self.user_data)
        User_data = self.loads_from_json(self.user_data)
        username = User_data['user_name']
        passwd_md5 = User_data['passwd_md5']
        if username == 'admin':     # 系统用户
            if passwd_md5 == self.get_md5('admin'):
                print('admin login in successful!')
                self.request.send(b'OK')
                print('OK')
                return User_data
            else:
                self.request.send(b'ERROR')
                print('None')
                return None

        else:       # 其他用户
            while input_count < Max_count:
                # print(user_info_dir+username+'.json',   os.path.isfile(user_info_dir + username + '.json'))
                if os.path.isfile(user_info_dir + username + '.json'):   # 存在该用户数据
                    with open(user_info_dir + username + '.json', 'r', encoding='utf-8') as f:    # 读取用户数据
                        user_db = json.loads(f.read())
                        if user_db['passwd_md5'] == passwd_md5:     # 密码验证有效
                            if user_db['is_authenticated'] == -1:
                                user_db['is_authenticated'] = 0  # 本次登陆有效
                            elif user_db['is_authenticated'] == 1:
                                user_db['is_authenticated'] = 1
                            self.request.send(self.get_json(
                                user_db).encode('utf-8'))  # 发送该用户的数据
                            with open(user_info_dir + username + '.json', 'w', encoding='utf-8') as f:
                                user_db['is_authenticated'] = - \
                                    1  # 针对其他设备来说来说，是已经在登陆过的了
                                json.dump(user_db, f, indent=4)
                            return user_db
                        else:       # 密码错误
                            user_db['passwd_md5'] = ''
                            # self.request.send(b'Error passwd')
                            self.request.send(self.get_json(
                                user_db).encode('utf-8'))  # 发送该用户的数据
                            input_count += 1
                else:   # 该用户不存在
                    User_data['user_name'] = ''
                    # self.request.send(b'None')
                    input_count += 1
                    self.request.send(self.get_json(
                        User_data).encode('utf-8'))  # 发送该用户的数据

    def add_user(self, Recv_dict):      # add_dict
        user_name = Recv_dict['user_name']
        Recv_dict.pop('func')
        if os.path.isfile(user_info_dir + user_name + '.json'):
            self.request.send(b'EXIST')
        else:
            with open(user_info_dir + user_name + '.json', 'w', encoding='utf-8') as f:
                json.dump(Recv_dict, f, indent=4)   # 先删除 'func'的键值
            os.chdir(user_data_base_dir)
            # 在linux中为mkdir, windows中为md
            print(os.popen('mkdir %s' % user_name).read())
            os.chdir(user_data_base_dir + user_name)    # 切换到用户路径下
            os.popen('touch %s.log' % user_name)
            self.request.send(b'OK')

    def del_user(self, Recv_dict):
        user_name = Recv_dict['user_name']
        if os.path.isfile(user_info_dir + user_name + '.json'):
            os.popen('rm %s' % (user_info_dir + user_name + '.json'))
            self.request.send(b'OK')
        else:
            self.request.send(b'Not Found')

    def query_user(self, Recv_dict):
        user_name = Recv_dict['user_name']
        if os.path.isfile(user_info_dir + user_name + '.json'):
            os.popen('rm %s' % (user_info_dir + user_name + '.json'))
            with open(user_info_dir + user_name + '.json', 'rb') as f:
                user_info_dict = json.load(f)
                del user_info_dict['passwd_md5']    # 删掉用户密码
                self.request.send(user_info_dict)
        else:
            self.request.send(b'Not Found')

    def alter_uer(self, Recv_dict):
        user_name = Recv_dict['user_name']
        if os.path.isfile(user_info_dir + user_name + '.json'):
            os.popen('rm %s' % (user_info_dir + user_name + '.json'))
            with open(user_info_dir + user_name + '.json', 'rb') as f:
                user_info_dict = json.load(f)
                user_info_dict[Recv_dict['alter_item']] = Recv_dict['alter_info']
            with open(user_info_dir + user_name + '.json', 'w') as f:
                json.dump(user_info_dict, f)
            self.request.send(b'OK')
        else:
            self.request.send(b'Not Found')

    def ls(self, I_cmd):
        # os.chdir(user_data_base_dir + I_cmd['re_dir'])
        # ls_res = os.popen(I_cmd['func']).read()
        # ls_res_bytes = bytes(ls_res, 'utf-8')
        # ls_dict = {
        #     'func': I_cmd['func'],
        #     'res_len': len(ls_res_bytes),     # 结果的长度
        #     'path': I_cmd['re_dir'],
        #     'run_successfully': True
        # }
        # self.request.send(self.get_json(ls_dict).encode('utf-8'))
        # comfirm_info = self.request.recv(1024).decode()
        # if comfirm_info == 'Ready to recv':
        #     self.request.send(ls_res_bytes)
        #     print('ls done...')
        self.no_change_cmd(I_cmd)

    def pwd(self, I_cmd):
        ''' pwd 显示当前文件夹的目录绝对目录 '''
        os.chdir(user_data_base_dir + I_cmd['re_dir'])
        current_abs_path = os.popen('pwd').read()   # 用户当前的绝对路径
        list1 = re.split(user_data_base_dir.strip(
            '/'), current_abs_path)  # 用正则模块对路径进行划分
        res_path = list1[1].strip('/').strip()                  # 去掉服务器的真实路径
        # res = os.popen(I_cmd['func']).read()
        res_bytes = bytes(res_path, 'utf-8')
        cmd_dict = {
            'func': I_cmd['func'],
            'res_len': len(res_bytes),  # 结果的长度
            'path': res_path,
            'run_successfully': True
        }
        self.request.send(self.get_json(cmd_dict).encode('utf-8'))
        comfirm_info = self.request.recv(1024).decode()
        if comfirm_info == 'Ready to recv':
            self.request.send(res_bytes)
            print('\033[32;1m%s done...\033[0m' % I_cmd['func'])

        # self.no_change_cmd(I_cmd)

    def ifconfig(self, I_cmd):
        self.no_change_cmd(I_cmd)

    def tree(self, I_cmd):
        '''
        tree 显示目录树
        :param I_cmd:
        :return:
        '''
        self.no_change_cmd(I_cmd)

    def date(self, I_cmd):
        '''时间'''
        self.no_change_cmd(I_cmd)

    def cal(self, I_cmd):
        '''日历'''
        self.no_change_cmd(I_cmd)

    def cat(self, I_cmd):
        '''cat'''
        self.no_change_cmd(I_cmd)

    def more(self, I_cmd):
        '''more'''
        self.no_change_cmd(I_cmd)

    def rm(self, I_cmd):
        '''rm 删除'''
        self.no_change_cmd(I_cmd)

    def cd(self, I_cmd):
        os.chdir(user_data_base_dir + I_cmd['re_dir'])
        current_abs_path = os.popen('pwd').read()     # 当前绝对目录
        # print('current_abs_path: ', current_abs_path)
        cmd_dict = {
            'func': I_cmd['func'],
            'res_len': 0,
            'path': I_cmd['re_dir'],
            'run_successfully': True
        }
        # 只有cd命令，不带参数； 或者是返回家目录的参数
        if len(I_cmd['func'].split(' ')) == 1 or I_cmd['func'].split(' ')[1] == '~':
            cmd_dict['run_successfully'] = True
            cmd_dict['path'] = self.loads_from_json(
                self.user_data)['user_name']  # 直接回到用户根目录

        elif I_cmd['func'].split(' ')[1] == '/':        # 试图访问根目录
            cmd_dict['run_successfully'] = 'extent of authority'
            cmd_dict['path'] = self.loads_from_json(
                self.user_data)['user_name']  # 直接回到用户根目录

        else:
            try:
                os.chdir(I_cmd['func'].split(' ')[1])
                after_change_abs_path = os.popen('pwd').read().strip()
                list1 = re.split(user_data_base_dir, after_change_abs_path)
                if len(list1) == 1:  # 试图访问其他向上无权限的文件夹
                    cmd_dict['run_successfully'] = 'Dir False'
                    cmd_dict['path'] = self.loads_from_json(
                        self.user_data)['user_name']  # 直接回到用户家目录
                elif len(list1) == 2:   # 有访问权限
                    cmd_dict['run_successfully'] = True
                    cmd_dict['path'] = list1[1].strip('/')
                # print('after_change_abs_path: ', after_change_abs_path)
            except FileNotFoundError as e:      # 输入的目录不正确
                print('Error')
                cmd_dict['run_successfully'] = False
        self.request.send(self.get_json(cmd_dict).encode('utf-8'))
        print(cmd_dict)
        comfirm_info = self.request.recv(1024).decode()
        if comfirm_info == 'Ready to recv':
            print('\033[32;1m%s done...\033[0m' % I_cmd['func'])

    def no_change_cmd(self, I_cmd):
        os.chdir(user_data_base_dir + I_cmd['re_dir'])
        res = os.popen(I_cmd['func']).read()
        res_bytes = bytes(res, 'utf-8')
        cmd_dict = {
            'func': I_cmd['func'],
            'res_len': len(res_bytes),  # 结果的长度
            'path': I_cmd['re_dir'],
            'run_successfully': True
        }
        self.request.send(self.get_json(cmd_dict).encode('utf-8'))
        comfirm_info = self.request.recv(1024).decode()
        if comfirm_info == 'Ready to recv':
            self.request.send(res_bytes)
            print('\033[32;1m%s done...\033[0m' % I_cmd['func'])

    def push(self, I_cmd):
        ''' 服务器接收文件
        :param I_cmd:
        :return:
        '''
        user_name = self.loads_from_json(self.user_data)['user_name']
        os.chdir(user_data_base_dir + user_name)  # 切换到自己的目录
        # 执行du -sb命令，返回两个值，第一个值为当前目录的使用空间大小 ，第二个值为当前相对目录，str类型
        user_size_res = os.popen('du -sb').read()
        user_use_size = int(user_size_res.strip()[0])         # 自己目录的大小
        with open(user_info_dir + user_name + '.json', 'r', encoding='utf-8') as f:    # 读取用户数据
            user_db = json.loads(f.read())
        tol_user_size = user_db['disk_size']
        free_disk_size = tol_user_size - user_use_size      # 剩余磁盘大小
        if free_disk_size < I_cmd['file_size']:     # 磁盘空间不足
            info_dict = {
                'info': 'No free disk space',
                'recv_file_md5': None,
                'cursor_pos': 0,
                'recved_bytes': 0  # 已经下载的文件大小
            }
            # self.request.send(b'No free disk space')
        else:
            os.chdir(user_data_base_dir + I_cmd['re_dir'])
            # 没有完成时的信息文件
            downloading_info_filename = I_cmd['file_name'] + \
                '.downloading_info'
            downloading_filename = I_cmd['file_name'] + \
                '.downloading'      # 没有完成时的文件

            # 如果源下载源文件和信息文件同时存在时，说明上次没有接收完成， 可以进行断点传送
            if os.path.isfile(downloading_info_filename) and os.path.isfile(downloading_filename):
                with open(downloading_info_filename, 'r', encoding='utf-8') as f:
                    downloading_info_file_dict = json.load(f)
                    info_dict = {
                        'info': 'Ready to recv rest file',
                        'recv_file_md5': downloading_info_file_dict['recv_file_md5'],
                        # 光标位置
                        'cursor_pos': downloading_info_file_dict['cursor_pos'],
                        # 已经下载的文件大小
                        'recved_bytes': downloading_info_file_dict['recved_file_size']
                    }
                # self.request.send(self.get_json(info_dict).encode('utf-8'))
            else:                       # 重新接收，如果有同名文件，将被覆盖
                info_dict = {
                    'info': 'Ready to recv full file',
                    'recv_file_md5': None,
                    'cursor_pos': 0,
                    'recved_bytes': 0  # 已经下载的文件大小
                }
                # self.request.send(b'Ready to recv full file')
        self.request.send(self.get_json(info_dict).encode('utf-8'))
    # 开始接收文件，md5验证文件的有效性
        self.recv_file(I_cmd, info_dict['recved_bytes'])

    def pull(self, I_cmd):
        ''' 服务器发送文件
        :param I_cmd:
        :return:
        '''
        user_name = self.loads_from_json(self.user_data)['user_name']
        os.chdir(user_data_base_dir + user_name)  # 切换到自己的目录

        file_name = I_cmd['func'].split(' ')[1]  # 文件名
        if os.path.isfile(file_name):  # 存在该文件
            file_size = os.stat(file_name).st_size
            cmd_dict = {
                'func': I_cmd['func'],
                'path': I_cmd['re_dir'],
                'file_size': file_size,
                'info': 'File not exist'
            }
            self.request.send(self.get_json(cmd_dict).encode('utf-8'))
            cmd_dict = self.request.recv(1024).decode()
            self.send_file(I_cmd, cmd_dict)
        else:
            cmd_dict = {
                'func': I_cmd['func'],
                'path': I_cmd['re_dir'],
                'info': 'File not exist'
            }
            self.request.send(self.get_json(cmd_dict).encode('utf-8'))

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

    def loads_from_json(self, dict):
        return json.loads(dict)

    def recv_file(self, I_cmd, recved_bytes=0):
        if recved_bytes == 0:       # 新下载文件
            recv_file_md5 = hashlib.md5()
            recv_size = 0
        else:           # 断点续传文件
            with open(I_cmd['file_name'] + '.downloading_info', 'r') as f:
                downloading_info_dict = json.load(f)
                recv_file_md5 = hashlib.md5()       # 这里只对剩下的进行md5计算，后续再更改
                # recv_file_md5 = downloading_info_dict['recv_file_md5']
                recv_size = downloading_info_dict['recved_file_size']
        f = open(I_cmd['file_name'] + '.downloading', 'ab+')     # 追加模式打开
        recv_info_file = open(I_cmd['file_name'] + '.downloading_info', 'w')
        while recv_size < I_cmd['file_size']:   # 没有完全传完
            if I_cmd['file_size'] - recv_size > 1024:
                size = 1024
            else:
                size = I_cmd['file_size'] - recv_size
            recv_file = self.request.recv(size)
            f.write(recv_file)
            recv_file_md5.update(recv_file)
            recv_size += len(recv_file)
            recv_file_dict = {
                'file_name': I_cmd['file_name'],
                'recved_file_size': recv_size,
                'recv_time': time.time(),
                'cursor_pos': f.tell(),
                'recv_file_md5': recv_file_md5.hexdigest()
            }
            recv_info_file.seek(0)
            recv_info_file.truncate(0)  # 截断操作，不管光标的当前位置，从文件开始位置数0个字符后去掉后面的字符
            json.dump(recv_file_dict, recv_info_file, indent=4)
            # recv_info_file.seek(0)
        else:
            recv_info_file.close()
            f.close()
            send_from_client_md5 = self.request.recv(1024).decode()
            if recv_file_md5.hexdigest() == send_from_client_md5:   # 通过md5检测文件的完整性
                os.popen('rm %s' % (I_cmd['file_name'] + '.downloading_info'))
                os.popen('mv %s %s' % (
                    I_cmd['file_name'] + '.downloading', I_cmd['file_name']))
                self.request.send(b'File recved completely')
            else:
                self.request.send(b'File recved uncompletely')

    def send_file(self, I_cmd, cmd_dict):
        pass


def run():
    print("server is running...")
    server = socketserver.ThreadingTCPServer(
        (settings.HOST, settings.PORT), MyTCPHandlers)
    server.serve_forever()
    server.server_close()
