import agent_server.fabfile
import MessageServer.fabfile
import WebServer.fabfile
import RepositoryUpdater.fabfile
import StorageServer
import fabutils
from images.web import *
from deployment.fabfile import *

def setup_agent_server():
    fabutils.base_linux_configuration()
    AgentServer.fabfile.accounts()
    AgentServer.fabfile.setup()
    AgentServer.fabfile.install_ruby_support()
    AgentServer.fabfile.install_dotnet()
    AgentServer.fabfile.install_python_support()

def setup_repotracker_server():
    fabutils.base_linux_configuration()
    RepositoryUpdater.fabfile.accounts()
    RepositoryUpdater.fabfile.setup()
    RepositoryUpdater.fabfile.install_dotnet()

def setup_web_server():
    fabutils.base_linux_configuration()
    WebServer.fabfile.accounts()
    WebServer.fabfile.setup()
    WebServer.fabfile.install_nginx()
    WebServer.fabfile.python_env()

def setup_store_server():
    fabutils.base_linux_configuration()
    StorageServer.prepare()
    StorageServer.accounts()
    StorageServer.install_riak()

def setup_queue_server():
    fabutils.base_linux_configuration()
    MessageServer.fabfile.accounts()
    MessageServer.fabfile.setup()

def start_store_server():
    StorageServer.start_riak()