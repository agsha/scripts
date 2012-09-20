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
HOME_DIR = abspath(expanduser("~"))
USR_LOCAL = abspath("/usr/local")

def _downloadVialogues():
    chdir(HOME_DIR)
    exec_command("git clone git@bitbucket.org:edlab/apps-vialogues.git projects/vialogues_code")

def _downloadDjangoCas():
    chdir(HOME_DIR)
    exec_command("git clone git@bitbucket.org:edlab/apps-django-cas.git projects/django.cas")

def _extractVialogues():
    chdir(join(HOME_DIR, "projects", "vialogues_code"))
    exec_command("ln -s %s apps/accounts"%join(HOME_DIR, "projects", "django-cas"))
    exec_command("touch debug.log")
    exec_command("chmod go+rwx debug.log")
    exec_command("cp settings.py.development settings.py")
    exec_command("python manage.py syncdb")
    exec_command("python bootstrap.py")


def main():
    _downloadDjangoCas()
    _downloadVialogues()
    _extractVialogues()

if __name__ == '__main__':
    method = 'main'
    if len(sys.argv) > 1 :
        method = sys.argv[1]
        globals()[sys.argv[1]]()
    else:
        main()
