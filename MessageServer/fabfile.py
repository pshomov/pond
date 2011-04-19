import sys
import os

base_folder = os.path.normpath(os.path.abspath(os.path.dirname(__file__))+'/..')
sys.path[0:0] = [base_folder]

from fabric.api import *
from fabric.contrib.console import confirm
from fabric.contrib.files import contains,append
from fabenv import env
from fabric.operations import sudo

def accounts():
    sudo("apt-get -y install makepasswd")
    passwd = run("echo queue | makepasswd --clearfrom=- --crypt-md5 |awk '{ print $2 }'")
    env.warn_only = True
    sudo("userdel -f -r queue", )
    env.warn_only = False
    sudo("useradd -d /home/queue -m queue -p '"+passwd+"' -r -G ssh,sudo -s /bin/bash")
    sudo("mkdir -p /home/queue/.ssh")
    put("queue_id.pub", "/home/queue/.ssh/authorized_keys", use_sudo=True)
    env.user = "queue"

def setup():
    if not contains("/etc/apt/sources.list", "rabbitmq"):
        append("/etc/apt/sources.list", "deb http://www.rabbitmq.com/debian/ testing main", use_sudo=True)
        run("wget http://www.rabbitmq.com/rabbitmq-signing-key-public.asc")
        sudo("apt-key add rabbitmq-signing-key-public.asc")
        
    sudo("apt-get update")
    sudo("apt-get -y install rabbitmq-server")
    _install_management_console()

def _install_management_console():
    run("wget http://www.rabbitmq.com/releases/plugins/v2.4.1/mochiweb-2.4.1.ez")
    run("wget http://www.rabbitmq.com/releases/plugins/v2.4.1/webmachine-2.4.1.ez")
    run("wget http://www.rabbitmq.com/releases/plugins/v2.4.1/amqp_client-2.4.1.ez")
    run("wget http://www.rabbitmq.com/releases/plugins/v2.4.1/rabbitmq-mochiweb-2.4.1.ez")
    run("wget http://www.rabbitmq.com/releases/plugins/v2.4.1/rabbitmq-management-agent-2.4.1.ez")
    run("wget http://www.rabbitmq.com/releases/plugins/v2.4.1/rabbitmq-management-2.4.1.ez")
    sudo("mv *.ez /usr/lib/rabbitmq/lib/rabbitmq_server-2.4.1/plugins/")
    sudo("/etc/init.d/rabbitmq-server restart")
        
    