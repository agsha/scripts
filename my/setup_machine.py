import json
import sys
import os
import subprocess
from os import path
import logging

__author__ = 'sharath.g'


def main():
    s = subprocess.check_output("ssh -o StrictHostKeyChecking=no iaas-infra-0001.nm.flipkart.com 'kloud-cli instance list -e ga --appId=dev-d42sharath --json'", shell=True)
    s = json.loads(s)
    ok = False
    for obj in s:
        if 'osd' not in obj['hostname']:
            continue
        ip = obj['primary_ip']
        host = obj['hostname']
        setup_for_ip(ip)

def setup_for_ip(ip):
    log.debug(ip)
    proj = os.path.abspath(os.path.dirname(__file__))

    subprocess.call("ssh -o StrictHostKeyChecking=no {0} 'rm -rf ~/my'".format(ip), shell=True)
    subprocess.call("ssh -o StrictHostKeyChecking=no {0} 'mkdir ~/my'".format(ip), shell=True)
    subprocess.call("ssh -o StrictHostKeyChecking=no {0} 'mkdir ~/.vim'".format(ip), shell=True)

    # copy this file to remote machine ;)
    copy_to_remote(ip)
    subprocess.check_call("scp " + os.path.join(proj, "profile") + " {0}:~/my".format(ip), shell=True)
    subprocess.call("scp " + os.path.join(proj, "vimrc") + " {0}:~/.vimrc".format(ip), shell=True)
    subprocess.call("scp " + os.path.join(proj, "tmux.conf") + " {0}:~/.tmux.conf".format(ip), shell=True)
    subprocess.call("scp " + os.path.join(proj, "bash_profile") + " {0}:~/.bash_profile".format(ip), shell=True)
    subprocess.call("scp -r " + os.path.join(proj, "vim/*") + " {0}:~/.vim".format(ip), shell=True)

def copy_to_remote(ip):
    subprocess.check_call("scp " + __file__ + " {0}:~/my".format(ip), shell=True)


def remote_install_java():
    subprocess.check_call("echo 'deb http://10.47.2.22:80/repos/oracle-java/4 /' | sudo tee /etc/apt/mysources.list.d",
                          shell=True)
    subprocess.check_call("sudo apt-get update", shell=True)
    subprocess.check_call("sudo apt-get update", shell=True)
    subprocess.check_call("sudo apt-get -y install oracle-j2sdk1.7", shell=True)


def remote_setup():
    remote_create_bash_profile()


def remote_create_bash_profile():
    f = open("~/.bash_profile", "w")
    f.write("source ~/my/profile\n")
    f.close()


if __name__ == '__main__':
    # setup logging to console with line number
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(logging.Formatter("line:%(lineno)d - %(message)s"))
    logging.getLogger('').addHandler(console)
    logging.getLogger('').setLevel(logging.DEBUG)
    log = logging.getLogger(__name__)

    method = 'main'
    setup_for_ip('10.33.126.1')
    # if len(sys.argv) > 1:
    #     method = sys.argv[1]
    #     globals()[sys.argv[1]]()
    # else:
    #     main('sdf')
