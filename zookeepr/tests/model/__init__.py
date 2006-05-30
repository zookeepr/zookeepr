from sqlalchemy import create_session

import zookeepr.models as model
from zookeepr.tests import TestBase, monkeypatch

class ModelTestGenerator(type):
    """Monkeypatching metaclass for data model test classes.

    This metaclass generates test methods in the target class based on the
    class attributes set, to reduce the amount of code needed to be
    written to do common model tests, thus improving TDD!
    """
    def __init__(cls, name, bases, classdict):
        if 'model' in classdict:
            monkeypatch(cls, 'test_crud', 'crud')


class ModelTest(TestBase):
    """Base class for testing the data model classes.

    Derived classes should set the following attributes:

    ``model`` is a string containing the name of the class being tested,
    scoped relative to the module ``zookeepr.models``.

    ``samples`` is a list of dictionaries of attributes to use when
    creating test model objects.

    ``mangles`` is a dictionary mapping attributes to functions, for
    attributes that are modified by the model object so that the value
    returned is not the same as the one set.  Set the function to
    somethign that mangles the value as you expect, and the test will
    check that the returned result is correct.

    An example using this base class follows.

    class TestSomeModel(TestModel):
        model = 'module.User'
        samples = [dict(name='testguy',
                        email_address='test@example.org',
                        password='test')]
        mangles = dict(password=lambda p: md5.new(p).hexdigest())
    """
    __metaclass__ = ModelTestGenerator

    def get_model(self):
        """Return the model object, coping with scoping.

        Set the ``model`` class variable to the name of the model class
        relative to anchor.model.
        """
        module = model
        # cope with classes in sub-models
        for submodule in self.model.split('.'):
            module = getattr(module, submodule)
        return module
        
    def check_empty_session(self):
        """Check that the database was left empty after the test"""
        session = create_session()
        results = session.query(self.get_model()).select()
        self.assertEqual(0, len(results))

    def crud(self):
        """Test CRUD operations on data model object.

        This test creates an object of the data model, checks that it was
        inserted into the database, and then deletes it.  We don't bother
        testing 'update' because it's assumed that SQLAlchemy provides
        this for us already.  We only want to test that our class behaves
        the way we expect it (i.e. contains the data we want, and any
        property methods do the right thing).
    
        Set the attributes for this model object in the ``samples`` class
        variable.

        If an attribute goes through a mangle process, list it in the
        ``mangles`` dictionary, keyed on the attribute name, and make
        the value on that key a callable that mangles the sample
        data as expected.

        For example,

        class TestSomeModel(ModelTest):
            model = 'mod'
            samples = [dict(password='test')]
            mangles = dict(password=lambda p: md5.new(p).hexdigest())
        
        """
        self.failIf(len(self.samples) < 1,
            "not enough sample data, stranger")

        session = create_session()
        
        for sample in self.samples:
            # instantiating model
            o = self.get_model()(**sample)
    
            # committing to db
            session.save(o)
            session.flush()
            oid = o.id

            # clear the session, invalidating o
            session.clear()
            del o
    
            # check it's in the database
            o = session.get(self.get_model(), oid)
            self.failIfEqual(None, o, "object not in database")
        
            # checking attributes
            for key in sample.keys():
                # test each attribute
                self.check_attribute(o, key, sample[key])
    
            # deleting object
            session.delete(o)
            session.flush()
    
            # checking db
            self.check_empty_session()

        session.close()

    def check_attribute(self, obj, key, value):
        """Check that the attribute has the correct value.

        ``obj`` is the model class being tested.

        ``key`` is the name of the attribute being tested.

        ``value`` is the expected value of the attribute.

        This function checks the test's ``mangle`` class dictionary to
        modify the ``value if necessary.
        """
        print "testing %s.%s is %s" % (obj.__class__.__name__, key, value)
        if hasattr(self, 'mangles'):
            if key in self.mangles.keys():
                value = self.mangles[key](value)
        result = getattr(obj, key)
        self.assertEqual(value, result,
                         "unexpected value on attribute '%s': expected '%s', got '%s'" % (key, value, result))

__all__ = ['ModelTest', 'model', 'create_session']
