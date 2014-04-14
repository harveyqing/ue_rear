# -*- coding: utf-8 -*-
r"""
    front
    ~~~~~~~

    :copyright: (c) 2013 by Harvey Wang.
"""

from flask import Blueprint
from flask import abort, current_app, g, request
from flask import redirect, render_template, url_for
from ..utils.account import require_staff_user
from ..utils.frontdb import QueryDB
from ..utils.mail import *
from ..models import Users, db

bp = Blueprint('user', __name__)

user_state = {
    0: u"没有激活",
    1: u"已冻结",
    2: u"未初始化",
    3: u"未设置个人信息",
    4: u"普通用户",
    5: u"申请认证",
    6: u"已认证"}

sex = {'0': u"男", '1': u"女", '2': u"机构"}

verify = {'0': u"尚未认证", '1': u"文创人", '2': u"媒体人", '3': u"专业机构"}


@bp.route('/user_admin')
@require_staff_user
def user_admin():
    query = """SELECT u.uid, u.account, b.job, u.status, p.sex
                     FROM user AS u
                     LEFT OUTER JOIN basicinfo AS b
                     ON u.uid = b.bsc_id
                     LEFT OUTER JOIN property AS p
                     ON u.uid = p.proper_id
                     ORDER BY u.uid
                 """

    querydb = QueryDB(g.fdb, query)
    querydb.getall()
    userinfo = querydb.results

    return render_template(
        'user/user-admin.html',
        title='用户管理|优意座标后台管理系统'.decode('utf8'),
        userinfo=userinfo,
        count=querydb.count,
        user_state=user_state,
        sex=sex)


@bp.route('/user_view', methods=['POST', 'GET'])
@require_staff_user
def user_view():
    uid = request.args.get('uid')

    if uid:
        query = """SELECT u.account, u.uid, b.uname, b.area, b.job,
                                b.organ, b.birth, b.height, b.weight, b.extend,
                                p.ptype, b.vertext, u.status
                        FROM user AS  u
                        LEFT OUTER JOIN basicinfo AS b
                        ON u.uid = b.bsc_id
                        LEFT OUTER JOIN property AS p
                        ON u.uid = p.proper_id
                        WHERE u.uid = %s
                    """ % str(uid)

        querydb = QueryDB(g.fdb, query)
        querydb.getone()
        userinfo = querydb.results

        return render_template(
            'user/user-admin-view.html',
            title='用户详细信息|优意座标后台管理系统'.decode('utf8'),
            userinfo=userinfo,
            verify=verify)

    return abort(404)


@bp.route('/user_lock', methods=['GET'])
@require_staff_user
def user_lock():
    l_uid = request.args.get('lock')
    if l_uid:
        lock_user(g.fdb, l_uid)
        return redirect(url_for('user.user_view', uid=l_uid))

    ul_uid = request.args.get('unlock')
    if ul_uid:
        unlock_user(g.fdb, ul_uid)
        return redirect(url_for('user.user_view', uid=ul_uid))


@bp.route('/gen_invitation_code', methods=['POST', 'GET'])
@require_staff_user
def gen_invitation_code():

    fdb = g.fdb

    if request.method == 'GET':
        uid = request.args.get('uid')
        if uid:
            query = """SELECT u.uid, u.email, u.account,
                                           p.ptype, b.vertext, u.status
                              FROM user AS  u
                              LEFT OUTER JOIN basicinfo AS b
                              ON u.uid = b.bsc_id
                              LEFT OUTER JOIN property AS p
                              ON u.uid = p.proper_id
                              WHERE u.uid = %s
                          """ % str(uid)

            querydb = QueryDB(fdb, query)
            querydb.getone()
            userinfo = querydb.results

            return render_template(
                'user/user-gen-invitation-code.html',
                title='生成邀请码|优意座标后台管理系统'.decode('utf8'),
                userinfo=userinfo,
                verify=verify)

        abort(404)

    if request.method == 'POST':
        uid = request.args.get('uid')
        email = request.form['email']
        realname = request.form['realname']
        vertext = request.form['vertext']
        vertype = request.form['radios']

        invitation_code = create_verify_token(g.user)

        send_verify_code(realname, email, invitation_code, current_app.config['ADMINS'][0])

        cur = g.fdb.cursor() # here gose change
        upStatus = "UPDATE user SET status = 5 WHERE uid = %s" % str(uid)
        upVer = "UPDATE basicinfo SET vertext = '%s', vercode = '%s' WHERE bsc_id = %s" %  \
            (vertext, invitation_code, str(uid))
        upType = "UPDATE property SET ptype = %d WHERE proper_id = %s" % (int(vertype), str(uid))
        try:
            cur.execute("set names gbk")
            cur.execute(upStatus)
            cur.execute(upType)
            cur.execute(upVer.encode('gbk'))
            cur.connection.commit()
        except:
            cur.connection.rollback()

        return redirect(url_for("user.user_admin"))


@bp.route('/user_verify_admin', methods=['POST', 'GET'])
@require_staff_user
def user_verify_admin():
    """ 申请验证用户查看
    """
    query = """SELECT u.uid, u.account, b.job, p.ptype, p.sex
                     FROM user AS u
                     LEFT OUTER JOIN basicinfo AS b
                     ON u.uid = b.bsc_id
                     LEFT OUTER JOIN property AS p
                     ON u.uid = p.proper_id
                     WHERE u.status = "5" AND u.status <> "1"
                     ORDER BY u.uid
                 """
    fdb = g.fdb

    querydb = QueryDB(fdb, query)
    querydb.getall()
    userinfo = querydb.results
    workcount = querydb.count

    return render_template(
        'user/user-verify-admin.html',
        title='认证审核|优意座标后台管理系统'.decode('utf8'),
        userinfo=userinfo,
        workcount=workcount,
        verify=verify,
        sex=sex)


@bp.route('/user_verify', methods=['POST', 'GET'])
@require_staff_user
def user_verify():
    """ 验证用户认证申请
    """
    fdb = g.fdb
    uid = request.args.get('uid')
    if uid and request.method == 'GET':

        query = """SELECT u.uid, u.account, b.vertext, c.sinawb, p.ptype
                         FROM user AS u
                         LEFT OUTER JOIN basicinfo AS b
                         ON u.uid = b.bsc_id
                         LEFT OUTER JOIN property AS p
                         ON u.uid = p.proper_id
                         LEFT OUTER JOIN contactinfo AS c
                         ON u.uid = c.con_id
                         WHERE u.uid = %s
                     """ % uid
        querydb = QueryDB(fdb, query)
        querydb.getone()
        userinfo = querydb.results

        return render_template(
            '/user/user-verify.html',
            title='认证审核|优意座标后台管理系统'.decode('utf8'),
            userinfo=userinfo)

    if request.method == 'POST':
        uid = request.args.get('uid')

        # realname = request.form['realname']
        vertext = request.form['vertext']
        vertype = request.form['radios']

        cur = g.fdb.cursor() # here gose change
        upStatus = "UPDATE user SET status = 6 WHERE uid = %s" % str(uid)
        upVer = "UPDATE basicinfo SET vertext = '%s' WHERE bsc_id = %s" %  \
            (vertext, str(uid))
        upType = "UPDATE property SET ptype = %d WHERE proper_id = %s" % (int(vertype), str(uid))
        try:
            cur.execute("set names gbk")
            cur.execute(upStatus)
            cur.execute(upType)
            cur.execute(upVer.encode('gbk'))
            cur.connection.commit()
        except:
            cur.connection.rollback()

        return redirect(url_for("user.user_verify_admin"))

    return abort(404)


def lock_user(fdb, uid):
    cur = fdb.cursor()
    lookup = "SELECT status FROM user WHERE uid = %s" % str(uid)
    cur.execute(lookup)
    row = cur.fetchone()

    global db
    newlock = Users(int(uid), int(row[0]))
    db.session.add(newlock)
    db.session.commit()

    update = "UPDATE user SET status = 1 WHERE uid = %s" % str(uid)
    try:
        cur.execute(update)
        cur.connection.commit()
    except:
        cur.connection.rollback()


def unlock_user(fdb, uid):
    lockeduser = Users.query.filter_by(uid=uid).first()

    cur = fdb.cursor()
    update = "UPDATE user SET status = %s WHERE uid = %s" % \
        (str(lockeduser.orginstate), str(uid))
    try:
        cur.execute(update)
        cur.connection.commit()
    except:
        cur.connection.rollback()

    global db
    db.session.delete(lockeduser)
    db.session.commit()

