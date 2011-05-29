import AgentServer.fabfile
import WebServer.fabfile
import RepositoryUpdater.fabfile
import StorageServer
from fabutils import base_linux_configuration

def agent_server():
    base_linux_configuration()
    AgentServer.fabfile.accounts()
    AgentServer.fabfile.setup()
    AgentServer.fabfile.install_ruby_support()
    AgentServer.fabfile.install_dotnet()
    AgentServer.fabfile.install_python_support()

def repotracker_server():
    base_linux_configuration()
    RepositoryUpdater.fabfile.accounts()
    RepositoryUpdater.fabfile.setup()
    RepositoryUpdater.fabfile.install_dotnet()

def web_server():
    base_linux_configuration()
    WebServer.fabfile.accounts()
    WebServer.fabfile.setup()
    WebServer.fabfile.install_dotnet_xsp()
    WebServer.fabfile.install_nginx()

def web_server_part2():
    WebServer.fabfile.python_env()

def storage_server():
    base_linux_configuration()
    StorageServer.prepare()
    StorageServer.install_riak()
