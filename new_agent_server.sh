#!/bin/bash

fab cleanup create_web_server setup_agent_server reconfigure_server && fab select_last_server deploy_agent:../frog/output  start_agent_server rename_as_agent_server --user=agent --password=agent -i agent_server/agent_id
