# -*- coding: utf-8 -*-

from gluon import SPAN, A, URL
from helpers.log import logger
from gluon.contrib.appconfig import AppConfig
from model import DataBase
from gluon.sqlhtml import SQLFORM
from gluon.globals import current
from helpers.utils import thumb

class Apps(object):
    def __init__(self, db, define_tables=True):
        self.db = db
        if define_tables:
            DataBase(db=self.db, tables=['t_apps'])
        self.session = current.session
        self.request = current.request
        self.config = AppConfig()

    def grid(self):
        fields = [self.db.t_apps.f_title, self.db.t_apps.f_is_active, self.db.t_apps.f_order_id]

        fields[1].represent = lambda value, row: SPAN('active', _class='label label-success') \
            if value == True else SPAN('disable', _class='label label-danger')

        links = [
            lambda row: A('Enable',  _class="btn-success btn-mini", callback=URL('apps', 'action', args=[str(row.id), 'enable']))
            if row.f_is_active == False else "",
            lambda row: A('Disable', _class="btn-danger btn-mini", callback=URL('apps', 'action', args=[str(row.id), 'disable']))
            if row.f_is_active == True else "",]

        self.db.t_apps.f_thumbnail.readable = True
        grid = SQLFORM.grid(self.db.t_apps,
                                 ui='web2py',
                                 fields=fields,
                                 links=links,
                                 csv=False,
                                 searchable=True)
        return grid

    def get(self):
        """
        :return: list
        """
        return self.db(self.db.t_apps.f_is_active == True).select( orderby=self.db.t_apps.f_order_id)

    def action(self, app_id, action):
        """The app can be enable or disable
        :param app_id:
        :param action: enable or disable
        :return:True or False
        """
        try:
            query = self.db(self.db.t_apps.id == app_id).select().first()
            if action == 'disable':
                query.update_record(f_is_active=False)
            elif action == 'enable':
                query.update_record(f_is_active=True)

            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error(str(e))
            return False
        return True