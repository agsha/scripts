'''
Created on Jun 17, 2012

@author: sharath
'''

from Test import exec_command as ex
import re

import sys
from constants import surveysidekick, researchbroker, vialogues, nlt, cas, user

def is64Bit():
    out = ex("uname -a")[0]
    for line in out:
        if re.match(".*RELEASE_X86_64 x86_64$", line) is not None:
            return True
        elif re.match(".*RELEASE_I386 i386$", line) is not None:
            return False
        else:
            raise Exception("Cant detect if cpu is 32 bit or 64 bit")

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
