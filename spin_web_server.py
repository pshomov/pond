#!/usr/bin/env python
from porcelan_support import launch_and_wait

launch_and_wait("fab spin_web_server reconfigure_server  --user=web --password=web -i web_server/web_id -D")
