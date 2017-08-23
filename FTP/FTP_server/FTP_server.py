#!/usr/bin/env python
# Funtion:      
# Filename:

# 开发简单的FTP：
# 1. 用户登陆   #可以完成
# 2. 上传/下载文件
# 3. 不同用户家目录不同
# 4. 查看当前目录下文件
# 5. 充分使用面向对象知识

import socket,os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))    # 即为FTP的绝对路径
# BASE_DIR = BASE_DIR+'/db/'
# print(BASE_DIR)
class Ftp_server(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def run_server(self):
        server = socket.socket()
        server.bind((self.ip, self.port))
        server.listen(5)
        while True:
            conn, addr = server.accept()
            self.recv_platform = conn.recv(1024).decode()   # 先接受客户端的平台信息
            while True:
                recv_data = conn.recv(1024)
                if not recv_data:
                    break
                command = recv_data.decode()
                print("recv command: ",command)

                if command == "login":  # 登陆
                    self.in_login(conn)    # 登陆
                elif command == "download": # 下载文件
                    self.download(conn)
                elif command == "upload":   # 上传文件
                    self.upload(conn)
                elif command == "ls":       # 显示文件目录
                    self.ls(conn)
                # else:
                #     conn.send("ERROR!".encode())
        server.close()


    def read_User_Passwd(self, input_user, input_passwd):
        with open("username_passwd.txt", 'r+', encoding="utf-8") as f:
            for line in f:
                username = line.split(",")[0].strip()
                passwd = line.split(",")[1].strip()
                if input_user == username and input_passwd == passwd:
                    if not os.path.isdir(BASE_DIR+os.sep+username):     # 判断该用户的家目录是否存在
                        os.mkdir(BASE_DIR+os.sep+username)
                    os.chdir(username)  # 切换目录到用户目录下
                    self.username = username
                    return username     # 如果用户名和密码正确返回用户名，如果不正确返回None
        return None

    def in_login(self, conn):
        username = conn.recv(1024)
        passwd = conn.recv(1024)
        login_user = self.read_User_Passwd(username.decode(), passwd.decode())
        if login_user != None:
            conn.send(login_user.encode())
            print(login_user)
        else:
            print("No user")
            conn.send("None".encode())

    def download(self, conn):
        file_name = conn.recv(1024).decode()
        allfile = os.listdir('.')
        if file_name in allfile:
            print("begin send file")
            with open(file_name, 'r', encoding='utf-8') as f:
                ff = f.read()
                conn.send(ff.encode())
            print("send file successful!")
        else:
            conn.send("None".encode())


    def upload(self, conn):
        file_name = conn.recv(1024).decode()
        print("file_name", file_name)
        ff = conn.recv(1024000).decode()
        print(ff)
        with open(file_name, 'w', encoding="utf-8") as f:
            f.write(ff)
        conn.send("OK".encode())

    def ls(self, conn):
        print(os.path)
        if self.recv_platform == "win32":
            data = os.popen('dir').read()       #  BASE_DIR+os.sep+self.username
        elif self.recv_platform == "linux":
            data = os.popen('ls' ).read()
        print("当前目录: \n", data)
        conn.send(data.encode())

ftp_server = Ftp_server("localhost", 6969)
ftp_server.run_server()
