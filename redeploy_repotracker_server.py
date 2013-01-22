#!/usr/bin/env python
import sys
from porcelan_support import launch_and_wait

server = 's-repotracker'
if len(sys.argv) > 1: server = sys.argv[1]
launch_and_wait("fab select_server:{server} shutdown_repotracker_server deploy_repotracker:../frog/output/ start_repotracker_server --user=repotracker -i repository_updater/repotracker_id -D".format(server=server))
