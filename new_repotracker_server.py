#!/usr/bin/env python
from porcelan_support import launch_and_wait, generate_temp_server_name


server_id = generate_temp_server_name()
launch_and_wait("fab create_server:{server} setup_repotracker_server reconfigure_server".format(server=server_id))
launch_and_wait(
    "fab select_server:{server} deploy_repotracker:../frog/output  start_repotracker_server rename_as_repotracker_server:{server} --user=repotracker --password=repotracker -i repository_updater/repotracker_id".format(
        server=server_id))
