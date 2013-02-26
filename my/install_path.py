import sys
from Test import exec_command
from os.path import join, abspath
from os import chdir, getcwd
import re
import os
from os.path import expanduser
DOWNLOAD_DIR = abspath(expanduser("~/Downloads"))
HOME = abspath(expanduser("~"))
USR_LOCAL = abspath("/usr/local")
PCRE_URL = "ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.20.tar.gz"
HTTPD_URL = "http://apache.cs.utah.edu//httpd/httpd-2.4.3.tar.gz"
PCRE_DIR = "pcre-8.20"
HTTPD_DIR = "httpd-2.4.3"
MOD_WSGI_URL = "http://modwsgi.googlecode.com/files/mod_wsgi-3.3.tar.gz"
MOD_WSGI_DIR = "mod_wsgi"


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

def setgit():
    exec_command("git config --global color.ui auto")
    email = raw_input("\n\n\n\n\n\nEnter your email like you want it in git(Example: pgarg@gmail.com):\n")
    name  = raw_input("\n\n\n\n\n\nEnter your name like you want it in git(Example: Pranav Garg):\n")
    raw_input( "i AM USING EMAIL:%s AND NAME:%s FOR YOUR GIT. iF WRONG, THEN PRESS ctrl-c NOW AND RERUN THIS SCRIPT (PYTHON INSTALL_PATH.PY)"%(email, name))
    exec_command('git config --global user.email "%s"'%email)
    exec_command('git config --global user.name "%s"'%name)
    chdir(HOME)
    exec_command('curl https://raw.github.com/git/git/master/contrib/completion/git-completion.bash -O')
    chdir(PROJECT_ROOT)

def setpath():
    exec_command('touch %s'%join(HOME, '.bash_profile'))
    exec_command('echo source %s | tee -a %s'%(join(PROJECT_ROOT, "profile"), join(HOME, '.bash_profile')))
    exec_command('source %s'%join(HOME, '.bash_profile'))

def setup_vim():
    chdir(HOME)
    exec_command('ln -s %s .vimrc'%join(PROJECT_ROOT, "vimrc"))
    exec_command('ln -s %s .vim'%join(PROJECT_ROOT, "vim"))
    exec_command('mkdir -p %s'%join(HOME, ".vim", "bundle"))
    chdir(join(HOME, ".vim", "bundle"))
    exec_command("git clone https://github.com/kien/ctrlp.vim.git")
    chdir(PROJECT_ROOT)

def main():
    setgit()
    setpath()
    setup_vim()

if __name__ == '__main__':
    method = 'main'
    if len(sys.argv) > 1 :
        method = sys.argv[1]
        globals()[sys.argv[1]]()
    else:
        main()
