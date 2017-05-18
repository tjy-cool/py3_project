#!/usr/bin/env python
# Funtion:      
# Filename:

import os,sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
# print(sys)

from core import main
if __name__ == '__main__':
    # main.example()
    main.run()
