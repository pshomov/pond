#!/usr/bin/env python
from porcelan_support import launch_and_wait, generate_temp_server_name


server_id = generate_temp_server_name()

launch_and_wait("fab create_server:{server} "
                "setup_store_server setup_queue_server setup_agent_server setup_repotracker_server setup_projections_server setup_web_server "
                "start_store_server start_queue_server reconfigure_single_server".format(server=server_id))


launch_and_wait(
    "fab select_server:{server} "
    "deploy_agent:../frog/output  "
    "start_agent_server "
    "--user=agent --password=agent -i agent_server/agent_id".format(
        server=server_id))

launch_and_wait(
    "fab select_server:{server} "
    "deploy_repotracker:../frog/output  start_repotracker_server "
    " --user=repotracker --password=repotracker -i repository_updater/repotracker_id".format(
        server=server_id))

launch_and_wait(
    "fab select_server:{server} "
    "deploy_projections:../frog/output  start_projections_server "
    " --user=projections --password=projections -i projections/projections_id".format(
        server=server_id))

launch_and_wait(
    "fab select_server:{server} shutdown_web_server_status deploy_web_status:../frog/output/ start_web_server_status --user=web -i web_server/web_id -D".format(
        server=server_id))

launch_and_wait(
    "fab rename_as_one_server:{server}".format(
        server=server_id))



