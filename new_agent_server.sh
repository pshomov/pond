#!/bin/bash

fab cleanup create_web_server setup_agent_server && fab select_last_server deploy_agent:../frog/output reconfigure_server start_agent_server --user=agent --password=agent -i agent_server/agent_id
