# -*- coding: utf-8 -*-

if ('admin' or 'editor') not in auth.user_groups.values():
    if auth.is_logged_in():
        from helpers.prettyexception import PRETTYHTTP
        raise PRETTYHTTP(401, 'Unauthorized')
    else:
        redirect(URL(request.application, 'default', 'user', args=['login'],
                      vars=dict(send=URL(args=request.args, vars=request.vars))))

from apps import Apps


def manage():
    apps = Apps(db, auth)
    response.view = '%s/admin/apps/manage.html' % CONFIG_THEME
    return dict(grid = apps.grid())


def action():
    apps = Apps(db, auth)
    if apps.action(request.args(0), request.args(1)):
        result = '<div class="alert">Changes saves, reload the page.</div>'
    else:
        result = '<div class="alert alert-error">Error, trying to perform the action.</div>'

    return result