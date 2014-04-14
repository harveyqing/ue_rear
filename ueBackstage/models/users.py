# -*- coding: utf-8 -*-
r"""
    users
    ~~~~~~~

    Data model of users.

    :copyright: (c) 2013 by Harvey Wang.
"""

from ._base import db, SessionMixin

__all__ = ['Users']


class Users(db.Model, SessionMixin):
    uid = db.Column(db.Integer, primary_key=True)
    orginstate = db.Column(db.Integer)

    def __init__(self, uid, orginstate):
        self.uid = uid
        self.orginstate = orginstate

    def __str__(self):
        return self.uid

    def __repr__(self):
        return '<User: %r>' % self.uid
