#!/usr/bin/env python
# Funtion:
# Filename:

import socket
import json
import sys
import os
import hashlib
from conf import settings

# __all__ = [run, authentication,
#         ls, pwd, ifconfig, tree, date, cal, more,
#         rm, touch, mkdir, cd,
#         push, pull]


class FTP_Client(object):
    def __init__(self, HOST, PORT):
        self.HOST = HOST
        self.PORT = PORT
        self.client = socket.socket()
        # try:
        self.client.connect((HOST, PORT))
        # except ConnectionRefusedError as e:
        #     print('错误代码 4,', settings.MYERRORS[4])

    def run(self):
        self.user_db = self.authentication()
        if isinstance(self.user_db, dict):     # 返回的数据是字典格式
            user_re_dir = "%s" % (self.user_db['user_name'])   # 保存的是相对用户目录
            while True:
                cmd = input(user_re_dir + ':/$ ').strip()
                # print(cmd)
                if len(cmd):
                    if hasattr(self, cmd.split(' ')[0]):
                        func = getattr(self, cmd.split(' ')[0])
                        cmd_dict = {
                            'func': cmd,
                            're_dir': user_re_dir
                        }
                        user_re_dir = func(cmd_dict)
                    else:
                        print('Error command, Try again...')
                # else:
                #     continue
        else:
            self.client.close()

    def authentication(self):
        '''
        用户登陆函数
        :return: 接受到来自客户端的用户数据
        '''
        Max_count = 3
        input_count = 0
        user_data = settings.USER_DATA
        while input_count < Max_count:
            username = input('user name: ').strip()  # 输入用户名
            if len(username) == 0:  # 用户名不能为空
                print('Invalid username, please input username again')
                continue
            user_data['user_name'] = username
            passwd = input('passwd: ').strip()  # 输入密码
            passwd_md5 = self.get_md5(passwd)

            user_data['passwd_md5'] = passwd_md5
            send_data = self.get_json(user_data)  # 将用户数据格化为json格式
            self.client.send(send_data.encode('utf-8'))     # 将用户数据发送给服务器
            recv_user_data = self.client.recv(1024).decode()  # 接收到的用户数据
            recv_user_data = json.loads(recv_user_data)      # 反json序列化

            # 用户名或密码错误，返回的字典会将用户名或密码置为空字符
            if recv_user_data['user_name'] == '' or recv_user_data['passwd_md5'] == '':
                print('invalid username or password,try again!')
                input_count += 1
            elif recv_user_data['locked'] == 1:   # 用户已经被锁住了
                exit('user [%s] has been locked' % recv_user_data['user_name'])
            elif recv_user_data['is_authenticated'] == 1:  # 1表示已经在其他设备登陆中
                exit('user [%s] has logined in other device' %
                     recv_user_data['user_name'])
            elif recv_user_data['is_authenticated'] == 0:   # 0表示正常登陆
                print('[%s] login successful...' % recv_user_data['user_name'])
                return recv_user_data
        else:
            exit('Too many times attempt...')

    def ls(self, cmd_dict):
        return self.no_change_cmd(cmd_dict)

    def pwd(self, cmd_dict):
        return self.no_change_cmd(cmd_dict)

    def ifconfig(self, cmd_dict):
        return self.no_change_cmd(cmd_dict)

    def tree(self, cmd_dict):
        return self.no_change_cmd(cmd_dict)

    def date(self, cmd_dict):
        '''时间'''
        return self.no_change_cmd(cmd_dict)

    def cal(self, cmd_dict):
        '''日历'''
        return self.no_change_cmd(cmd_dict)

    def cat(self, cmd_dict):
        '''cat'''
        return self.no_change_cmd(cmd_dict)

    def more(self, cmd_dict):
        '''more'''
        return self.no_change_cmd(cmd_dict)

    def mkdir(self, cmd_dict):
        ''' 创建目录 '''
        return self.no_change_cmd(cmd_dict)

    def rm(self, cmd_dict):
        '''rm '''
        return self.no_change_cmd(cmd_dict)

    def cd(self, cmd_dict):
        self.client.send(self.get_json(cmd_dict).encode(
            'utf-8'))  # 发送dict的json格式数据到服务器
        res = self.client.recv(1024).decode()
        res_dict = json.loads(res)
        if res_dict['run_successfully'] == True:
            self.client.send(b'Ready to recv')
            return res_dict['path']
        elif res_dict['run_successfully'] == 'Dir False':
            self.client.send(b'Ready to recv')
            print('超出权限，返回家目录。。。')
            return res_dict['path']
        elif res_dict['run_successfully'] == 'extent of authority':
            self.client.send(b'Ready to recv')
            print('超出权限，返回家目录。。。')
            return res_dict['path']
        else:
            self.client.send(b'Error')
            print('错误的目录')
            return cmd_dict['re_dir']

    def no_change_cmd(self, cmd_dict):
        self.client.send(self.get_json(cmd_dict).encode(
            'utf-8'))  # 发送dict的json格式数据到服务器
        res = self.client.recv(1024).decode()
        res_dict = json.loads(res)
        if res_dict['run_successfully'] == True:
            self.client.send(b'Ready to recv')
            res = self.recv_bytes(res_dict['res_len'])
            if cmd_dict['func'].startswith('pwd'):
                print('/home/' + res)
            else:
                print(res)
            return res_dict['path']

    def push(self, cmd_dict):
        '''  客户端发送文件
        :param cmd_dict:
        :return: 
        '''
        func = cmd_dict['func']
        if len(func.strip().strip(' ')) == 1:   # 没有接文件名参数
            print('push command must be followed by a parameter filename')
            # return cmd_dict['re_dir']      # 直接返回相对家目录的路径
        else:
            file_name = cmd_dict['func'].split(' ')[1]   # 文件名
            if os.path.isfile(file_name):            # 存在该文件
                file_size = os.stat(file_name).st_size
                cmd_dict['file_name'] = file_name
                cmd_dict['file_size'] = file_size   # 将文件大小写入到字典中
                self.client.send(self.get_json(cmd_dict).encode(
                    'utf-8'))  # 发送dict的json格式数据到服务器
                comfirm = self.client.recv(1024).decode()
                comfirm_dict = json.loads(comfirm)      # dumps为dict形式
                print('comfirm_dict: ', comfirm_dict)
                if comfirm_dict['info'] == 'No free disk space':     # 磁盘空间不足
                    print('\033[31;1mYou have no more free disk space\033[0m')
                else:
                    if comfirm_dict['info'] == 'Ready to recv rest file':      # 开始接收剩余的文件大小
                        print('\033[31;1m上次下载没有完成，本次下载将进行断点续传。。。\033[0m')
                        # self.send_file(cmd_dict, comfirm_dict['recved_bytes'])
                    elif comfirm_dict['info'] == 'Ready to recv full file':
                        print('\033[32;1m本次下载立即开始。。。\033[0m')
                        # self.send_file(cmd_dict)
                    self.send_file(cmd_dict, comfirm_dict)
                    res_comfirm = self.client.recv(1024).decode()
                    print('\n' + res_comfirm)

            else:
                print('File does not found')
        return cmd_dict['re_dir']       # 直接返回相对家目录的路径

    def pull(self, cmd_dict):
        '''  客户端接收文件
        :param I_cmd:
        :return:
        '''
        func = cmd_dict['func']
        if len(func.strip().strip(' ')) == 1:   # 没有文件名参数
            print('push command must be followed by a parameter filename')
            return cmd_dict['re_dir']      # 直接返回相对家目录的路径
        else:
            file_name = cmd_dict['func'].split(' ')[1]  # 文件名

            # 发送dict的json格式数据到服务器
            self.client.send(self.get_json(cmd_dict).encode('utf-8'))
            comfirm_dict_json = self.client.recv(1024).decode()
            comfirm_dict = json.loads(comfirm_dict_json)
            if comfirm_dict['info'] == 'File not exist':    # 接收到回信文件不存在
                print('\033[31;1mServer does not exist file %s' % file_name)
                return cmd_dict['re_dir']  # 直接返回相对家目录的路径
            else:   # 接收到回信文件存在
                tol_file_size = comfirm_dict['file_size']
                cmd_dict['file_name'] = file_name           # 文件名
                cmd_dict['tol_file_size'] = tol_file_size   # 全部文件大小

                downloading_info_filename = file_name + '.downloading_info'  # 没有完成时的信息文件
                downloading_filename = file_name + '.downloading'  # 没有完成时的文件
                # 如果源下载源文件和信息文件同时存在时，说明上次没有接收完成， 可以进行断点传送
                if os.path.isfile(downloading_filename) and os.path.isfile(downloading_info_filename):
                    try:
                        with open(downloading_info_filename, 'r', encoding='utf-8') as f:
                            downloading_info_file_dict = json.load(f)
                            cmd_dict['recv_file_md5'] = downloading_info_file_dict['recv_file_md5']
                            # 已经下载的文件大小
                            cmd_dict['recved_bytes'] = downloading_info_file_dict['recved_file_size']
                            cmd_dict['cursor_pos'] = downloading_info_file_dict['cursor_pos']
                    except Exception as e:  # 抓住所有错误
                        cmd_dict['recv_file_md5'] = None
                        cmd_dict['recved_bytes'] = 0  # 已经下载的文件大小
                        cmd_dict['cursor_pos'] = 0
                else:   # 不存在断点续传
                    cmd_dict['recv_file_md5'] = None
                    cmd_dict['recved_bytes'] = 0  # 已经下载的文件大小
                    cmd_dict['cursor_pos'] = 0
                self.client.send(self.get_json(cmd_dict).encode('utf-8'))
                print('send info', cmd_dict)
                comfirm_dict_json = self.client.recv(1024).decode()
                comfirm_dict = json.loads(comfirm_dict_json)  # dumps为dict形式
                self.recv_file(comfirm_dict)

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

    def recv_bytes(self, len_bytes, check_md5=False):
        recv_len = 0
        res = b''
        while recv_len < len_bytes:
            if len_bytes - recv_len > 1024:
                recv_size = 1024
            else:
                recv_size = len_bytes - recv_len
            part_res = self.client.recv(recv_size)
            recv_len += len(part_res)
            res += part_res
        else:
            res_str = res.decode()
            return res_str

    def send_file(self, cmd_dict, comfirm_dict):
        # print('cmd_dict', cmd_dict)
        if comfirm_dict['recved_bytes'] == 0:   # 新下载文件
            file_md5 = hashlib.md5()
        else:
            file_md5 = hashlib.md5()    # 只对后面接收的文件进行md5计算
            # file_md5 = comfirm_dict['recv_file_md5']
        print('ready to send file')
        with open(cmd_dict['file_name'], 'rb') as f:
            send_size = comfirm_dict['recved_bytes']    # 已经发送的文件文件大小将从确认信息中获取
            tol_size = cmd_dict['file_size'] - send_size
            f.seek(comfirm_dict['cursor_pos'])      # 将光标移到待续传的位置
            filename = cmd_dict['file_name']
            last_send_percent = 0
            for line in f:
                self.client.send(line)
                file_md5.update(line)
                send_size += len(line)
                # 开始打印进度条
                this_send_percent = int(send_size / tol_size * 100)
                if last_send_percent != this_send_percent:
                    # self.show_progress_bar(cmd_dict['file_name'], send_size/tol_size)
                    percent = send_size / tol_size
                    sys.stdout.write('sending file %s: [' % filename + int(percent * 50) * '#' + '->'
                                     + (50 - int(percent * 50)) * ' ' + ']' + str(this_send_percent) + '%\r')
                    sys.stdout.flush()
                    last_send_percent = this_send_percent
                if this_send_percent == 100:
                    sys.stdout.write('sending file %s: [' % filename + int(percent * 50) * '#' + '##'
                                     + (50 - int(percent * 50)) * ' ' + ']' + str(int(percent) * 100) + '%\n')
                    sys.stdout.flush()

            self.client.send(file_md5.hexdigest().encode('utf-8'))

    def recv_file(self, cmd_dict):
        recv_file_md5 = hashlib.md5()
        recv_size = cmd_dict['recved_bytes']
        tol_file_size = cmd_dict['tol_file_size']
        recv_file_md5 = hashlib.md5()
        f = open(cmd_dict['file_name'] + '.downloading', 'ab+')
        recv_info_f = open(cmd_dict['file_name'] + '.downloading_info', 'w')
        while recv_size < tol_file_size:
            if tol_file_size - recv_size > 1024:
                size = 1024
            else:
                size = cmd_dict['file_size'] - recv_size
            recv_file = self.client.recv(size)
            f.write(recv_file)
            recv_file_md5.update(recv_file)
            recv_size += len(recv_file)
            recv_file_dict = {
                'file_name': cmd_dict['file_name'],
                'recved_file_size': recv_size,
                'recv_time': cmd_dict.time(),
                'cursor_pos': f.tell(),
                'recv_file_md5': recv_file_md5.hexdigest()
            }
            recv_info_f.seek(0)
            recv_info_f.truncate(0)
            json.dump(recv_file_dict, recv_info_f)
        else:
            recv_info_f.close()
            f.close()
            send_from_server_md5 = self.client.recv(1024).decode()
            if recv_file_md5.hexdigest() == send_from_server_md5:
                os.popen('rm %s' %
                         (cmd_dict['file_name'] + '.downloading_info'))
                os.popen('mv %s %s' % (cmd_dict['file_name']
                                       + '.downloading', cmd_dict['file_name']))
                print('\033[32;1mFile recved completely\033[0m')
            else:
                print('\033[31;1mFile recved uncompletely\033[0m')
    # def show_progress_bar(self, filename, percent):
    #     # NUM = 50
    #     sys.stdout.write('sending file %s: [' % filename + int(percent * 50) * '#' + '->'
    #                      + (50 - int(percent * 50)) * ' ' + ']' + str(int(percent)*100) + '%\r')
    #     sys.stdout.flush()
    #     if percent<1:
    #
    #         sys.stdout.write('sending file %s: [' % filename + int(percent * 50) * '#' + '->'
    #                          + (50 - int(percent * 50)) * ' ' + ']' + str(int(percent* 100)) + '%\r')
    #         # sys.stdout.write()
    #
    #         sys.stdout.flush()
    #
    #     elif percent==1:
    #         sys.stdout.write('sending file %s: [' %filename + 52*'#' + ']100%')
    #         # sys.stdout.flush()
    #         sys.stdout.flush()


def run():
    print('client is running ...')
    client = FTP_Client(settings.HOST, settings.PORT)
    client.run()
