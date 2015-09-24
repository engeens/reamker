# -*- coding: utf-8 -*-

from gluon.validators import IS_IMAGE, IS_SLUG, IS_IN_SET, IS_NOT_IN_DB, IS_NOT_EMPTY, IS_INT_IN_RANGE
from gluon.dal import Field
from functools import wraps
from helpers.utils import thumb

class DataBase(object):
    def __init__(self, db=None, auth=None, request=None, tables=['all']):
        self.request = request
        self.db = db
        self.auth = auth
        self.__define_table(tables)

    def __define_table(self, tables):
        if tables[0] == 'all':
            tables = []
            for item in dir(self):
                if item.startswith('_t_'):
                    tables.append(item[1:])
        for table in tables:
            if table not in self.db.tables:
                run = getattr(self, '_'+table)
                run()

    def _depends_on(*args):
        def _define(f):
            def _decorator(self):
                for table in args:
                    if table not in self.db.tables:
                        run = getattr(self, '_'+table)
                        run()
                f(self)
            return wraps(f)(_decorator)
        return _define


    def _t_apps(self):
        self.db.define_table('t_apps',
            Field('f_title', 'string', label='App name'),
            Field('f_picture', 'upload', autodelete=True, label='Icon', requires=[IS_IMAGE()]),
            Field('f_thumbnail', 'upload', autodelete=True, compute=lambda r: thumb(r['f_picture'], nx=300, ny=189)),
            Field('f_link', 'string', label='Link'),
            Field('f_description', 'string', label='Description'),
            Field('f_order_id', 'integer', label='Location priority'),
            Field("f_is_active", "boolean", default=True, label='Active')
        )
