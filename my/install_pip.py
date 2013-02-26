'''
Created on Jun 27, 2012

@author: sharath
'''
from Test import exec_command
from os.path import join, abspath, expanduser
from os import chdir, getcwd
import re
import os
import sys

DOWNLOAD_DIR = abspath(expanduser("~/Downloads"))
USR_LOCAL = abspath("/usr/local")


def _downloadPip():
    chdir(DOWNLOAD_DIR)
    exec_command("curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | sudo python")

def main():
    _downloadPip()

if __name__ == '__main__':
    method = 'main'
    if len(sys.argv) > 1 :
        method = sys.argv[1] 
        globals()[sys.argv[1]]()
    else:
        main()    