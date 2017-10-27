# 高级FTP服务器开发：
## 项目介绍
编写一个高级FTP的服务端和客户端，要求符合一下条件：
```
1. 用户加密认证
2. 多用户同时登陆
3. 每个用户有自己的家目录且只能访问自己的家目录
4. 对用户进行磁盘配额、不同用户配额可不同
5. 用户可以登陆server后，可切换目录
6. 查看当前目录下文件
7. 上传下载文件，保证文件一致性
8. 传输过程中现实进度条
9. 支持断点续传
```

## 程序介绍
- 作者：tengjuyuan
- 版本：v1.0
- 程序功能：本程序实现了以上所有要求，server端必须在linux下运行，client端在windows下运行，client端单独设计了一个管理员登陆的程序，可以进行用户增、删、改、查。
---    
    管理员的用户名和密码都为：admin
    普通用户的用户名：tjy, 密码：abcd1234
---
主要功能有：
---
    （一）、客户端：
    客户端有两个，一个是管理员登陆的，一个是普通用户登陆的
    1.1 运行FTP_client/bin/ftp_nameage_user.py，可以进行普通用户的增（add_user）、删(del_user)、改(alter_uer)、查(query_user)。
    比如：增加用户tom，只需要输入：add_user tom
    然后按照提示一步一步完成输入就可以增加tom用户了

    1.2 运行FTP_client/bin/ftp_nameage_user.py，可以对用户进行多种操作（常见的linux操作），以及上传下载文件操作，实现的指令有：
    ls, pwd, ifconfig, tree, date, cal,
    cat, more, mkdir, rm, cd
    push(上传文件)
    pull(下载文件)

    1.3 在pycharm中不能展示传输过程中现实进度条，在cmd中可以很好的看到进度条

    1.4 如果需要修改客户端的ip地址和端口号，在conf/settings.py里面进行修改

    1.5 如果执行了cd指令，修改了目录，提示也会相应的进行修改，但是不能访问自己家目录之外的目录

    （二）、服务端
    2.1 直接运行bin/ftf_server.py即可
    2.2 用户信息保存在db/username_passwd文件夹里面，以json格式保存。
    2.3  用户的目录为 home/xxx
    2.4 如果需要修改客户端的ip地址和端口号，在conf/settings.py里面进行修改
    
    注：普通用户没有写log（后续加上），但是管理员有log
---

## 程序结构
```
Advanced_FTP/
├── FTP_client          # 客户端
│   ├── bin     #主程序
│   │   ├── ftp_client.py       # 普通用户客户端
│   │   ├── ftp_manage_user.py  # 管理员用户客户端
│   │   └── __init__.py
│   ├── conf    # 
│   │   ├── __init__.py
│   │   └── settings.py     # 全局设置， 如ip地址和port修改等 
│   ├── core
│   │   ├── __init__.py
│   │   ├── logger.py       # 日志模块
│   │   ├── main.py         # 普通用户客户端的主函数
│   │   └── user_management.py  # 管理员用户客户端的主函数
│   ├── db      # 暂时没用
│   │   └── __init__.py
│   └── log     # 日志
│       ├── admin_log   # 管理员用户的日志
│       ├── __init__.py
│       └── tjy_log     # 普通用户的日志，暂时没有写
├── FTP_server      # 服务端
│   ├── bin     # 主程序
│   │   ├── ftp_server.py   # 服务端入口模块
│   │   └── __init__.py
│   ├── conf
│   │   ├── __init__.py
│   │   └── settings.py      # 全局设置， 如ip地址和port修改等 
│   ├── core
│   │   ├── __init__.py
│   │   ├── logger.py       # 日志模块
│   │   ├── main.py         # 服务端主函数
│   ├── db                  # 用户数据
│   │   ├── home            # 所有的普通用户的家目录都在这个文件夹下
│   │   │   └── tjy         # 普通用户家目录，
│   │   │       └── tjy.log     # 普通用户的日志，暂时没用
│   │   ├── __init__.py
│   │   └── username_passwd # 存放普通用户的用户信息
│   │       └── tjy.json
│   └── log
│       └── __init__.py
└── readme.md   

```