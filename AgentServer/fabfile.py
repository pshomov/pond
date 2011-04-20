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

def accounts():
    fabutils._create_account(user = "agent", passwd = "agent", public_key="agent_id.pub")

def setup():
    sudo("apt-get update")
    sudo("apt-get -y install git-core curl ruby-full")
    
def install_dotnet():
    install_mono("2.10.1", "2.10")
    
def install_mono(version, libgdi_version):
    process_erb("mono.erb", {'MONO_VERSION' : version})
    sudo("apt-get -y install build-essential autoconf automake bison libcairo2-dev libpango1.0-dev libfreetype6-dev libexif-dev libjpeg62-dev libtiff4-dev libgif-dev zlib1g-dev")
    put("mono", "/usr/local/bin/mono-%s" % version, use_sudo = True)
    sudo("chmod +x /usr/local/bin/mono-%s" % version)
    process_erb("compile_script.sh.erb", {'MONO_VERSION' : version})
    put("compile_script.sh")
    run("chmod +x compile_script.sh && ./compile_script.sh")
    
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

def process_erb(file, kwargs):

    for key,value in kwargs.iteritems():
            os.environ[key] = value

    local("erb %s > %s" % (file, file[:-4]))