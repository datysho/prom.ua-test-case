# -*- coding: utf-8 -*-
from app import db
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship


class Users(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(20), nullable=False)
    password = Column(String(20), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password


books_authors_associations = Table(
    'association',
    db.metadata,
    Column('books', Integer, ForeignKey('books.id'), nullable=True),
    Column('authors', Integer, ForeignKey('authors.id'), nullable=True)
)


class Authors(db.Model):
    id = Column(Integer, primary_key=True)
    author_name = Column(String(65), nullable=True)

    def __init__(self, author_name):
        self.author_name = author_name

    @staticmethod
    def columns_names():
        return ['ID', u'Имя автора']

    def columns_data(self):
        author_name = self.author_name
        if not author_name:
            author_name = 'None'
        return [self.id, author_name]


class Books(db.Model):
    id = Column(Integer, primary_key=True)
    book_title = Column(String(65), nullable=False)
    author = relationship(
        "Authors",
        secondary=books_authors_associations,
        backref="books",
    )

    def __init__(self, book_title, authors):
        self.book_title = book_title
        self.author = authors

    def append_author(self, author):
        self.author += [author]

    @staticmethod
    def columns_names():
        return ['ID', u'Название книги', u'Список Авторов']

    def columns_data(self):
        return [self.id, self.book_title, self.get_authors_names()]

    def get_authors_names(self):
        authors = [author.author_name for author in self.author]
        if not authors:
            authors = [u'None']
        return authors

    def get_authors_id(self):
        return [author.id for author in self.author]