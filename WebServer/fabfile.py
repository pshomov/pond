import os
from fabric.api import *
from fabric.contrib.files import exists
from fabric.operations import sudo
import fabutils

mono_version = "2.10.2"
mono_xsp_version = "2.10.2"
libgdi_version = "2.10"
base_folder = os.path.normpath(os.path.abspath(os.path.dirname(__file__)))

def accounts():
    fabutils._create_account(user="web", passwd="web", public_key=base_folder + "/web_id.pub")


def setup():
    sudo("apt-get -y install python2.6 python-setuptools python-protobuf p7zip-full")

def python_env():
    sudo("easy_install -U virtualenv || { echo \"easy_install failed\"; exit 1; }")
    put(base_folder + "/setup_virtenv.sh", "/home/web", use_sudo=True)
    with cd("/home/web"):
        sudo("chmod +x ./setup_virtenv.sh")
        run("chown web:web ./setup_virtenv.sh")
        sudo("./setup_virtenv.sh", user="web")

def install_nginx():
    sudo("apt-get -y install nginx")
    if exists("/etc/init.d/apache2"):
        sudo("/etc/init.d/apache2 stop")
        sudo("update-rc.d apache2 disable")
    sudo("update-rc.d nginx enable")
    put(base_folder + "/webz.nginx.conf", "/etc/nginx/sites-enabled/default", use_sudo=True)
    sudo("/etc/init.d/nginx restart")
    with fabutils.process_erb(base_folder + "/runz-webz.sh.erb", {}) as f:
        put(f.name, "/home/web/runz-webz.sh", use_sudo=True)
        sudo("chmod +x /home/web/runz-webz.sh")


def build_mono_xsp(mono_version, mono_xsp_version):
    sudo("apt-get -y install build-essential autoconf automake pkg-config  p7zip-full")
    put(base_folder + "/bins/xsp-%s.7z" % mono_xsp_version)
    run("rm -rdf xsp-%s" % mono_xsp_version)
    run("7z x xsp-%s.7z" % mono_xsp_version)
    with cd("xsp-%s" % mono_xsp_version):
        run("mono-%s ./configure --prefix=/opt/mono-%s && mono-%s make" % (mono_version, mono_version, mono_version))
        sudo("make install")