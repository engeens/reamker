# -*- coding: utf-8 -*-

if not auth.is_logged_in():
    redirect(URL(request.application, 'default', 'user', args=['login'],
                  vars=dict(send=URL(args=request.args, vars=request.vars))))

def index():
    response.view = '%s/home/index.html' % CONFIG_THEME
    from apps import Apps
    apps = Apps(db)
    return dict(apps=apps.get())


def set_timezone():
    """Ajax call to set the timezone information for the session."""
    tz_name = request.vars.name
    from pytz import all_timezones_set
    if tz_name in all_timezones_set:
        session.user_timezone = tz_name
    pass

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    from model import DataBase
    DataBase(db=db, tables=['t_apps'])
    return response.download(request, db)