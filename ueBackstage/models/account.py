# -*- coding: utf-8 -*-
r"""
    account
    ~~~~~~~

    Data model of accounts.

    :copyright: (c) 2013 by Harvey Wang.
"""

from datetime import datetime
from werkzeug import security
from ._base import db, SessionMixin

__all__ = ['Account']


class Account(db.Model, SessionMixin):
    accid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, index=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    role = db.Column(db.String(10), default='new')
    active = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    created = db.Column(db.DateTime, default=datetime.utcnow)
    token = db.Column(db.String(20))

    def __init__(self, **kwargs):
        self.token = self.create_token(16)

        if 'username' in kwargs:
            username = kwargs.pop('username')
            self.username = username.lower()

        if 'password' in kwargs:
            rawpass = kwargs.pop('password')
            self.password = self.create_password(rawpass)

        if 'email' in kwargs:
            email = kwargs.pop('email')
            self.email = email.lower()

        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return self.username

    def __repr__(self):
        return '<Account: %r at %r>' % (self.username, self.email)

    @staticmethod
    def create_password(rawpass):
        passwd = '%s%s' % (rawpass, db.app.config['PASSWORD_SECRET'])
        return security.generate_password_hash(passwd)

    @staticmethod
    def create_token(length=16):
        return security.gen_salt(length)

    @property
    def is_admin(self):
        # accid == 1, the `super administrator`
        if self.accid == 1 or self.role == 'admin':
            return True

    @property
    def is_staff(self):
        if self.role != 'new':
            return True
        return False

    def check_password(self, rawpass):
        passwd = '%s%s' % (rawpass, db.app.config['PASSWORD_SECRET'])
        return security.check_password_hash(self.password, passwd)

    def change_password(self, rawpass):
        self.password = self.create_password(rawpass)
        self.token = self.create_token()
        return self
