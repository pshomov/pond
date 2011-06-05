#!/bin/bash

fab cleanup create_web_server setup_web_server && fab select_last_server deploy_web:../frog/output store_web_image --user web -i web_server/web_id
