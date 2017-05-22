## 员工管理系统
### 项目介绍
模拟数据库操作，实现数据库的增删改查操作
```
1. 可进行模糊查询，语法至少支持下面3种:
    (1). select name,age from staff_table where age > 22
    (2). select  * from staff_table where dept = "IT"
    (3). select  * from staff_table where enroll_date like "2013"
2. 查到的信息，打印后，最后面还要显示查到的条数

3. 可创建新员工纪录，以phone做唯一键，staff_id需自增，增加语法：
    insert into staff_table values Alex Li,22,13455662334,IT,2013-02-11

4. 可删除指定员工信息纪录，删除语法：
    delete from staff_table where id=5

5. 可修改员工信息，语法如下:
    UPDATE staff_table SET dept="Market" WHERE dept = "IT"
```

### 程序说明
- 作者：tengjuyuan
- 版本：v1.0
- 程序功能：以txt文件模拟数据库，实现数据库的增删改查功能。

---
功能说明：

where后面的判断条件可以为以下几种：

    基本功能：
        1. id判断，可以为 运算符>=、<=、>、<、=，运算符两边可以有任意空格，如id =5或 id>=  3
        2. name判断，可以为 name = "Jack Wang" ，待查找的名字必须用双引号
        3. age判断，同id判断，如age >=22
        4. phone判断，程序同id判断，但是输入等号符合实际情况，如phone=13434545667
        5. dept判断，同name，如dept="IT"
        6. enroll_data判断， 可以为 enroll_date like "2013"， 
            也可以输入年和月，格式为：year-month-day如enroll_date like "2013-10-10"
    高级功能：
        可以使用【and, or, not】连接以上任意两个条件，如age >= 20 and dept="IT"

select显示说明：
    select后面的显示可以为一个或多个的组合或全部（*），以逗号连接，中间不能有空格，如 id,name,age 或id,dept,enroll_date

数据说明：

    输出存储格式：['id', 'name', 'age', 'phone', 'dept', 'enroll_date']
    如：1,Alex Li,22,13651054608,IT,2013-04-01


---






