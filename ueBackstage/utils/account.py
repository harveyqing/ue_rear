# -*- coding: utf-8 -*-
r"""
	account
	~~~~~~~

	Utility for account control.

	:copyright: (c) 2013 by Harvey Wang.
"""

import time
import base64
import hashlib
import functools
from flask import current_app, g, request, session
from flask import url_for, redirect
from flask import flash
from ..models import Account

all_roles = {
    'admin': 0,		# 超级管理员
    'new': 1,		# 新添加而尚未激活管理员
    'staff_user': 2,	# 用户管理员
    'staff_content': 3,	# 内容管理员
    'staff_check': 4,	# 内容审核员
}

class require_role(object):

    def __init__(self, role):
        self.role = role   

    def __call__(self, method):
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            if not g.user:	# 尚未登录
                url = url_for('account.signin')
                if '?' not in url:
                    url += '?next=' + request.url # 记录下当前的url，以便登录后跳转
                return redirect(url)    
            if g.user.role == 'admin':
                # this is superuser, have no limitation
                return method(*args, **kwargs)    
            if g.user.role == 'new':
                flash('Please verify your email.', 'warn')
                return redirect('/account/settings')    
            if g.user.role == 'staff_user':
                return redirect('/user/user')    
            if g.user.role == 'staff_content':
                return redirect('/content/content')    
            if g.user.role == 'staff_check':
                return redirect('/check/check')    
            return method(*args, **kwargs)
        return wrapper

require_login = require_role(None)
require_admin = require_role('admin')
require_staff_user = require_role('staff_user')
require_staff_content = require_role('staff_content')
require_staff_check = require_role('staff_check')

# 获取当前浏览页面用户
def get_current_user():
	if 'accid' in session and 'token' in session:
		user = Account.query.get(int(session['accid']))
		if not user:
			return None
		if user.token != session['token']:
			return None
		return user
	return None

# 登录指定用户
def login_user(user, permanent=False):
	if not user:
		return None
	session['accid'] = user.accid
	session['token'] = user.token
	if permanent:
		session.permanent = True
	return user

# 登出当前用户
def logout_user():
	if 'accid' not in session:
		return
	session.pop('accid')
	session.pop('token')

# 创建认证口令
def create_auth_token(user):
	timestamp = int(time.time())
	secret = current_app.secret_key
	token = '%s%s%s%s' % (secret, timestamp, user.accid, user.token)
	hsh = hashlib.sha1(token).hexdigest()
	return base64.b32encode('%s|%s%s' % (timestamp, user.accid, hsh))

# 口令验证
def verify_auth_token(token, expires=30):
	try:
		token = base64.b32decode(token)
	except:
		return None
	bits = token.split('|')
	if len(bits) != 3:
		return None
	timestamp, user_accid, hsh = bits
	try:
		timestamp = int(timestamp)
		user_accid = int(user_accid)
	except:
		return None
	delta = time.time() - timestamp
	if delta < 0:
		return None
	user = Account.query.get(user_accid)
	if not user:
		return None
	secret = current_app.secret_key
	_hsh = hashlib.sha1('%s%s%s%s' % (secret, timestamp, user_accid, user.token))
	if hsh == _hsh.hexdigest():
		return user
	return None

def get_roles():
	roles = []
	global all_roles
	roles.append(all_roles[g.user.role])
	if g.user.role == 'admin':
		roles = list((0, 1, 2, 3, 4))
	return roles
