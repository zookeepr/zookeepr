import os

from paste.deploy import loadapp
from paste.fixture import TestApp
from routes import url_for
from sqlalchemy import create_session

import zookeepr.models as model
from zookeepr.tests import TestBase, monkeypatch

here_dir = os.path.dirname(__file__)
conf_dir = os.path.dirname(os.path.dirname(os.path.dirname(here_dir)))

class ControllerTestGenerator(type):
    """Monkeypatching metaclass for controller test generation.

    This metaclass constructs test methods at class definition time
    based on the class attributes in the child; this way we can define
    a few bits of test data and have the test runner run as many tests
    on it as possible.
    """
    def __init__(mcs, name, bases, classdict):
        type.__init__(mcs, name, bases, classdict)
        if 'url' in classdict and 'model' in classdict:
            monkeypatch(mcs, 'test_create', 'create')

class ControllerTest(TestBase):
    __metaclass__ = ControllerTestGenerator
    
    def __init__(self, *args):
        wsgiapp = loadapp('config:test.ini', relative_to=conf_dir)
        self.app = TestApp(wsgiapp)
        TestBase.__init__(self, *args)

    def setUp(self):
        self.session = create_session()

    def tearDown(self):
        self.assertEmptyModel()
        self.session.close()
        del self.session

    def assertEmptyModel(self):
        self.assertEqual([], self.session.query(self.model).select())


    def create(self):
        """Test create action on controller"""

        url = url_for(controller=self.url, action='new')
        print "url for create is", url

        # emulate the first browser request; the client browser
        # will GET the page before POSTing the form data, and
        # we might have some weird session errors that we'd like to
        # catch here in the test.
        response = self.app.get(url)

        # post some sample data
        response = self.app.post(url, params=self.sample)

        # now check that the data is in the database
        os = self.session.query(self.model).select()
        self.assertNotEqual(0, len(os))
        self.assertEqual(1, len(os))

        self.session.delete(os[0])
        self.session.flush()

__all__ = ['ControllerTest', 'model', 'url_for']
