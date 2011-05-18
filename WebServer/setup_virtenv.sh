#!/bin/bash

echo "Preparing virtual env for app"
sudo easy_install -U virtualenv || { echo "easy_install failed"; exit 1; } 
virtualenv --distribute webz_virtenv || { echo "virtualenv failed"; exit 1; } 
source ./webz_virtenv/bin/activate 
pip install bobo || { echo "installing bobo failed"; exit 1; } 
pip install gunicorn || { echo "installing gunicorn failed"; exit 1; } 
pip install riak || { echo "installing riak python client failed"; exit 1; } 
deactivate
echo "Virtual env installed and deactivated"
