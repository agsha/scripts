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
LIBEVENT_URL = "https://github.com/downloads/libevent/libevent/libevent-2.0.20-stable.tar.gz"
MEMCACHED_URL = "http://memcached.googlecode.com/files/memcached-1.4.15.tar.gz"

def downloadLibevent():
    chdir(DOWNLOAD_DIR)
    exec_command("curl -o libevent-2.0.20-stable.tar.gz -L %s"%LIBEVENT_URL)

def extractLibevent():
    chdir(DOWNLOAD_DIR)
    exec_command("tar xvzf libevent-2.0.20-stable.tar.gz -C %s"%DOWNLOAD_DIR)
    chdir(join(DOWNLOAD_DIR,"libevent-2.0.20-stable"))
    exec_command(join(DOWNLOAD_DIR, "libevent-2.0.20-stable", "configure"))
    exec_command("make")
    exec_command("sudo make install")
    exec_command(" sudo ln -s /usr/local/lib/libevent-2.0.5.dylib /usr/lib")



def downloadMemcached():
    chdir(DOWNLOAD_DIR)
    exec_command("curl -o memcached-1.4.15.tar.gz -L %s"%MEMCACHED_URL)

def extractMemcached():
    chdir(DOWNLOAD_DIR)
    exec_command("tar xvzf memcached-1.4.15.tar.gz -C %s"%DOWNLOAD_DIR)
    chdir(join(DOWNLOAD_DIR,"memcached-1.4.15"))
    exec_command(join(DOWNLOAD_DIR, "memcached-1.4.15", "configure"))
    exec_command("make")
    exec_command("sudo make install")


def main():
    downloadLibevent()
    extractLibevent()
    downloadMemcached()
    extractMemcached()


if __name__ == '__main__':
    method = 'main'
    if len(sys.argv) > 1 :
        method = sys.argv[1]
        globals()[sys.argv[1]]()
    else:
        main()
