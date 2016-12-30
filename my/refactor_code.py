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
    call("ssh -o StrictHostKeyChecking=no {0} 'rm -rf ~/my;mkdir ~/my'".format(ip))
    call("scp {0} {1}:~/my/{2}".format(os.path.abspath(__file__), ip, os.path.basename(__file__)))


def prettify(cmd):
    return "{tame_color}[{host} {cwd}]$ {bold_color}{cmd}{end_color}".format(tame_color=bcolors.TAME,
                                                                             bold_color=bcolors.PRETTY,
                                                                             host=socket.gethostname(), cwd=os.getcwd(),
                                                                             cmd=cmd, end_color=bcolors.ENDC)


def execute_on_remote(ip, command):
    cc("ssh -o StrictHostKeyChecking=no %s 'python %s %s'" % (
        ip, "/home/sharath.g/my/" + os.path.basename(__file__), command))


def for_each():
    s = co("/home/sharath.g/bin/kloud-cli instance list -e ga --appId={} --json")
    s = json.loads(s)
    for obj in s:
        ip = obj['primary_ip']
        host = obj['hostname']
        type = obj['instance_type']


def cc(cmd):
    log.debug(prettify(cmd))
    subprocess.check_call(cmd, shell=True)


def co(cmd):
    log.debug(prettify(cmd))
    return subprocess.check_output(cmd, shell=True)


def call(cmd):
    log.debug(prettify(cmd))
    return subprocess.call(cmd, shell=True)


def refactor(params):
    str = ""
    with open (params[0], "r") as myfile:
        str=myfile.read()
    str = str.replace("subprocess.check_call", "cc").replace("subprocess.call", "call").replace("subprocess.check_output", "co").replace(", shell=True", "")
    log.debug(str)



if __name__ == '__main__':
    # setup logging to console with line number
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(logging.Formatter("%(message)s"))
    logging.getLogger('').addHandler(console)
    logging.getLogger('').setLevel(logging.DEBUG)
    log = logging.getLogger(__name__)

    method = 'main'
    if len(sys.argv) > 1:
        method = sys.argv[1]
        params = []
        if len(sys.argv) > 2:
            params = sys.argv[2:]
        globals()[sys.argv[1]](params)
    else:
        main()
