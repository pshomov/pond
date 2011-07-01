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
    sudo("echo \"deb http://ppa.launchpad.net/nginx/stable/ubuntu $(lsb_release -cs) main\" >> /etc/apt/sources.list")
    sudo("apt-key adv --keyserver keyserver.ubuntu.com --recv-keys C300EE8C")
    sudo("apt-get update && apt-get -y install nginx")

    if exists("/etc/init.d/apache2"):
        sudo("/etc/init.d/apache2 stop")
        sudo("update-rc.d apache2 disable")
    sudo("update-rc.d nginx enable")

    with fabutils.process_erb(base_folder + "/webz.nginx.conf.erb", {"ROOT_DIRECTORY" : "/home/web/runz", "WEBZ_SITE_ROOT_DIRECTORY" : "/home/web/runz/webz/site"}) as f:
        put(f.name, "/etc/nginx/sites-enabled/default", use_sudo=True)

    sudo("/etc/init.d/nginx restart")
    put(base_folder + "/runz-webz.sh", "/home/web/runz-webz.sh", use_sudo=True)
    sudo("chmod +x /home/web/runz-webz.sh")
    with fabutils.process_erb(base_folder + "/runz-web.sh.erb", {"MONO_VERSION" : mono_version}) as f:
        put(f.name, "/home/web/runz-web.sh", use_sudo=True)
        sudo("chmod +x /home/web/runz-web.sh")

def generate_nginx_config(runz_output_path, output_file):
    with fabutils.process_erb(base_folder + "/webz.nginx.conf.erb", {"ROOT_DIRECTORY" : os.path.abspath(runz_output_path), "WEBZ_SITE_ROOT_DIRECTORY" : os.path.abspath(os.path.join(runz_output_path, "webz/site"))}) as f:
        with open(output_file, "w") as out:
          out.writelines(f.readlines())


def build_mono_xsp(mono_version, mono_xsp_version):
    sudo("apt-get -y install build-essential autoconf automake pkg-config  p7zip-full")
    run("wget http://ftp.novell.com/pub/mono/sources/xsp/xsp-%s.tar.bz2" % mono_xsp_version)
    run("rm -rdf xsp-%s" % mono_xsp_version)
    run("tar xjf xsp-%s.tar.bz2" % mono_xsp_version)
    with cd("xsp-%s" % mono_xsp_version):
        run("mono-%s ./configure --prefix=/opt/mono-%s && mono-%s make" % (mono_version, mono_version, mono_version))
        sudo("make install")

def install_dotnet():
    fabutils.install_mono(mono_version)
    build_mono_xsp(mono_version, mono_xsp_version)
