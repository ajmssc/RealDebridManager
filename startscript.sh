#!/bin/bash
trap 'pkill -P $$; exit 1;' TERM INT
PUID=${PUID:-911}
PGID=${PGID:-911}

apk --no-cache add shadow > /dev/null
groupmod --gid "$PGID" abc
usermod --uid "$PUID" --gid "$PGID" abc

echo "
User uid:    $(id -u abc)
User gid:    $(id -g abc)
-------------------------------------
"
chown -R abc:abc /app /config /watch

export WATCH_PATH=${WATCH_PATH:-/watch}
export DB_PATH=${DB_PATH:-/config/main.db}
su abc -c "gunicorn --bind 0.0.0.0:${rdmport:-5000} realdebridmanager.mainwebui:app"

PYTHON_PID=$!
wait $PYTHON_PID
