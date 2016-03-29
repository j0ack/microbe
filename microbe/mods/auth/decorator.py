#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Decorator for auth mod in Microbe
"""

from functools import wraps
from flask import current_app, request
from sqlalchemy.sql.expression import or_
from flask.ext.login import current_user

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
        return current_app.login_manager.unauthorized()
    return decorated
