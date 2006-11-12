import warnings

import sqlalchemy.mods.threadlocal
from sqlalchemy import objectstore, Query

from zookeepr import model
from zookeepr.tests import TestBase, monkeypatch

class ModelTestGenerator(type):
    """Monkeypatching metaclass for data model test classes.

    This metaclass generates test methods in the target class based on the
    class attributes set, to reduce the amount of code needed to be
    written to do common model tests, thus improving TDD!
    """
    def __init__(cls, name, bases, classdict):
        if 'domain' not in classdict:
            warnings.warn("no domain attribute found in %s" % name, stacklevel=2)
        else:
            monkeypatch(cls, 'test_crud', 'crud')


class ModelTest(TestBase):
    """Base class for testing the data model classes.

    Derived classes should set the following attributes:

    ``domain`` is the class (not an instance) that is having it's API
    tested.

    ``samples`` is a list of dictionaries of attributes to use when
    creating test model objects.

    ``mangles`` is a dictionary mapping attributes to functions, for
    attributes that are modified by the model object so that the value
    returned is not the same as the one set.  Set the function to
    somethign that mangles the value as you expect, and the test will
    check that the returned result is correct.

    An example using this base class follows.

    class TestSomeModel(ModelTest):
        model = model.core.User
        samples = [dict(name='testguy',
                        email_address='test@example.org',
                        password='test')]
        mangles = dict(password=lambda p: md5.new(p).hexdigest())
    """
    __metaclass__ = ModelTestGenerator

    def check_empty_session(self):
        """Check that the database was left empty after the test"""
        results = Query(self.domain).select()
        self.assertEqual([], results)

    def additional(self, obj):
        """Perform additional modifications to the model object before saving.

        Derived classes can override this to set up dependent objects for CRUD
        tests.
        """
        return obj
    
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
#             domain = model.SomeModel
#             samples = [dict(password='test')]
#             mangles = dict(password=lambda p: md5.new(p).hexdigest())
        
#         """
        self.failIf(len(self.samples) < 1,
            "not enough sample data, stranger")

        for sample in self.samples:
            # instantiating model
            o = self.domain(**sample)

            # perform additional operations
            o = self.additional(o)
            
            # committing to db
            objectstore.save(o)
            objectstore.flush()
            oid = o.id

            # clear the session, invalidating o
            objectstore.clear()
            del o
    
            # check it's in the database
            print self.domain
            print oid
            o = objectstore.get(self.domain, oid)
            self.failIfEqual(None, o, "object not in database")
        
            # checking attributes
            for key in sample.keys():
                # test each attribute
                self.check_attribute(o, key, sample[key])
    
            # deleting object
            objectstore.delete(o)
            objectstore.flush()
    
            # checking db
            self.check_empty_session()

        objectstore.close()

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
        if 'table' not in classdict:
            warnings.warn("no table attribute found in %s" % name, stacklevel=2)
        else:
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

    def check_empty_table(self):
        """Check that the database was left empty after the test"""
        query = sqlalchemy.select([sqlalchemy.func.count(self.table.c.id)])
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
            query = self.table.insert()
            query.execute(sample)

            for key in sample.keys():
                col = getattr(self.table.c, key)
                query = sqlalchemy.select([col])
                result = query.execute()
                row = result.fetchone()
                print "row:", row
                self.assertEqual(sample[key], row[0])

            self.table.delete().execute()

        # do this again to make sure the test data is all able to go into
        # the db, so that we know it's good to do uniqueness tests, for example
        for sample in self.samples:
            query = self.table.insert()
            query.execute(sample)

        # get the count of rows
        query = sqlalchemy.select([sqlalchemy.func.count(self.table.c.id)])
        result = query.execute()
        # check that it's the same length as the sample data
        self.assertEqual(len(self.samples), result.fetchone()[0])

        # ok, delete it
        self.table.delete().execute()

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

            query = self.table.insert()
            self.assertRaisesAny(query.execute, coldata)

            self.table.delete().execute()

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

            self.table.insert().execute(self.samples[0])

            attr = {}
            attr.update(self.samples[1])

            attr[col] = self.samples[0][col]

            query = self.table.insert()
            self.assertRaisesAny(query.execute, attr)

            self.table.delete().execute()

            self.check_empty_table()


__all__ = ['TableTest', 'ModelTest',
           'objectstore', 'Query',
           'model',
           ]
