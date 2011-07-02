#!/usr/bin/env python
from porcelan_support import launch_and_wait

launch_and_wait("fab spin_store_server prepare_store_new_server --user=store --password=store -i storage_server/store_id -D")
