import time
from fabric.contrib.files import contains, append, sed
from fabric.operations import reboot
import openstack.compute
import os
import fabric.api

current_server = None

def get_rackspace_manager():
    return openstack.compute.Compute(username=os.environ["RACKSPACE_USERNAME"], apikey=os.environ["RACKSPACE_API_KEY"])

rackspace = get_rackspace_manager()

def create_server(server_name, image_name="Ubuntu 10.10 (maverick)", generate_user=True):
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

    if generate_user:
        fabric.api.env.password = rootPass
        fabric.api.env.user = 'root'
    fabric.api.env.hosts = [server.public_ip]


def store_server_image(image_name):
    reboot(5)
    image = rackspace.images.create(image_name, current_server.id)
    while image.status != u"ACTIVE":
        time.sleep(5)
        image = rackspace.images.get(image.id)
        print "status: " + image.status
        if image.status in [u"ACTIVE", u"SAVING"]: print "progress: " + str(image.progress)

    current_server.delete()


def delete_server(server_name):
    for server in rackspace.servers.findall(name=server_name):
        server.delete()

def delete_all_servers():
    for server in rackspace.servers.list():
        server.delete()


def delete_image(image_name):
    for image in rackspace.images.findall(name=image_name):
        image.delete()

def select_server(server_name):
    server = rackspace.servers.find(name=server_name)
    fabric.api.env.hosts = [server.public_ip]
    global  current_server
    current_server = server

def rename_server(server_name, new_server_name):
    server = rackspace.servers.find(name=server_name)
    rackspace.servers.update(server, new_server_name)

def get_queue_ip():
    return rackspace.servers.find(name="s-queue").public_ip


def get_store_ip():
    return rackspace.servers.find(name="s-store").public_ip


def set_environment_in_file(file, environment_line, variable_name):
    if not contains(file, variable_name):
        print "{variable} not found, appending it".format(variable=variable_name)
        append(file, str(environment_line), use_sudo=True)
    else:
        print "{variable} found, replacing it".format(variable=variable_name)
        sed(file, "^%s=.*$" % variable_name, environment_line, use_sudo=True)


def reset_env_variable(variable_name, variable_value):
    environment_line = '%s=%s' % (variable_name, variable_value)
    print environment_line
    set_environment_in_file("/etc/environment", environment_line, variable_name)
    set_environment_in_file("/etc/profile", environment_line, variable_name)

def print_env():
    print str(fabric.api.env)


def all_servers():
    return rackspace.servers.list()