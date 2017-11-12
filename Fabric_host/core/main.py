#!/usr/bin/env python
# Funtion:
# Filename:

import paramiko
import threading
import os
import sys
import pickle
import time
from conf import settings


def mian():
    help_msg = '''
        欢迎来到Fabric主机管理界面
        1. 创建主机
        2. 删除主机
        3. 自动激活所有主机
        4. 开始远程操控
        5. 退出程序
    '''
    func_dict = {
        '1': new_host,
        '2': del_host,
        '3': auto_activeHost,
        '4': remote_Host,
        '5': Exit
    }

    while True:
        print(help_msg)
        choose = input('请输入你的选择(num)：').strip()
        if choose in func_dict:
            func_dict[choose]()
        else:
            print('\033[31;1m输入错误，请检查后重新输入！\033[0m')


if __name__ == '__main__':
    main()
