#!/usr/bin/env python
from porcelan_support import launch_and_wait, generate_temp_server_name


server_id = generate_temp_server_name()
launch_and_wait("fab create_server:{server} setup_queue_server start_queue_server rename_as_queue_server:{server}".format(server=server_id))
