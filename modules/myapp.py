# -*- coding: utf-8 -*-
from gluon.http import HTTP
from helpers.log import logger
from gluon.globals import current
from gluon.html import URL
from gluon.tools import Mail
from gluon.contrib.appconfig import AppConfig
from helpers.prettyexception import PRETTYHTTP


def str2bool(v):
  return v.lower() in ("yes", "true", "1")


class Access(object):
    def __init__(self, db, auth):
        self.db = db
        self.auth = auth
        self.config = AppConfig()
        self.session = current.session
        self.request = current.request

        # Not allow
        self.auth.settings.actions_disabled.append('register')
        self.auth.settings.actions_disabled.append('request_reset_password')
        self.auth.settings.actions_disabled.append('retrieve_password')
        self.auth.settings.actions_disabled.append('profile')
        self.auth.settings.registration_requires_approval = False
        self.auth.settings.registration_requires_verification = False

        #Set general settings
        self.auth.settings.expiration = int(self.config.take('general.session_expiration'))
        self.auth.settings.remember_me_form = self.config.take('general.remember_me_form')

        if self.config.take('general.auth_type') == 'ldap':
                self.auth.settings.login_onvalidation = [lambda form: self.__define_domain(form.vars.email.split('@')[1])]

        elif self.config.take('general.auth_type') == 'local':
            if str2bool(self.config.take('auth_local.enable_change_password')) is not True:
                self.auth.settings.actions_disabled.append('change_password')

        # Disable group for each user
        self.auth.settings.create_user_groups = False
        self.auth.settings.login_next = URL('home', 'index')


    def __define_domain(self, domain):
        domain = domain.lower()
        try:
            count = 1
            while True:
                ldap_connection = 'auth_ldap_0' + str(count)
                if self.config.__getattribute__(ldap_connection).is_active:
                    if self.config.__getattribute__(ldap_connection).domain == domain:
                        self.__load_ldap_connection(ldap_connection)
                        break

                count += 1

        except Exception as e:
            #from log import logger
            #logger.warning("Not possible to connect to LDAP.")
            raise PRETTYHTTP(400, 'Upppss, the domain you have type, I could not find it...')

    def __load_ldap_connection(self, ldap):
        try:
            if self.config.__getattribute__(ldap).is_active:
                from gluon.contrib.login_methods.ldap_auth import ldap_auth
                if self.config.auth.auth_local_database:
                    self.auth.settings.login_methods.append(ldap_auth(
                        mode=self.config.__getattribute__(ldap).mode,
                        secure=self.config.__getattribute__(ldap).secure,
                        server=self.config.__getattribute__(ldap).server,
                        port=self.config.__getattribute__(ldap).port,
                        base_dn=self.config.__getattribute__(ldap).base_dn,
                        allowed_groups=self.config.__getattribute__(ldap).allowed_groups,
                        group_dn=self.config.__getattribute__(ldap).group_dn,
                        group_name_attrib=self.config.__getattribute__(ldap).group_name_attrib,
                        group_member_attrib=self.config.__getattribute__(ldap).group_member_attrib,
                        group_filterstr=self.config.__getattribute__(ldap).group_filterstr,
                        manage_user=True,
                        user_firstname_attrib='cn:1',
                        user_lastname_attrib='cn:2',
                        user_mail_attrib='mail',
                        db=self.db,

                    ))

                else:
                    self.auth.settings.login_methods = [(ldap_auth(
                        mode=self.config.__getattribute__(ldap).mode,
                        secure=self.config.__getattribute__(ldap).secure,
                        server=self.config.__getattribute__(ldap).server,
                        port=self.config.__getattribute__(ldap).port,
                        base_dn=self.config.__getattribute__(ldap).base_dn,
                        allowed_groups=self.config.__getattribute__(ldap).allowed_groups,
                        group_dn=self.config.__getattribute__(ldap).group_dn,
                        group_name_attrib=self.config.__getattribute__(ldap).group_name_attrib,
                        group_member_attrib=self.config.__getattribute__(ldap).group_member_attrib,
                        group_filterstr=self.config.__getattribute__(ldap).group_filterstr,
                        manage_user=True,
                        user_firstname_attrib='cn:1',
                        user_lastname_attrib='cn:2',
                        user_mail_attrib='mail',
                        db=self.db

                    ))]
        except Exception as e:
            #from log import logger
            #logger.warning("Not possible to connect to LDAP.")
            raise PRETTYHTTP(500, e)


class Mailer(Mail):
    def __init__(self,):
        Mail.__init__(self)
        self.config = AppConfig()
        self.settings.tls = self.config.take('smtp.tls')
        self.settings.server = self.config.take('smtp.server')
        self.settings.sender = self.config.take('smtp.sender')
        if self.config.take('smtp.login'):
            self.settings.login = self.config.take('smtp.login')
        self.request = current.request

    def build_message_from_template(self, event_type, render_html=True, **kwargs):
        from gluon.html import XML
        from gluon.template import render
        path = self.request.folder + '/' + 'private/email_templates/' + event_type + '.html'
        template = str(XML(open(path).read()))

        if not template:
            logger.warning("App notification message, you need to define an email template for %s event \n %s" % (event_type, str(kwargs)))

        self.render = lambda text: render(text, context=dict(event_type=event_type, **kwargs))
        try:
            if render_html:
                html_message = self.render(template)
                import html2text
                plain_message = html2text.html2text(html_message)

        except Exception as e:
            html_message = ''
            logger.warning("Render email template %s. Please, edit the email template carefully" % event_type)
            logger.warning(str(e))

        return dict(message=[plain_message, html_message], reply_to=self.config.take('smtp.reply_to'))


    def send_email(self, to, subject, event_type, attachments=[], render_html=True, **kwargs):
        message = self.build_message_from_template(event_type, render_html, **kwargs)
        try:
            if attachments:
                attachment = []
                for i in attachments:
                    attachment.append(self.Attachment(i))
                params = dict(to=to, subject=subject, attachments=attachment, bcc=self.config.take('smtp.bcc_to'), **message)
            else:
                params = dict(to=to, subject=subject, bcc=self.config.take('smtp.bcc_to'), **message)
            sent = self.send(**params)
        except Exception, e:
            logger.error("Fail sending email to: %s" % to)
            logger.error(str(e))
            sent = False

        return sent

