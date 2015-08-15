#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Users module for Microbe app
"""

from microbe.mods.users.models import Users

__author__ = 'TROUVERIE Joachim'


def load_user(username):
    """Load user from config

    :param username: user name
    :type username: str
    """
    return Users.get(username)
