# -*- coding: utf-8 -*-

if 'admin' not in auth.user_groups.values():
    if auth.is_logged_in():
        from helpers.prettyexception import PRETTYHTTP
        raise PRETTYHTTP(401, 'Unauthorized')
    else:
        redirect(URL(request.application, 'default', 'user', args=['login'],
                      vars=dict(send=URL(args=request.args, vars=request.vars))))


def manage():
    #users = Users(db, auth)
    grid = users.grid()
    response.view = '%s/admin/users/manage.html' % CONFIG_THEME
    return dict(grid=grid)


def action():
    if users.action(request.args(0), request.args(1)):
        response.flash = T.M('Action done, please [[reload %s]] the page to see the changes') % URL(args=request.args, vars=request.get_vars)
    else:
        response.flash = 'Error, trying to perform the action'