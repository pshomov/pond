import time
from fabric.contrib.files import contains, append, sed
import openstack.compute
import os
import fabric.api

current_server = None

def get_rackspace_manager():
    return openstack.compute.Compute(username=os.environ["RACKSPACE_USERNAME"], apikey=os.environ["RACKSPACE_API_KEY"])

rackspace = get_rackspace_manager()

def create_server(server_name, image_name = "Ubuntu 10.10 (maverick)"):
    flavour = rackspace.flavors.find(ram=256)
    images = rackspace.images.find(name=image_name)
    server = rackspace.servers.create(server_name, images, flavour)
    global current_server
    current_server = server
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


def store_server_image(image_name):
    image = rackspace.images.create(image_name, current_server.id)
    while image.status != u"ACTIVE":
        time.sleep(5)
        image = rackspace.images.get(image.id)
        print "status: " + image.status
        if image.status in [u"ACTIVE", u"SAVING"]: print "progress: " + str(image.progress)

    current_server.delete()


def reconfigure_server():
    reset_env_variable("RUNZ_RIAK_HOST", get_store_ip())
    reset_env_variable("RUNZ_RABBITMQ_SERVER", get_queue_ip())


def get_queue_ip():
    return rackspace.servers.find(name="s-queue").public_ip


def get_store_ip():
    return rackspace.servers.find(name="s-store").public_ip


def reset_env_variable(variable_name, variable_value):
    if not contains("/etc/environment", variable_name):
        append("/etc/environment", "%s=%s" % (variable_name, variable_value), use_sudo=True)
    else:
        sed("/etc/environment", "^%s=.*$" % variable_name, "%s=%s" % (variable_name, variable_value), use_sudo=True)
