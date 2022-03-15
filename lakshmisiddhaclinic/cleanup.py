#####################################################################
# Copyright 2021 Arun Madhu www.arunmadhu.com . All Rights Reserved.
# Owner       :  Arun Madhu
# Created Date:  16/11/2021
# Updater     :  Arun Madhu
# Updated Date:  18/11/2021
#####################################################################

import os
import re
import shutil
cwd = os.getcwd()

for dir, subdir, files in os.walk(cwd):
    if re.search(r'_pycache_$', dir):
        shutil.rmtree(dir)
    
    if re.search(r'.idea$', dir):
        shutil.rmtree(dir)
    if re.search(r'.swo$', dir):
        shutil.rmtree(dir)
    if re.search(r'.swp$',dir):
        shutil.rmtree(dir) 
    if re.search(r'.pyc',dir):
        shutil.rmtree(dir) 