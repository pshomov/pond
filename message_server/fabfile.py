import sys
import os
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.contrib.files import contains,append
from fabric.operations import sudo
import fabutils

base_folder = os.path.normpath(os.path.abspath(os.path.dirname(__file__)))
rabbit_mq_version = "2.7.0"
def accounts():
    fabutils._create_account(user = "queue", passwd = "queue", public_key=base_folder+"/queue_id.pub")

def setup():
    if not contains("/etc/apt/sources.list", "rabbitmq"):
        append("/etc/apt/sources.list", "deb http://www.rabbitmq.com/debian/ testing main", use_sudo=True)
        run("wget http://www.rabbitmq.com/rabbitmq-signing-key-public.asc")
        sudo("apt-key add rabbitmq-signing-key-public.asc")

    sudo("apt-get update")
    sudo("apt-get -y install rabbitmq-server".format(rabbit_mq = rabbit_mq_version))
    # _install_management_console()

def _install_management_console():
    run("wget http://www.rabbitmq.com/releases/plugins/v{rabbit_mq}/mochiweb-1.3-rmq{rabbit_mq}-git9a53dbd.ez".format(rabbit_mq = rabbit_mq_version))
    run("wget http://www.rabbitmq.com/releases/plugins/v{rabbit_mq}/webmachine-1.7.0-rmq{rabbit_mq}-hg0c4b60a.ez".format(rabbit_mq = rabbit_mq_version))
    run("wget http://www.rabbitmq.com/releases/plugins/v{rabbit_mq}/amqp_client-{rabbit_mq}.ez".format(rabbit_mq = rabbit_mq_version))
    run("wget http://www.rabbitmq.com/releases/plugins/v{rabbit_mq}/rabbitmq_mochiweb-{rabbit_mq}.ez".format(rabbit_mq = rabbit_mq_version))
    run("wget http://www.rabbitmq.com/releases/plugins/v{rabbit_mq}/rabbitmq_management_agent-{rabbit_mq}.ez".format(rabbit_mq = rabbit_mq_version))
    run("wget http://www.rabbitmq.com/releases/plugins/v{rabbit_mq}/rabbitmq_management-{rabbit_mq}.ez".format(rabbit_mq = rabbit_mq_version))
    sudo("mv *.ez /usr/lib/rabbitmq/lib/rabbitmq_server-{rabbit_mq}/plugins/".format(rabbit_mq = rabbit_mq_version))
    sudo("/etc/init.d/rabbitmq-server restart")
        
def start_rabbitmq_server():
    sudo("/etc/init.d/rabbitmq-server start")