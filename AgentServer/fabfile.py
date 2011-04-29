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
    if not contains("/etc/environment", "RUNZ_RABBITMQ_SERVER"):
        append("/etc/environment", "RUNZ_RABBITMQ_SERVER=%s" % env.roledefs['queue'], use_sudo=True)
        
def install_ruby_support():
    put("bins/rubygems-1.7.2.tgz")
    run("tar -xf rubygems-1.7.2.tgz")
    with cd("rubygems-1.7.2"):
        sudo("ruby setup.rb")

    fabutils._install("ruby1.8-dev ruby1.8 ri1.8 rdoc1.8 irb1.8 build-essential")
    fabutils._install("libreadline-ruby1.8 libruby1.8 libopenssl-ruby")
    fabutils._install("libxml2 libxml2-dev")
    fabutils._install("libxslt-ruby1.8 libxslt1-dev")
    fabutils._install("rake")
    sudo("gem1.8 install bundler rack")
    sudo("gem1.8 install therubyracer")
    
def install_dotnet():
    fabutils.install_mono(mono_version)
    install_nunit(mono_version)
        
def install_nunit(version):
    mono_runz_addons = "/opt/mono-%s/runz" % version
    sudo("mkdir -p %s/bin" % mono_runz_addons)
    put("bins/NUnit", mono_runz_addons, mirror_local_mode=True, use_sudo=True)
    put("nunit", "%s/bin" % mono_runz_addons, mirror_local_mode=True, use_sudo=True)
