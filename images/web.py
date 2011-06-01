import time
from fabric.contrib.files import contains, append, sed
import openstack.compute
import os
import fabric.api

def image_web_server():
    rackspace = get_rackspace_manager()
    flavour = rackspace.flavors.find(ram=256)
    images = rackspace.images.find(name="Ubuntu 10.10 (maverick)")
    server = rackspace.servers.create("img-agent", images, flavour)
    serverId = server.id
    rootPass = server.adminPass
    while server.status != u"ACTIVE":
        time.sleep(5)
        server = rackspace.servers.get(serverId)
        print "status: " + server.status
        print "progress: " + str(server.progress)

    fabric.api.env.password = rootPass
    fabric.api.env.user = 'root'
    fabric.api.env.hosts = [server.public_ip]


def store_web_server():
    pass


def spin_web_server():
    pass


def reconfigure_server():
    reset_env_variable("RUNZ_RIAK_HOST", get_store_ip())
    reset_env_variable("RUNZ_RABBITMQ_SERVER", get_queue_ip())


def get_rackspace_manager():
    return openstack.compute.Compute(username=os.environ["RACKSPACE_USERNAME"], apikey=os.environ["RACKSPACE_API_KEY"])


def get_queue_ip():
    rackspace = get_rackspace_manager()
    return rackspace.servers.find(name="dev-queue").public_ip


def get_store_ip():
    rackspace = get_rackspace_manager()
    return rackspace.servers.find(name="dev-queue").public_ip


def reset_env_variable(variable_name, variable_value):
    if not contains("/etc/environment", variable_name):
        append("/etc/environment", "%s=%s" % (variable_name, variable_value), use_sudo=True)
    else:
        sed("/etc/environment", "^%s=.*$" % variable_name, "%s=%s" % (variable_name, variable_value), use_sudo=True)
