# -*- coding: utf-8 -*-
r"""
    front
    ~~~~~~~

    :copyright: (c) 2013 by Harvey Wang.
"""

from flask import Blueprint, render_template
from ..utils.account import require_login, get_roles

bp = Blueprint('front', __name__)


@bp.route('/')
@require_login
def home():
    """The homepage of the site."""
    return render_template(
        'index.html',
        title="HOME|优意座标后台管理系统".decode("utf8"),
        whitch=0,
        roles=get_roles())
