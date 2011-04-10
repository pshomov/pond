from fabric.api import *
from fabric.contrib.console import confirm
from fabric.operations import sudo

def install_packages():
    sudo("mkdir -p /opt/mono-2.10.1/runz/bin")
    put("bins/NUnit", "/opt/mono-2.10.1/runz", mirror_local_mode=True, use_sudo=True)
    put("nunit", "/opt/mono-2.10.1/runz/bin", mirror_local_mode=True, use_sudo=True)