import inspect
import json
import logging
import os
import re
import sys
import subprocess
import threading
import socket
from multiprocessing import Process, Queue

# import requests
# setup logging to console with line number
from time import sleep

console = logging.StreamHandler(sys.stdout)
console.setFormatter(logging.Formatter("%(message)s"))
logging.getLogger('').addHandler(console)
logging.getLogger('').setLevel(logging.DEBUG)
log = logging.getLogger(__name__)

this_host = socket.gethostname()
try:
    this_ip = socket.gethostbyname(this_host)
except:
    pass
this_file = os.path.abspath(__file__)
this_file_name = os.path.basename(__file__)
home = os.path.abspath(os.path.expanduser("~"))

__author__ = 'sharath'


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


def l(*args):
    log.debug(*args)


def sf(string, *args, **kwargs):
    return string.format(*args, **kwargs)


def copy_to_remote(ip):
    call("ssh -o StrictHostKeyChecking=no {ip} 'rm  /tmp/{f}'".format(ip=ip, f=os.path.basename(__file__)))
    call("scp {0} {1}:/tmp".format(os.path.abspath(__file__), ip))


def prettify(cmd, line=-1, plain_text=False):
    if not plain_text:
        return "{tame_color}[{host} {cwd}:{line}]$ {bold_color}{cmd}{end_color}".format(tame_color=bcolors.TAME,
                                                                                        bold_color=bcolors.PRETTY,
                                                                                        host=socket.gethostname(),
                                                                                        cwd=os.getcwd(),
                                                                                        line=line,
                                                                                        cmd=cmd, end_color=bcolors.ENDC)
    return "[{host} {cwd}:{line}]$ {cmd}".format(
        host=socket.gethostname(),
        cwd=os.getcwd(),
        line=line,
        cmd=cmd)


def execute_on_remote(ip, command, sudo=False):
    sudo_str = "sudo" if sudo else ""
    cc("ssh -o StrictHostKeyChecking=no %s '%s python3 %s %s'" % (
        ip, sudo_str, "/tmp/" + os.path.basename(__file__), command), rewind=1)



def lineno1():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno


def lineno2():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_back.f_lineno


def lineno3():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_back.f_back.f_lineno


# debug_level:
# 0 : log nothing
# 1: only log command
# 2: log both command and output
def cc(cmd, log_cmd=True, log_op=True, debug_dest=sys.stdout, rewind=0):
    rewind += 2
    if debug_dest == sys.stdout:
        if log_cmd:
            log.debug(prettify(cmd, globals()["lineno" + str(rewind)]()
                               ))
        if log_op:
            subprocess.check_call(cmd, shell=True)
        else:
            with open(os.devnull, "w") as f:
                subprocess.check_call(cmd, shell=True, stdout=f)

    else:
        with open(debug_dest, 'w') as f:
            with open(os.devnull, "w") as devnull:
                if log_cmd:
                    f.write(prettify(cmd, globals()["lineno" + str(rewind)](),
                                     plain_text=True))
                if log_op:
                    subprocess.check_call(cmd, shell=True, stdout=f)
                else:
                    subprocess.check_call(cmd, shell=True, stdout=devnull)


# debug_level:
# 0 : log nothing
# 1: only log command
# 2: log both command and output
def co(cmd, log_cmd=False, log_op=False, debug_dest=sys.stdout, rewind=0):
    rewind += 2
    if debug_dest == sys.stdout:
        output = subprocess.check_output(cmd, shell=True)
        cmd_str_log = prettify(cmd, globals()["lineno" + str(rewind)]()) if log_cmd else ""
        output_log = output if log_op else ""
        final_output = cmd_str_log + "\n" + output_log
        if final_output != "\n":
            log.debug(final_output)
    else:
        with open(debug_dest, 'w') as f:
            output = subprocess.check_output(cmd, shell=True)
            cmd_str_log = prettify(cmd, globals()["lineno" + str(rewind)](),
                                   plain_text=True) if log_cmd else ""
            output_log = output if log_op else ""
            final_output = cmd_str_log + "\n" + output_log
            if final_output != "\n":
                f.write(final_output)
    return output


def call(cmd):
    log.debug(prettify(cmd, lineno2()))
    return subprocess.call(cmd, shell=True)


this_os = 'Darwin'
try:
    if 'Linux' in co("uname"):
        this_os = 'Linux'
except:
    pass


###### Multicast copy: copy from single machine to many machines
def to_host_task(ip, src, dst, sudo=False, debug=False):
    sudo_str = "--rsync-path='sudo rsync'" if sudo else ""
    cc("""rsync -zaP -e 'ssh -o StrictHostKeyChecking=no' {sudo_str} {src} {ip}:{dst}""".format(sudo_str=sudo_str,
                                                                                                ip=ip, src=src,
                                                                                                dst=dst, ),
       log_cmd=debug, log_op=debug)


def to_hosts(ips, src, dst, sudo=False, debug=False):
    threads = []
    for ip in ips:
        t1 = Process(target=to_host_task, args=(ip, src, dst, sudo, debug))
        t1.start()
        threads.append(t1)
    for t in threads:
        t.join()


def multicast_copy_anywhere(ips, src, dst, sudo=False, debug=False):
    # if only one ip, then convert it into a list of one element
    if isinstance(ips, str):
        ips = ips.split()

    # if only one host or already in dc then just copy to there and be done.
    if len(ips) == 1 or this_os == 'Linux':
        to_hosts(ips, src, dst, sudo, debug)
        return

    # for multiple hosts from outside dc
    # first copy to jumphost
    to_host_task(ips[0], src, dst, sudo, debug)

    # copy this file over also. (if not already done so in previous step)
    if this_file != src:
        to_host_task(ips[0], this_file, "/tmp/{}".format(this_file_name))

    # from there, copy everywhere else
    cc(
        "ssh -o StrictHostKeyChecking=no {jumphost} 'python3 /tmp/{this_file_name} multicast_copy_anywhere_wrapper \"{ips}\" {src} {dst} {sudo} {debug}'".format(
            jumphost=ips[0], this_file_name=this_file_name, ips=' '.join(ips[1:]), src=dst, dst=dst, sudo=sudo,
            debug=debug), log_cmd=debug, log_op=debug)


def multicast_copy_anywhere_wrapper(params):
    sudo = True if len(params) > 3 and params[3].lower() == "true" else False
    debug = True if len(params) > 4 and params[4].lower() == "true" else False
    multicast_copy_anywhere(params[0].split(), params[1], params[2], sudo=sudo, debug=debug)


##### Multicast run ###############


# assuming this file is already there in all ips in the given path
def multicast_run_task(ip, command, ret_q=None, sudo=False, debug=False):
    try:
        sudo_str = "sudo" if sudo else ""
        cmd = "ssh -o StrictHostKeyChecking=no {ip} '{sudo} python3 /tmp/{this_file_name} {command}'".format(ip=ip,
                                                                                                            sudo=sudo_str,
                                                                                                            this_file_name=this_file_name,
                                                                                                            command=command)
        ret_q.put(co(cmd, log_cmd=debug, log_op=False))
    except:
        ret_q.put("ERROR")
        log.exception("error")


def multicast_run(ips, command, sudo=False, debug=False):
    threads = []
    ret_q = Queue()
    for ip in ips:
        t1 = Process(target=multicast_run_task, args=(ip, command, ret_q, sudo, debug))
        t1.start()
        threads.append(t1)
    for i in range(len(ips)):
        item = ret_q.get()
        log.debug(item)
    for t in threads:
        t.join()


# fun is the actual function object and args is a string args
def multicast_run_anywhere(ips, command, sudo=False, debug=False):
    # if only one ip, then convert it into a list of one element
    if isinstance(ips, str):
        ips = [ips]
    # if only one host or already in dc then just run there
    if len(ips) == 1 or this_os == 'Linux':
        multicast_run(ips, command, sudo, debug)
        return

    # for multiple hosts from outside dc, run via jumphost
    cmd = "ssh -o StrictHostKeyChecking=no {jumphost} 'python3 /tmp/{this_file_name} multicast_run_anywhere_wrapper \"{ips}\" {command} {sudo} {debug}'" \
        .format(jumphost=ips[0], this_file_name=this_file_name, ips=' '.join(ips), command=command, sudo=sudo, debug=debug)

    cc(cmd, log_cmd=debug, log_op=True)


def multicast_run_anywhere_wrapper(params):
    sudo = True if len(params) > 2 and params[2].lower() == "true" else False
    debug = True if len(params) > 3 and params[3].lower() == "true" else False
    multicast_run_anywhere(params[0].split(), params[1], sudo=sudo, debug=debug)

def copy_this(ips, debug=False):
    if isinstance(ips, str):
        ips = [ips]
    multicast_copy_anywhere(ips, this_file, "/tmp/{}".format(this_file_name), debug=debug)


scripts = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def clean():
    cc("rm -rf ~/scripts ~/my ~/.ssh/config")
    cc("mkdir -p ~/scripts/my")

def setup_localhost(params=[]):
    remote_scripts = "/home/sharath/scripts"

    cc("rm -rf ~/.bash_profile ~/.xinitrc ~/.xmodmaprc ~/.tmux.conf ")
    cc("ln -s {src} {tgt}".format(src=os.path.join(remote_scripts, "my/linux_setup/linux_profile"), tgt=os.path.join(home, ".bash_profile")))
    cc("ln -s {src} {tgt}".format(src=os.path.join(remote_scripts, "my/linux_setup/.xinitrc"), tgt=os.path.join(home, ".xinitrc")))
    cc("ln -s {src} {tgt}".format(src=os.path.join(remote_scripts, "my/linux_setup/.xmodmaprc"), tgt=os.path.join(home, ".xmodmaprc")))
    cc("ln -s {src} {tgt}".format(src=os.path.join(remote_scripts, "my/linux_setup/tmux.conf"), tgt=os.path.join(home, ".tmux.conf")))

    cc("rm -rf ~/.vim")
    cc("rm -rf ~/.vimrc")
    cc("ln -s {src} {tgt}".format(src=os.path.join(remote_scripts, "my/.vim"), tgt=os.path.join(home, ".vim")))
    vimrc = """
source {remote_scripts}/my/.vim/common_vimrc
source {remote_scripts}/my/.vim/vimrc-pathogen
source {remote_scripts}/my/.vim/vimrc-ctrlp
source {remote_scripts}/my/.vim/cscope_maps.vim
    """.format(remote_scripts=remote_scripts)
    with open(os.path.expanduser("~/.vimrc"), "w") as f:
        f.write(vimrc)
    call("mkdir -p ~/.vim_undodir")
    call("mkdir -p ~/.ssh/sockets")
    cc("ln -s {src} {tgt}".format(src=os.path.join(scripts, "my/linux_setup/ssh_config"), tgt=os.path.join(home, ".ssh/config")))




class myThread (threading.Thread):
    def __init__(self, ip):
        threading.Thread.__init__(self)
        self.ip = ip
    def run(self):
        cc(sf("ssh -o StrictHostKeyChecking=no {ip} 'sudo apt-get install --yes --allow-unauthenticated rsync'".format(ip=self.ip)))


def install_rsync1(ips):
    lt = []
    for ip in ips:
        t = myThread(ip)
        t.start()
        lt.append(t)
    for t in lt:
        t.join()

def install_rsync(ips):
    copy_to_remote(ips[0])
    execute_on_remote(ips[0], sf("install_rsync1 {}", " ".join(ips)))


class goodChecker(threading.Thread):
    def __init__(self, ip):
        threading.Thread.__init__(self)
        self.ip = ip
        self.good = False
    def run(self):
        try:
            cc(sf("ssh -o StrictHostKeyChecking=no {ip} 'echo hi'", ip=self.ip))
            self.good = True
        except:
            pass


def check_ip(ips):
    lt = []
    for ip in ips:
        t = goodChecker(ip)
        t.start()
        lt.append(t)
    good = []
    bad = []
    sleep(5)
    for t in lt:
        t.join()
        if t.good:
            good.append(t.ip)
        else:
            bad.append(t.ip)

    print ("good")
    print (" ".join(good))

    print ("bad")
    print (" ".join(bad))

def split(s, delim="\n"):
    return filter(None, [x.strip() for x in re.split(delim, s.strip())])


def main(params):
    # setup_for_app_id("pre-prod-fdphadoop")
    # setup_localhost()
    # return
    if params:
        ips = params
    else:
        ip = ['10.33.0.95']
    ips = ['174.138.121.200', '192.168.29.27', '192.168.29.38']
    ips = ['10.33.0.29']
    # ips = co("pre-prod-fdphadoop").split()
    # ips = [s['primary_ip'] for s in instance_list("prod-fdg-dart-mirror2-kafka") ]
    # ips = [s['primary_ip'] for s in instance_list("prod-specter-mirror-maker")]
    # print " ".join(ips)
    # check_ip(ips)
    # print len(ips)
    # return


    install_rsync(ips)
    copy_this(ips)
    multicast_run_anywhere(ips, "clean")
    multicast_copy_anywhere(ips, os.path.join(scripts, "my/.vim/"), "/home/sharath/scripts/my/.vim/")
    multicast_copy_anywhere(ips, os.path.join(scripts, "my/linux_setup/"), "/home/sharath/scripts/my/linux_setup/")
    multicast_run_anywhere(ips, "setup_localhost")

if __name__ == '__main__':
    """
    python __file__ executes main([])
    python __file__ func executes func()
    python __file__ func param1 param2 executes func([param1, param2])
    """
    method = 'main'
    num_args = len(sys.argv)
    if num_args == 1 or sys.argv[1] not in globals():
        main(sys.argv[1:])
    elif num_args == 2:
        globals()[sys.argv[1]]()
    else:
        globals()[sys.argv[1]](sys.argv[2:])
