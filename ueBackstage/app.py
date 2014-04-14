# -*- coding: utf-8 -*-

import os
import time
import hashlib
from flask import Flask
from flask import request, g
from datetime import datetime

from .models.account import db
from .models.users import Users
from .utils import frontdb
from .utils.mail import mail
from .utils.notification import (get_numbers, format_datetime, \
     cover_url)
from .utils.content_datawrapper import content_count

def create_app(config=None):
    app = Flask(
                __name__,
                template_folder='templates',
    )
    app.config.from_pyfile('_settings.py')

    if isinstance(config, dict):
        app.config.update(config)
    elif config:
        app.config.from_pyfile(os.path.abspath(config))

    app.static_folder = app.config.get('STATIC_FOLDER')
    app.config.update({'SITE_TIME': datetime.utcnow()})

    register_hooks(app)
    register_jinja(app)
    register_database(app)
    register_mail(app)      
    register_routes(app)

    return app


def register_database(app):
    """Database related configuration."""
    #: prepare for database 
    db.init_app(app)
    db.app = app

def register_mail(app):
    mail.init_app(app)
    mail.app = app

def register_hooks(app):
    """Hooks for request."""
    from .utils.account import get_current_user

    # 每次请求前都尝试获取当前用户
    @app.before_request
    def load_current_user():
        g.user = get_current_user()
        if g.user and g.user.is_staff:
            g._before_request_time = time.time()

            # 这里保存一个前台的数据库连接
            g.fdb = frontdb.connect_db()

    @app.after_request
    def rendering_time(response):
        if hasattr(g, '_before_request_time'):
            delta = time.time() - g._before_request_time
            response.headers['X-Render-Time'] = delta * 1000
        return response

    @app.teardown_request
    def teardown_request(exception):
        """Closes the database again at the end of the request"""
        if hasattr(g, 'fdb'):
            g.fdb.close()

def register_routes(app):
    from .handlers import account, check,  content, front, user
    app.register_blueprint(front.bp, url_prefix='')
    app.register_blueprint(account.bp, url_prefix='/account')
    app.register_blueprint(check.bp, url_prefix='/check')
    app.register_blueprint(content.bp, url_prefix='/content')
    app.register_blueprint(user.bp, url_prefix='/user')

    return app

def register_jinja(app):
    if not hasattr(app, '_static_hash'):
        app._static_hash = {}

    def static_url(filename):
        if filename in app._static_hash:
            return app._static_hash[filename]

        with open(os.path.join(app.static_folder, filename), 'r') as f:
            content = f.read()
            hsh = hashlib.md5(content).hexdigest()

        prefix = app.config.get('SITE_STATIC_PREFIX', '/static/')
        value = '%s%s?v=%s' % (prefix, filename, hsh[:5])
        app._static_hash[filename] = value
        return value

    def show_notification(item):
        return get_numbers(item)

    @app.context_processor
    def register_context():
        return dict(
            static_url=static_url,
            show_notification=show_notification,
            format_datetime=format_datetime,
            cover_url=cover_url,
            content_count=content_count
        )
