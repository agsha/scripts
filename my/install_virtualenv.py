'''
Created on Jun 27, 2012

@author: sharath
'''
from Test import exec_command
from os.path import join, abspath, expanduser
from os import chdir, getcwd
import re
import os

DOWNLOAD_DIR = abspath(expanduser("~/Downloads"))
USR_LOCAL = abspath("/usr/local")

def _installVirtualEnv():
    exec_command("sudo pip install virtualenv virtualenvwrapper")
    #FIXME: port for linux also
    chdir("/Library/Python/2.7/site-packages")


def main():
    _installVirtualEnv()

if __name__ == '__main__':
    main()
