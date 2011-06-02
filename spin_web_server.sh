#!/bin/bash

fab spin_web_server reconfigure_server --user=web --password=web -i WebServer/web_id
