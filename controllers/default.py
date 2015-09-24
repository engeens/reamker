# -*- coding: utf-8 -*-

def index():
    redirect(URL(request.application, 'home', 'index'))


def user():
    # We define the type of access (login)
    from myapp import Access
    Access(db, auth)
    form = auth()
    form.element(_type='submit')['_class']="btn btn-lg btn-success btn-block"
    response.view = '%s/login/user.html' % CONFIG_THEME
    return dict(form=form)


def init():
    from config import InitApp
    init_app = InitApp(db, INIT_APP, auth)
    status, traceback = init_app.set()
    return traceback