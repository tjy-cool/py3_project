#!/usr/bin/env python
# Funtion:      
# Filename:

import socket, time, json, os

class Client(object):
    def __init__(self, Port, Host):
        self.client = socket.socket()
        self.client.connect((Host, Port))

    def run(self):
        while True:
            cmd = input('>> ').strip()
            if len(cmd):
                if hasattr(self, cmd.split(' ')[0]):
                    func = getattr(self, cmd.split(' ')[0])
                    file_name = cmd.split(' ')[1]
                    cmd_dict = {
                        'func': func,
                    }
                    func(cmd_dict)
                else:
                    print('Error command, Try again...')

    def push(self, cmd_dict):
        func = cmd_dict['func']
        if len(func.strip().strip(' ')) == 1:   # 没有接文件名参数
            print('push command must be followed by a parameter filename')
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
                    # self.send_file(cmd_dict, comfirm_dict)
                    res_comfirm = self.client.recv(1024).decode()
                    print('\n' + res_comfirm)

            else:
                print('File does not found')

    def get_json(self, src):
        # 将数据格式化为json格式
        return json.dumps(src)

    def pull(self, cmd_dict):
        pass