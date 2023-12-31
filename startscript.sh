#!/bin/bash
export dbinfo=/config/main.db
export watchpath=/watch
exec python3 -m realdebridmanager.FileWatch &
exec gunicorn --bind 0.0.0.0:${rdmport:-5000} realdebridmanager.mainwebui:app