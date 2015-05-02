from pyramid.paster import get_app
import os
application = get_app(
  os.path.dirname(os.path.realpath(__file__)) + '/../development.ini', 'main')
