from flask import Blueprint, render_template, request, redirect

from realdebridmanager.app import basic_auth
from realdebridmanager.database import database

tasks_router = Blueprint('tasks', __name__)


@tasks_router.get('/')
@basic_auth.required
def get_settings():
    settings = database.get_all_settings()
    return render_template("settings.html", settings=settings, alert=None)


@tasks_router.post('/')
@basic_auth.required
def post_settings():
    settings = database.get_all_settings()
    for setting_name in settings:
        setting_value = request.form[setting_name]
        if setting_value != settings[setting_name]:
            database.update_setting(setting_name, setting_value)
    settings = database.get_all_settings()
    return render_template("settings.html", settings=settings, alert="Saved Settings - Please Press Home!")


@tasks_router.get('/<task_id>')
@basic_auth.required
def get_task(task_id):
    task = database.get_task(task_id)
    return render_template("task.html", task=task)


@tasks_router.get('/delete/<task_id>')
@basic_auth.required
def delete_task(task_id):
    database.delete_task(task_id)
    return redirect('/')


@tasks_router.route('/deleteall')
@basic_auth.required
def delete_all():
    database.delete_all_tasks()
    return redirect('/')


@tasks_router.route('/deletecompleted')
@basic_auth.required
def delete_completed():
    con = sql.connect(databaseinfo, timeout=20)
    con.row_factory = sql.Row
    cur = con.cursor()
    rd_status = "Sent to aria2"
    cur.execute("SELECT * FROM tasks where rdstatus=?", (rd_status,))
    rows = cur.fetchall();
    todeleteid = []
    for row in rows:
        downloadid = (row[0])
        if downloadid in todeleteid:
            pass
        else:
            todeleteid.append(downloadid)
    for i in todeleteid:
        cur.execute("delete FROM tasks where id=?", (i,))
    con.commit()
    return redirect('/')
