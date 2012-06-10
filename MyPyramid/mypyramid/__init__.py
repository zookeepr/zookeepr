from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import DBSession
from legacy_view import LegacyView

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    
    legacy_view = LegacyView(global_config, **settings)
    config.add_view(context='pyramid.exceptions.NotFound', view=legacy_view)
    config.scan()
    return config.make_wsgi_app()

