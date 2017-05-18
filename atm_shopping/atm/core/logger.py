#!/usr/bin/env python
# Funtion:      
# Filename:


import logging, os
from conf import settings

log_id = {
    'ac_id': [],
    'tr_id': []
}

def is_create(log_type):
    def outwripper(func):
        def wripper(*args, **kwargs):
            username = args[0]
            if log_type == "access" :
                if username in log_id['ac_id']:
                    return logging.getLogger(username + '_' + log_type)
                else:
                    log_id['ac_id'].append(username)
                    return func(*args, **kwargs)
            elif log_type == "transaction" :
                if username in log_id['tr_id']:
                    return logging.getLogger(username + '_' + log_type)
                else:
                    log_id['tr_id'].append(username)
                    return func(*args, **kwargs)
        return wripper
    return outwripper

@is_create(log_type = 'access')
def set_ac_logger(username, isshowonscreen = False):
    return logger(username, 'access', isshowonscreen)

@is_create(log_type = 'transaction')
def set_tr_logger(username, isshowonscreen = False):
    return logger(username, 'transaction', isshowonscreen)

def logger(username, log_type, isshowonscreen):
    # create logger
    logger = logging.getLogger(username+'_'+log_type)
    logger.setLevel(settings.LOG_LEVEL)
    if isshowonscreen == True:
        # 设置屏幕输出的日志信息
        ch = logging.StreamHandler()
        ch.setLevel(settings.LOG_LEVEL)
        ch_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(ch_format)
        logger.addHandler(ch)

    # create file handler and set level to warning
    log_file = "%s/log/%s_log/%s_%s" % (settings.BASE_DIR, log_type, username, settings.LOG_TYPES[log_type])
    fh = logging.FileHandler(log_file)
    fh.setLevel(settings.LOG_LEVEL)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger


