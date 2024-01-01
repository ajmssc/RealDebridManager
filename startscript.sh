#!/bin/bash
export dbinfo=/config/main.db
exec gunicorn --bind 0.0.0.0:${rdmport:-5000} realdebridmanager.mainwebui:app