from pyramid.paster import get_app
import os
application = get_app(
  os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'production.ini')), 'main')
