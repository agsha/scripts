'''
Created on Jun 17, 2012

@author: sharath
'''

from Test import exec_command as ex
from os.path import join, abspath
from os import chdir, getcwd
import re
from string import strip
import os
import sys
from os.path import expanduser
DOWNLOAD_DIR = abspath(expanduser("~/Downloads"))
MYSQL_64_URL = "http://dev.mysql.com/get/Downloads/MySQL-5.5/mysql-5.5.25-osx10.6-x86_64.tar.gz/from/http://mysql.mirrors.pair.com/"
MYSQL_32_URL = "http://dev.mysql.com/get/Downloads/MySQL-5.5/mysql-5.5.25-osx10.5-x86.tar.gz/from/http://mysql.mirrors.pair.com/"
USR_LOCAL = abspath("/usr/local")

surveysidekick = "surveysidekick"
researchbroker = "researchbroker"
vialogues = "vialogues"
nlt = "nlt"
cas = "cas"
def is64Bit():
    out = ex("uname -a")[0]
    for line in out:
        if re.match(".*RELEASE_X86_64 x86_64$", line) is not None:
            return True
        elif re.match(".*RELEASE_I386 i386$", line) is not None:
            return False
        else:
            raise Exception("Cant detect if cpu is 32 bit or 64 bit")

user = "edlab"
def _createDb(project):
    ex("mysqladmin --user=root drop %s"%project)
    ex("mysqladmin --user=root create %s"%project)
    ex("mysql -u root --execute \"GRANT ALL ON %s.* TO '%s'@'localhost';\""%(project, user))
    pass

def main():
    ex("sudo ln -s /usr/local/mysql/lib/libmysqlclient.18.dylib /usr/lib/libmysqlclient.18.dylib")
    ex("mysql -u root --execute \"create user '%s'@'localhost'\""%user)
    _createDb(nlt)
    _createDb(researchbroker)
    _createDb(surveysidekick)
    _createDb(vialogues)
    _createDb(cas)


if __name__ == '__main__':
    method = 'main'
    if len(sys.argv) > 1 :
        method = sys.argv[1]
        globals()[sys.argv[1]]()
    else:
        main()
