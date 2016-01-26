import json
import logging
import os
import sys
import subprocess
import socket

__author__ = 'sharath.g'


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    PRETTY = '\033[1;36m'
    FAIL = '\033[91m'
    TAME = '\033[0;36m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def copy_to_remote(ip):
    call("ssh -o StrictHostKeyChecking=no {ip} 'rm  /tmp/{f}'".format(ip=ip, f=os.path.basename(__file__)))
    call("scp {0} {1}:/tmp".format(os.path.abspath(__file__), ip))


def prettify(cmd):
    return "{tame_color}[{host} {cwd}]$ {bold_color}{cmd}{end_color}".format(tame_color=bcolors.TAME,
                                                                             bold_color=bcolors.PRETTY,
                                                                             host=socket.gethostname(), cwd=os.getcwd(),
                                                                             cmd=cmd, end_color=bcolors.ENDC)


def execute_on_remote(ip, command):
    cc("ssh -o StrictHostKeyChecking=no %s 'python %s %s'" % (
        ip, "/tmp/" + os.path.basename(__file__), command))


def for_each(appId):
    s = co("/home/sharath.g/bin/kloud-cli instance list -e 10.33.65.0 --appId={appId} --json".format(appId=appId))
    s = json.loads(s)
    for obj in s:
        ip = obj['primary_ip']
        host = obj['hostname']
        type = obj['instance_type']
        setup_for_ip(ip)

def echo(params):
    log.debug("hihihihi")


def cc(cmd):
    log.debug(prettify(cmd))
    subprocess.check_call(cmd, shell=True)


def co(cmd):
    log.debug(prettify(cmd))
    return subprocess.check_output(cmd, shell=True)


def call(cmd):
    log.debug(prettify(cmd))
    return subprocess.call(cmd, shell=True)

def setup_for_ip(ip):
    log.debug(ip)
    proj = os.path.abspath(os.path.dirname(__file__))

    call("ssh -o StrictHostKeyChecking=no {0} 'rm -rf ~/my'".format(ip))
    log.debug("a")
    call("ssh -o StrictHostKeyChecking=no {0} 'mkdir ~/my'".format(ip))
    log.debug("b")

    call("ssh -o StrictHostKeyChecking=no {0} 'mkdir ~/.vim'".format(ip))
    log.debug("c")

    # copy this file to remote machine ;)
    cc("scp " + os.path.join(proj, profile) + " {0}:~/my".format(ip))
    log.debug("d")

    call("scp " + os.path.join(proj, "vimrc") + " {0}:~/.vimrc".format(ip))
    log.debug("e")
    call("scp " + os.path.join(proj, "tmux.conf") + " {0}:~/.tmux.conf".format(ip))
    log.debug("f")
    call("scp " + os.path.join(proj, "bash_profile") + " {0}:~/.bash_profile".format(ip))
    log.debug("g")
    call("scp -r " + os.path.join(proj, "vim/*") + " {0}:~/.vim".format(ip))
    log.debug("h")



def remote_install_java():
    cc("echo 'deb http://10.47.2.22:80/repos/oracle-java/4 /' | sudo tee /etc/apt/mysources.list.d")
    cc("sudo apt-get update")
    cc("sudo apt-get update")
    cc("sudo apt-get -y install oracle-j2sdk1.7")


def remote_setup():
    remote_create_bash_profile()


def remote_create_bash_profile():
    f = open("~/.bash_profile", "w")
    f.write("source ~/my/profile\n")
    f.close()

def main(params):
    for_each("dev-d42sharath1")


if __name__ == '__main__':
    # setup logging to console with line number
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(logging.Formatter("line:%(lineno)d - %(message)s"))
    logging.getLogger('').addHandler(console)
    logging.getLogger('').setLevel(logging.DEBUG)
    log = logging.getLogger(__name__)

    os = "linux" if "Linux" in co("uname -a") else "mac"
    profile = "linux_profile" if os == "linux" else "mac-profile
    method = 'main'
    if len(sys.argv) > 1:
        method = sys.argv[1]
        params = []
        if len(sys.argv) > 2:
            params = sys.argv[2:]
        globals()[sys.argv[1]](params)
    else:
        main(sys.argv[1:])
