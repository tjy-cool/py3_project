#!/usr/bin/env python
# Funtion:      
# Filename:

import os, sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(base_dir)

from core import user_management

if __name__ == '__main__':
    user_management.run()
