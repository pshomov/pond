#!/usr/bin/env python
import sys
from porcelan_support import launch_and_wait

server = 's-projections'
if len(sys.argv) > 1: server = sys.argv[1]
launch_and_wait("fab select_server:{server} shutdown_projections_server deploy_projections:../frog/output/ start_projections_server --user=projections -i projections/projections_id -D".format(server=server))
