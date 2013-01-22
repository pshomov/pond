#!/usr/bin/env python
import sys
from porcelan_support import launch_and_wait

server = 's-web'
if len(sys.argv) > 1: server = sys.argv[1]
launch_and_wait("fab select_server:{server} shutdown_web_server_status deploy_web_status:../frog/output/ start_web_server_status --user=web -i web_server/web_id -D".format(server=server))
