#!/usr/bin/env python
# Funtion:      
# Filename:

import os,sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
# 将atm的地址也加到系统路径中
atm_base_dir = __file__
for i in range(3):
    atm_base_dir = os.path.dirname(atm_base_dir)
atm_core_dir = '%s/atm' % atm_base_dir
sys.path.append(atm_core_dir)

from shop_core import main

if __name__ == '__main__':
    main.run()