# -*- coding: utf-8 -*-
import os


basedir = os.path.abspath(os.path.dirname(__file__))


CSRF_ENABLED = True
SECRET_KEY = 'z:;\xd2)\x8ey\xfb\xa3\x84\xc5\xec\xb6G\x05z\xb1J\x00(}\xc8\x03\xbde'
DEBUG = True
# database section
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test-case.db')
USERNAME = 'username'
PASSWORD = 'password'
# other
TABLES_BLACK_LIST = ['association', 'users']