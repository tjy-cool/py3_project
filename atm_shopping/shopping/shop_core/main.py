#!/usr/bin/env python
# Funtion:      
# Filename:
import os,sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from shop_core import login
from data_base import data

# atm 目录下的库
from core import login as atm_login  # atm文件夹下的core
from core import main as atm_main
from core import data_handler
from core import logger

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def run():
    user_file = "%s/data_base/user_db/username_passwd.txt" % base_dir
    err_file = '%s/data_base/user_db/err.txt' % base_dir
    goods_file = '%s/data_base/goods/goods_list.txt' % base_dir
    user = login.login(user_file, err_file)
    if user != '':  # 成功登陆
        shopping( goods_file)
    else:  # 没有成功登陆
        print('login err!')

def shopping(goods_list_file):
    with open(goods_list_file, 'r', encoding='utf_8') as f:
        goods_list = data.file_2_list(f)    # 读取超市商品列表
    exit_flag = False
    while not exit_flag:
        flag = input('Do you want buy goods?(Y/N)').strip()
        if flag == 'Y':
            exit_flag = True
        elif flag == 'N':
            exit()
        else:
            print('Invalid input!')
            continue
        bought_goods_list = choose_goods(goods_list)    # 将商品加入购物车
        print('=' * 50)
        print('\033[32;1mPlease login your credit card \033[0m')
        pay_for(atm_main.user_data,bought_goods_list)  # 为选购商品付款

def choose_goods(goods_list):
    bought_goods_list = []
    show_goods_flag = 1
    exit_flag = False
    while not exit_flag:
        if show_goods_flag:
            data.show_list('Goods List', goods_list)
        your_choose = input('Please input you want buy goods index(quit:q, check:c): ')
        if your_choose.isnumeric():  # 为纯数字
            your_choose = int(your_choose)
            if your_choose in range(len(goods_list)):
                goods_name = goods_list[your_choose][0]
                goods_price = int(goods_list[your_choose][1])
                bought_goods_list.append([goods_name,goods_price])
                print('\033[1;31;44m%s\033[0m have been added to the bin_shopping car!' % goods_name)
                show_goods_flag = 1
            else:
                print("Your choose goods not exist! Please choose again .")
        elif your_choose == 'q':  # quit 退出
            data.show_list('Your bin_shopping car list', bought_goods_list)
            exit_flag = True
        elif your_choose == 'c':  # check 查询
            data.show_list('Your bin_shopping car list', bought_goods_list)
            show_goods_flag = 0
        else:
            print("Your input goods list invalid! Please choose again .")
    data.show_list('Your bin_shopping car list', bought_goods_list)
    return bought_goods_list

@atm_login.login_acquired
def pay_for(acc_data, goods_list):
    account_data = data_handler.get_user_db(acc_data['account_id'])
    tr_log_obj = logger.set_tr_logger(account_data['id'])
    balance = account_data['balance']
    print('Your balance is: %s' % balance)
    buy_flag = input('Do you really want to buy the goods(Y/N): ').strip()
    if buy_flag == 'Y': # 确定购买
        all_goods_price = 0    # 所有商品的价格
        for goods in goods_list:
            all_goods_price += goods[1]
        if all_goods_price <= account_data['balance']:
            account_data['balance'] -= all_goods_price
            for val in goods_list:
                tr_log_obj.info('Buy %s ,cost %s$' %(val[0], val[1]))
            print('\033[33;1mYou have bought all the goods! Thanks for your Custom\033[0m')
        else:
            print('Your credit card have no enough money to pay for the goods!')
    elif buy_flag == 'N':
        exit()
    else :
        exit('Invalid input, see you next time!')