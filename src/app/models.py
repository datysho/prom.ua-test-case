# -*- coding: utf-8 -*-
from app import db
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

class Users(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True)
    username = Column(String(20), nullable = False)
    password = Column(String(20), nullable = False)

    def __init__(self, username, password):
        self.username = username
        self.password = password


books_authors_table = Table(
    'association',
    db.metadata,
    Column('fk_books', Integer, ForeignKey('books.id'), nullable=True),
    Column('fk_authors', Integer, ForeignKey('authors.id'), nullable=True)
)


class Authors(db.Model):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    author_name = Column(String(65), nullable=False)

    def __init__(self, author_name):
        self.author_name = author_name

    @staticmethod
    def columns_name():
        return ['ID', u'Имя автора']

    def columns_data(self):
        return [self.id, self.author_name]


class Books(db.Model):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    book_title = Column(String(65), nullable=False)
    authors = relationship(
        "Authors",
        secondary=books_authors_table,
        backref="books",
    )

    def __init__(self, book_title, authors=None):
        if not authors: authors = [
            Authors(author_name=u'Автор неизвестен')
        ]
        self.book_title = book_title
        self.authors = authors

    @staticmethod
    def columns_name():
        return ['ID', u'Название книги', u'Список Авторов']

    def columns_data(self):
        return [self.id, self.book_title, self.get_authors()]

    def get_authors(self):
        authors = [author.author_name for author in self.authors]
        if authors == []:
            authors = [u'Не указано']
        return authors