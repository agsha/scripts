'''
Created on Jun 27, 2012

@author: sharath
'''
from os.path import join, abspath, expanduser, exists, dirname
from os import chdir, getcwd
import re
import os
import sys


DOWNLOAD_DIR = abspath(expanduser("~/Downloads"))
HOME_DIR = abspath(expanduser("~"))
USR_LOCAL = abspath("/usr/local")
PROJECT_PATH = abspath(expanduser("~/projects/researchbroker"))
DB_DUMP = abspath(expanduser("/Users/joshlopez/projects/db_dumps/researchbroker.sql"))
VIRT_ENV = abspath(expanduser("~/projects/virtual/RB"))
PROJECT_ROOT = abspath(dirname(__file__))
sys.path.append(dirname(dirname(PROJECT_ROOT)))
from my.Test import exec_command

def _install():
    exec_command("deactivate")
    if exists(VIRT_ENV):
        exec_command("rm -rf %s"%VIRT_ENV)
    chdir("/Library/Python/2.7/site-packages")
    exec_command("mkdir -p %s"%VIRT_ENV)
    exec_command("python virtualenv.py %s"%VIRT_ENV)
    chdir(VIRT_ENV)
    exec_command("source bin/activate;pip install -r %s"%join(PROJECT_ROOT, "requirements.txt") )


    if not exists(join(PROJECT_PATH, "settings.py.example")):
        print "ERROR: please update the path of research broker in this script"
        return
    if not exists(join(PROJECT_PATH, "apps", "accounts")):
        print "ERROR: please download djangocas: git clone https://agsha@bitbucket.org/edlab/apps-django-cas.git and create a symlink \"accounts\" in the apps folder "
        return
    chdir(PROJECT_PATH)
    exec_command("touch debug.log")
    exec_command("chmod go+rwx debug.log")
    exec_command("cp settings.py.example settings.py")

def _dbdump():
    if not exists(DB_DUMP):
        print "error: please update the path to the DB_DUMP in this file"
        return
    from my.install_mysql import researchbroker, _createDb
    _createDb(researchbroker)
    exec_command("mysql -u root %s < %s"%(researchbroker, DB_DUMP))

def main():
    _install()
    _dbdump()

if __name__ == '__main__':

    method = 'main'
    if len(sys.argv) > 1 :
        method = sys.argv[1]
        globals()[sys.argv[1]]()
    else:
        main()
