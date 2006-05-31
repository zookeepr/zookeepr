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

        # patch if we have a model defined
        if 'model' in classdict:
            for t in ['create', 'edit', 'delete',
                      'invalid_get_on_edit',
                      'invalid_get_on_delete',
                      'invalid_get_on_new',
                      'invalid_delete']:
                monkeypatch(mcs, 'test_' + t, t)

class ControllerTest(TestBase):
    """Base class for testing CRUD on controller objects.

    Derived classes should set the following attributes:

    ``url`` is the first part of the URL that is mapped to this
    controller.
    
    ``name`` is the prefix used in forms, as decoded by FormEncode.

    ``model`` is the class that this controller acts on.

    ``samples`` is a list of dictionaries of data to use when testing
    CRUD operations.

    An example using this base class:

    class TestSomeController(ControllerTest):
        name = 'Person'
        model = model.Person
        url = '/person'
        samples = [dict(name='testguy'),
                   dict(name='testgirl')]
    """
    __metaclass__ = ControllerTestGenerator
    
    def __init__(self, *args):
        wsgiapp = loadapp('config:test.ini', relative_to=conf_dir)
        self.app = TestApp(wsgiapp)
        TestBase.__init__(self, *args)

    def setUp(self):
        self.session = create_session()
        self.assertEmptyModel()

    def tearDown(self):
        self.assertEmptyModel()
        self.session.close()
        del self.session

    def assertEmptyModel(self):
        """Check that there are no models"""
        self.assertEqual([], self.session.query(self.model).select())


    def form_params(self, params):
        """Prepend the controller's name to the param dict for use
        when posting into the form."""
        result = {}
        for key in params.keys():
            result[self.name + '.' + key] = params[key]
        print result
        return result
    
    def create(self):
        #"""Test create action on controller"""

        url = url_for(controller=self.url, action='new')
        print "url for create is", url

        # emulate the first browser request; the client browser
        # will GET the page before POSTing the form data, and
        # we might have some weird session errors that we'd like to
        # catch here in the test.
        response = self.app.get(url)

        # post some sample data
        response = self.app.post(url, params=self.form_params(self.samples[0]))

        # now check that the data is in the database
        os = self.session.query(self.model).select()
        self.assertNotEqual(0, len(os))
        self.assertEqual(1, len(os))

        for key in self.samples[0].keys():
            self.assertEqual(self.samples[0][key], getattr(os[0], key))

        self.session.delete(os[0])
        self.session.flush()

    def edit(self):
        #"""Test edit action on controller"""

        # create an instance of the model
        o = self.model(**self.samples[0])
        self.session.save(o)
        self.session.flush()
        oid = o.id
        self.session.clear()

        # 
        url = url_for(controller=self.url, action='edit', id=oid)

        # get the page before posting, see create above for details
        response = self.app.get(url)

        response = self.app.post(url, params=self.form_params(self.samples[1]))

        # test
        o = self.session.get(self.model, oid)
        for k in self.samples[1].keys():
            self.assertEqual(self.samples[1][k], getattr(o, k))

        self.session.delete(o)
        self.session.flush()

    def delete(self):
        #"""Test delete action on controller"""

        # create something
        o = self.model(**self.samples[0])
        self.session.save(o)
        self.session.flush()
        oid = o.id
        self.session.clear()

        ## delete it
        url = url_for(controller=self.url, action='delete', id=oid)
        # get the form
        response = self.app.get(url)
        response = self.app.post(url)

        # check db
        o = self.session.get(self.model, oid)
        self.assertEqual(None, o)

    def invalid_get_on_edit(self):
        #"""Test that GET requests on edit action don't modify"""

        # create some data
        o = self.model(**self.samples[0])
        self.session.save(o)
        self.session.flush()
        oid = o.id
        self.session.clear()

        url = url_for(controller=self.url, action='edit', id=oid)

        response = self.app.get(url, params=self.form_params(self.samples[1]))

        o = self.session.get(self.model, oid)
        for key in self.samples[1].keys():
            self.failIfEqual(self.samples[1][key], getattr(o, key))

        self.session.delete(o)
        self.session.flush()

    def invalid_get_on_delete(self):
        #"""Test that GET requests on delete action don't modify"""
        
        # create some data
        o = self.model(**self.samples[0])
        self.session.save(o)
        self.session.flush()
        oid = o.id
        self.session.clear()

        url = url_for(controller=self.url, action='delete', id=oid)
        res = self.app.get(url)
        
        # check
        o = self.session.get(self.model, oid)
        self.failIfEqual(None, o)
        
        # clean up
        self.session.delete(o)
        self.session.flush()

    def invalid_get_on_new(self):
        #"""Test that GET requests on new action don't modify"""

        # verify there's nothing in there
        self.assertEmptyModel()

        url = url_for(controller=self.url, action='new')
        res = self.app.get(url, params=self.form_params(self.samples[0]))

    def invalid_delete(self):
        #"""Test delete of nonexistent object is caught"""

        # verify there's nothing in there
        self.assertEmptyModel()
        
        url = url_for(controller=self.url, action='delete', id=1)
        res = self.app.post(url)

__all__ = ['ControllerTest', 'model', 'url_for']
