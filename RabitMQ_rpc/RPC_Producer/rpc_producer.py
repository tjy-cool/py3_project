import pika
import uuid
import time
import re


class HostManage_Client(object):
    def __init__(self):
        self.connections = {}

    def on_response(self):
        pass

    def call(self):
        pass

    def run(self, input_cmd):
        
        body = input_cmd.split("run \"")[1].split("\" ")[0]
        hosts = input_cmd.split("--hosts")[1].strip().split(" ")
        for host_ip in hosts:
            if self.judge_legal_ip(host_ip):        # 判断IP地址的合法性
                '''
                self.connections = {
                    host_ip1:{
                        'connection': pika.BlockingConnection(),
                        'channel': Channel1,
                        'callback_queue': result.method.queue
                    },
                    host_ip2:{
                        'connection': pika.BlockingConnection(),
                        'channel': Channel2,
                        'callback_queue': result.method.queue
                    }
                }
                '''
                print("IP [%s] is Legal ip" % host)
                conn_info = {}

                conn_info['connection'] = pika.BlockingConnection(
                    pika.ConnectionParameters(host=host))
                conn_info['channel'] = conn_info['connection'].channel(
                )
                result = self.channel.queue_declare(exclusive=True)
                conn_info['callback_queue'] = result.method.queue
                conn_info['channel'].basic_consume(
                    self.on_response, no_ack=True, queue=conn_info['callback_queue'])
                
                conn_info['response'] = None
                self.connections[host_ip] = conn_info
            else:
                print("IP [%s] is Illegal ip" % host_ip)

    def check(self, input_cmd):
        pass

    def main(self):
        while True:
            input_cmd = input(">> ").strip()

            cmd = input_cmd.split(' ')[0]
            if hasattr(self, cmd):
                func = getattr(self, cmd)
                func(input_cmd)

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


if __name__ == '__main__':
    client = HostManage_Client()
    client.main()
