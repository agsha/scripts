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
    exec_command("sudo pip install Django")

def _installHayStack():
    exec_command("sudo pip install django-haystack")

def _installMySqlDb():
    exec_command("sudo pip install MySQL-python")

def _installPySolr():
    exec_command("sudo pip install pysolr")

def _installBoto():
    exec_command("sudo pip install boto")

def _installPiston():
    exec_command("sudo pip install django-piston")

def _installPyCrypto():
    exec_command("sudo pip install pycrypto")

def _installSimpleJson():
    exec_command("sudo pip install simplejson")

def _installMechanize():
    exec_command("sudo pip install mechanize")

def _installMemcache():
    exec_command("sudo pip install python-memcached")

def _installDjangoGuardian():
    exec_command("sudo pip install django-guardian")

def _installBeautifulSoup();
    exec_command("sudo pip install beautifulsoup==3.2.0")

def main():
    _installDjango()
    _installHayStack()
    _installMySqlDb()
    _installPySolr()
    _installBoto()
    _installPiston()
    _installSimpleJson()
    _installPyCrypto()
    _installMechanize()
    _installMemcache()
    _installDjangoGuardian()
    _installBeautifulSoup()

if __name__ == '__main__':
    main()
