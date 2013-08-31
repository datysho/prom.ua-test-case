# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True)
    username = Column(String(20), nullable = False)
    password = Column(String(20), nullable = False)

    def __init__(self, username, password):
        self.username = username
        self.password = password


books_authors_table = Table(
    'association',
    Base.metadata,
    Column('fk_books', Integer, ForeignKey('books.id')),
    Column('fk_authors', Integer, ForeignKey('authors.id'))
)


class Books(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    book_title = Column(String(65), nullable=False)
    authors = relationship(
        "Authors",
        secondary=books_authors_table,
        backref="books"
    )


class Authors(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key = True)
    author_name = Column(String(65), nullable = False)