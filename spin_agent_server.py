#!/usr/bin/env python
from porcelan_support import launch_and_wait

launch_and_wait("fab spin_agent_server reconfigure_server  --user=agent --password=agent -i agent_server/agent_id -D")
