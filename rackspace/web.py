import os
import time
import rackspace.primitives
from rackspace.primitives import create_server, select_server, find_server_ip
import storage_server

WEB_IMAGE_NAME = "img-web"
WEB_SERVER_NAME = "s-web"
STORE_IMAGE_NAME = "img-store"
STORE_SERVER_NAME = "s-store"
QUEUE_IMAGE_NAME = "img-queue"
QUEUE_SERVER_NAME = "s-queue"
TEMP_SERVER = "temp-server"
AGENT_SERVER_NAME = "s-agent"
AGENT_IMAGE_NAME = "img-agent"
REPOTRACKER_SERVER_NAME = "s-repotracker"
REPOTRACKER_IMAGE_NAME = "img-repotracker"

def store_web_image():
    rackspace.primitives.store_server_image(WEB_IMAGE_NAME)


def store_store_image():
    rackspace.primitives.store_server_image(STORE_IMAGE_NAME)


def store_queue_image():
    rackspace.primitives.store_server_image(QUEUE_IMAGE_NAME)


def store_agent_image():
    rackspace.primitives.store_server_image(AGENT_IMAGE_NAME)


def store_repotracker_image():
    rackspace.primitives.store_server_image(REPOTRACKER_IMAGE_NAME)


def spin_queue_server():
    rackspace.primitives.create_server(QUEUE_SERVER_NAME, QUEUE_IMAGE_NAME, generate_user=False)


def spin_store_server():
    rackspace.primitives.create_server(STORE_SERVER_NAME, STORE_IMAGE_NAME, generate_user=False)


def spin_web_server():
    rackspace.primitives.create_server(WEB_SERVER_NAME, WEB_IMAGE_NAME, generate_user=False)


def spin_agent_server():
    rackspace.primitives.create_server(AGENT_SERVER_NAME, AGENT_IMAGE_NAME, generate_user=False)


def spin_repotracker_server():
    rackspace.primitives.create_server(REPOTRACKER_SERVER_NAME, REPOTRACKER_IMAGE_NAME, generate_user=False)


def rename_as_web_server(server_name):
    rackspace.primitives.rename_server(server_name, WEB_SERVER_NAME)


def rename_as_queue_server(server_name):
    rackspace.primitives.rename_server(server_name, QUEUE_SERVER_NAME)


def rename_as_store_server(server_name):
    rackspace.primitives.rename_server(server_name, STORE_SERVER_NAME)


def rename_as_agent_server(server_name):
    rackspace.primitives.rename_server(server_name, AGENT_SERVER_NAME)


def rename_as_repotracker_server(server_name):
    rackspace.primitives.rename_server(server_name, REPOTRACKER_SERVER_NAME)


def cleanup():
    rackspace.primitives.delete_server(TEMP_SERVER)


def list_servers():
    for server in rackspace.primitives.all_servers():
        print "{name} - {ip}({pip})".format(name=server.name, ip=server.public_ip(), pip=server.private_ip())


def reconfigure_server():
    rackspace.primitives.reset_env_variable("RUNZ_RIAK_HOST", get_store_ip())
    rackspace.primitives.reset_env_variable("RUNZ_RABBITMQ_SERVER", get_queue_ip())

def prepare_store_new_server():
    storage_server.shutdown_riak()
    storage_server.remove_the_ring_file_since_it_is_tight_to_the_IP_address()
    storage_server.start_riak()

def get_queue_ip():
    return find_server_ip(QUEUE_SERVER_NAME)

def get_store_ip():
    return find_server_ip(STORE_SERVER_NAME)

def get_web_ip():
    return find_server_ip(WEB_SERVER_NAME)

def view_queue_mgmt():
    os.system("open http://{server}:55672/mgmt".format(server = get_queue_ip()))

def view_web():
    web_ip = get_web_ip()
    os.system("open http://{server}:8000/register/index.html".format(server = web_ip))
    os.system("open http://{server}:8000/stat/project/github/jasondentler/cqrs/status".format(server = web_ip))

def view_store_mgmt():
    os.system("open http://{server}:8098/riak/rekon/go#/buckets/projects".format(server = get_store_ip()))
