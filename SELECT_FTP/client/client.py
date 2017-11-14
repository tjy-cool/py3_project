#!/usr/bin/env python
# Funtion:      
# Filename:

import socket
import time
import json
import hashlib
import os
import sys

class Client(object):
    def __init__(self, HOST, PORT):
        self.client = socket.socket()
        self.client.connect((HOST, PORT))

    def run(self):
        while True:
            cmd = input('>> ').strip()
            if len(cmd):
                if hasattr(self, cmd.split(' ')[0]):
                    func = getattr(self, cmd.split(' ')[0])
                    # file_name = cmd.split(' ')[1]
                    # print(cmd.split(' ')[0])
                    cmd_dict = {
                        'func': cmd
                    }
                    func(cmd_dict)
                else:
                    print('Error command, Try again...')

    def push(self, cmd_dict):
        fun = cmd_dict['func']
        if len(fun.strip().split(' ')) == 1:   # 没有接文件名参数
            print('push command must be followed by a parameter filename')
        else:
            file_name = cmd_dict['func'].split(' ')[1]   # 文件名
            if os.path.isfile(file_name):            # 存在该文件
                file_size = os.stat(file_name).st_size
                cmd_dict['func'] = fun.strip().split(' ')[0]
                cmd_dict['file_name'] = file_name
                cmd_dict['file_size'] = file_size   # 将文件大小写入到字典中
                # 发送dict的json格式数据到服务器
                self.client.send(self.get_json(cmd_dict).encode('utf-8'))
                comfirm = self.client.recv(1024).decode()
                comfirm_dict = json.loads(comfirm)      # dumps为dict形式
                # print('comfirm_dict: ', comfirm_dict)

                if comfirm_dict['info'] == 'Ready to recv':
                    print('\033[32;1m 本次上传立即开始。。。\033[0m')
                        # self.send_file(cmd_dict)
                    self.send_file(cmd_dict)
                    # res_comfirm = self.client.recv(1024).decode()
                    # print('\n' + res_comfirm)
            else:
                print('File does not found')

    def pull(self, cmd_dict):   # 接收文件
        fun = cmd_dict['func']
        if len(fun.strip().split(' ')) == 1:  # 没有接文件名参数
            print('push command must be followed by a parameter filename')
        else:
            file_name = cmd_dict['func'].split(' ')[1]  # 文件名
            cmd_dict['func'] = fun.split(' ')[0]
            cmd_dict['file_name'] = file_name
            cmd_dict['recv_file_md5'] = None
            cmd_dict['recved_bytes'] = 0  # 已经下载的文件大小
            cmd_dict['cursor_pos'] = 0

            # 发送dict的json格式数据到服务器
            self.client.send(self.get_json(cmd_dict).encode('utf-8'))
            # print('send ok')
            comfirm_dict_json = self.client.recv(1024).decode()
            comfirm_dict = json.loads(comfirm_dict_json)
            # print(comfirm_dict_json)
            if comfirm_dict['info'] == 'Ready to send':
                # cmd_dict['func'] = func.split(' ')[0]
                # cmd_dict['file_name'] = fun.split(' ')[1]
                # self.client.send(self.get_json(cmd_dict).encode('utf-8'))
                print('\033[32;1m 本次下载立即开始。。。\033[0m')
                cmd_dict['tol_file_size'] = comfirm_dict['file_size']
                # print('ready to recv')
                self.recv_file(cmd_dict)
                # print('recv ok')

    def send_file(self, cmd_dict):
        file_md5 = hashlib.md5()    # 只对后面接收的文件进行md5计算
            # file_md5 = comfirm_dict['recv_file_md5']
        # print('ready to send file')
        with open(cmd_dict['file_name'], 'rb') as f:
            send_size = 0    # 已经发送的文件文件大小将从确认信息中获取
            tol_size = cmd_dict['file_size'] - send_size
            # f.seek(comfirm_dict['cursor_pos'])      # 将光标移到待续传的位置
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

            # self.client.send(file_md5.hexdigest().encode('utf-8'))

    def recv_file(self, cmd_dict):
        recv_file_md5 = hashlib.md5()
        recv_size = cmd_dict['recved_bytes']  # 已经接收的文件大小（byte）
        tol_file_size = cmd_dict['tol_file_size']
        file_name = cmd_dict['file_name']
        last_send_percent = 0

        # f = open(file_name + '.downloading', 'ab+')
        # recv_info_f = open(file_name + '.downloading_info', 'w')
        f = open(file_name, 'wb')
        # print('open OK')
        while recv_size < tol_file_size:
            if tol_file_size - recv_size > 1024:
                size = 1024
            else:
                size = tol_file_size - recv_size
            # print(size)
            recv_file = self.client.recv(size)
            # print('recv_file', recv_file)
            f.write(recv_file)
            recv_file_md5.update(recv_file)
            recv_size += len(recv_file)
            # recv_file_dict = {
            #     'file_name': cmd_dict['file_name'],
            #     'recved_file_size': recv_size,
            #     'cursor_pos': f.tell(),
            #     'recv_file_md5': recv_file_md5.hexdigest()
            # }
            # recv_info_f.seek(0)
            # recv_info_f.truncate(0)
            # json.dump(recv_file_dict, recv_info_f, indent=4)

            # 开始打印进度条
            this_send_percent = int(recv_size / tol_file_size * 100)
            if last_send_percent != this_send_percent:
                # self.show_progress_bar(cmd_dict['file_name'], send_size/tol_size)
                percent = recv_size / tol_file_size
                sys.stdout.write('recving file %s (%sb): [' % (file_name, recv_size) + int(percent * 50) * '#' + '->'
                                 + (50 - int(percent * 50)) * ' ' + ']' + str(this_send_percent) + '%\r')
                sys.stdout.flush()
                last_send_percent = this_send_percent
            if this_send_percent == 100:
                sys.stdout.write('recving file %s ((%sb)): [' % (file_name, recv_size) + int(percent * 50) * '#' + '##'
                                 + (50 - int(percent * 50)) * ' ' + ']' + str(int(percent) * 100) + '%\n')
                sys.stdout.flush()
        else:
            # recv_info_f.close()
            f.close()
            send_from_server_md5 = self.client.recv(1024).decode()
            # print('recv_md5-----', send_from_server_md5)
            # print('cal_md5', recv_file_md5.hexdigest())
            if recv_file_md5.hexdigest() == send_from_server_md5:
                # os.popen('del %s' %
                #          (cmd_dict['file_name'] + '.downloading_info'))
                # os.popen('rename %s %s' % (cmd_dict['file_name']
                #                            + '.downloading', cmd_dict['file_name']))
                print('\033[32;1mFile recved completely\033[0m')
            else:
                print('\033[31;1mFile recved uncompletely\033[0m')

    def quit(self, cmd_dict):
        self.client.close()
        exit()


    def get_json(self, src):
        # 将数据格式化为json格式
        return json.dumps(src)

    # def pull(self, cmd_dict):
    #     pass

if __name__ == '__main__':
    client = Client('localhost', 9999)
    client.run()