import sqlalchemy
from sqlalchemy import create_session

from zookeepr import model
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
    scoped relative to the module ``zookeepr.model``.

    ``samples`` is a list of dictionaries of attributes to use when
    creating test model objects.

    ``mangles`` is a dictionary mapping attributes to functions, for
    attributes that are modified by the model object so that the value
    returned is not the same as the one set.  Set the function to
    somethign that mangles the value as you expect, and the test will
    check that the returned result is correct.

    An example using this base class follows.

    class TestSomeModel(ModelTest):
        model = 'module.User'
        samples = [dict(name='testguy',
                        email_address='test@example.org',
                        password='test')]
        mangles = dict(password=lambda p: md5.new(p).hexdigest())
    """
    __metaclass__ = ModelTestGenerator

    def setUp(self):
        super(ModelTest, self).setUp()
        self.objectstore = create_session()

    def tearDown(self):
        self.objectstore.close()
        del self.objectstore
        super(ModelTest, self).tearDown()

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
        session.close()

    def crud(self):
        #
#         """Test CRUD operations on data model object.

#         This test creates an object of the data model, checks that it was
#         inserted into the database, and then deletes it.  We don't bother
#         testing 'update' because it's assumed that SQLAlchemy provides
#         this for us already.  We only want to test that our class behaves
#         the way we expect it (i.e. contains the data we want, and any
#         property methods do the right thing).
    
#         Set the attributes for this model object in the ``samples`` class
#         variable.

#         If an attribute goes through a mangle process, list it in the
#         ``mangles`` dictionary, keyed on the attribute name, and make
#         the value on that key a callable that mangles the sample
#         data as expected.

#         For example,

#         class TestSomeModel(ModelTest):
#             model = 'mod'
#             samples = [dict(password='test')]
#             mangles = dict(password=lambda p: md5.new(p).hexdigest())
        
#         """
        self.failIf(len(self.samples) < 1,
            "not enough sample data, stranger")

        for sample in self.samples:
            # instantiating model
            o = self.get_model()(**sample)
    
            # committing to db
            self.objectstore.save(o)
            self.objectstore.flush()
            oid = o.id

            # clear the session, invalidating o
            self.objectstore.clear()
            del o
    
            # check it's in the database
            print self.get_model()
            print oid
            o = self.objectstore.get(self.get_model(), oid)
            self.failIfEqual(None, o, "object not in database")
        
            # checking attributes
            for key in sample.keys():
                # test each attribute
                self.check_attribute(o, key, sample[key])
    
            # deleting object
            self.objectstore.delete(o)
            self.objectstore.flush()
    
            # checking db
            self.check_empty_session()

        self.objectstore.close()

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
                         "unexpected value on attribute '%s': expected '%r', got '%r'" % (key, value, result))



class TableTestGenerator(type):
    """Monkeypatching metaclass for table schema test classes.
    
    This metaclass does some funky class method rewriting to generate
    test methods so that one doesn't actually need to do any work to get
    table tests written.  How awesome is that for TDD? :-)
    """
    def __init__(mcs, name, bases, classdict):
        type.__init__(mcs, name, bases, classdict)
        if 'table' in classdict:
            monkeypatch(mcs, 'test_insert', 'insert')
            
            for k in ['not_nullable', 'unique']:
                if k + 's' in classdict:
                    monkeypatch(mcs, 'test_' + k, k)


class TableTest(TestBase):
    """Base class for testing the database schema.

    Derived classes should set the following attributes:

    ``table`` is a string containing the name of the table being tested,
    scoped relative to the module ``zookeepr.model``.

    ``samples`` is a list of dictionaries of columns and their values to use
    when inserting a row into the table.

    ``not_nullables`` is a list of column names that must not be undefined
    in the table.

    ``uniques`` is a list of column names that must uniquely identify
    the object.

    An example using this base class:

    class TestSomeTable(TableTest):
        table = 'module.SomeTable'
        samples = [dict(name='testguy', email_address='test@example.org')]
        not_nullables = ['name']
        uniques = ['name', 'email_address']
    """
    __metaclass__ = TableTestGenerator

    def get_table(self):
        """Return the table, coping with scoping.

        Set the ``table`` class variable to the name of the table variable
        relative to anchor.model.
        """
        module = model
        # cope with classes in sub-models
        for submodule in self.table.split('.'):
            module = getattr(module, submodule)
        return module
        
    def check_empty_table(self):
        """Check that the database was left empty after the test"""
        query = sqlalchemy.select([sqlalchemy.func.count(self.get_table().c.id)])
        result = query.execute()
        self.assertEqual(0, result.fetchone()[0])

    def insert(self):
        #"""Test insertion of sample data
        #
        #Insert a row into the table, check that it was
        #inserted into the database, and then delete it.
        #
        #Set the attributes for this model object in the ``attrs`` class
        #variable.
        #"""

        self.failIf(len(self.samples) < 1, "not enough sample data, stranger")
        
        for sample in self.samples:
            print "testing insert of sample data:", sample
            query = self.get_table().insert()
            query.execute(sample)

            for key in sample.keys():
                col = getattr(self.get_table().c, key)
                query = sqlalchemy.select([col])
                result = query.execute()
                row = result.fetchone()
                print "row:", row
                self.assertEqual(sample[key], row[0])

            self.get_table().delete().execute()

        # do this again to make sure the test data is all able to go into
        # the db, so that we know it's good to do uniqueness tests, for example
        for sample in self.samples:
            query = self.get_table().insert()
            query.execute(sample)

        # get the count of rows
        query = sqlalchemy.select([sqlalchemy.func.count(self.get_table().c.id)])
        result = query.execute()
        # check that it's the same length as the sample data
        self.assertEqual(len(self.samples), result.fetchone()[0])

        # ok, delete it
        self.get_table().delete().execute()

        self.check_empty_table()

    def not_nullable(self):
        """Check that certain columns of a table are not nullable.
         
        Specify the ``not_nullables`` class variable with a list of column names
        that must not be null, and this method will insert into the table rows
        with each set to null and test for an exception from the database layer.
        """

        self.failIf(len(self.samples) < 1, "not enough sample data, stranger")

        for col in self.not_nullables:
            print "TEST: testing that %s is not nullable" % col
            
            # construct an attribute dictionary without the 'not null' attribute
            coldata = {}
            coldata.update(self.samples[0])
            coldata[col] = None
    
            # create the model object
            print coldata

            query = self.get_table().insert()
            self.assertRaisesAny(query.execute, coldata)

            self.get_table().delete().execute()

            self.check_empty_table()

    def unique(self):
        """Check that certain attributes of a model object are unique.

        Specify the ``uniques`` class variable with a list of attributes
        that must be unique, and this method will create two copies of the
        model object with that attribute the same and test for an exception
        from the database layer.
        """

        self.failIf(len(self.samples) < 2, "not enough sample data, stranger")

        for col in self.uniques:

            self.get_table().insert().execute(self.samples[0])

            attr = {}
            attr.update(self.samples[1])

            attr[col] = self.samples[0][col]

            query = self.get_table().insert()
            self.assertRaisesAny(query.execute, attr)

            self.get_table().delete().execute()

            self.check_empty_table()


__all__ = ['TableTest', 'ModelTest', 'model', 'create_session']
