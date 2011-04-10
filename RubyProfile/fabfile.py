from fabric.api import *
from fabric.contrib.console import confirm
from fabric.operations import sudo

def install_packages():
    put("rubygems-1.7.2.tgz")
    run("tar -xf rubygems-1.7.2.tgz")
    with cd("rubygems-1.7.2"):
        sudo("ruby setup.rb")
        
    _install("ruby1.8-dev ruby1.8 ri1.8 rdoc1.8 irb1.8")
    _install("libreadline-ruby1.8 libruby1.8 libopenssl-ruby")
    _install("libxml2 libxml2-dev")
    _install("libxslt-ruby1.8 libxslt1-dev")
    _install("rake")
    sudo("gem install bundler rack")
    sudo("gem install therubyracer")
    
def _install(packages):
    sudo("apt-get -y install "+packages)
    