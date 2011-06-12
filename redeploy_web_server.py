#!/usr/bin/env python
from porcelan_support import launch_and_wait

launch_and_wait("fab select_server:s-web shutdown_web_server deploy_web:../frog/output/ start_web_server --user=web -i web_server/web_id")
