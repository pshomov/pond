#!/usr/bin/env python
import sys
from porcelan_support import launch_and_wait

server = 's-agent'
if len(sys.argv) > 1: server = sys.argv[1]
launch_and_wait("fab select_server:{server} shutdown_agent_server deploy_agent:../frog/output/ start_agent_server --user=agent -i agent_server/agent_id -D".format(server = server))
