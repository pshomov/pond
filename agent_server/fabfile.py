import sys
import os

from fabric.api import *
from fabric.contrib.files import contains,append
from fabric.operations import sudo
import fabutils

mono_version = "2.10.2"
libgdi_version = "2.10"
base_folder = os.path.normpath(os.path.abspath(os.path.dirname(__file__)))

def accounts():
    fabutils._create_account(user = "agent", passwd = "agent", public_key=base_folder+"/agent_id.pub")

def setup():
    sudo("apt-get -y install git-core curl ruby-full p7zip-full")
    with fabutils.process_erb(base_folder+"/runz-agent.sh.erb", {"MONO_VERSION" : mono_version}) as f:
        put(f.name, "/home/agent/runz-agent.sh", use_sudo=True)
        sudo("chmod +x /home/agent/runz-agent.sh")

def install_ruby_support():
    put(os.path.join(base_folder,"gemrc"), "/home/agent/.gemrc")
    run("mkdir -p /home/agent/.gem")
    run("chown agent:agent /home/agent/.gem")

    rubygems_version = "rubygems-1.8.10"
    put(base_folder+"/bins/%s.tgz" % rubygems_version)
    run("tar -xf %s.tgz" % rubygems_version)
    with cd(rubygems_version):
        sudo("ruby setup.rb")

    fabutils._install("ruby1.8-dev ruby1.8 ri1.8 rdoc1.8 irb1.8 build-essential")
    fabutils._install("libreadline-ruby1.8 libruby1.8 libopenssl-ruby")
    fabutils._install("libxml2 libxml2-dev")
    fabutils._install("libxslt-ruby1.8 libxslt1-dev")

    sudo("gem1.8 install bundler --no-rdoc --no-ri")
    sudo("gem1.8 install rake therubyracer --no-rdoc --no-ri")

def install_python_support():
    sudo("apt-get -y install python python-dev python-pip")


def install_dotnet():
    fabutils.install_mono(mono_version)
    install_nunit(mono_version)

def install_nunit(version):
    sudo("apt-get -y install realpath")
    mono_runz_addons = "/opt/mono-%s/runz" % version
    sudo("mkdir -p %s/bin" % mono_runz_addons)
    put(base_folder+"/bins/NUnit", mono_runz_addons, mirror_local_mode=True, use_sudo=True)
    put(base_folder+"/nunit", "%s/bin" % mono_runz_addons, mirror_local_mode=True, use_sudo=True)
