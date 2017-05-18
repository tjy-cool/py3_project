# ATM+购物车项目
## 项目介绍
模拟实现一个ATM+购物商城程序
```
1. 额度 15000或自定义
2. 实现购物商城，买东西加入 购物车，调用信用卡接口结账
3. 可以提现，手续费5%
3. 支持多账户登录
4. 支持账户间转账
5. 记录每月日常消费流水
6. 提供还款接口
7. ATM记录操作日志 
8. 提供管理接口，包括添加账户、用户额度，冻结账户等。。。
9. 用户认证用装饰器
```

## 程序介绍
- 作者：tengjuyuan
- 版本：v1.0
- 程序功能：本程序实现了ATM的用户和管理者的常用功能，以及shopping购物车的部分功能
---
    用户的功能有：
    1. 账户信息     2. 还款       3. 取款
    4. 转账         5. 账单       6. 退出
    已有账号：tjy(123), 51cto(51cto), abc(hao123)

    管理者的操作有：
    1. 注册用户     2. 重置密码
    3. 修改密码     4. 注销用户
    5. 冻结用户     6. 解冻用户
    7. 修改期限     8. 修改额度

    同时，还实现了简单的购物车进行商品选购，然后登陆信用卡进行付款，并将购买商品记录在atm的用户信息日志中
        已有账号：user(passwd)，  tom(asdf) ,   jack(asdf)等
---
- 注：
- 1. ATM的用户登陆和用户日志模块都用了装饰器，分别在my/atm/atm/core/login.py 和 my_atm/atm/core/logger.py文件中
- 2. 整个程序一般都可以按 q 结束整个程序，包括输入密码阶段

## 程序结构
```
my_atm
├── atm   #信用卡相关操作的程序
│   ├── bin #主程序
│   │   ├── atm.py              #信用卡使用操作，用户操作
│   │   └── user_management.py  #信用卡管理操作，系统管理员使用
│   ├── conf
│   │   └── settings.py       #全局设置
│   ├── core    #信用卡的核心模块
│   │   ├── data_handler.py   #数据处理模块
│   │   ├── logger.py         #日志模块
│   │   ├── login.py          #atm登陆模块
│   │   ├── main.py           #atm操作最主要函数
│   │   ├── transaction.py    #与转账相关的函数
│   │   └── user_manage.py    #管理信用卡的主要函数
│   ├── db  # 用户信息
│   │   ├── accounts    #用户数据文件，每个用户一个文件
│   │   │   └── tjy.json
│   │   ├── default_db.py   #用于生成默认用户数据
│   └── log #日志，每个用户采用单独的日志文件记录
│       ├── access_log              #用户登陆日志
│       │   └── tjy_access.log
│       └── transaction_log         #用户信用卡操作日志，转账，查询，消费，取现等
│           └── tjy_transactions.log
├── doc #文档，说明等
│   ├── Readme.txt
│    └── flow_chart.pdf
└── shopping    #购物车模块
    ├── bin_shopping    #购物车主运行程序
    │   ├── shopping_mall.py    #购物车主运行程序，用户使用
    │   └── user_management.py  #管理购物车用户账号信息，管理者使用，很简单，没具体实现
    ├── data_base       #一些数据相关的操作和文件
    │   ├── data.py             #数据操作，比如读取数据文件等
    │   ├── default_db.py       #设置默认的用户数据文件，没有使用上
    │   ├── goods               #商品列表
    │   │   └── goods_list.txt
    │   └── user_db             #用户数据
    │       ├── err.txt                 #错误数据
    │       └── username_passwd.txt     #用户名与密码文件
    └── shop_core       #购物车核心模块
        ├── login.py               #登陆模块
        ├── main.py                #主程序模块
        └── user_manage.py         #用户管理模块，只做了提示，没有具体实现
```
