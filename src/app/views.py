# -*- coding: utf-8 -*-
from app import app
from flask import render_template, request, session, redirect, url_for, flash
from utils import password_hash, db_session
from models import Base, Authors, Books
from sqlalchemy import select
from utils import engine
from forms import LoginForm


@app.route('/', methods=['GET'])
def test_case():
    return render_template('test-case.html')

@app.route('/authentication', methods=['GET', 'POST'])
def authentication():
    form = LoginForm(request.form)
    if request.method == 'GET':
        return render_template('authentication.html')
    elif request.method == 'POST' and form.validate():
        username = form.username.data
        password = password_hash(form.password.data)
        user = db_session.query(Users).filter_by(username=username).first()

        if user is not None and username == user.username and password == user.password:
            session['username'] = username
        else:
            flash(u"Указанной вами связки логина и пароля не существует, возможно вы ввели неправильный логин или пароль, мы могли бы сказать конкретнее, но вдруг вы пытаетесь подобрать логин для брута...")
        return redirect(url_for('authentication'))

    elif 'logout' in request.form:
        session.pop('username', None)
        return redirect(url_for('authentication'))

    else:
        flash(u'Указанной вами связки логина и пароля не существует, возможно вы ввели неправильный логин или пароль, мы могли бы сказать конкретнее, но вдруг вы пытаетесь подобрать логин для брута...')
        return redirect(url_for('authentication'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'GET':
        metadata = Base.metadata
        tables = metadata.tables.keys()
        black_list = ['association', 'users']
        for table in black_list: tables.remove(table)
        return render_template('admin.html',
                               tables=tables
        )

    elif request.method == 'POST':
        table_name = request.form['table-name']
        tables = {
            'books': [Books, 'id', 'book_title'],
            'authors': [Authors, 'id', 'author_name']
        }
        selected = select([tables[table_name][0]])
        rows = engine.execute(selected)
        rows_list = list(rows)
        rows_list.insert(0, tables[table_name][1:])
        return render_template('admin.html',
                               rows=rows_list,
                               table_name=table_name)