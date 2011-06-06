import agent_server.fabfile
import message_server.fabfile
import web_server.fabfile
import repository_updater.fabfile
import storage_server
import fabutils

def setup_agent_server():
    fabutils.base_linux_configuration()
    agent_server.fabfile.accounts()
    agent_server.fabfile.setup()
    agent_server.fabfile.install_ruby_support()
    agent_server.fabfile.install_dotnet()
    agent_server.fabfile.install_python_support()

def setup_repotracker_server():
    fabutils.base_linux_configuration()
    repository_updater.fabfile.accounts()
    repository_updater.fabfile.setup()
    repository_updater.fabfile.install_dotnet()

def setup_web_server():
    fabutils.base_linux_configuration()
    web_server.fabfile.accounts()
    web_server.fabfile.setup()
    web_server.fabfile.install_nginx()
    web_server.fabfile.python_env()

def setup_store_server():
    fabutils.base_linux_configuration()
    storage_server.prepare()
    storage_server.accounts()
    storage_server.install_riak()

def setup_queue_server():
    fabutils.base_linux_configuration()
    message_server.fabfile.accounts()
    message_server.fabfile.setup()

def start_store_server():
    storage_server.start_riak()

def start_queue_server():
    message_server.fabfile.start_rabbitmq_server()