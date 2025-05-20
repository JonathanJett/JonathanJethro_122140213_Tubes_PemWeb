from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from .models import DBSession, Base  # Mengimpor DBSession dan Base dari models

def main(global_config, **settings):
    """
    Fungsi utama yang digunakan oleh Pyramid saat aplikasi dijalankan.
    """
    # Buat engine SQLAlchemy dari file .ini
    engine = engine_from_config(settings, 'sqlalchemy.')
    Base.metadata.bind = engine

    # Buat konfigurasi Pyramid
    config = Configurator(settings=settings)

    # Setup DB session
    DBSession.configure(bind=engine)

    # Tambahkan pemetaan routes dan scan views
    config.include('pyramid_tm')  # opsional, jika menggunakan pyramid_tm
    config.include('pyramid_jinja2')  # opsional, jika pakai Jinja2
    config.include('.routes')
    config.add_static_view('static', 'bookapi:static', cache_max_age=3600)
    config.include('.models')
    config.add_route('get_books', '/api/books')
    config.add_route('create_book', '/api/books')
    config.add_route('update_book', '/api/books/{id}')
    config.add_route('delete_book', '/api/books/{id}')
    config.scan()

    return config.make_wsgi_app()

