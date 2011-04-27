import sys
import os

base_folder = os.path.normpath(os.path.abspath(os.path.dirname(__file__))+'/..')
sys.path[0:0] = [base_folder]

from fabric.api import *
from fabric.contrib.console import confirm
from fabric.contrib.files import contains,append
from fabenv import env
from fabric.operations import sudo
import fabutils

mono_version = "2.10.1"
libgdi_version = "2.10"

def accounts():
    fabutils._create_account(user = "agent", passwd = "agent", public_key="agent_id.pub")

def setup():
    sudo("apt-get -y install git-core curl ruby-full p7zip-full")
    with fabutils.process_erb("runz-agent.sh.erb", {"MONO_VERSION" : mono_version}) as f:
        put(f.name, "/home/agent/runz-agent.sh", use_sudo=True)
        sudo("chmod +x /home/agent/runz-agent.sh")
    
    
def install_dotnet():
    fabutils.install_mono(mono_version)
    install_nunit(mono_version)
        
def install_nunit(version):
    mono_runz_addons = "/opt/mono-%s/runz" % version
    sudo("mkdir -p %s/bin" % mono_runz_addons)
    put("bins/NUnit", mono_runz_addons, mirror_local_mode=True, use_sudo=True)
    put("nunit", "%s/bin" % mono_runz_addons, mirror_local_mode=True, use_sudo=True)
