#!/usr/bin/env python
# Funtion:
# Filename:

import paramiko
import threading
import os
import sys
import json
import time
import re
from conf import settings


class MyParamiko(object):
    def __init__(self, host, port, username, passwd):
        self.host = host
        self.port = port
        self.username = username
        self.passwd = passwd

    def ssh_client_connect(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.ssh.connect(hostname=self.host,
                         port=self.port,
                         username=self.username,
                         password=self.passwd)

    def ssh_cmd(self):
        ''' 执行一次ssh '''
        while True:
            cmd = input('>> ').strip()
            if cmd == 'q':  # q 退出ssh
                break
            elif cmd_str == 'exit':
                exit()
            else:
                stdin, stdout, stderr = self.ssh.exec_command(cmd)
                res, err = stdout.read(), stderr.read()
                result = res if res else err
                print(result.decode())

    def sftp_client_connect(self):
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.username, password=self.passwd)

        self.sftp = paramiko.SFTPClient.from_transport(transport)

    def push(self, cmd_str):
        ''' 上传文件, sftp.put '''
        try:
            source_file = cmd_str.split(' ')[1]
            obj_file = cmd_str.split(' ')[2]
            self.sftp.put(source_file, obj_file)
        except Exception as e:
            print('命令错误', e)

    def pull(self, cmd_str):
        ''' 下载文件,sftp.get '''
        try:
            source_file = cmd_str.split(' ')[1]
            obj_file = cmd_str.split(' ')[2]
            self.sftp.get(source_file, obj_file)
        except Exception as e:
            print('命令错误', e)

    def sftp_cmd(self):
        ''' put src_file remote_file'''
        while True:
            cmd_str = input('>> ').strip()
            if cmd_str == 'q':  # q 退出sftp
                break
            elif cmd_str == 'exit':
                exit()
            cmd = cmd_str.split(' ')[0]
            if hasattr(self, cmd):
                func = getattr(self, cmd)
                func(cmd_str)
            else:
                print('输入格式错误！')

    def run(self):
        while True:
            cmd_str = input('请输入目标用途(ssh/sftp): ').strip()
            if cmd_str == 'ssh':
                try:
                    self.ssh_client_connect()
                except paramiko.ssh_exception.AuthenticationException as e:
                    print('Authentication failed')
                    return 'Authentication failed'
                    break
                except Exception as e:
                    print(e)
                    return 'host or port error'
                    break

                self.ssh_cmd()
            elif cmd_str == 'sftp':
                try:
                    self.sftp_client_connect()
                except paramiko.ssh_exception.AuthenticationException as e:
                    print('Authentication failed')
                    return 'Authentication failed'
                    break
                except Exception as e:
                    print(e)
                    return 'host or port error'
                    break
                self.sftp_cmd()
            elif cmd_str == 'q':
                return None
                break
            elif cmd_str =='exit':
                exit()
            else:
                print("输入错误，只能输入(ssh/sftp/q)")


class Fabric(object):

    def add_host(self):
        '''
        [{'host':'192.168.1.1', 'port':8888}]
        '''
        while True:
            host = input('请输入远程主机ip地址：').strip()
            port = input('请输入端口号：').strip()
            if self.judge_legal_ip(host) and port.isnumeric():  # 用户名和端口格式正确
                new_host_dict = {
                    'host': host,
                    'port': int(port)
                }
                host_list = self.load_host()
                res = self.update_host(
                    host_list, new_host_dict, 'add')   # 增加主机并写入到文件中
                if res == 0:
                    print('\033[32;1madd [%s] successful!\033[0m' % host)
                else:
                    print('\033[31;1maadd [%s] failed!\033[0m' % host)
            elif host == '' and port == '':     # 当全部输入为空时，退出增加主机模式
                break
            else:
                print('主机ip或端口号格式错误，请重新输入!')

    def del_host(self):
        host = input('请输入需要删除的主机IP: ')
        host_list = self.load_host()
        res = self.update_host(host_list, host, 'del')  # 删除主机
        if res == 0:    # 删除成功
            print('\033[32;1mdel [%s] successful!\033[0m' % host)
        elif res == -1:  # 文件中没有保存该主机
            print('host [%s] is not saved yet' % port)
        elif res == -2:  # 未知错误
            print('unknow error')

    def list_allHost(self):
        # with open()
        host_list = self.load_host()
        self.show_host(host_list)

    def remote_Host(self):
        self.remote_flag = 1
        while True:
            host_list = self.load_host()
            self.show_host(host_list)
            host_num = input('请输入主机编号：').strip()
            if host_num == 'q':
                self.remote_flag = 0
                break
            else:
                try:
                    host = host_list[int(host_num)]['host']
                    port = host_list[int(host_num)]['port']
                except ValueError as e:
                    print('输入的主机编号不合法，请重新输入......')
                    continue
                except IndexError as e:
                    print('输入的主机编号不存在')
                    continue
                while True:
                    username = input('请输入主机用户名：').strip()
                    passwd = input('请输入主机用户密码：').strip()
                    para = MyParamiko(host, port, username, passwd)
                    res = para.run()
                    if res == 'Authentication failed':
                        continue
                    elif res == 'host or port error':
                        print('host or port error')
                        break
                    else:
                        break

    def Exit(self):
        exit()

    def load_host(self):
        '''
        读取存放主机的文件返回 主机列表，
        列表里存放了字典，每个字典都存放了一台主机的ip地址和端口号
        '''
        with open(settings.host_json_file_path, 'r', encoding='utf-8') as f:
            host_list = json.load(f)
            return host_list

    def update_host(self, host_list, input_host=None, action=None):
        '''
        对主机列表将输入新的host进行增删，然后写入到文件中，
        input_host为字典，格式为：
        input_host = {
                    'host': host,
                    'port': int(port)
                }
        action 为 'add'， 或者是 'del'
        return 0:   正常
        return -1:  未找到待删除的IP 
        return -2:  其他错误
        '''
        if input_host == None and action == None:   # 直接写入hostlist列表
            with open(settings.host_json_file_path, 'w', encoding='utf-8') as f:
                host_list = json.dump(host_list, f, indent=4)
            return 0
        elif type(input_host) == dict and action == 'add':    # 增加主机
            host_list.append(input_host)
            with open(settings.host_json_file_path, 'w', encoding='utf-8') as f:
                host_list = json.dump(host_list, f, indent=4)
            return 0
        # num = 0
        elif type(input_host) == str and action == 'del':
            for index, host in enumerate(host_list):
                while host['host'] == input_host:
                    num = index
                    del host_list[index]
                    with open(settings.host_json_file_path, 'w', encoding='utf-8') as f:
                        host_list = json.dump(host_list, f, indent=4)
                    return 0
            else:
                return -1
        else:
            return -2

    def show_host(self, host_list):
        for index, host_port in enumerate(host_list):
            print("%s. %s" % (index, host_port))

    def judge_legal_ip(self, one_str):
        '''
        正则匹配方法判断一个字符串是否是合法IP地址 
        '''
        compile_ip = re.compile(
            '^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
        if compile_ip.match(one_str):
            return True
        else:
            return False

    def interaction(self):
        help_msg = '''
    欢迎来到Fabric主机管理界面
    1. 创建主机
    2. 删除主机
    3. 列出所有主机
    4. 开始远程操控
    5. 退出程序
        '''
        func_dict = {
            '1': self.add_host,
            '2': self.del_host,
            '3': self.list_allHost,
            '4': self.remote_Host,
            '5': self.Exit
        }
        self.remote_flag = 0
        while True:
            if self.remote_flag == 0:
                print(help_msg)
            choose = input('请输入你的选择(num)：').strip()
            if choose in func_dict:
                func_dict[choose]()
            else:
                print('\033[31;1m输入错误，请检查后重新输入！\033[0m')


def run():

    fab = Fabric()
    # fab.interaction()
    th = threading.Thread(target=fab.interaction)
    th.start()
    # paramiko.ssh_exception.NoValidConnectionsError:
    # TimeoutError:
    # paramiko.ssh_exception.AuthenticationException:
    # para = MyParamiko('192.168.6.128', 22, 'root', 'lemker')
    # para.run()

    # new_host = {
    #     'host': '192.168.1.12',
    #     'port': 8888
    # }
    # host_name = '192.168.1.12'

    # host_list = fab.load_host()
    # print(fab.update_host(host_list, host_name, 'del'))
    # print(fab.judge_legal_ip('1.1.1.1'))


if __name__ == '__main__':
    fab = Fabric()
    # print(fab)
    fab.interaction()
    # print(fab.judge_legal_ip('1.1.1.1'))
