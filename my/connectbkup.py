import json
import sys
import os
import subprocess
from os import path
import logging

__author__ = 'sharath.g'

def check():
    f = open("/Users/sharath.g/bkupmachines")
    for ip in f:
        ip = ip[:-1]
        s = "ssh -o StrictHostKeyChecking=no {0} 'echo {0}'".format(ip)
        print s
        try:
            subprocess.check_call(s, shell=True)
        except  Exception:
            print "failed: {0}".format(ip)


def check2():
    data = json.load(open("/Users/sharath.g/bkupjson"))
    for d in data:
        if 'rgw' not in d['hostname']:
            continue
        s = "ssh -o StrictHostKeyChecking=no {0} 'echo {0};sudo tail -100 /var/log/radosgw/radosgw-{1}.log'".format(d['primary_ip'], d['hostname'])
        subprocess.check_call(s, shell=True)


def main2(project):
    devnull = open(os.devnull, 'w')

    project = os.path.abspath(path.expanduser(project))
    os.chdir(project)
    validRepos = ['d42-ansible', 'd42-setup', 'd42-locust']
    repo = os.path.basename(project)

    if repo not in validRepos or not path.exists(path.join(project, '.git')):
        log.error('Invalid path:{0}; Path should point to one of the d42 repos:{0}', project, validRepos)
        return

    out1 = subprocess.check_output("git remote -v", shell=True)
    out2 = subprocess.check_output("git branch", shell=True)
    if 'git@github.com:Flipkart/{0}.git' % repo in out1 and 'corpMaster' in out2:
        log.debug("All good, nothing modified.")
        return

    # delete existing remotes and add correct remotes
    subprocess.call("git remote rm origin", shell=True, stderr=devnull)
    subprocess.call("git remote rm corp", shell=True, stderr=devnull)
    subprocess.check_call("git remote add origin git@github.com:Flipkart/{0}" % repo, shell=True)
    subprocess.check_call("git remote add corp git.corp.flipkart.com:/git/d42/{0}" % repo, shell=True)

    # fetch remotes
    subprocess.check_call("git fetch origin", shell=True)
    subprocess.check_call("git fetch corp", shell=True)

    # rename master to corpMaster
    subprocess.check_call("git branch -m master corpMaster", shell=True)

    # make corpMaster track corp/master
    subprocess.check_call("git branch --set-upstream-to=corp/master corpMaster", shell=True)

    # create master branch to track github master
    subprocess.check_call("git checkout -b master origin/master", shell=True)

    # merge any existing commits to github master
    subprocess.check_call("git merge corpMaster", shell=True)

    log.debug("Success!")


def main(ip):
    log.debug(ip)
    proj = os.path.abspath(os.path.dirname(__file__))

    subprocess.call("ssh {0} 'rm -rf ~/my'".format(ip), shell=True)
    subprocess.call("ssh {0} 'mkdir ~/my'".format(ip), shell=True)
    subprocess.call("ssh {0} 'mkdir ~/.vim'".format(ip), shell=True)

    # copy this file to remote machine ;)
    copy_to_remote(ip)
    subprocess.check_call("scp " + os.path.join(proj, "profile") + " {0}:~/my".format(ip), shell=True)
    subprocess.call("scp " + os.path.join(proj, "vimrc") + " {0}:~/.vimrc".format(ip), shell=True)
    subprocess.call("scp " + os.path.join(proj, "tmux.conf") + " {0}:~/.tmux.conf".format(ip), shell=True)
    subprocess.call("scp " + os.path.join(proj, "bash_profile") + " {0}:~/.bash_profile".format(ip), shell=True)
    subprocess.call("scp -r " + os.path.join(proj, "vim/*") + " {0}:~/.vim".format(ip), shell=True)


    #
    # subprocess.check_call("rm -rf ~/.vim", shell=True)
    # subprocess.check_call("rm -rf ~/.vimrc", shell=True)
    # subprocess.check_call("rm -rf ~/.vim", shell=True)
    # subprocess.check_call("rm -rf ~/.vim", shell=True)


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
    #main(sys.argv[1])
    check2()
    # if len(sys.argv) > 1:
    #     method = sys.argv[1]
    #     globals()[sys.argv[1]]()
    # else:
    #     main('sdf')
