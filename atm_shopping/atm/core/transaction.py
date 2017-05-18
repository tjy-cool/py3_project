#!/usr/bin/env python
# Funtion:      
# Filename:

from conf import settings
from core import data_handler
from core import logger
def make_transaction(log_obj, user_db, tran_type, amount):
    amount = float(amount)
    if tran_type in settings.TRANSACTION_TYPE:
        interest = amount * settings.TRANSACTION_TYPE[tran_type]['interest']    # 利息
        old_balance = user_db['balance']   # 旧款
        if settings.TRANSACTION_TYPE[tran_type]['action'] == 'plus':  # 当为加
            new_balance = old_balance + amount - interest
        elif settings.TRANSACTION_TYPE[tran_type]['action'] == 'minus':   # 为减时
            new_balance = old_balance - amount - interest
            if new_balance < 0: #
                print('''\033[31;1mYour credit [%s] is not enough for this transaction [-%s], '
                      your current balance is [%s]''' %(user_db['credit'],(amount + interest), old_balance ))
                return
        user_db['balance'] = new_balance
        data_handler.set_user_db(user_db['id'], user_db)  # 保存数据
        # 保存相应日志到相应文件
        log_obj.info('action:%s   amount:%s     interest:%s'
                         %(tran_type, amount, interest))
        return user_db
    else:
        print("\033[31;1mTransaction type [%s] is not exist!\033[0m" % tran_type)