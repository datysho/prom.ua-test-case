#!/usr/bin/python
# -*- coding: utf-8 -*-
import flask, flask.views

users = {'test':'test'}

class TestCase(flask.views.MethodView):
    def get(self):
        return flask.render_template('test-case.html')