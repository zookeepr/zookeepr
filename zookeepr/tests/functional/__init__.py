import os

from paste.deploy import loadapp
from paste.fixture import TestApp
from routes import url_for
from sqlalchemy import create_session, objectstore

from zookeepr import model
from zookeepr.config.routing import make_map
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
                      'delete_nonexistent']:
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

    ``no_test`` is a list of attributes that should not be compared when
    comparing the model to the form data, e.g. password confirmation
    boxes.

    ``mangles`` is a dictionary of attributes that are mangled by the
    form submission process, e.g. passwords that are hashed.

    An example using this base class:

    class TestSomeController(ControllerTest):
        name = 'Person'
        model = model.core.Person
        url = '/person'
        samples = [dict(name='testguy',
                        password='test',
                        password_confirm='test'),
                   dict(name='testgirl',
                        password='stuff',
                        password_confirm='stuff')]
        no_test = ['password_confirm']
        mangles = dict(password=lambda p: md5.new(p).hexdigest())
    """
    __metaclass__ = ControllerTestGenerator
    
    def __init__(self, *args):
        wsgiapp = loadapp('config:test.ini', relative_to=conf_dir)
        self.app = TestApp(wsgiapp)
        TestBase.__init__(self, *args)

    def setUp(self):
        # add a routing map for testing routes within the controller tests
        self.map = make_map()

        # check that the objectstore is currently empty
        self.assertEmptyModel()

    def tearDown(self):
        self.assertEmptyModel()

    def assertEmptyModel(self, model=None):
        """Check that there are no models"""
        if model is None:
            if hasattr(self, 'model'):
                model = self.model
                
        if model:
            session = create_session()
            self.assertEqual([], session.query(model).select())
            session.close()

    def form_params(self, params):
        """Prepend the controller's name to the param dict for use
        when posting into the form."""
        result = {}
        for key in params.keys():
            result[self.name + '.' + key] = params[key]

        return result
    
    def create(self):
        #"""Test create action on controller"""

        url = url_for(controller=self.url, action='new')

        # get the form
        response = self.app.get(url)
        form = response.form

        print form.text
        print form.fields
        # fill it out
        params = self.form_params(self.samples[0])
        for k in params.keys():
            form[k] = params[k]

        # submit
        form.submit()

        # now check that the data is in the database
        os = self.model.select()
        self.assertEqual(1, len(os), "data object not in database")

        for key in self.samples[0].keys():
            self.check_attribute(os[0], key, self.samples[0][key])

        os[0].delete()
        os[0].flush()

    def check_attribute(self, obj, attr, expected):
        """check that the attribute has the correct value.

        ``obj`` is the model class being tested.

        ``attr`` is the name of the attribute being tested.

        ``expected`` is the expected value of the attribute.

        The function checks the test's ``mangles`` class dictionary to
        modify ``expected``, and ignores attributes listed in the test's
        ``no_test`` class list.
        """
        if hasattr(self, 'no_test') and attr in self.no_test:
            return
        
        if hasattr(self, 'mangles'):
            if attr in self.mangles.keys():
                expected = self.mangles[attr](expected)
        result = getattr(obj, attr)
        self.assertEqual(expected, result,
                         "unexpected value of attribute '%s.%s': expected %r, got %r" % (obj.__class__.__name__, attr, expected, result))

    def make_model_data(self):
        result = {}
        for key in self.samples[0].keys():
            if not hasattr(self, 'no_test') or key not in self.no_test:
                result[key] = self.samples[0][key]
        return result

    def edit(self):
        #"""Test edit action on controller"""

        # create an instance of the model
        o = self.model(**self.make_model_data())
        o.save()
        o.flush()
        oid = o.id
        
        objectstore.clear()

        # get the form
        url = url_for(controller=self.url, action='edit', id=oid)
        response = self.app.get(url)
        form = response.form
        
        print form.text
        print form.fields

        # fill it out
        params = self.form_params(self.samples[1])
        for k in params.keys():
            form[k] = params[k]

        # submit!
        form.submit()

        # test
        o = self.model.get(oid)
        for k in self.samples[1].keys():
            self.check_attribute(o, k, self.samples[1][k])

        o.delete()
        o.flush()

    def delete(self):
        #"""Test delete action on controller"""
        # create something
        o = self.model(**self.make_model_data())
        o.save()
        o.flush()
        oid = o.id

        objectstore.clear()

        ## delete it
        url = url_for(controller=self.url, action='delete', id=oid)

        # get the form
        response = self.app.get(url)
        form = response.form

        # send it
        form.submit()

        # check db
        o = self.model.get(oid)
        print o
        self.assertEqual(None, o)

    def invalid_get_on_edit(self):
        #"""Test that GET requests on edit action don't modify"""

        # create some data
        o = self.model(**self.make_model_data())
        o.save()
        o.flush()
        oid = o.id
        objectstore.clear()

        url = url_for(controller=self.url, action='edit', id=oid)

        response = self.app.get(url, params=self.form_params(self.samples[1]))

        o = self.model.get(oid)

        for key in self.samples[1].keys():
            if not hasattr(self, 'no_test') or key not in self.no_test:
                self.failIfEqual(self.samples[1][key], getattr(o, key), "key '%s' was unchanged after edit (%r == %r)" % (key, self.samples[1][key], getattr(o, key)))

        o.delete()
        o.flush()


    def invalid_get_on_delete(self):
        #"""Test that GET requests on delete action don't modify"""
        
        # create some data
        o = self.model(**self.make_model_data())
        o.save()
        o.flush()

        oid = o.id
        objectstore.clear()

        url = url_for(controller=self.url, action='delete', id=oid)
        res = self.app.get(url)
        
        # check
        o = self.model.get(oid)
        self.failIfEqual(None, o)
        
        # clean up
        o.delete()
        o.flush()

    def invalid_get_on_new(self):
        #"""Test that GET requests on new action don't modify"""

        # verify there's nothing in there
        self.assertEmptyModel()

        url = url_for(controller=self.url, action='new')
        res = self.app.get(url, params=self.form_params(self.samples[0]))

    def delete_nonexistent(self):
        #"""Test delete of nonexistent object is caught"""

        # verify there's nothing in there
        self.assertEmptyModel()
        
        url = url_for(controller=self.url, action='delete', id=1)
        res = self.app.post(url, status=404)

__all__ = ['ControllerTest', 'model', 'url_for', 'objectstore']
