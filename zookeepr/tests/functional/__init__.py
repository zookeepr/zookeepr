import md5
import os
import re
import warnings

from formencode import variabledecode
from paste.deploy import loadapp
from paste.fixture import TestApp
from routes import url_for
from sqlalchemy import create_session, Query

from zookeepr import model
from zookeepr.config.routing import make_map
from zookeepr.tests import TestBase, monkeypatch

here_dir = os.path.dirname(__file__)
conf_dir = os.path.dirname(os.path.dirname(os.path.dirname(here_dir)))

class ControllerTest(TestBase):
    """Base class for controller tests"""
    def __init__(self, *args):
        wsgiapp = loadapp('config:test.ini', relative_to=conf_dir)
        self.app = TestApp(wsgiapp)
        super(ControllerTest, self).__init__(*args)

    def setUp(self):
        # add a routing map for testing routes within the controller tests
        self.map = make_map()

        # create a db session
        self.dbsession = create_session()

    def assertEmptyModel(self, model=None):
        """Check that there are no objects left in the data store.
       
        We leak knowledge of inheriting classes here, by testing to see if
        they've set the model attribute.
        """
        if model is None:
            if hasattr(self, 'model'):
                model = self.model
                
        if model:
            contents = Query(model).select()
            self.assertEqual([], contents, "model %r is not empty (contains %r)" % (model, contents))


class CRUDControllerTestGenerator(type):
    """Monkeypatching metaclass for cruddy controller test generation.

    This metaclass constructs test methods at class definition time
    based on the class attributes in the child; this way we can define
    a few bits of test data and have the test runner run as many tests
    on it as possible.
    """
    def __init__(mcs, name, bases, classdict):
        type.__init__(mcs, name, bases, classdict)

        # Don't patch if we're the base class
        if not name.startswith('Test'):
            return

        # patch if we have a model defined
        if 'model' not in classdict:
            warnings.warn("no model attribute in %s" % name, stacklevel=2)
        else:
            for t in ['create', 'edit', 'delete',
                      'invalid_get_on_edit',
                      'invalid_get_on_delete',
                      'invalid_get_on_new',
                      'delete_nonexistent']:
                if 'crud' not in classdict or t in classdict['crud']:
                    monkeypatch(mcs, 'test_' + t, t)

class CRUDControllerTest(ControllerTest):
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
    form proposal process, e.g. passwords that are hashed.

    An example using this base class:

    class TestSomeController(CRUDControllerTest):
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
    __metaclass__ = CRUDControllerTestGenerator
    
    def setUp(self):
        super(CRUDControllerTest, self).setUp()

        # check that the self.dbsession is currently empty
        self.assertEmptyModel()
        self.assertEmptyModel(model.Proposal)

    def tearDown(self):
        self.assertEmptyModel(model.Proposal)
        self.assertEmptyModel()

    def form_params(self, params):
        """Flatten the params dictionary for form posting.
        
        like a reverse variabledecode.NestedVariables.  If self.name exists,
        prepend it onto the params keys.
        """
        if hasattr(self, 'name'):
            prepend = self.name
        else:
            prepend = ''

        result = variabledecode.variable_encode(params, prepend)

        return result

    def additional(self, obj):
        """Modify the object further before saving.

        Child classes can override this method to add additional data to the object
        before it is saved.
        """
        return obj
    
    def create(self):
        #"""Test create action on controller"""

        url = url_for(controller=self.url, action='new')
        print "url retrieved is:", url
        # get the form
        response = self.app.get(url)
        #print response
        form = response.form
        print "form fields are:", form.fields

        # fill it out
        params = self.form_params(self.samples[0])
        for k in params.keys():
            form[k] = params[k]

        print "about to submit with these fields:", form.submit_fields()

        # submit
        resp = form.submit()
        #print "response:", resp
        error_match = re.search(r'<!-- for:.*<span class="error-message">[^<]*</span>', str(resp), re.DOTALL)
        if error_match is not None:
            self.fail("Errors in message: %s" % error_match.group(0))

        # now check that the data is in the database
        os = Query(self.model).select()
        print 'objects of type %s in the db: %r' % (self.model.__name__,  os)
        self.failIfEqual([], os, "data object %r not in database" % (self.model,))
        self.assertEqual(1, len(os), "more than one object in database (currently %r)" % (os,))

        # dodgy hack
        params = self.samples[0]
        if isinstance(params, dict) and hasattr(self, 'param_name'):
            params = params[self.param_name]
            print "params", params

        for key in params.keys():
            self.check_attribute(os[0], key, params[key])

        print "os before delete:", os
        self.dbsession.delete(os[0])
        self.dbsession.flush()
        print "os after delete:", Query(self.model).select()
        print "new objects after delete flush in create:", self.dbsession.new
        self.failUnlessEqual([], list(self.dbsession.new), "uncommitted objects: %r" % (objectstore.new,))
        print "deleted:", self.dbsession.deleted
        print "dirty:", self.dbsession.dirty
        print "new:", self.dbsession.new

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
        params = self.samples[0]
        if hasattr(self, 'param_name'):
            params = params[self.param_name]
        for key in params.keys():
            if not hasattr(self, 'no_test') or key not in self.no_test:
                result[key] = params[key]
        return result

    def edit(self):
        #"""Test edit action on controller"""

        # create an instance of the model
        o = self.model(**self.make_model_data())
        o = self.additional(o)
        self.dbsession.save(o)
        self.dbsession.flush()
        oid = o.id
        
        self.dbsession.clear()

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
        o = self.dbsession.get(self.model, oid)
        for k in self.samples[1].keys():
            self.check_attribute(o, k, self.samples[1][k])

        self.dbsession.delete(o)
        self.dbsession.flush()

    def delete(self):
        #"""Test delete action on controller"""
        # create something
        o = self.model(**self.make_model_data())
        o = self.additional(o)
        self.dbsession.save(o)
        self.dbsession.flush()
        oid = o.id

        self.dbsession.clear()

        ## delete it
        url = url_for(controller=self.url, action='delete', id=oid)

        # get the form
        response = self.app.get(url)
        form = response.form

        # send it
        form.submit()

        # check db
        o = self.dbsession.get(self.model, oid)
        print o
        self.assertEqual(None, o)

    def invalid_get_on_edit(self):
        #"""Test that GET requests on edit action don't modify"""

        # create some data
        o = self.model(**self.make_model_data())
        o = self.additional(o)
        self.dbsession.save(o)
        self.dbsession.flush()
        oid = o.id
        self.dbsession.clear()

        url = url_for(controller=self.url, action='edit', id=oid)

        response = self.app.get(url, params=self.form_params(self.samples[1]))

        o = self.dbsession.get(self.model, oid)

        for key in self.samples[1].keys():
            if not hasattr(self, 'no_test') or key not in self.no_test:
                self.failIfEqual(self.samples[1][key], getattr(o, key), "key '%s' was unchanged after edit (%r == %r)" % (key, self.samples[1][key], getattr(o, key)))

        self.dbsession.delete(o)
        self.dbsession.flush()


    def invalid_get_on_delete(self):
        #"""Test that GET requests on delete action don't modify"""
        
        # create some data
        o = self.model(**self.make_model_data())
        o = self.additional(o)
        self.dbsession.save(o)
        self.dbsession.flush()

        oid = o.id
        self.dbsession.clear()

        url = url_for(controller=self.url, action='delete', id=oid)
        res = self.app.get(url)
        
        # check
        o = self.dbsession.get(self.model, oid)
        self.failIfEqual(None, o)
        
        # clean up
        self.dbsession.delete(o)
        self.dbsession.flush()

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


class SignedInCRUDControllerTest(CRUDControllerTest):
    """Test base class that signs us in first.
    """
    def setUp(self):
        super(SignedInCRUDControllerTest, self).setUp()
        self.assertEmptyModel(model.Person)
        self.person = model.Person(email_address='testguy@example.org',
                                   password='test',
                                   fullname='Testguy McTest'
                                   )
        self.person.activated = True
        self.dbsession.save(self.person)
        self.dbsession.flush()
        self.pid = self.person.id
        resp = self.app.get(url_for(controller='account',
                                    action='signin'))
        f = resp.form
        f['email_address'] = 'testguy@example.org'
        f['password'] = 'test'
        resp = f.submit()
        self.failUnless('signed_in_person_id' in resp.session)
        self.assertEqual(self.pid, resp.session['signed_in_person_id'])

    def tearDown(self):
        self.dbsession.clear()
        
        self.dbsession.delete(Query(model.Person).get(self.pid))
        self.dbsession.flush()
        super(SignedInCRUDControllerTest, self).tearDown()


__all__ = ['ControllerTest',
    'CRUDControllerTest', 'SignedInCRUDControllerTest',
    'Query', 'model', 'url_for']

