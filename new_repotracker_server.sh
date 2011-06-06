#!/bin/bash

fab cleanup create_web_server setup_repotracker_server && fab select_last_server deploy_repotracker:../frog/output reconfigure_server start_repotracker_server --user=repotracker --password=repotracker -i repository_updater/repotracker_id
