import os
from fabric.api import run
from fabric.operations import sudo

RIAK_VERSION = "0.14.1-1"
RIAK_ARCH = "i386"

def prepare():
    """ prepares the server for installing riak"""
    sudo("apt-get -y install wget")

def install_riak():
    """ installs riak storage server """
    riak_deb = "riak_%s_%s.deb" % (RIAK_VERSION, RIAK_ARCH)
    riak_url = "http://downloads.basho.com/riak/CURRENT/%s" % riak_deb
    run("wget %s" % riak_url)
    sudo("apt-get -y install %s" % riak_deb)
    # TODO: set name of the node and IP address in config files prior to upload
    put(os.path.join(__path__, "conf", "app_config"), "/etc/riak")
    put(os.path.join(__path__, "conf", "vm.args", "/etc/riak"))