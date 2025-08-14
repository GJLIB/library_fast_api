from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, index = True)
    username = Column(String(150), unique = True, nullable = False)
    email = Column(String(150))
    password = Column(String, nullable = False)

    
class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    bio = Column(String)


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    pages = Column(Integer, default=10)

    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship("Author")