#!/bin/bash

fab spin_web_server reconfigure_server --user=web --password=web -i web_server/web_id
