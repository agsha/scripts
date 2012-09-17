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

def _installDjango():
    exec_command("pip install Django")

def _installHayStack():
    exec_command("pip install django-haystack")

def _installMySqlDb():
    exec_command("pip install MySQL-python")

def _installPySolr():
    exec_command("pip install pysolr")

def _installBoto():
    exec_command("pip install boto")

def _installPiston():
    exec_command("pip install django-piston")

def _installPyCrypto():
    exec_command("pip install pycrypto")

def _installSimpleJson():
    exec_command("pip install simplejson")

def main():
    _installDjango()
    _installHayStack()
    _installMySqlDb()
    _installPySolr()
    _installBoto()
    _installPiston()
    _installSimpleJson()
    _installPyCrypto()

if __name__ == '__main__':
    main()
