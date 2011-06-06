import message_server
import storage_server

def start_store_server():
    storage_server.start_riak()

def start_queue_server():
    message_server.fabfile.start_rabbitmq_server()