#!/bin/bash

fab cleanup create_web_server setup_web_server reconfigure_server && fab select_last_server deploy_web:../frog/output start_web_server rename_as_web_server --user=web --password=web -i web_server/web_id
