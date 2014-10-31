#! /usr/bin/env python
#-*- coding: utf-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:

"""
    Users module for Microbe app 
"""

__author__ = 'TROUVERIE Joachim'

from microbe.mods.users.models import Users

def load_user(username) :
    """
        Load user from config

        :param username: user name
        :type username: str
    """
    return Users.get(username)