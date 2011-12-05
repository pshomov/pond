#!/usr/bin/env python
from porcelan_support import launch_and_wait

launch_and_wait("fab select_server:s-web shutdown_web_server shutdown_web_server_status deploy_web_status:../frog/output/ start_web_server_status --user=web -i web_server/web_id -D")
