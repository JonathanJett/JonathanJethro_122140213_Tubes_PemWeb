from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker, configure_mappers
from .meta import Base, DBSession
from .book import Book
import zope.sqlalchemy

# Import atau definisikan semua model di sini untuk memastikan mereka terdaftar di Base.metadata
from .mymodel import MyModel  # flake8: noqa

# Jalankan ``configure_mappers`` setelah mendefinisikan semua model untuk memastikan
# semua relasi dapat diatur dengan baik.
configure_mappers()

def get_engine(settings, prefix='sqlalchemy.'):
    """Mendapatkan engine dari pengaturan."""
    return engine_from_config(settings, prefix)

def get_session_factory(engine):
    """Mendapatkan session factory dengan engine yang telah dikonfigurasi."""
    factory = sessionmaker()
    factory.configure(bind=engine)
    return factory

def get_tm_session(session_factory, transaction_manager, request=None):
    """
    Mendapatkan instance dari ``sqlalchemy.orm.Session`` yang terhubung dengan transaction.

    Fungsi ini menghubungkan session ke transaction manager yang akan mengurus commit atau
    rollback transaksi sesuai dengan status error atau sukses.
    """
    dbsession = session_factory(info={"request": request})
    zope.sqlalchemy.register(
        dbsession, transaction_manager=transaction_manager
    )
    return dbsession

def includeme(config):
    """
    Inisialisasi model untuk aplikasi Pyramid.

    Aktifkan setup ini dengan ``config.include('bookapi.models')``.
    """
    settings = config.get_settings()
    settings['tm.manager_hook'] = 'pyramid_tm.explicit_manager'

    # Gunakan pyramid_tm untuk menghubungkan siklus hidup transaksi dengan request.
    # Package ``pyramid_tm`` dan ``transaction`` bekerja bersama untuk
    # secara otomatis menutup session database setelah setiap request.
    config.include('pyramid_tm')

    # Gunakan pyramid_retry untuk mencoba request lagi saat terjadi exception sementara
    config.include('pyramid_retry')

    # Inisialisasi engine dan session factory
    dbengine = settings.get('dbengine')
    if not dbengine:
        dbengine = get_engine(settings)

    session_factory = get_session_factory(dbengine)
    config.registry['dbsession_factory'] = session_factory

    # Membuat request.dbsession tersedia untuk digunakan di Pyramid
    def dbsession(request):
        dbsession = request.environ.get('app.dbsession')
        if dbsession is None:
            dbsession = get_tm_session(
                session_factory, request.tm, request=request
            )
        return dbsession

    config.add_request_method(dbsession, reify=True)
