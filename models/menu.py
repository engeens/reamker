# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B('web',SPAN(2),'py'),XML('&trade;&nbsp;'),
                  _class="navbar-brand",_href="http://www.web2py.com/",
                  _id="web2py-logo")
response.title = request.application.replace('_',' ').title()
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Your Name <you@example.com>'
response.meta.description = 'a cool new app'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (CAT(I(_class='fa fa-dashboard fa-fw'), T(' Home ')), False, URL('admin', 'index')),
    (CAT(I(_class='fa fa-edit fa-fw'), T(' Manage '), SPAN(_class='fa arrow')), False, '#', [
        (CAT(I(_class='fa fa-user fa-fw'), T(' Users ')), False, URL('users', 'manage')),
        (CAT(I(_class='fa fa-th-list fa-fw'), T(' Apps ')), False, URL('apps', 'manage'))
    ]),
    (CAT(I(_class='fa fa-wrench fa-fw'), T(' Settings ')), False, URL('config', 'manage')),
    (CAT(I(_class='fa fa-history fa-fw'), T(' History '), SPAN(_class='fa arrow')), False, '#', [
        (CAT(I(_class='fa fa-user fa-fw'), T(' User logs ')), False, URL('admin', 'history')),
        (CAT(I(_class='fa fa-th-list fa-fw'), T(' User sessions ')), False, URL('admin', 'sessions')),
    ]),

    (CAT(I(_class='fa fa-home fa-fw'), T(' APP HOME ')), False, URL('default', 'index')),
]

if auth.is_logged_in():

    def custom_navbar(auth_navbar):
        bar = auth_navbar
        user = bar["user"]
        toggletext = "%s %s" % (bar["prefix"], user)
        toggle = A(toggletext,
                   _href="#",
                   _class="dropdown-toggle",
                   _rel="nofollow",
                   **{"_data-toggle": "dropdown"})

        li_profile = LI(A(I(_class="icon icon-lock glyphicon glyphicon-lock"), ' ',
                          "Change password",
                          _href=bar["change_password"], _rel="nofollow"))

        li_logout = LI(A(I(_class="icon icon-off glyphicon glyphicon-off"), ' ',
                         "logout",
                         _href=bar["logout"], _rel="nofollow"))

        li_admin = ''
        if ('admin' or 'editor' or 'viewer') in auth.user_groups.values():
            if request.controller == 'admin':
                toggle = A(I(_class="fa fa-user fa-fw"),I(_class="fa fa-caret-down"),
                           _href="#",
                           _class="dropdown-toggle",
                           _rel="nofollow",
                           **{"_data-toggle": "dropdown"})

                li_admin = LI(A(I(_class="icon-book"), ' ',
                                "Apps home",
                                _href=URL("home", "index"), rel="nofollow"))
            else:

                li_admin = LI(A(I(_class="icon-book"), ' ',
                                 "Admin dashboard",
                                 _href=URL("admin", "index"), rel="nofollow"))

        dropdown = UL(li_profile,
                      LI('', _class="divider"),
                      li_admin,
                      LI('', _class="divider"),
                      li_logout,
                      _class="dropdown-menu", _role="menu")

        return LI(toggle, dropdown, _class="dropdown")

    navbar = custom_navbar(auth.navbar('Welcome',mode='bare'))

