#!/bin/bash

fab cleanup create_web_server setup_repotracker_server reconfigure_server && fab select_last_server deploy_repotracker:../frog/output  start_repotracker_server rename_as_repotracker_server --user=repotracker --password=repotracker -i repository_updater/repotracker_id
