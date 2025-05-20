from sqlalchemy import Column, Integer, Text, String
from .meta import Base

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=True)
    rating = Column(Integer, default=0)
    status = Column(String(50), default='unread')