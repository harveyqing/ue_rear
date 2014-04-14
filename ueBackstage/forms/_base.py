# -*- coding: utf-8 -*-
r"""
    _base
    ~~~~~~~

    Base form class for Form objects.
    :copyright: (c) 2013 by Harvey Wang.
"""

from flask.ext.wtf import Form

__all__ = ['BaseForm']


class BaseForm(Form):
    def __init__(self, *args, **kwargs):
        self._obj = kwargs.get('obj', None)
        super(BaseForm, self).__init__(*args, **kwargs)
