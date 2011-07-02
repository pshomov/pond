#!/usr/bin/env python
from porcelan_support import launch_and_wait

launch_and_wait("fab select_server:s-agent shutdown_agent_server deploy_agent:../frog/output/ start_agent_server --user=agent -i agent_server/agent_id -D")
