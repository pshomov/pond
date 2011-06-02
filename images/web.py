import images.primitives

WEB_IMAGE_NAME = "img-web"
WEB_SERVER_NAME = "s-web"
STORE_IMAGE_NAME = "img-store"
STORE_SERVER_NAME = "s-store"
QUEUE_IMAGE_NAME = "img-queue"
QUEUE_SERVER_NAME = "s-queue"
TEMP_SERVER = "temp-server"

def create_web_server():
    images.primitives.create_server(TEMP_SERVER)


def store_web_image():
    images.primitives.store_server_image(WEB_IMAGE_NAME)


def create_store_server():
    images.primitives.create_server(TEMP_SERVER)


def store_store_image():
    images.primitives.store_server_image(STORE_IMAGE_NAME)


def create_queue_server():
    images.primitives.create_server(TEMP_SERVER)


def store_queue_image():
    images.primitives.store_server_image(QUEUE_IMAGE_NAME)


def spin_queue_server():
    images.primitives.create_server(QUEUE_SERVER_NAME, QUEUE_IMAGE_NAME)


def spin_store_server():
    images.primitives.create_server(STORE_SERVER_NAME, STORE_IMAGE_NAME)


def spin_web_server():
    images.primitives.create_server(WEB_SERVER_NAME, WEB_IMAGE_NAME, generate_user=False)


def select_last_server():
    images.primitives.select_server(TEMP_SERVER)


def cleanup():
    images.primitives.delete_server(TEMP_SERVER)