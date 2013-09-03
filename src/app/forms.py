# -*- coding: utf-8 -*-
from wtforms import Form, TextField, PasswordField, validators


class LoginForm(Form):
    username = TextField('username', [validators.Length(min=4, max=25)])
    password = PasswordField('password')


class AddForm(Form):
    book_title = TextField('book_title', [validators.Length(min=1, max=50), validators.Optional])
    author_name = TextField('author_name', [validators.Length(min=1, max=50), validators.Optional])

    def one_of_two_validate(self):
        if self.book_title.data or self.author_name.data:
            return True
        else:
            return False


class SearchForm(Form):
    search = TextField('search', [validators.Length(min=1, max=50)])