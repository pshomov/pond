import sys
import os

base_folder = os.path.normpath(os.path.abspath(os.path.dirname(__file__))+'/..')
sys.path[0:0] = [base_folder]

from fabric.api import *
from fabric.contrib.console import confirm
from fabric.contrib.files import contains,append
from fabenv import env
from fabric.operations import sudo
import fabutils

def accounts():
    fabutils._create_account(user = "agent", passwd = "agent", public_key="agent_id.pub")

def setup():
    sudo("apt-get update")
    sudo("apt-get -y install git-core curl ruby-full")
