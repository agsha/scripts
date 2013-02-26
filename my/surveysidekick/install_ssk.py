'''
Created on Jun 27, 2012

@author: sharath
'''
from my.Test import exec_command
from os.path import join, abspath, expanduser, exists
from os import chdir, getcwd
import re
import os
import sys

DOWNLOAD_DIR = abspath(expanduser("~/Downloads"))
HOME_DIR = abspath(expanduser("~"))
USR_LOCAL = abspath("/usr/local")
SSK = abspath(expanduser(""))
DB_DUMP = abspath(expanduser(""))
VIRT_SSK = abspath(expanduser("~/VIRT_SSK"))
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
def _downloadVialogues():
    chdir(HOME_DIR)
    exec_command("git clone git@bitbucket.org:edlab/apps-vialogues.git projects/vialogues_code")

def _downloadDjangoCas():
    chdir(HOME_DIR)
    exec_command("git clone git@bitbucket.org:edlab/apps-django-cas.git projects/django.cas")

def _install():
    if exists(VIRT_SSK):
        exec_command("rm -rf %s"%VIRT_SSK)
    chdir("/Library/Python/2.7/site-packages")
    exec_command("python virtualenv.py %s"%VIRT_SSK)
    chdir(VIRT_SSK)
    exec_command("source bin/activate;pip install -r %s"%join(PROJECT_ROOT, "ssk-requirements.txt") )

    
    if not exists(join(SSK, "settings.py")):
        print "ERROR: please update the path of surveysidekick in this script"
        return
    if not exists(join(SSK, "apps", "accounts")):
        print "ERROR: please download djangocas: git clone https://agsha@bitbucket.org/edlab/apps-django-cas.git and create a symlink \"accounts\" in the apps folder "
        return
    chdir(SSK)
    exec_command("touch debug.log")
    exec_command("chmod go+rwx debug.log")
    exec_command("cp settings.py.example settings.py")
    exec_command("python manage.py syncdb")
    exec_command("python bootstrap.py")

def dbdump():
    if not exists(DB_DUMP):
        print "error: please update the path to the DB_DUMP in this file"
        return
    from my.install_mysql import surveysidekick, _createDb
    _createDb(surveysidekick)
    exec_command("mysql -u root %s < %s"%(surveysidekick, DB_DUMP))
        
def main():
    _install()

if __name__ == '__main__':
    
    method = 'main'
    if len(sys.argv) > 1 :
        method = sys.argv[1]
        globals()[sys.argv[1]]()
    else:
        main()
