#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Decorator for auth mod in Microbe
"""

import ldap3 as ldap

from functools import wraps
from flask import current_app, request
from sqlalchemy.sql.expression import or_
from flask.ext.login import current_user, login_user

from microbe.database import db
from microbe.mods.users.models import User

__author__ = u'TROUVERIE Joachim'


def auth_required(fn):
    """Authentification required decorator"""
    @wraps(fn)
    def decorated(*args, **kwargs):
        # login_required
        login_disabled = current_app.login_manager._login_disabled
        current_user_auth = current_user.is_authenticated
        if login_disabled or current_user_auth:
            return fn(*args, **kwargs)
        # not logged in
        else:
            # test http basic auth
            auth = request.authorization
            if auth and auth.username:
                user = User.query.filter(or_(auth.username == User.name,
                                             auth.username == User.email)).first()
                if user:
                    result = user.check_password(auth.password)
                    if result:
                        return fn(*args, **kwargs)
                # try ldap auth
                user = _ldap_auth(auth.username, auth.password)
                if user:
                    # add user to db
                    db.session.add(user)
                    db.session.commit()
                    login_user(user)
                    return fn(*args, **kwargs)
        return current_app.login_manager.unauthorized()
    return decorated


def _ldap_auth(username, password):
    """If LDAP is enabled in config look for given username
    and try to login into the LDAP server
    :param username: User name
    :param password: User password
    :return: User object or None according to given username exists in LDAP
    """
    user = None
    if current_app.config.get('LDAP_ENABLED'):
        # config keys
        server = current_app.config.get('LDAP_SERVER')
        basedn = current_app.config.get('LDAP_BASE_DN')
        username_key = current_app.config.get('LDAP_NAME_KEY')
        mail_key = current_app.config.get('LDAP_MAIL_KEY')
        # connect to LDAP
        try:
            ldap_server = ldap.Server(server, get_info=ldap.ALL)
            ld = ldap.Connection(ldap_server, auto_bind=True)
            # look for user with this username
            filters = '(!({0}={1})({2}={1}))'.format(username_key, username, mail_key)
            res = ld.search(basedn, filters)
            if res and len(ld.entries) == 1:
                # get user credentials
                entry = ld.entries[0]
                uid = entry.get(username_key)
                mail = entry.get(mail_key)
                # login using ldap
                if ld.rebind(uid, password):
                    # - LDAP auth succeded
                    user = User(uid, password, mail)
        except Exception:
            pass
        finally:
            ld.unbind()
    return user
