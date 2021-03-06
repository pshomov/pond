#!/bin/bash

### BEGIN INIT INFO
# Provides:          monoserve.sh
# Required-Start:    $local_fs $syslog $remote_fs
# Required-Stop:     $local_fs $syslog $remote_fs
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start fastcgi mono server with hosts
### END INIT INFO

NAME=runz-webz
DESC="It serves the Webz ;)"

GUNICORN_PID=$(ps auxf | grep gunicorn | grep -v grep | awk '{print $2}')


case "$1" in
        start)
                if [ -z "${GUNICORN_PID}" ]; then
                        echo "starting Runz webz"
						cd /home/web/runz/webz/app
						source /home/web/webz_virtenv/bin/activate
						gunicorn -D -b unix:/tmp/gunicorn.sock --log-file=webz.log project:application
                        echo "Runz webz started"
                else
                        echo "Runz webz is already running"
                fi
        ;;
        stop)
                if [ -n "${GUNICORN_PID}" ]; then
                        kill ${GUNICORN_PID}
                        echo "Runz webz stopped"
                else
                        echo "Runz webz is not running"
                fi
        ;;
esac

exit 0
