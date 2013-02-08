import os

from fabric.api import *
from fabric.operations import sudo
import fabutils

base_folder = os.path.normpath(os.path.abspath(os.path.dirname(__file__)))
mono_version = "3.0.3"

def accounts():
    fabutils._create_account(user = "projections", passwd = "projections", public_key=base_folder+"/projections_id.pub")

def setup():
    sudo("apt-get -y install p7zip-full")
    with fabutils.process_erb(base_folder+"/runz-projections.sh.erb", {"MONO_VERSION" : mono_version}) as f:
        put(f.name, "/home/projections/runz-projections.sh", use_sudo=True)
        sudo("chmod +x /home/projections/runz-projections.sh")

def install_dotnet():
    fabutils.install_mono(mono_version)
        