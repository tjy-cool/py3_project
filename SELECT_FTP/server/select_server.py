#!/usr/bin/env python
# Funtion:      
# Filename:

import select, socket, queue, json
import os, hashlib

class Select_server(object):
    def __init__(self, HOST,PORT):
        self.server = socket.socket()
        self.server.bind((HOST, PORT))
        self.server.listen(1000)
        self.server.setblocking(False)      # 设置为非阻塞

        self.inputs = [self.server, ]
        self.outputs = []
        self.conn_info_dict = {}
        self.residue_recv_size = 0  # 剩余需要接收的文件大小，b
        self.residue_send_size = 0  # 剩余需要发送的文件大小，b

        # conn_info_dict= {
        #     conn1: { 'conn': conn,
        #               'q_recv_data':  queue.Queue()
        #                 first_recv = 0 代表首次接收，即接受命令，
        #                 否则 first_recv=1 接受上传的数据， first_recv = 2 代表发送数据
        #              'first_recv': 0,
        #              'recv_or_send': recv,
        #              'residue_send_size': 0,
        #              'residue_recv_size': 0,
        #              'recv_cmd': None,
        #              'send_cmd': Info_cmd,
        #              'file_obj': send_file_obj 或 recv_file_obj
        # }

    def run(self):
        print('server is running...')
        while True:
            readable, writeable, exceptional = select.select(self.inputs, self.outputs, self.inputs)
            for r in readable:
                if r is self.server:    #每个r就是一个socket
                    conn, client_addr = r.accept()
                    conn.setblocking(False)
                    print('来了个新链接: ', client_addr)
                    self.inputs.append(conn)

                    self.conn_info_dict[conn] = { }
                    # self.conn_info_dict[conn]['conn'] = conn
                    self.conn_info_dict[conn]['q_recv_data'] = queue.Queue()       # conn_info_dict[0]
                    self.conn_info_dict[conn]['first_recv'] = 0         # 0 代表首次接收，即接受命令, 1 表示接收数据， 2 表示发送数据

                else:    # r不是server的话,那就只能是一个与客户端建立的连接的fd了
                    if self.conn_info_dict[r]['first_recv'] == 0:
                        # print('ready to recv')
                        try:
                            cmd_dict_json = r.recv(1024).decode()
                        except ConnectionResetError as e:
                            print(e)
                            if r in self.outputs:  # 既然客户端都断开了，我就不用再给它返回数据了，
                                # 所以这时候如果这个客户端的连接对象还在outputs列表中，就把它删掉
                                self.outputs.remove(r)
                            self.inputs.remove(r)  # inputs中也删除掉
                            r.close()  # 把这个连接关闭掉
                            del self.conn_info_dict[r]
                            break

                        # print('cmd_dict_json', cmd_dict_json)
                        if len(cmd_dict_json) == 0:
                            if r in self.outputs:  # 既然客户端都断开了，我就不用再给它返回数据了，
                                # 所以这时候如果这个客户端的连接对象还在outputs列表中，就把它删掉
                                self.outputs.remove(r)
                            self.inputs.remove(r)  # inputs中也删除掉
                            r.close()  # 把这个连接关闭掉
                            del self.conn_info_dict[r]

                        else:
                            try:
                                # print('cmd_dict_json', cmd_dict_json)
                                cmd_dict = json.loads(cmd_dict_json)
                            finally:
                                pass

                                self.conn_info_dict[r]['recv_cmd'] = cmd_dict  # 将命令接收进去，为conn_info_dict[2]

                                if cmd_dict['func'] == 'push':      # 接收文件命令
                                    info_dict = {
                                        'info': 'Ready to recv'
                                    }
                                    if self.conn_info_dict[r]['recv_cmd']['file_size'] != 0:
                                        self.conn_info_dict[r]['first_recv'] = 1  # 1 表示接下来要接收数据
                                        self.conn_info_dict[r]['residue_recv_size'] = cmd_dict['file_size']

                                    r.send(json.dumps(info_dict).encode('utf-8'))  # 开始接收文件

                                if cmd_dict['func'] == 'pull':      # 发送文件命令
                                    file_name = cmd_dict['file_name']
                                    if os.path.isfile(file_name):
                                        file_size = os.stat(file_name).st_size
                                        info_dict = {
                                            'info': 'Ready to send',
                                            'file_name': file_name,
                                            # 'tol_file_size': file_size,
                                            'file_size': file_size     # 待发送的文件大小
                                        }
                                        self.conn_info_dict[r]['send_cmd'] = info_dict
                                        self.conn_info_dict[r]['first_recv'] = 2
                                        self.conn_info_dict[r]['residue_send_size'] = \
                                            os.stat(self.conn_info_dict[r]['send_cmd']['file_name']).st_size
                                        self.outputs.append(r)
                                    else:
                                        info_dict = {
                                            'info': 'File dose not Exist'
                                        }

                                    r.send(json.dumps(info_dict).encode('utf-8'))  # 开始发送文件
                                    # print(' seond ok', info_dict)
                                    # print('conn_info_dict', self.conn_info_dict)


                    elif self.conn_info_dict[r]['first_recv'] == 1:      # 1 表示接收数据
                        data = r.recv(1024)
                        # print('data', data.decode())
                        # self.conn_info_dict[r]['q_recv_data'].put(data)
                        if self.conn_info_dict[r]['residue_recv_size'] == self.conn_info_dict[r]['recv_cmd']['file_size']:
                            file_name = self.conn_info_dict[r]['recv_cmd']['file_name']
                            self.conn_info_dict[r]['file_obj'] = open(file_name, 'wb')
                            self.conn_info_dict[r]['recv_file_md5'] = hashlib.md5()

                        self.conn_info_dict[r]['file_obj'].write(data)
                        self.conn_info_dict[r]['residue_recv_size'] -= len(data)
                        self.conn_info_dict[r]['recv_file_md5'].update(data)
                        if self.conn_info_dict[r]['residue_recv_size'] == 0:
                            # recved_md5 = r.recv(1024)

                            self.conn_info_dict[r]['first_recv'] = 0
                            self.conn_info_dict[r]['file_obj'].close()

                    # elif self.conn_info_dict[r]['first_recv'] == 2:      # 2 表示发送数据
                    #     print('in 2')
                    #     self.conn_info_dict[r]['residue_send_size'] = \
                    #         os.stat(self.conn_info_dict[r]['send_cmd']['file_name']).st_size
                    #     self.outputs.append(r)

            for w in writeable:     # 发送文件
                # print('In w')
                if self.conn_info_dict[w]['residue_send_size'] == self.conn_info_dict[w]['send_cmd']['file_size']:
                    self.conn_info_dict[w]['send_file_md5'] = hashlib.md5()
                    self.conn_info_dict[w]['file_obj'] = open(self.conn_info_dict[w]['send_cmd']['file_name'], 'rb')
                line = self.conn_info_dict[w]['file_obj'].readline()
                # print('w',self.conn_info_dict[w], 'line', line)
                w.send(line)
                self.conn_info_dict[w]['residue_send_size'] -= len(line)
                self.conn_info_dict[w]['send_file_md5'].update(line)
                if self.conn_info_dict[w]['residue_send_size'] == 0:    # 发送完了文件
                    md5_hex = self.conn_info_dict[w]['send_file_md5'].hexdigest()
                    # print('-----', md5_hex)
                    w.send(md5_hex.encode('utf-8'))

                    self.conn_info_dict[w]['first_recv'] = 0
                    self.outputs.remove(w)

            for e in exceptional:       # 断开了连接
                if e in self.outputs:
                    self.outputs.remove(e)
                self.inputs.remove(e)
                del self.conn_info_dict[e]
                e.close()


    # def push(self):
    #     pass
    #
    # def pull(self, Recv_dict):
    #     pass

if __name__ == '__main__':
    sel_server = Select_server('localhost', 9999)
    sel_server.run()