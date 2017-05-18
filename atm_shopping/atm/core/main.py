#!/usr/bin/env python
# Funtion:      
# Filename:

from core import login
from core import logger
from core import data_handler
from core import transaction
import os,time
# ac_log = {}
# tr_log = {}

# 用户数据，存在内存中
user_data = {
    'account_id':None,
    'is_authenticated':False,
}

@login.login_acquired
def account_info(acc_data):
    '''
    查询账户信息
    :param acc_data: 
    :return: 
    '''
    account_data = data_handler.get_user_db(acc_data['account_id'])
    tr_log_obj = logger.set_tr_logger(account_data['id'])
    info_title = ("\033[31;m %s's Bank info\033[0m" % acc_data['account_id']).center(55, '-')
    info_body = '''\033[32;m
    username:           %s
    credit:             %s
    balance:            %s
    enroll date:        %s
    expire date:        %s
    last logout data:   %s
\033[0m''' % (account_data['id'], account_data['credit'],
              account_data['balance'], account_data['enroll_date'],
              account_data['expire_date'], account_data['last_login_time'])

    info = info_title + info_body + '-' * 45
    print(info)
    tr_log_obj.info('query the account information')

@login.login_acquired
def repay(acc_data):
    '''
    还款
    :param acc_data:   包含user_db和用户是否登陆 的字典
    :return: 
    '''
    account_data = data_handler.get_user_db(acc_data['account_id'])
    tr_log_obj = logger.set_tr_logger(account_data['id'])
    current_balance = '''---------------- BALABCE INFO --------------
        Credit :  %s
        Balance:  %s
-------------------------------------------''' % (account_data['credit'], account_data['balance'])
    print(current_balance)
    back_flag = False
    while not back_flag:
        repay_amount = input('\033[1;34mInput repay amount: \033[0m').strip()
        if len(repay_amount) > 0 and repay_amount.isdigit():
            new_balance = transaction.make_transaction(tr_log_obj, account_data, 'repay', repay_amount)
            if new_balance:
                print('New:Balance:\033[32;1m %s \033[0m' % new_balance['balance'])
        elif repay_amount == 'b':  # 返回
            back_flag = True
        elif repay_amount == 'q':  # 退出程序
            exit('请保管好您的信用卡，欢迎下次使用！')
        else:  # 错误输入
            print('\033[31;1m[%s] is not a valid amount, only accept integer!\033[0m' % repay_amount)


@login.login_acquired
def withdraw(acc_data):
    '''
    提现
    :param acc_data: 
    :return: 
    '''
    account_data = data_handler.get_user_db(acc_data['account_id'])
    tr_log_obj = logger.set_tr_logger(account_data['id'])
    current_balance = '''---------------- BALABCE INFO --------------
        Credit :  %s
        Balance:  %s
-------------------------------------------''' % (account_data['credit'], account_data['balance'])
    print(current_balance)
    back_flag = False
    while not back_flag:
        withdraw_amount = input('\033[1;34mInput withdraw amount: \033[0m').strip()
        if withdraw_amount.isdigit():
            new_balance = transaction.make_transaction(tr_log_obj, account_data, 'withdraw', withdraw_amount)
            if new_balance:
                print('New:Balance:\033[32;1m %s \033[0m' % new_balance['balance'])
        elif withdraw_amount == 'b':  # 返回
            back_flag = True
        elif withdraw_amount == 'q':  # 退出程序
            exit('请保管好您的信用卡，欢迎下次使用！')
        else:  # 错误输入
            print('\033[31;1m[%s] is not a valid amount, only accept integer!\033[0m' % withdraw_amount)

@login.login_acquired
def transfer(acc_data):
    '''
    转账
    :param acc_data: 
    :return: 
    '''
    account_data = data_handler.get_user_db(acc_data['account_id'])
    tr_log_obj = logger.set_tr_logger(account_data['id'])
    all_user = data_handler.get_all_username()  # 存在data/accounts文件夹下的所有用户
    current_balance = '''---------------- BALABCE INFO --------------
        Credit :  %s
        Balance:  %s
-------------------------------------------''' % (account_data['credit'], account_data['balance'])
    print(current_balance)
    back_flag = False
    while not back_flag:
        tran_id = input('\033[1;34mInput what account you want transfer: \033[0m').strip()
        if tran_id in all_user:  # 用户存在
            tran_amount = input('\033[1;34mInput withdraw amount: \033[0m').strip()
            if tran_amount.isdigit():  # 数字
                new_balance = transaction.make_transaction(tr_log_obj, account_data, 'withdraw', tran_amount)
                if new_balance:  # 返回的 new_balance 有效，即钱够
                    # 汇款方进行相关操作并进行相关日志记录
                    tran_data = data_handler.get_user_db(tran_id)
                    tran_data['balance'] += int(tran_amount)
                    data_handler.set_user_db(tran_id, tran_data)
                    traned_log_obj = logger.set_tr_logger(tran_id)
                    traned_log_obj.info('Received account %s transfer amount %s' % (account_data['id'], tran_amount))

                    print('New:Balance:\033[32;1m %s \033[0m' % new_balance['balance'])
            elif tran_amount == 'b':  # 返回
                back_flag = True
            elif tran_amount == 'q':  # 退出程序
                exit('请保管好您的信用卡，欢迎下次使用！')
            else:  # 错误输入
                print('\033[31;1m[%s] is not a valid amount, only accept integer!\033[0m' % tran_amount)
        elif tran_id == 'b':  # 返回
            back_flag = True
        elif tran_id == 'q':  # 退出程序
            exit('请保管好您的信用卡，欢迎下次使用！')
        else:  # 错误输入
            print('\033[31;1m[%s] is not a valid id' % tran_id)


@login.login_acquired
def pay_check(acc_data):
    # 账单
    account_data = data_handler.get_user_db(acc_data['account_id'])

    Base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tr_log_path = '%s/log/transaction_log/%s_transactions.log' %(Base_path, account_data['id'])
    # print(tr_log_path)
    with open(tr_log_path, 'r', encoding='utf-8') as f:
        print(f.read())
    # tr_log_obj = logger.set_tr_logger(account_data['id'])
    # print('')
    # 取款信息
    # 转账信息
    # 消费信息



def logout(acc_data):
    '''
    退出登陆
    :param acc_data: 
    :return: 
    '''
    if acc_data['is_authenticated'] == False:
        print('\033[31;1mWarning,You are not login...\033[0m')
    else:
        account_data = data_handler.get_user_db(acc_data['account_id'])
        username = account_data['id']
        ac_log_obj = logger.set_ac_logger(username)
        ac_log_obj.info('account [%s] are logout' % username)
        acc_data['is_authenticated'] = False
        if username in logger.log_id['ac_id']:
            logger.log_id['ac_id'].remove(username)
        elif username in logger.log_id['tr_id']:
            logger.log_id['tr_id'].remove(username)
        print('您已退出ATM系统，请保管好您的信用卡')

def interactive(acc_data):
    menu_title = "\033[31;m Bank Action Menu \033[0m".center(55, '-')
    # menu_title = ("\033[31;m %s's Bank Action Menu \033[0m" % acc_data['account_id']).center(55, '-')
    menu_body = '''\033[32;1m
    1. 账户信息     2. 还款       3. 取款
    4. 转账         5. 账单       6. 退出\033[0m
'''
    menu = menu_title + menu_body + '-' * 44
    menu_dict = {
        '1': account_info,
        '2': repay,
        '3': withdraw,
        '4': transfer,
        '5': pay_check,
        '6': logout
    }
    exit_flag = False
    while not exit_flag:
        print(menu)
        user_option = input('>> ').strip()
        if user_option in menu_dict:
            # print('accdata ',acc_data)
            menu_dict[user_option](acc_data)
        elif user_option == 'q':
            exit('请保管好您的信用卡，欢迎下次使用！')
        else:
            print("\033[31;1mOption does not exist!\033[0m")

def run():
    login.login(user_data)
    if user_data['is_authenticated']:
        interactive(user_data)
