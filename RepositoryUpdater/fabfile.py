import sys
import os

base_folder = os.path.normpath(os.path.abspath(os.path.dirname(__file__)))
sys.path[0:0] = [base_folder+"/.."]

from fabric.api import *
from fabric.contrib.files import contains,append
from fabenv import env
from fabric.operations import sudo
import fabutils

mono_version = "2.10.1"
libgdi_version = "2.10"

def accounts():
    fabutils._create_account(user = "repotracker", passwd = "repotracker", public_key=base_folder+"/repotracker_id.pub")

def setup():
    sudo("apt-get -y install git-core curl ruby-full p7zip-full")
    with fabutils.process_erb(base_folder+"/runz-repo-tracker.sh.erb", {"MONO_VERSION" : mono_version}) as f:
        put(f.name, "/home/repotracker/runz-repo-tracker.sh", use_sudo=True)
        sudo("chmod +x /home/repotracker/runz-repo-tracker.sh")
    if not contains("/etc/environment", "RUNZ_RABBITMQ_SERVER"):
        append("/etc/environment", "RUNZ_RABBITMQ_SERVER=%s" % env.roledefs['queue'], use_sudo=True)
        
def install_dotnet():
    fabutils.install_mono(mono_version)
        