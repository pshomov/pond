import shutil
import os
import sys

base_folder = os.path.normpath(os.path.abspath(os.path.dirname(__file__))+'/..')
sys.path[0:0] = [base_folder]

from fabric.api import *
from fabric.contrib.console import confirm
from fabric.contrib.files import exists
from fabenv import env
from fabric.operations import sudo
import fabutils

def deploy_web(build_output):
    WEB_ARCHIVE = "web.7z"
    if os.path.exists(WEB_ARCHIVE):
        os.remove(WEB_ARCHIVE)
    local("7z a -r %s %s/web" % (WEB_ARCHIVE, build_output))
    if exists("runz/web"):
        run("rm -rdf runz")
        
    run("mkdir -p runz/web")
    put(WEB_ARCHIVE, "runz/")
    run("~/fastcgi-mono-server4.sh stop")
    
    run("7z x -orunz runz/%s" % WEB_ARCHIVE)
    run("chmod -R 755 runz/web")

    fabutils._run_background_process("~/fastcgi-mono-server4.sh start", "web")

def deploy_agent(build_output):
    AGENT_ARCHIVE = "agent.7z"
    if os.path.exists(AGENT_ARCHIVE):
        os.remove(AGENT_ARCHIVE)
    local("7z a -r %s %s/agent" % (AGENT_ARCHIVE, build_output))
    if exists("runz/agent"):
        run("rm -rdf runz/agent")

    run("mkdir -p runz/agent")
    put(AGENT_ARCHIVE, "runz/")
    run("~/runz-agent.sh stop")

    run("7z x -orunz runz/%s" % AGENT_ARCHIVE)
    run("chmod -R 755 runz/agent")

    fabutils._run_background_process("~/runz-agent.sh start", "agent")

def deploy_repotracker(build_output):
    REPOTRACKER_ARCHIVE = "repotracker.7z"
    if os.path.exists(REPOTRACKER_ARCHIVE):
        os.remove(REPOTRACKER_ARCHIVE)
    local("7z a -r %s %s/repotracker" % (REPOTRACKER_ARCHIVE, build_output))
    if exists("runz/repotracker"):
        run("rm -rdf runz/repotracker")

    run("mkdir -p runz/repotracker")
    put(REPOTRACKER_ARCHIVE, "runz/")
    run("~/runz-repo-tracker.sh stop")

    run("7z x -orunz runz/%s" % REPOTRACKER_ARCHIVE)
    run("chmod -R 755 runz/repotracker")

    fabutils._run_background_process("~/runz-repo-tracker.sh start", "repotracker")

