#!/usr/bin/env python
from porcelan_support import launch_and_wait, generate_temp_server_name


server_id = generate_temp_server_name()
launch_and_wait("fab create_server:{server} setup_agent_server reconfigure_server".format(server=server_id))
launch_and_wait(
    "fab select_server:{server} deploy_agent:../frog/output  start_agent_server rename_as_agent_server --user=agent --password=agent -i agent_server/agent_id".format(
        server=server_id))