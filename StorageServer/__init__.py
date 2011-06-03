import os
from fabric.api import run, put
from fabric.operations import sudo
import fabutils

RIAK_VERSION = "0.14.1-1"
RIAK_ARCH = "amd64"

def prepare():
    """ prepares the server for installing riak"""
    sudo("apt-get -y install wget")

def accounts():
    base_folder = os.path.normpath(os.path.abspath(os.path.dirname(__file__)))
    fabutils._create_account(user = "store", passwd = "store", public_key=base_folder+"/store_id.pub")

def install_riak():
    """ installs riak storage server """
    riak_deb = "riak_%s_%s.deb" % (RIAK_VERSION, RIAK_ARCH)
    riak_url = "http://downloads.basho.com/riak/CURRENT/%s" % riak_deb
    run("wget %s" % riak_url)
    sudo("dpkg -i %s" % riak_deb)
    # TODO: set name of the node and IP address in config files prior to upload
    put(os.path.join(__path__[0], "conf", "app.config"), "/etc/riak/", use_sudo=True)
    put(os.path.join(__path__[0], "conf", "vm.args"), "/etc/riak", use_sudo=True)
    
    sudo("update-rc.d riak defaults")
    
def start_riak():
    sudo("/etc/init.d/riak start")