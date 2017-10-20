#!/usr/bin/env python
# Funtion:      
# Filename:


import socketserver
import json, hashlib, os
from conf import settings

user_data_base_dir = settings.BASE_DIR+'/db'+'/home/'
user_info_dir = settings.BASE_DIR+'/db'+'/username_passwd/'

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
                if os.path.isfile(user_info_dir+username+'.json'):   # 存在该用户数据
                    with open(user_info_dir+username+'.json', 'r', encoding='utf-8') as f:    # 读取用户数据
                        user_db = json.loads(f.read())
                        if user_db['passwd_md5'] == passwd_md5:     # 密码验证有效
                            if user_db['is_authenticated'] == -1:
                                user_db['is_authenticated'] = 0  # 本次登陆有效
                            elif user_db['is_authenticated'] == 1:
                                user_db['is_authenticated'] = 1
                            self.request.send(self.get_json(user_db).encode('utf-8'))  # 发送该用户的数据
                            with open(user_info_dir + username + '.json', 'w', encoding='utf-8') as f:
                                user_db['is_authenticated'] = -1  # 针对其他设备来说来说，是已经在登陆过的了
                                json.dump(user_db, f, indent=4)
                            return user_db
                        else:       # 密码错误
                            user_db['passwd_md5'] = ''
                            # self.request.send(b'Error passwd')
                            self.request.send(self.get_json(user_db).encode('utf-8'))  # 发送该用户的数据
                            input_count += 1
                else:   # 该用户不存在
                    User_data['user_name'] = ''
                    # self.request.send(b'None')
                    input_count += 1
                    self.request.send(self.get_json(User_data).encode('utf-8'))  # 发送该用户的数据

    def add_user(self, Recv_dict):      # add_dict
        user_name = Recv_dict['user_name']
        Recv_dict.pop('func')
        if os.path.isfile(user_info_dir+user_name+'.json'):
            self.request.send(b'EXIST')
        else:
            with open(user_info_dir+user_name+'.json', 'w', encoding='utf-8') as f:
                json.dump(Recv_dict, f, indent=4)   # 先删除 'func'的键值
            os.chdir(user_data_base_dir)
            print(os.popen('mkdir %s'%user_name).read())   # 在linux中为mkdir, windows中为md
            os.chdir(user_data_base_dir + user_name)    # 切换到用户路径下
            os.popen('touch %s.log' % user_name)
            self.request.send(b'OK')

    def del_user(self, I_cmd):
        pass

    def query_user(self, I_cmd):
        pass

    def alter_uer(self, I_cmd):
        pass

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
        self.no_change_cmd(I_cmd)

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

    def cd(self, I_cmd):
        current_abs_path = user_data_base_dir + I_cmd['re_dir']     # 当前绝对目录


        pass

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

    # def send_bytes(self, src_bytes):
    #     '''发送字节到客户端'''
    #     send_len = 0
    #     len_src_bytes = len(src_bytes)
    #     while send_len < len_src_bytes:
    #         if len_src_bytes - send_len > 1024:
    #             send_size = 1024
    #         else:
    #             send_size = len_src_bytes - send_len
    #         self.request.send(send_size)

def run():
    print("server is running...")
    server = socketserver.ThreadingTCPServer((settings.HOST, settings.PORT), MyTCPHandlers)
    server.serve_forever()
    server.server_close()


