from fabric.decorators import roles
from fabric.operations import sudo
import AgentServer.fabfile
import WebServer.fabfile
import RepositoryUpdater.fabfile
import StorageServer
import fabenv

@roles('agents')
def agent_server():
    _apt_update()
    AgentServer.fabfile.accounts()
    AgentServer.fabfile.setup()
    AgentServer.fabfile.install_ruby_support()
    AgentServer.fabfile.install_dotnet()
    AgentServer.fabfile.install_python_support()

@roles('repotracker')
def repotracker_server():
    _apt_update()
    RepositoryUpdater.fabfile.accounts()
    RepositoryUpdater.fabfile.setup()
    RepositoryUpdater.fabfile.install_dotnet()

@roles('web')
def web_server():
    _apt_update()
    WebServer.fabfile.accounts()
    WebServer.fabfile.setup()
    WebServer.fabfile.install_dotnet_xsp()
    WebServer.fabfile.install_nginx()

@roles('storage')
def storage_server():
    StorageServer.prepare()
    StorageServer.install_riak()


def _apt_update():
    sudo("apt-get -y update")