from fabric.decorators import roles
from fabric.operations import sudo
import AgentServer.fabfile

@roles('agents')
def agent_server():
    _apt_update()
    AgentServer.fabfile.accounts()
    AgentServer.fabfile.setup()
    AgentServer.fabfile.install_ruby_support()
    AgentServer.fabfile.install_dotnet()
    AgentServer.fabfile.install_python_support()

def _apt_update():
    sudo("apt-get -y update")