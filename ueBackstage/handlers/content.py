# -*- coding: utf-8 -*-
r"""
    front
    ~~~~~~~

    :copyright: (c) 2013 by Harvey Wang.
"""

from flask import Blueprint
from flask import abort, current_app, g, request
from flask import redirect, render_template, url_for
from ..utils.account import require_staff_content
from ..utils.content_datawrapper import content_count, list_works 
from ..utils.const import month, work_type
from ..utils.notification import format_datetime, cover_url

bp = Blueprint('content', __name__)


@bp.route('/content_manage')
@require_staff_content
def content_manage():
    work_counts = []
    for i in range(0, len(work_type)):
        work_counts.append(content_count(i))


    return str(work_counts) 


@bp.route('/content_works')
@require_staff_content
def content_works():
    work_counts = []
    for i in range(0, len(work_type)):
        work_counts.append(content_count(type=i))

    works = list_works()

    return render_template(
        'content/content-manage.html',
        title=u'内容管理|优意坐标后台管理系统',
        work_counts = work_counts,
        works = works)



