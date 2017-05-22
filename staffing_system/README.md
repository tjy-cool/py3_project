## 员工管理系统
### 项目介绍
模拟数据库操作，实现数据库的增删改查操作
- 1. 可进行模糊查询，语法至少支持下面3种:
```
    1. select name,age from staff_table where age > 22
    2. select  * from staff_table where dept = "IT"
    3. select  * from staff_table where enroll_date like "2013"
```
- 2. 查到的信息，打印后，最后面还要显示查到的条数
- 3. 可创建新员工纪录，以phone做唯一键，staff_id需自增，增加语法：
```
insert into staff_table values Alex Li,22,13455662334,IT,2013-02-11
```
- 4. 可删除指定员工信息纪录，删除语法：
```
delete from staff_table where id=5
```
- 5. 可修改员工信息，语法如下:
```　　
1. UPDATE staff_table SET dept="Market" WHERE dept = "IT"
```

### 程序说明





