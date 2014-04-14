# -*- coding: utf-8 -*-
r"""
    check 
    ~~~~~~~

    :copyright: (c) 2013 by Harvey Wang.
"""

from flask import Blueprint
from flask import abort, current_app, g, request
from flask import redirect, render_template, url_for
from ..utils.account import require_staff_check
from ..utils.content_datawrapper import (content_count, list_works, \
                                         get_work, check_action)
     
from ..utils.const import month, work_type, work_class
from ..utils.notification import format_datetime, cover_url

bp = Blueprint('check', __name__)


@bp.route('/works')
@require_staff_check
def works():
    work_counts = []
    for i in range(0, len(work_type)):
        count = content_count(condition="WHERE w.status=0 AND w.check_status=4 AND w.type=%d" % i)
        work_counts.append(count)
    
    works = list_works(table='work',
        condition='WHERE w.status=0 AND w.check_status=4')
    
    return render_template(
        'check/works.html',
        title=u'内容审核|优意坐标后台管理系统',
        work_counts = work_counts,
        works = works)


@bp.route('/work')
@require_staff_check 
def work():
    id = request.args.get('id', 0)
    work = get_work(id)
    w_type = work_class[int(work[0])] 
     
    info = {}
    info['id'] = id
    info['type'] = work[0]
    info['user'] = work[5]
    info['title'] = work[1]
    info['content'] = [work[2]]
    if int(work[0]) == 2:
        pics = work[2].split(';')
        pics = ['http://www.ueue.cc%s' % pic for pic in pics]
        info['content'] = pics
    info['description'] = work[3]
    info['class'] = w_type
    
    action = request.args.get('action')
    if action: 
       check_action(request.args.get('id'), action)

       return redirect(url_for('check.works'))

    return render_template(
       'check/work.html',
       info=info)
