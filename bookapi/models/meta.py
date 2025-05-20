from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import engine_from_config

DBSession = scoped_session(sessionmaker())
Base = declarative_base()


def init_sqlalchemy(settings):
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
