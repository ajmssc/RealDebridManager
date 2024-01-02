from flask import render_template

from realdebridmanager.app import app, basic_auth
from realdebridmanager.database import database
from realdebridmanager.web.settings import settings_router
from realdebridmanager.web.tasks import tasks_router

app.register_blueprint(settings_router, url_prefix='/settings')
app.register_blueprint(tasks_router, url_prefix='/tasks')


@app.route('/')
@basic_auth.required
def list():
    settings = database.get_all_settings()
    if settings.get('rdapikey', 'placeholderapikey') == 'placeholderapikey':
        return render_template("firstlogin.html")
    else:
        return render_template("main.html", tasks=database.get_tasks())


if __name__ == '__main__':
    app.run(debug=True)
