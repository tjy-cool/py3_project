#!/usr/bin/env python
# Author: tengjuyuan
# Funtion: Implement the calculator function with re module
# Filename: calculator.py

import re

def strlist_to_num(src_str_list):
    '''
    将字符串列表转换为数字，主要是对有无小数点进行处理
    :param src_str: 数字字符串列表
    :return: 转换后的数字
    '''
    n = []
    for src_str in src_str_list:
        if re.search('\.', src_str) == None:
            n.append(int(src_str))
        else:
            n.append(float(src_str))
    return n
  

def deal_multiply_divide(src_str):
    '''
    将传入的字符串进行乘除法计算
    测试代码：print(deal_multiply_divide("-3*2*-5/5"))
    :param src_str: 只含乘除计算法则，不含加减法则的字符串
    :return: 计算后的结果的字符串
    '''
    num_str_list = re.split(r'\*|\/', src_str)   # 数字字符串
    num = strlist_to_num(num_str_list)
    rules = re.findall(r'\*|\/', src_str)   # 运算法则，乘号或除号
    result = num[0]
    for index,rule in enumerate(rules):
        if rule == '*':
            result *= num[index+1]
        else :
            result /= num[index+1]
    return str(result)

def deal_plus_minus(src_str):
    '''
    将传入的字符串进行加减法计算
    测试代码：print(deal_plus_minus('-23.4+34.5-56+21.345'))
    :param src_str: 只含加减计算法则，不含乘除法则的字符串
    :return: 计算后的结果的字符串
    '''
    src_str = re.sub(r'\+\-', '-', src_str)
    src_str = re.sub(r'\-\-', '+', src_str)
    num_str_list = re.split(r'\+|\-', src_str)
    rules = re.findall(r'\+|\-', src_str)
    if num_str_list[0] == '':
        del num_str_list[0]
        del rules[0]
        num_str_list[0] = '-%s' % num_str_list[0]

    num = strlist_to_num(num_str_list)
    result = num[0]
    for index,rule in enumerate(rules):
        if rule == '+':
            result += num[index+1]
        elif rule == '-':
            result -= num[index+1]
    return str(result)


def deal_four_rules(src_str):
    '''
    计算只包含加减乘除法的字符串
    测试代码：print(deal_four_rules('-23.4+34.5-56-21.345*23*-3.4-23*34.5'))
    :param src_str: 
    :return: 
    '''
    while True:
        times = re.search(r'(\-?\d+\.?\d*(\*|\/))+(\-?\d+\.?\d*)', src_str)
        if times != None:   # 包含乘除法的源字符串
            times_str = times.group()
            result = deal_multiply_divide(times_str)
            if re.match('-',times_str) != None and re.match('-', result) == None:   # 以减号开始，计算后的字符串
                result = '+' + result
            src_str = re.sub(r'(\-?\d+\.?\d*(\*|\/))+(\-?\d+\.?\d*)', result, src_str, count = 1)
        else:
            break
    while True:
        add = re.search(r'(\-?\d+\.?\d*(\+|\-))+(\-?\d+\.?\d*)', src_str)
        if add != None:     # 包含加减法的源字符串
            add_str = add.group()
            result = deal_plus_minus(add_str)
            src_str = re.sub(r'(\-?\d+\.?\d*(\+|\-))+(\-?\d+\.?\d*)', result, src_str, count = 1)
        else:
            break
    return src_str

def calc(src_str):
    '''
    计算含括号，四则运算
    :param src_str: 包含括号和四则运算的字符串
    :return: 计算后结果的字符串
    '''
    src_str = re.sub(r' ', '', src_str)     # 去除空格
    while True:
        inter = re.search(r'\([^()]+\)', src_str)
        if inter != None:
            str1 = re.sub(r'\(|\)', '', inter.group())
            inter_calc_str = deal_four_rules(str1)
            src_str = re.sub(r'\([^()]+\)', inter_calc_str, src_str, count=1)
        else:
            src_str = deal_four_rules(src_str)
            break

    if re.search('\.', src_str) == None:
        return int(src_str)
    else:
        return float(src_str)

def main():
    with open('formula.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            src_str = line
            result = calc(src_str)
            print(result, type(result))

if __name__ == '__main__':
    main()
