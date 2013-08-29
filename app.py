#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, redirect, render_template, views
import settings

# Views
from authorization import Authorization
from test_case import TestCase

class View(views.MethodView):
    def get(self):
        return render_template('base.html')

app = Flask(__name__)
app.secret_key = settings.secret_key
app.debug = settings.debug

# Routes
app.add_url_rule('/authorization/',
                 view_func=Authorization.as_view('authorization'),
                 methods=["GET", "POST"])
app.add_url_rule('/',
                 view_func=TestCase.as_view('test-case'),
                 methods=["GET"])

app.run()