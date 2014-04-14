# -*- coding: utf-8 -*-
r"""
    mail
    ~~~~~~~

    Utility for generating verify-code.

    :copyright: (c) 2013 by Harvey Wang.
"""

import time
import base64
import hashlib
from flask.ext.mail import Mail, Message
from flask import current_app, render_template
from threading import Thread

# 利用当前管理员的信息生成验证码
def create_verify_token(user):
    timestamp = int(time.time())
    secret = current_app.secret_key
    token = '%s%s%s%s' % (secret, timestamp, user.accid, user.token)
    hsh = hashlib.sha1(token).hexdigest()
    return str(base64.b32encode('%s|%s%s' % (timestamp, user.accid, hsh)))[0:16]

def send_async_mail(msg):
    mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender = sender, recipients = recipients)
    msg.body = text_body
    msg.html = html_body
    thr = Thread(target = send_async_mail, args = [msg])
    thr.start()

def send_verify_code(username, useremail, verifycode, sender):
    send_email("您的UE坐标邀请码",
        sender[0],
        [useremail],
        render_template("user/verify_code.txt",
            username = username,
            verifycode = verifycode),
        render_template("user/verify_code.html",
            username = username,
            verifycode = verifycode),
        )

mail = Mail()