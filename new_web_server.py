#!/usr/bin/env python
from porcelan_support import launch_and_wait, generate_temp_server_name


server_id = generate_temp_server_name()
launch_and_wait("fab create_server:{server} setup_web_server reconfigure_server rename_as_web_server:{server}".format(server=server_id))
launch_and_wait("./redeploy_web_server.py")
