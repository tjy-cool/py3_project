#!/usr/bin/env python
# Funtion:      
# Filename:

# 开发简单的FTP：
# 1. 用户登陆
# 2. 上传/下载文件
# 3. 不同用户家目录不同
# 4. 查看当前目录下文件
# 5. 充分使用面向对象知识

import socket, sys

user_data = {
    'user_name': None,
    'is_authenticated':False,
    'base_path': None
}

def login(func):
    def wripper(*args, **kwargs):
        if args[1]["is_authenticated"] == False:
            print('\033[31;0mNo user authenticated. Please authenticated\033[0m')
        else :
            func(*args, **kwargs)
    return wripper
# 显示信息
msg1 = '''\033[1;31m===============================\033[0m
\033[1;32m       用户登陆（login)
 上传(upload)/下载(download)文件
     查看当前目录下文件(ls)\033[0m
\033[1;31m==============================\033[0m'''
msg2 = '''\033[1;31m===============================\033[0m
\033[1;32m 上传(upload)/下载(download)文件
    查看当前目录下文件(ls)\033[0m
\033[1;31m==============================\033[0m'''

class Ftp_client(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        client = socket.socket()
        client.connect((self.ip, self.port))
        self.client = client

    def run_client(self):
        platform = sys.platform
        self.client.send(platform.encode())  # 先发送客户平台
        while True:
            if user_data['is_authenticated'] == False:
                print(msg1)
            else:
                print(msg2)
            send_command = input("请输入您的动作：")
            if len(send_command) == 0:
                continue

            if send_command == 'login':
                self.in_login()
            elif send_command == "download": # 下载文件
                self.download(user_data)
            elif send_command == "upload":   # 上传文件
                self.upload(user_data)
            elif send_command == "ls":       # 显示文件目录
                self.ls(user_data)
        self.client.close()

    def in_login(self):
        if user_data['is_authenticated'] == False:
            self.client.send('login'.encode())  # 发送命令
            user = input("username: ")
            self.client.send(user.encode())  # 发送用户名
            passwd = input("passwd: ")
            self.client.send(passwd.encode())  # 发送密码
            recv_user = self.client.recv(1024)
            if recv_user.decode() == user:  # 返回了正确的用户名
                user_data["user_name"] = user
                user_data["is_authenticated"] = True
                print("welcome! login successful!")
            else:
                print("user or passwd invalid!")
        else:
            print("%s had been authenticated." % user_data['user_name'])


    @login
    def download(self, user_acc):
        self.client.send('download'.encode())  # 发送命令
        file_name = input("Please Input filename what you want download: ")
        self.client.send(file_name.encode())    # 发送需要下载的文件
        ff = self.client.recv(1024000)
        if ff.decode() == "None":
            print("\033[31;1mInput Error Filename！\033[0m")
        else:
            with open(file_name, 'w', encoding="utf-8") as f:
                f.write(ff.decode())
                print("download file <%s> successful!" % file_name)

    @login
    def upload(self, user_acc):
        self.client.send('upload'.encode())
        file_name = input("Please Input filename what you want upload: ")
        self.client.send(file_name.encode())
        with open(file_name, 'r', encoding='utf-8') as f:
            self.client.send(f.read().encode())
        if self.client.recv(1024).decode() == 'OK':
            print("Send file <%s> successful!" % file_name)
        else:
            print("Send file faild!")
    @login
    def ls(self, user_acc):
        self.client.send('ls'.encode())  # 发送命令
        data = self.client.recv(1024)
        print(data.decode())

client = Ftp_client("localhost", 6969)
client.run_client()


