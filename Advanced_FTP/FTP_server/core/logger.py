#!/usr/bin/env python
# Funtion:      
# Filename:

# logging.debug("debug")
# logging.info('info')
# logging.warning("warning")
# logging.error('error')
# logging.critical("critical")

import logging, os
from conf import settings

def logger(username, isshowonscreen):
    # create logger
    logger = logging.getLogger(username+'_')
    logger.setLevel(settings.LOG_LEVEL)
    if isshowonscreen == True:
        # 设置屏幕输出的日志信息
        ch = logging.StreamHandler()
        ch.setLevel(settings.LOG_LEVEL)
        ch_format = logging.Formatter(settings.Ch_Format)
        ch.setFormatter(ch_format)
        logger.addHandler(ch)

    # create file handler and set level to warning
    log_file = "%s/log/%s_log" % (settings.BASE_DIR,username)

    fh = logging.FileHandler(log_file)
    fh.setLevel(settings.LOG_LEVEL)
    formatter = logging.Formatter(settings.Fh_Format)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger


