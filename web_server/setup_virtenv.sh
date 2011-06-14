#!/bin/bash

echo "Preparing virtual env for app"
virtualenv --distribute webz_virtenv || { echo "virtualenv failed"; exit 1; }
source webz_virtenv/bin/activate
easy_install -U bobo || { echo "installing bobo failed"; exit 1; }
easy_install -U gunicorn || { echo "installing gunicorn failed"; exit 1; }
easy_install -U riak || { echo "installing riak python client failed"; exit 1; }
deactivate
echo "Virtual env installed and deactivated"
