from fabric.api import *
from fabric.contrib.console import confirm
from fabric.contrib.files import contains,append
from fabenv import env
from fabric.operations import sudo

def _create_account(user, passwd, public_key=None):
    sudo("apt-get -y install makepasswd")
    passwd = run("echo %s | makepasswd --clearfrom=- --crypt-md5 |awk '{ print $2 }'" % passwd)
    env.warn_only = True
    sudo("userdel -f -r %s" % user)
    env.warn_only = False
    sudo("useradd -d /home/%(user)s -m %(user)s -p '%(passwd)s' -r -G ssh,sudo -s /bin/bash" % {"user" : user, "passwd" : passwd})
    if public_key is not None:
        sudo("mkdir -p /home/%s/.ssh" % user)
        put(public_key, "/home/%s/.ssh/authorized_keys" % user, use_sudo=True)
