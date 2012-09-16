
from Test import exec_command
from os.path import join, abspath
from os import chdir, getcwd
import re
import os
from os.path import expanduser
DOWNLOAD_DIR = abspath(expanduser("~/Downloads"))
USR_LOCAL = abspath("/usr/local")
PCRE_URL = "ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.20.tar.gz"
HTTPD_URL = "http://apache.cs.utah.edu//httpd/httpd-2.4.3.tar.gz"
PCRE_DIR = "pcre-8.20"
HTTPD_DIR = "httpd-2.4.3"
MOD_WSGI_URL = "http://modwsgi.googlecode.com/files/mod_wsgi-3.3.tar.gz"
MOD_WSGI_DIR = "mod_wsgi"


def setpath():
    exec_command('cat profile | sudo tee -a /etc/profile')
    exec_command('sudo source /etc/profile')

def setvimrc():
    exec_command('sudo cp edlabvimrc /usr/share/vim')
    exec_command('echo "source /usr/share/vim/edlabvimrc" | sudo tee -a /usr/share/vim/vimrc')

if __name__ == '__main__':
    setpath()
    setvimrc()
