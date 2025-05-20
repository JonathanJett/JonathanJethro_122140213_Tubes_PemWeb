from sqlalchemy import Column, Integer, String
from . import Base  # dari models/__init__.py

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    rating = Column(Integer)
    status = Column(String)  # e.g. 'unread', 'read'
