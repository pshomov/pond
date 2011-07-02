#!/usr/bin/env python
from porcelan_support import launch_and_wait

launch_and_wait("fab spin_repotracker_server reconfigure_server  --user=repotracker --password=repotracker -i repository_updater/repotracker_id -D")
