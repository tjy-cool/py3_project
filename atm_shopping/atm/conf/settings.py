#!/usr/bin/env python
# Funtion:      
# Filename:

import os
import logging

BASE_DIR = os.path.dirname( os.path.dirname(os.path.abspath(__file__)))     # atm 文件夹的绝对地址

DATABASE = {
    'engine': 'file_storage',   # 方便后期支持 mysql
    'name': 'accounts',
    'path': '%s/data' % BASE_DIR
}

LOG_LEVEL = logging.INFO
LOG_TYPES = {
    'transaction': 'transactions.log',   # 记录用户用钱信息
    'access': 'access.log'  # 记录用户登陆信息
}

TRANSACTION_TYPE = {
    'repay':{   # 还款到信用卡
        'action':'plus',
        'interest':0},
    'withdraw': # 取现
        {'action':'minus',
         'interest':0.05},
    'transfer': # 转账
        {'action':'minus',
         'interest':0.05},
    'consume':{     # 消费，无利息付款
        'action':'minus',
        'interest':0}
}

