#!/usr/bin/env python
# Funtion:      
# Filename:

import time,datetime

enroll_date = time.strftime("%Y-%m-%d",time.localtime())

expire_year = time.localtime()[0]   # 当前年份
expire_date = datetime.datetime.now().replace(year=expire_year+10).strftime('%Y-%m-%d')

default_db = {
    "id": '',
    "password": '888888',
    "credit_id": '',
    "expire_date": expire_date,    # 新注册用户有10年有效期
    "enroll_date": enroll_date,    # 新注册用户的时间"2017-05-11"
    "status": 0,  # 0=normal, 1=locked, 2=disabled
    "last_login_time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
}