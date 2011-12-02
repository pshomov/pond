import os
from fabric.api import *
from fabric.contrib.files import exists
from fabric.operations import sudo
import tempfile

base = os.path.abspath(os.path.dirname(__file__))
agent_folder = os.path.join(base, 'agent_server')

def _create_account(user, passwd, public_key=None):
    sudo("apt-get -y install makepasswd")
    passwd = run("echo %s | makepasswd --clearfrom=- --crypt-md5 |awk '{ print $2 }'" % passwd)
    env.warn_only = True
    sudo("userdel -f -r %s" % user)
    env.warn_only = False
    sudo("useradd -d /home/%(user)s -m %(user)s -p '%(passwd)s' -r -G ssh,sudo -s /bin/bash" % {"user": user,
                                                                                                "passwd": passwd})
    if public_key is not None:
        sudo("mkdir -p /home/%s/.ssh" % user)
        user_key_path = "/home/%s/.ssh/authorized_keys" % user
        put(public_key, user_key_path, use_sudo=True)
        sudo("chmod 600 "+user_key_path)
        sudo("chown {user}:{user} {key_path}".format(user = user, key_path = user_key_path))


def base_linux_configuration():
    _apt_update()
    put(os.path.join(base, "base_linux", "sshd_config"), "/etc/ssh", use_sudo=True)

def install_mono(version):
    if not exists("/opt/mono-{mono_version}".format(mono_version=version)):
        sudo("apt-get -y install p7zip-full")
        run("wget -O mono-%s.7z https://s3.amazonaws.com/mono_builds/mono-%s-amd64.7z" % (version, version))
        run("rm -rdf mono-%s" % version)
        run("7z x mono-%s.7z" % version)
        sudo("rm -rdf /opt/mono-%s && mv mono-%s /opt" % (version, version))
        _generate_mono_wrapper_script(version)


def build_mono(version, libgdi_version):
    sudo(
        "apt-get -y install build-essential autoconf automake bison libcairo2-dev libpango1.0-dev libfreetype6-dev libexif-dev libjpeg62-dev libtiff4-dev libgif-dev zlib1g-dev")

    with process_erb(agent_folder + "/compile_script.sh.erb", {'MONO_VERSION': version}) as f:
        put(f.name, "compile_script.sh")
    run("chmod +x compile_script.sh && ./compile_script.sh")
    _generate_mono_wrapper_script(version)

    run("wget http://download.mono-project.com/sources/mono/mono-%s.tar.bz2" % version)
    run("tar xjf mono-%s.tar.bz2" % version)
    run("wget http://download.mono-project.com/sources/libgdiplus/libgdiplus-%s.tar.bz2" % libgdi_version)
    run("tar xjf libgdiplus-%s.tar.bz2" % libgdi_version)

    with cd("libgdiplus-%s" % libgdi_version):
        run("./configure --prefix=/opt/mono-%s --with-pango && make" % version)
        sudo("make install")

    with cd("mono-%s" % version):
        run("./configure --prefix=/opt/mono-%s && make" % version)
        sudo("make install")


def _generate_mono_wrapper_script(version):
    with process_erb(agent_folder + "/mono.erb", {'MONO_VERSION': version}) as f:
        put(f.name, "/usr/local/bin/mono-%s" % version, use_sudo=True)
    sudo("chmod +x /usr/local/bin/mono-%s" % version)


def _install(packages):
    sudo("apt-get -y install " + packages)


def _run_background_process(command, output_prefix):
    # see http://stackoverflow.com/questions/29142/getting-ssh-to-execute-a-command-in-the-background-on-target-machine
    run("nohup {command} > ~/{prefix}.out 2> ~/{prefix}.err < /dev/null".format(prefix=output_prefix, command=command))


def process_erb(file, kwargs):
    for key, value in kwargs.iteritems():
        os.environ[key] = value

    tempf = tempfile.NamedTemporaryFile()
    local("erb %s > %s" % (file, tempf.name))
    return tempf


def _apt_update():
    sudo("apt-get -y update")