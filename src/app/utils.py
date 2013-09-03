# -*- coding: utf-8 -*-
import functools
import hashlib
import flask
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
# from models import Base
# from settings import DATABASE
#
#
# engine = create_engine(DATABASE, convert_unicode=True)
# db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
# Base.query = db_session.query_property()
# Session = sessionmaker(bind=engine)
#
#
# def init_db():
#     Base.metadata.create_all(bind=engine)


def login_required(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        if 'username' in flask.session:
            return method(*args, **kwargs)
        flask.flash(u"Только авторизированные пользователи могут делать это.")
        return flask.redirect(flask.url_for('authentication'))
    return wrapper


def password_hash(password):
    hash = hashlib.new('ripemd160')
    hash.update(password)
    return hash.hexdigest()