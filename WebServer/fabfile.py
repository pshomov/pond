import sys
import os
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.contrib.files import exists,contains,append
from fabenv import env
from fabric.operations import sudo
import fabutils
import tempfile

mono_version = "2.10.2"
mono_xsp_version = "2.10.2"
libgdi_version = "2.10"
base_folder = os.path.normpath(os.path.abspath(os.path.dirname(__file__)))

def accounts():
    fabutils._create_account(user = "web", passwd = "web", public_key=base_folder+"/web_id.pub")
    
def setup():
    if not contains("/etc/environment", "RUNZ_RABBITMQ_SERVER"):
        append("/etc/environment", "RUNZ_RABBITMQ_SERVER=%s" % env.roledefs['queue'], use_sudo=True)
    
    
def install_dotnet_xsp():
    if not exists("/opt/mono-%s" % mono_version):
        fabutils.build_mono(mono_version, mono_xsp_version)
    build_mono_xsp(mono_version, mono_xsp_version)
    
def install_nginx():
    sudo("apt-get -y install nginx")
    if exists("/etc/init.d/apache2"):
        sudo("/etc/init.d/apache2 stop")
        sudo("update-rc.d apache2 disable")
    sudo("update-rc.d nginx enable")
    put(base_folder+"/default","/etc/nginx/sites-enabled/default", use_sudo=True)
    sudo("/etc/init.d/nginx restart")
    with fabutils.process_erb(base_folder+"/fastcgi-mono-server4.sh.erb", {"MONO_VERSION" : mono_version}) as f:
        put(f.name, "/home/web/fastcgi-mono-server4.sh", use_sudo=True)
        sudo("chmod +x /home/web/fastcgi-mono-server4.sh")
    
        
def build_mono_xsp(mono_version, mono_xsp_version):
    sudo("apt-get -y install build-essential autoconf automake pkg-config  p7zip-full")
    put(base_folder+"/bins/xsp-%s.7z" % mono_xsp_version)
    run("rm -rdf xsp-%s" % mono_xsp_version)
    run("7z x xsp-%s.7z" % mono_xsp_version)
    with cd("xsp-%s" % mono_xsp_version):        
        run("mono-%s ./configure --prefix=/opt/mono-%s && mono-%s make" % (mono_version, mono_version, mono_version))
        sudo("make install")