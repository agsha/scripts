#specific imports
import inspect
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
    call("ssh -o StrictHostKeyChecking=no sharath.g@{ip} 'rm  /tmp/{f}'".format(ip=ip, f=os.path.basename(__file__)))
    call("scp {0} sharath.g@{1}:/tmp".format(os.path.abspath(__file__), ip))


def prettify(cmd, line=-1):
    return "{tame_color}[{host} {cwd}:{line}]$ {bold_color}{cmd}{end_color}".format(tame_color=bcolors.TAME,
                                                                             bold_color=bcolors.PRETTY,
                                                                             host=socket.gethostname(),
                                                                                     cwd=os.getcwd(),
                                                                                     line=line,
                                                                             cmd=cmd, end_color=bcolors.ENDC)


def execute_on_remote(ip, command):
    cc("ssh -o StrictHostKeyChecking=no sharath.g@%s 'python %s %s'" % (
        ip, "/tmp/" + os.path.basename(__file__), command))


def for_each(appId):
    s = co("/home/sharath.g/bin/kloud-cli instance list -e 10.33.65.0 --appId={appId} --json".format(appId=appId))
    s = json.loads(s)
    for obj in s:
        ip = obj['primary_ip']
        host = obj['hostname']
        type = obj['instance_type']
        try:
            copy_to_remote(ip)
            execute_on_remote(ip, "echo")
        except:
            log.debug("failed for {ip}".format(ip=ip))

def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno

def lineno2():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_back.f_lineno

def echo(params):
    log.debug("hihihihi")


def cc(cmd):
    log.debug(prettify(cmd, lineno2()))
    subprocess.check_call(cmd, shell=True)


def co(cmd):
    log.debug(prettify(cmd, lineno2()))
    stdout = subprocess.check_output(cmd, shell=True)
    log.debug(stdout)
    return stdout

def call(cmd):
    log.debug(prettify(cmd, lineno2()))
    return subprocess.call(cmd, shell=True)

home = os.path.abspath(os.path.expanduser("~"))
scripts = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def setup_for_ip(ip):

    cc("ssh -o StrictHostKeyChecking=no sharath.g@{0} 'rm -rf ~/scripts;mkdir -p ~/scripts/my'".format(ip))
    cc("scp -r {src1} {src2} sharath.g@{ip}:{tgt}".format(src1=os.path.join(scripts, "my/.vim"), src2=os.path.join(scripts, "my/linux_setup"), ip=ip, tgt="~/scripts/my"))

    copy_to_remote(ip)
    execute_on_remote(ip, "setup_localhost")



def setup_localhost(params=[]):
    cc("rm -rf ~/.bash_profile ~/.xinitrc ~/.xmodmaprc ~/.tmux.conf ")
    cc("ln -s {src} {tgt}".format(src=os.path.join(scripts, "my/linux_setup/linux_profile"), tgt=os.path.join(home, ".bash_profile")))
    cc("ln -s {src} {tgt}".format(src=os.path.join(scripts, "my/linux_setup/.xinitrc"), tgt=os.path.join(home, ".xinitrc")))
    cc("ln -s {src} {tgt}".format(src=os.path.join(scripts, "my/linux_setup/.xmodmaprc"), tgt=os.path.join(home, ".xmodmaprc")))
    cc("ln -s {src} {tgt}".format(src=os.path.join(scripts, "my/linux_setup/tmux.conf"), tgt=os.path.join(home, ".tmux.conf")))

    cc("rm -rf ~/.vim")
    cc("rm -rf ~/.vimrc")
    cc("ln -s {src} {tgt}".format(src=os.path.join(scripts, "my/.vim"), tgt=os.path.join(home, ".vim")))
    vimrc = """
source {scripts}/my/.vim/common_vimrc
source {scripts}/my/.vim/vimrc-pathogen
source {scripts}/my/.vim/vimrc-ctrlp
    """.format(scripts=scripts)
    with open(os.path.expanduser("~/.vimrc"), "w") as f:
        f.write(vimrc)
    cc("mkdir -p ~/.vim/undodir")



def remote_install_java():
    cc("sudo apt-get update")
    cc("sudo apt-get update")
    cc("sudo apt-get -y install oracle-j2sdk1.7")



def main(params):
    pass

if __name__ == '__main__':
    # setup logging to console with line number
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(logging.Formatter("line:%(lineno)d - %(message)s"))
    logging.getLogger('').addHandler(console)
    logging.getLogger('').setLevel(logging.DEBUG)
    log = logging.getLogger(__name__)

    thisos = "linux" if "Linux" in co("uname -a") else "mac"
    profile = "linux_profile" if os == "linux" else "mac-profile"
    method = 'main'
    if len(sys.argv) > 1:
        method = sys.argv[1]
        params = []
        if len(sys.argv) > 2:
            params = sys.argv[2:]
        globals()[sys.argv[1]](params)
    else:
        main(sys.argv[1:])
        setup_for_ip()
