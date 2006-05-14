import os, sys
from unittest import TestCase

here_dir = os.path.dirname(__file__)
conf_dir = os.path.dirname(os.path.dirname(here_dir))

sys.path.insert(0, conf_dir)

import pkg_resources

pkg_resources.working_set.add_entry(conf_dir)

pkg_resources.require('Paste')
pkg_resources.require('PasteScript')

from paste.deploy import loadapp
import paste.fixture

from zookeepr.config.routing import *
from pylons.myghtyroutes import RoutesResolver
from routes import request_config, url_for

from sqlalchemy import objectstore

class TestController(TestCase):
    def __init__(self, *args):
        wsgiapp = loadapp('config:development.ini', relative_to=conf_dir)
        self.app = paste.fixture.TestApp(wsgiapp)
        TestCase.__init__(self, *args)

    def setUp(self):
        # clear the objectstore at the start of each test because
        # we might not have deleted objects from the session at the
        # end of each test
        objectstore.clear()

__all__ = ['url_for', 'TestController']
