#!/usr/bin/env python
# Funtion:      
# Filename:

import socket, json, sys, os
import hashlib
from conf import settings

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
            user_re_dir = "%s"%(self.user_db['user_name'])   # 保存的是相对用户目录
            while True:
                cmd  = input(user_re_dir+':/$ ').strip()
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
            if  recv_user_data['user_name'] == '' or recv_user_data['passwd_md5'] == '':
                print('invalid username or password,try again!')
                input_count += 1
            elif recv_user_data['locked'] == 1:   # 用户已经被锁住了
                exit('user [%s] has been locked' % recv_user_data['user_name'])
            elif recv_user_data['is_authenticated'] == 1: # 1表示已经在其他设备登陆中
                exit('user [%s] has logined in other device' %recv_user_data['user_name'])
            elif recv_user_data['is_authenticated'] == 0:   # 0表示正常登陆
                print('[%s] login successful...'%recv_user_data['user_name'])
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

    def rm(self, cmd_dict):
        '''rm '''
        return self.no_change_cmd(cmd_dict)

    def cd(self, cmd_dict):
        self.client.send(self.get_json(cmd_dict).encode('utf-8'))  # 发送dict的json格式数据到服务器
        res = self.client.recv(1024).decode()
        res_dict = json.loads(res)
        if res_dict['run_successfully'] == True:
            self.client.send(b'Ready to recv')
            return res_dict['path']
        elif res_dict['run_successfully'] =='Dir False':
            self.client.send(b'Ready to recv')
            print('超出权限，返回家目录。。。')
            return res_dict['path']
        elif res_dict['run_successfully'] =='extent of authority':
            self.client.send(b'Ready to recv')
            print('超出权限，返回家目录。。。')
            return res_dict['path']
        else :
            self.client.send(b'Error')
            print('错误的目录')
            return cmd_dict['re_dir']

    def no_change_cmd(self, cmd_dict):
        self.client.send(self.get_json(cmd_dict).encode('utf-8'))  # 发送dict的json格式数据到服务器
        res = self.client.recv(1024).decode()
        res_dict = json.loads(res)
        if res_dict['run_successfully'] == True:
            self.client.send(b'Ready to recv')
            res = self.recv_bytes(res_dict['res_len'])
            if cmd_dict['func'].startswith('pwd'):
                print('/home/'+res)
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
            return cmd_dict['re_dir']      # 直接返回相对家目录的路径
        else:
            file_name = cmd_dict['func'].split(' ')[1]   # 文件名
            if os.path.isfile(file_name):            # 存在该文件
                file_size = os.stat(file_name).st_size
                cmd_dict['file_name'] = file_name
                cmd_dict['file_size'] = file_size   # 将文件大小写入到字典中
                self.client.send(self.get_json(cmd_dict).encode(
                'utf-8'))  # 发送dict的json格式数据到服务器
                comfirm = self.client.recv(1024).decode()   
                if comfirm == 'No free disk space':     # 磁盘空间不足
                    print('\033[31;1mYou have no more free disk space\033[0m')
                    return cmd_dict['re_dir']
                elif comfirm == 'Ready to recv':
                    self.send_file(cmd_dict)
                    res_comfirm = self.client.recv(1024).decode()
                    print('\n' + res_comfirm)
                    return cmd_dict['re_dir']

    def pull(self, I_cmd):
        '''  客户端接收文件
        :param I_cmd:
        :return:
        '''
        pass

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

    def recv_bytes(self, len_bytes, check_md5 = False):
        recv_len = 0
        res = b''
        while recv_len < len_bytes:
            if len_bytes - recv_len >1024:
                recv_size = 1024
            else:
                recv_size = len_bytes - recv_len
            part_res = self.client.recv(recv_size)
            recv_len += len(part_res)
            res += part_res
        else :
            res_str = res.decode()
            return res_str

    def send_file(self, cmd_dict):
        file_md5 = hashlib.md5()
        print('ready to send file')
        with open(cmd_dict['file_name'], 'rb') as f:
            send_size = 0
            tol_size = cmd_dict['file_size']
            for line in f:
                self.client.send(line)
                file_md5.update(line)
                send_size += len(line)
                self.show_progress_bar(cmd_dict['file_name'], send_size/tol_size)
            self.client.send(file_md5.hexdigest().encode('utf-8'))

    def show_progress_bar(self, filename, percent):
        # NUM = 50
        if percent<1:
            sys.stdout.write('sending file %s: [' % filename + int(percent*50)*'#' + '->')
            sys.stdout.write((50-int(percent*50))*' ' + ']'+ str(int(percent)) + '%\r')
        elif percent==1:
            sys.stdout.write('sending file %s: [' %filename + 52*'#' + ']100%')
        sys.stdout.flush()

def run():
    print('client is running ...')
    client = FTP_Client(settings.HOST, settings.PORT)
    client.run()
