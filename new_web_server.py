#!/usr/bin/env python
from porcelan_support import launch_and_wait, generate_temp_server_name


server_id = generate_temp_server_name()
launch_and_wait("fab create_server:{server} setup_web_server reconfigure_server".format(server=server_id))
launch_and_wait(
    "fab select_server:{server} deploy_web:../frog/output rename_as_web_server:{server} start_web_server  --user=web --password=web -i web_server/web_id".format(
        server=server_id))

