import rackspace.primitives
from rackspace.primitives import create_server, select_server

WEB_IMAGE_NAME = "img-web"
WEB_SERVER_NAME = "s-web"
STORE_IMAGE_NAME = "img-store"
STORE_SERVER_NAME = "s-store"
QUEUE_IMAGE_NAME = "img-queue"
QUEUE_SERVER_NAME = "s-queue"
TEMP_SERVER = "temp-server"
AGENT_SERVER_NAME = "s-agent"
REPOTRACKER_SERVER_NAME = "s-repotracker"

def store_web_image():
    rackspace.primitives.store_server_image(WEB_IMAGE_NAME)


def store_store_image():
    rackspace.primitives.store_server_image(STORE_IMAGE_NAME)


def store_queue_image():
    rackspace.primitives.store_server_image(QUEUE_IMAGE_NAME)


def spin_queue_server():
    rackspace.primitives.create_server(QUEUE_SERVER_NAME, QUEUE_IMAGE_NAME)


def spin_store_server():
    rackspace.primitives.create_server(STORE_SERVER_NAME, STORE_IMAGE_NAME)


def spin_web_server():
    rackspace.primitives.create_server(WEB_SERVER_NAME, WEB_IMAGE_NAME, generate_user=False)


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
        print "{name} - {ip}".format(name = server.name, ip = server.publicip)

def reconfigure_server():
    rackspace.primitives.print_env()
    rackspace.primitives.reset_env_variable("RUNZ_RIAK_HOST", rackspace.primitives.get_store_ip())
    rackspace.primitives.reset_env_variable("RUNZ_RABBITMQ_SERVER", rackspace.primitives.get_queue_ip())
