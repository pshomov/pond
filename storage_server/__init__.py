import os
from fabric.api import run, put
from fabric.operations import sudo
from fabric.state import env
import fabutils

RIAK_VERSION = "1.2.1-1"
RIAK_ARCH = "amd64"

def prepare():
    """ prepares the server for installing riak"""
    sudo("apt-get -y install wget libssl0.9.8 curl")

def accounts():
    base_folder = os.path.normpath(os.path.abspath(os.path.dirname(__file__)))
    fabutils._create_account(user = "store", passwd = "store", public_key=base_folder+"/store_id.pub")

def install_riak():
    """ installs riak storage server """
    riak_deb = "riak_%s_%s.deb" % (RIAK_VERSION, RIAK_ARCH)
    riak_url = "http://s3.amazonaws.com/downloads.basho.com/riak/1.2/1.2.1/ubuntu/natty/riak_1.2.1-1_amd64.deb"
    run("wget %s" % riak_url)
    sudo("dpkg -i %s" % riak_deb)

    put(os.path.join(__path__[0], "conf", "app.config"), "/etc/riak/", use_sudo=True)
    put(os.path.join(__path__[0], "conf", "vm.args"), "/etc/riak", use_sudo=True)
    put(os.path.join(__path__[0], "conf", "cert.pem"), "/etc/riak", use_sudo=True)
    put(os.path.join(__path__[0], "conf", "key.pem"), "/etc/riak", use_sudo=True)

    sudo("update-rc.d riak defaults")
    start_riak()
    sudo("curl -s rekon.basho.com | sh")
    shutdown_riak()

def start_riak():
    env.warn_only = True
    sudo("/etc/init.d/riak start")
    env.warn_only = False

def shutdown_riak():
    sudo("/etc/init.d/riak stop")

def remove_the_ring_file_since_it_is_tight_to_the_IP_address():
    sudo("sudo rm /var/lib/riak/ring/*")


