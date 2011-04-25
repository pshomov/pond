import sys
import os

base_folder = os.path.normpath(os.path.abspath(os.path.dirname(__file__))+'/..')
sys.path[0:0] = [base_folder]

from fabric.api import *
from fabric.contrib.console import confirm
from fabric.contrib.files import exists
from fabenv import env
from fabric.operations import sudo
import fabutils
import tempfile

def accounts():
    fabutils._create_account(user = "web", passwd = "web", public_key="web_id.pub")
    
def install_dotnet_xsp():
    mono_version = "2.10.1"
    mono_xsp_version = "2.10"
    libgdi_version = "2.10"
    if not exists("/opt/mono-%s" % mono_version):
        fabutils.install_mono(mono_version)
    build_mono_xsp(mono_version, mono_xsp_version)
    
def install_nginx():
    sudo("apt-get -y install nginx")
    if exists("/etc/init.d/apache2"):
        sudo("/etc/init.d/apache2 stop")
        sudo("update-rc.d apache disable")
    sudo("update-rc.d nginx enable")
    put("default","/etc/nginx/sites-enabled/default", use_sudo=True)
    sudo("/etc/init.d/nginx restart")
        
def build_mono_xsp(mono_version, mono_xsp_version):
    sudo("apt-get -y install build-essential autoconf automake pkg-config")
    put("bins/xsp-%s.7z" % mono_xsp_version)
    run("rm -rdf xsp-%s" % mono_xsp_version)
    run("7z x xsp-%s.7z" % mono_xsp_version)
    with cd("xsp-%s" % mono_xsp_version):        
        run("mono-%s ./configure --prefix=/opt/mono-%s && mono-%s make" % (mono_version, mono_version, mono_version))
        sudo("make install")