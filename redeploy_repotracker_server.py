#!/usr/bin/env python
from porcelan_support import launch_and_wait

launch_and_wait("fab select_server:s-repotracker shutdown_repotracker_server deploy_repotracker:../frog/output/ start_repotracker_server --user=repotracker -i repository_updater/repotracker_id -D")
