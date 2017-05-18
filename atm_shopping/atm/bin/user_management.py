#!/usr/bin/env python
# Funtion:      
# Filename:
import sys,os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from core import user_manage

if __name__ == '__main__':
    user_manage.run()