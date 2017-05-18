#!/usr/bin/env python
# Funtion:      
# Filename:

def file_2_dict(file_handle, split_str = ','):
    '''
    文件转换为字典，
    :param file_handle: 文件句柄
    :param dict: 字典
    :param split_str: 
    :return: 
    '''
    dict_1 = {}
    file_handle.seek(0)
    for line in file_handle.readlines():
        key_1 = line.split(split_str)[0].strip()
        val_1 = line.split(split_str)[1].strip()
        dict_1[key_1] = val_1
    return dict_1

def file_2_list(file_handle, split_str=','):
    '''
    文件内容保存为二级列表
    :param file_handle: 文件句柄
    :param split_str: 分割符
    :return: 二级列表
    '''
    list = []
    file_handle.seek(0)
    for line in file_handle.readlines():
        val_1 = line.split(split_str)[0].strip()
        val_2 = line.split(split_str)[1].strip()
        list.append([val_1,val_2])
    return list

def show_list(list_tittle, list, fist_line=0):
    '''
    显示二级列表
    :param list_tittle: 顶部名称
    :param list: 二级表格
    :return: 
    '''
    print(('\033[32;1m%s\033[0m' % list_tittle).center(61, '-'))
    print('\033[1;31mOrder'.center(15,' ') + '|' +
          'Goods'.center(28,' ') + '|' +
          'Price\033[0m'.center(18,' '))

    for i in range(fist_line, len(list)):
        print(('\033[1;31m%s' % i).center(15, ' ') + '|' +
              ('%s' % list[i][0]).center(28, ' ') + '|' +
              ('%s\033[0m' % list[i][1]).center(18, ' '))
        # print('\033[1;31m%s. %s %s\033[0m' % (i, list[i][0], list[i][1]))
    print(50 * '-')