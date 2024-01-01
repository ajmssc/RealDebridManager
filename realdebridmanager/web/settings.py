from flask import Blueprint, render_template, request

from realdebridmanager.app import basic_auth
from realdebridmanager.database import database

settings_router = Blueprint('settings', __name__)


@settings_router.get('/')
@basic_auth.required
def get_settings():
    settings = database.get_all_settings()
    return render_template("settings.html", settings=settings, alert=None)


@settings_router.post('/')
@basic_auth.required
def post_settings():
    settings = database.get_all_settings()
    for setting_name in settings:
        setting_value = request.form[setting_name]
        if setting_value != settings[setting_name]:
            database.update_setting(setting_name, setting_value)
    settings = database.get_all_settings()
    return render_template("settings.html", settings=settings, alert="Saved Settings - Please Press Home!")
