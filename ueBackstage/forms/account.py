# -*- coding: utf-8 -*-
r"""
    account
    ~~~~~~~

    Account form.
    :copyright: (c) 2013 by Harvey Wang.
"""

from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Length

from ._base import BaseForm
from ..models import Account


class SigninForm(BaseForm):
    account = TextField(
        Account,
        validators=[DataRequired(), Length(min=3, max=40)],
        description='Username')

    password = PasswordField('Password', validators=[DataRequired()])
