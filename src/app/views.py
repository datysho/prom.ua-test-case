# -*- coding: utf-8 -*-
from app import app, db
from flask import render_template, request, session, redirect, url_for, flash
from utils import password_hash
from models import Authors, Books, Users
from sqlalchemy import select
from forms import LoginForm, AddForm, SearchForm
from config import TABLES_BLACK_LIST


@app.route('/', methods=['GET'])
def test_case():

    # item1 = Users(username='test', password='5e52fee47e6b070565f74372468cdc699de89107')
    # item2 = Books(book_title=u'Изучаем Python', authors=[Authors(author_name=u'Марк Лутц')])
    # item3 = Books(book_title=u'Путь к силе', authors=[Authors(author_name=u'В.Л. Муравьев')])
    # db.create_all()
    # db.session.add(item1)
    # db.session.add(item2)
    # db.session.add(item3)
    # db.session.commit()

    return render_template('test-case.html')

@app.route('/authentication/', methods=['GET', 'POST'])
def authentication():
    if request.method == 'GET':
        return render_template('authentication.html')

    if 'logout' in request.form:
        session.pop('username', None)
        return redirect(url_for('authentication'))

    form = LoginForm(request.form)
    if form.validate():
        username = form.username.data
        password = password_hash(form.password.data)
        user = db.session.query(Users).filter_by(username=username).first()

        if username == user.username and password == user.password:
            session['username'] = username
        else:
            flash(u'Указанной вами связки логина и пароля не существует, возможно вы ввели неправильный логин или пароль, мы могли бы сказать конкретнее, но вдруг вы пытаетесь подобрать логин для брута...')
    return redirect(url_for('authentication'))

@app.route('/admin/', methods=['GET'])
def admin():
    return render_template('admin.html')

@app.route('/chose-table/', methods=['GET'])
def chose_table():
    metadata = db.Model.metadata
    tables = metadata.tables.keys()
    for table in TABLES_BLACK_LIST: tables.remove(table)
    return render_template('chose-table.html',
                           tables=tables
    )

@app.route('/edit-table/', methods=['POST', 'GET'])
@app.route('/edit-table/delete/<int:row_number_delete>', methods=['GET'])
@app.route('/edit-table/update/<int:row_number_update>', methods=['GET'])
def edit_table(row_number_delete=None, row_number_update=None):
    try:
        table_name = request.form['table-name']
        session['table_name'] = table_name
    except:
        table_name = session['table_name']

    tables = {'books': Books, 'authors': Authors}
    model = tables[table_name]

    form = AddForm(request.form)
    if form.one_of_two_validate():
        book_title = form.book_title.data.strip()
        authors_list = form.author_name.data.split(',')
        authors_list = [author_name.strip() for author_name in authors_list]
        if book_title and authors_list:
            item = Books(book_title, [Authors(author_name) for author_name in authors_list])
            db.session.add(item)
        elif not authors_list:
            item = Books(book_title)
            db.session.add(item)
        else:
            items = (Authors(author_name) for author_name in authors_list)
            [db.session.add(i) for i in items]
        db.session.commit()

    elif row_number_delete is not None:
        item = model.query.filter_by(id=row_number_delete).first()
        db.session.delete(item)
        db.session.commit()
        return redirect(url_for('edit_table'))

    # elif row_number_update is not None:
    #     item = model.query.filter_by(id=row_number_update).first()
    #     db.session.query(item).update()
    #     db.session.commit()
    #     return redirect(url_for('edit_table'))

    rows = model.query.all()
    rows = [row.columns_data() for row in rows]
    rows.insert(0, model.columns_name())

    return render_template('edit-table.html',
                           rows=rows,
                           table_name=table_name)

@app.route('/search/', methods=['GET', 'POST'])
def search():
    search_result = None
    if request.method == 'POST':
        form = SearchForm(request.form)
        if form.validate():

            search_result = Books.query.filter(
                Books.authors.any(
                    Authors.author_name.like('%' + form.search.data + '%')
                )
            ).all()

            search_result += Books.query.filter(
                Books.book_title.like('%' + form.search.data + '%')
            ).all()

            search_result = [result.columns_data() + result.get_authors() for result in search_result]
            search_result.insert(0, Books.columns_name())

    return render_template('search.html',
                           search_result=search_result)