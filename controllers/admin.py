# -*- coding: utf-8 -*-

if ('admin' or 'editor' or 'viewer') not in auth.user_groups.values():
    if auth.is_logged_in():
        from helpers.prettyexception import PRETTYHTTP
        raise PRETTYHTTP(401, 'Unauthorized')
    else:
        redirect(URL(request.application, 'default', 'user', args=['login'],
                      vars=dict(send=URL(args=request.args, vars=request.vars))))


def index():
    response.view = '%s/admin/home/index.html' % CONFIG_THEME
    return dict(morris_area_chart = users.history('chart', 'auth'), list_history = users.history('list', 'auth', session.user_timezone))


def status():
    return users.to_know(request.args(0))


def history():
    response.view = '%s/admin/home/history.html' % CONFIG_THEME
    return dict(sqlform = users.history('full-list', 'auth', session.user_timezone))


def sessions():
    from users import SessionSetDb
    set_db = SessionSetDb('web2py_session_cas', db)
    response.view = '%s/admin/home/sessions.html' % CONFIG_THEME
    return dict(sessions=set_db.sessions())


def version():
    from _version import get_versions
    version = get_versions()
    if version['error']:
        raise RuntimeError(version['error'])
    return version['version'].split('+')[0]