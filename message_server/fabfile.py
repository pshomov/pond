import os
from fabric.api import *
from fabric.contrib.files import contains, append
from fabric.operations import sudo
import fabutils

base_folder = os.path.normpath(os.path.abspath(os.path.dirname(__file__)))
rabbit_mq_version = "3.0.1"

def accounts():
    fabutils._create_account(user="queue", passwd="queue", public_key=base_folder + "/queue_id.pub")


def setup():
    if not contains("/etc/apt/sources.list", "rabbitmq"):
        append("/etc/apt/sources.list", "deb http://www.rabbitmq.com/debian/ testing main", use_sudo=True)
        run("wget http://www.rabbitmq.com/rabbitmq-signing-key-public.asc")
        sudo("apt-key add rabbitmq-signing-key-public.asc")

    sudo("apt-get update")
    sudo("apt-get -y install rabbitmq-server".format(rabbit_mq=rabbit_mq_version))
    sudo("rabbitmq-plugins enable rabbitmq_management")
    sudo("/etc/init.d/rabbitmq-server restart")


def start_rabbitmq_server():
    sudo("/etc/init.d/rabbitmq-server start")
