import os

from fabric.api import *
from fabric.operations import sudo
import fabutils

base_folder = os.path.normpath(os.path.abspath(os.path.dirname(__file__)))
mono_version = "2.10.2"
libgdi_version = "2.10"

def accounts():
    fabutils._create_account(user = "repotracker", passwd = "repotracker", public_key=base_folder+"/repotracker_id.pub")

def setup():
    sudo("apt-get -y install p7zip-full")
    with fabutils.process_erb(base_folder+"/runz-repo-tracker.sh.erb", {"MONO_VERSION" : mono_version}) as f:
        put(f.name, "/home/repotracker/runz-repo-tracker.sh", use_sudo=True)
        sudo("chmod +x /home/repotracker/runz-repo-tracker.sh")

def install_dotnet():
    fabutils.install_mono(mono_version)
        