import os
import sys
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker

from pyramid.paster import get_appsettings, setup_logging

from bookapi.models import Base, Book  # Pastikan ini sesuai
from bookapi.models import meta

def main(argv=sys.argv):
    if len(argv) != 2:
        print("Usage: initialize_bookapi_db <config_uri>")
        sys.exit(1)

    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)

    engine = engine_from_config(settings, 'sqlalchemy.')
    Base.metadata.create_all(engine)
