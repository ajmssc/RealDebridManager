import os

from flask import Flask
from flask_basicauth import BasicAuth
from flask_apscheduler import APScheduler

from realdebridmanager.blackhole.file_watch import watch_blackhole_folder
from realdebridmanager.database import database
from realdebridmanager.rd.task_watch import check_tasks_for_completion

app = Flask(__name__)

app_settings = database.get_all_settings()
app.config['BASIC_AUTH_USERNAME'] = app_settings['username']
app.config['BASIC_AUTH_PASSWORD'] = app_settings['password']

WATCH_PATH = os.getenv('watchpath')
if WATCH_PATH is None and app_settings.get('watchpath', None) is None:
    WATCH_PATH = os.path.abspath("./watch")
elif WATCH_PATH is None:
    WATCH_PATH = app_settings.get('watchpath', None)

WATCH_PATH = os.path.abspath(WATCH_PATH)
database.update_setting('watchpath', WATCH_PATH)

os.makedirs(WATCH_PATH + "/processed", mode=0o777, exist_ok=True)
os.makedirs(WATCH_PATH + "/errored", mode=0o777, exist_ok=True)

basic_auth = BasicAuth(app)

scheduler = APScheduler()


def background_tasks():
    watch_blackhole_folder()
    check_tasks_for_completion()


scheduler.add_job(id='Background Tasks', func=background_tasks, trigger="interval", seconds=3)
scheduler.start()