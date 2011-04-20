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
import tempfile

def accounts():
    fabutils._create_account(user = "agent", passwd = "agent", public_key="agent_id.pub")

def setup():
    sudo("apt-get update")
    sudo("apt-get -y install git-core curl ruby-full p7zip-full")
    
def install_dotnet():
    mono_version = "2.10.1"
    libgdi_version = "2.10"
    install_mono(mono_version)
    install_nunit(mono_version)
    
def install_mono(version):
    put("bins/mono-%s.7z" % version)
    run("rm -rdf mono-%s" % version)
    run("7z x mono-%s.7z" % version)
    sudo("rm -rdf /opt/mono-%s && mv mono-%s /opt" % (version, version))
    _generate_mono_wrapper_script(version)
        
def build_mono(version, libgdi_version):
        
    sudo("apt-get -y install build-essential autoconf automake bison libcairo2-dev libpango1.0-dev libfreetype6-dev libexif-dev libjpeg62-dev libtiff4-dev libgif-dev zlib1g-dev")
    
    with process_erb("compile_script.sh.erb", {'MONO_VERSION' : version}) as f:
        put(f.name, "compile_script.sh")
    run("chmod +x compile_script.sh && ./compile_script.sh")
    _generate_mono_wrapper_script(version)
    
    run("wget http://ftp.novell.com/pub/mono/sources/mono/mono-%s.tar.bz2" % version)
    run("tar xjf mono-%s.tar.bz2" % version)
    run("wget http://ftp.novell.com/pub/mono/sources/libgdiplus/libgdiplus-%s.tar.bz2" % libgdi_version)
    run("tar xjf libgdiplus-%s.tar.bz2" % libgdi_version)
    
    with cd("libgdiplus-%s" % libgdi_version):
        run("./configure --prefix=/opt/mono-%s --with-pango && make" % version)
        sudo("make install")

    with cd("mono-%s" % version):
        run("./configure --prefix=/opt/mono-%s && make" % version)
        sudo("make install")

def _generate_mono_wrapper_script(version):
    with process_erb("mono.erb", {'MONO_VERSION' : version}) as f:
        put(f.name, "/usr/local/bin/mono-%s" % version, use_sudo = True)
    sudo("chmod +x /usr/local/bin/mono-%s" % version)

def install_nunit(version):
    mono_runz_addons = "/opt/mono-%s/runz" % version
    sudo("mkdir -p %s/bin" % mono_runz_addons)
    put("bins/NUnit", mono_runz_addons, mirror_local_mode=True, use_sudo=True)
    put("nunit", "%s/bin" % mono_runz_addons, mirror_local_mode=True, use_sudo=True)

def process_erb(file, kwargs):

    for key,value in kwargs.iteritems():
            os.environ[key] = value

    tempf = tempfile.NamedTemporaryFile()
    local("erb %s > %s" % (file, tempf.name))
    return tempf