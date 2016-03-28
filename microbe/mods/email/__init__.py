#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Email support for Microbe
"""

from flask import copy_current_request_context
from flask.ext.mail import Message, Mail

from threading import Thread


mail = Mail()


def send_email(subject, recipients, text_body=u'', html_body=u''):
    """Send email asynchronously
    :param app: Flask app
    :param subject: email subject
    :param recipients: email recipients
    :param text_body: email text body
    :param html_body: email html body
    """
    sender = u'no-reply@microbe.app'
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html_body = html_body

    @copy_current_request_context
    def _send_mail(msg):
        mail.send(msg)

    thr = Thread(target=_send_mail, args=[msg])
    thr.start()
