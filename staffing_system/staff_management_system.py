#!/usr/bin/env python
# Author: tengjuyuan
# Funtion:  模拟数据库的增删改查
# Filename: staff_management_system

def eval_condition(condition):
    '''
    将单个筛选条件转换为eval可以执行的语句
    :param condition: 单个条件字符串
    :return: 可以用eval执行的字符串
    '''
    if condition.startswith('enroll_date'):
         condition = condition.replace('like', '.startswith(')
         condition = condition.replace(' ', '')
         condition = condition+')'
    elif condition.count('>=') == 1 or condition.count('<=') == 1:  # 去掉大于和小于的情况
        pass
    else:
        condition = condition.replace('=','==')     # 数据字符串将 = 变为 == 返回
    return condition

def eval_conditions(conditions):
    '''
    将含一个或两个条件的字符串转换为eval可以执行的语句
    :param conditions: 一个或两个条件的字符串
    :return: eval可以执行的语句
    :测试: print(eval_conditions('dept="IT" and age>22'))
    '''
    conj = ['and','or','not']
    for i in conj:
        if i in conditions:
            cond_list = conditions.split(i)
            for index, val in enumerate(cond_list):
                cond_list[index] = eval_condition(val.strip())
            cond = (' %s ' % i).join(cond_list)
            return cond
    else:
        return eval_condition(conditions)

def show_list(list_title, list, fist_line=0):
    '''
    显示二级列表
    :param list_tittle: 顶部名称
    :param list: 二级表格
    :return: 
    '''
    # print(('\033[32;1m %s \033[0m' % list_tittle).center(61, '-'))  # 输出抬头
    title_str = '\033[1;31m'
    for v in list_title:
        title_str += ('%s' % v).center(12) + '|'
    title_str += "\033[0m"
    print(title_str)
    for i in list:
        data_str = '\033[1;32m'
        for v in i:
            data_str += ('%s'% v).center(12)  + '|'
        data_str += '\033[0m'
        print(data_str)

def out_print(out_str, data):
    list_title = ['id', 'name', 'age', 'phone', 'dept', 'enroll_date']
    if out_str == '*':
        show_list(list_title,data)
    else:
        sub_data = []
        sub_title = out_str.split(',')
        for index,val in enumerate(data):   # 行号和每个人的数据列表
            sub_data.append([])
            for title in sub_title:     # 子名字，如name(age)等
                for j in range(len(list_title)):
                    if title == list_title[j]:
                        sub_data[index].append(data[index][j])
        show_list(sub_title,sub_data)

def select_data(file_obj, condition, negative=False, **kwargs):
    data = []
    for line in file_obj:
        data.append(line.strip().split(','))
    sub_data = []  # 存储所有满足条件的行号，从0开始
    for index, val in enumerate(data):
        id = int(data[index][0])
        name = data[index][1]
        age = int(data[index][2])
        phone = int(data[index][3])
        dept = data[index][4]
        enroll_date = data[index][5]
        if not negative:    # 不取反条件
            if eval(condition):
                if kwargs == {}:
                    sub_data.append(data[index])

                else:
                    data[index][kwargs['index']] = eval(kwargs['val'])
                    # print(data)
        else:   # 取反条件
            if not eval(condition):
                if kwargs == {}:
                    sub_data.append(data[index])
                else:
                    data[index][kwargs['index']] = eval(kwargs['val'])
    if kwargs == {}:
        return sub_data
    else:
        return data

def select_staff(input_str):
    '''
    select_staff('select name,age from staff_table where age>22')
    select_staff('select * from staff_table where dept="IT"')
    select_staff('select * from staff_table where enroll_date like "2013"')
    :return: 
    '''
    input_list = input_str.split(' ')
    out_str = input_list[1]
    file = input_list[3]
    condition = input_str.split('where')[-1].strip()    # where后面的条件字符串
    condition = eval_conditions(condition)
    # print("cond:", condition)
    with open('%s.txt' % file, 'r', encoding='utf-8') as f:
        sub_data = select_data(f, condition)    # 找到符合条件的
        out_print(out_str, sub_data)
        print("The total number of eligible is: %s" % len(sub_data))

def insert_staff(input_str):
    '''
    insert into staff_table values Alex Li,22,13455662334,IT,2013-02-11
    :param input_str: 
    :return: 
    '''
    input_list = input_str.split(' ')
    file_name = input_list[2]
    add_val = input_list[input_list.index('values')+1:][0]
    phone = add_val.split(',')[2]
    with open('%s.txt' % file_name, 'a+', encoding= 'utf-8') as f:
        f.seek(0)
        cnt = 0
        exist_same_phone = False
        for line in f:
            if phone == line[3]:
                exist_same_phone = True
            cnt += 1
        if exist_same_phone == False:
            f.write("%s,%s\n" % (cnt+1, add_val))
            print('Successful add. ')
        else:
            print('exist same phone, unchanged the sql.')
        # print("%s,%s" % (cnt+1, add_val))

def delete_staff(input_str):
    '''
    delete from staff_table where id=5
    :param input_str: 
    :return: 
    '''
    input_list = input_str.split(' ')
    file_name = input_list[input_list.index('from') + 1]
    condition = input_list[input_list.index('where') + 1:][-1].strip()
    condition = eval_conditions(condition)
    with open('%s.txt' % file_name, 'r', encoding='utf-8') as f:
        sub_data = select_data(f, condition, negative = True)  # 找出所有不符合条件的
    with open('%s.txt' % file_name, 'w', encoding='utf-8') as f:
        line_str = ''
        for i,val in enumerate(sub_data):
            line_str += '%s,' % (i+1)
            line_str += ','.join(val[1:])
            line_str += '\n'
        f.write(line_str)
        f.flush()
    print("Successful delete. ")

def UPDATE_staff(input_str):
    '''
    UPDATE staff_table SET dept="Market" WHERE dept="IT"
    :param input_str: 
    :return: 
    '''
    input_list = input_str.split(' ')
    file_name = input_list[1]
    print(file_name)
    new_val = input_list[input_list.index('SET') + 1].split('=')
    item = new_val[0].strip()
    list_title = ['id', 'name', 'age', 'phone', 'dept', 'enroll_date']
    condition = input_list[input_list.index('WHERE') + 1:][-1].strip()
    condition = eval_conditions(condition)
    with open('%s.txt' % file_name, 'r', encoding='utf-8') as f:
        sub_data = select_data(f, condition, negative=False,
                               index=list_title.index(item), val=new_val[1].strip() )  # 找到符合条件的
    with open('%s.txt' % file_name, 'w', encoding='utf-8') as f:
        line_str = ''
        for i, val in enumerate(sub_data):
            line_str += '%s,' % (i + 1)
            line_str += ','.join(val[1:])
            line_str += '\n'
        f.write(line_str)
        f.flush()
    print('UPDATE successful. ')

operator = {
    'select': select_staff,
    'UPDATE': UPDATE_staff,
    'insert': insert_staff,
    'delete': delete_staff
}

def sql_parsing(input_str):
    for key in operator:
        if input_str.startswith(key):
            return operator[key](input_str)

def main():
    while True:
        print('''\033[34;1m %s
    select name,age from staff_table where age>22 and age<35
    UPDATE staff_table SET dept="Market" WHERE dept="IT"
    insert into staff_table values Alex Li,22,13455662334,IT,2013-02-11
    delete from staff_table where id=5 \033[0m
        '''%'输入示例'.center(75,'-'))
        sql = input('sql> ').strip()
        if sql == 'exit':
            break
        elif sql == 0:
            continue
        else :
            sql_parsing(sql)

if __name__ == "__main__":
    main()
