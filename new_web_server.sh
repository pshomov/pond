#!/bin/bash

fab cleanup create_web_server setup_web_server && fab select_last_server deploy_web:../frog/output reconfigure_server start_web_server --user=web --password=web -i web_server/web_id
