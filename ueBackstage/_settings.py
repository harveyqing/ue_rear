# -*- coding: utf-8 -*-
import os

DEBUG = True
TESTING = False
VERIFY_EMAIL = True
VERIFY_USER = True

ROOT_FOLDER = os.path.dirname(os.path.abspath(__file__))
if os.path.exists('public/static'):
    STATIC_FOLDER = os.path.join(os.getcwd(), 'public', 'static')
else:
    STATIC_FOLDER = os.path.join(ROOT_FOLDER, 'public', 'static')

#: site
SITE_TITLE = 'ue Backstage'
SITE_URL = '/'
SITE_URL = 'http://www.ueue.cc/'

#: about page url
# SITE_ABOUT = '/node/about'

# SITE_ANALYTICS = 'UA-xxx-xxx'

#: session
SESSION_COOKIE_NAME = '_s'
#SESSION_COOKIE_SECURE = True
PERMANENT_SESSION_LIFETIME = 3600 * 24 * 30 	# coocie有效期为一个月

#: account
SECRET_KEY = 'secret key'
PASSWORD_SECRET = 'password secret'

#: sqlalchemy
# MYSQL_HOST = 'localhost'
# MYSQL_PORT = '3306'
# MYSQL_USER = 'root'
# MYSQL_PASS = ''
# MYSQL_DB = 'ueBackstage'
SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % os.path.join(

    os.getcwd(), 'db.sqlite'
)	# 开发时数据库为sqlite，数据库至当前工作目录
# SQLALCHEMY_POOL_SIZE = 100
# SQLALCHEMY_POOL_TIMEOUT = 10
# SQLALCHEMY_POOL_RECYCEL = 3600

# mail server settings
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = "harveyqing@gmail.com"
MAIL_PASSWORD = "wangjinshiwo"

# administrator list
ADMINS = ['harveyqing@gmail.com']

#: cache settings
# find options on http://pythonhosted.org/Flask-Cache/
# CACHE_TYPE = 'simple'

#: i18n settings
# BABEL_DEFAULT_LOCALE = 'zh'
# BABEL_SUPPORTED_LOCALES = ['zh']
