import sys
import os
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.contrib.files import contains,append
from fabenv import env
from fabric.operations import sudo
import fabutils

base_folder = os.path.normpath(os.path.abspath(os.path.dirname(__file__)))

def accounts():
    fabutils._create_account(user = "queue", passwd = "queue", public_key=base_folder+"/queue_id.pub")

def setup():
    if not contains("/etc/apt/sources.list", "rabbitmq"):
        append("/etc/apt/sources.list", "deb http://www.rabbitmq.com/debian/ testing main", use_sudo=True)
        run("wget http://www.rabbitmq.com/rabbitmq-signing-key-public.asc")
        sudo("apt-key add rabbitmq-signing-key-public.asc")
        
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
        
    