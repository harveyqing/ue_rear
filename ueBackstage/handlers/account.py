# -*- coding: utf-8 -*-
r"""
    account
    ~~~~~~~

    :copyright: (c) 2013 by Harvey Wang.
"""

from flask import Blueprint
from flask import flash, g, request
from flask import redirect, render_template
from ..models import Account
from ..forms import SigninForm
from ..utils.account import login_user, logout_user

__all__ = ['bp']

bp = Blueprint('account', __name__)


@bp.route('/signin', methods=['GET', 'POST'])
def signin():
    next_url = request.args.get('next', '/')

    if g.user:
        return redirect(next_url)

    form = SigninForm()
    if request.method == 'POST' and form.validate_on_submit():
        account = form.account.data
        user = Account.query.filter_by(username=account).first()
        if not user:
            flash('Invalid account or password.')
        else:
            if user.check_password(form.password.data):
                login_user(user)
                return redirect(next_url)
            flash('Invalid account or password.')
    return render_template('account/signin.html', form=form)


@bp.route('/signout')
def signout():
    """Sign out, and redirect."""
    logout_user()

    return redirect('/account/signin')
