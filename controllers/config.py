# -*- coding: utf-8 -*-

if 'admin' not in auth.user_groups.values():
    if auth.is_logged_in():
        from helpers.prettyexception import PRETTYHTTP
        raise PRETTYHTTP(401, 'Unauthorized')
    else:
        redirect(URL(request.application, 'default', 'user', args=['login'],
                      vars=dict(send=URL(args=request.args, vars=request.vars))))

from gluon.contrib.appconfig import AppConfig
from config import AppConfigLoader


def flush():
    if AppConfig(reload=True):
        response.flash = 'Configuration reloaded'


def manage():
    if request.env.request_method == 'GET':
        response.view = '%s/admin/config/manage.html' % CONFIG_THEME
        return dict(settings=AppConfig(reload=True), tab=None)
    elif request.env.request_method == 'POST':
        response.view = '%s/admin/config/manage.html' % CONFIG_THEME
        config = AppConfigLoader()
        if config.set_conf(request.vars):
            response.flash = 'Configuration updated'
            return dict(settings=AppConfig(reload=True), tab=request.vars.section)

        response.flash = 'Uppss error...'
        return dict(settings=AppConfig(reload=True), tab=request.vars.section)