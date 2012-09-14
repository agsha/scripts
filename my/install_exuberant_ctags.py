
'''
Created on Jun 24, 2012

@author: sharath
'''
from Test import exec_command
from os.path import join, abspath
from os import chdir, getcwd
import re
import os
from os.path import expanduser
DOWNLOAD_DIR = abspath(expanduser("~/Downloads"))
USR_LOCAL = abspath("/usr/local")
PCRE_URL = "ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.20.tar.gz"
CTAGS_URL  = "http://downloads.sourceforge.net/project/ctags/ctags/5.8/ctags-5.8.tar.gz?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fctags%2Ffiles%2Fctags%2F5.8%2F&ts=1347652343&use_mirror=superb-dca2"
CTAGS_DIR = "ctags-5.8"

HTTPD_URL = "http://apache.cs.utah.edu//httpd/httpd-2.4.3.tar.gz"
PCRE_DIR = "pcre-8.20"
HTTPD_DIR = "httpd-2.4.3"
MOD_WSGI_URL = "http://modwsgi.googlecode.com/files/mod_wsgi-3.3.tar.gz"
MOD_WSGI_DIR = "mod_wsgi"

def downloadCtags():
    chdir(DOWNLOAD_DIR)
    exec_command("curl -o ctags-5.8.tar.gz -L %s"%CTAGS_URL)

def extractCtags():
    chdir(DOWNLOAD_DIR)
    exec_command("tar xvzf ctags-5.8.tar.gz -C %s"%DOWNLOAD_DIR)
    chdir(join(DOWNLOAD_DIR, CTAGS_DIR))
    exec_command("%s --prefix=%s"%(join(DOWNLOAD_DIR, CTAGS_DIR, "configure"), join(USR_LOCAL, "ctags-exuberant")))
    exec_command("make")
    exec_command("sudo make install")

if __name__ == '__main__':
    downloadCtags()
    extractCtags()
