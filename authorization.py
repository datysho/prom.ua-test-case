#!/usr/bin/python
# -*- coding: utf-8 -*-
import flask, flask.views

users = {'test':'test'}

class Authorization(flask.views.MethodView):
    def get(self):
        return flask.render_template('authorization.html')

    def post(self):
        if 'logout' in flask.request.form:
            flask.session.pop('username', None)
            return flask.redirect(flask.url_for('authorization'))

        required = ['username', 'password']
        for r in required:
            if r not in flask.request.form:
                flask.flash("Error: {0} is required.".format(r))
                return flask.redirect(flask.url_for('authorization'))

        username = flask.request.form['username']
        password = flask.request.form['password']
        if username in users and users[username] == password:
            flask.session['username'] = username
        else:
            flask.flash(u"Указанной вами связки логина и пароля не существует в нашей базе данных, возможно вы ввели неправильный логин или пароль, мы конечно могли бы сказать конкретнее, но вдруг вы окажетесь хакером и попытаться сбрутить пароль существуюшего пользователя.")
        return flask.redirect(flask.url_for('authorization'))
