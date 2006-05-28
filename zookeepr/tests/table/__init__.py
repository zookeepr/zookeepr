import new
import unittest

from sqlalchemy import select, func

import zookeepr.models as model

class TableTestGenerator(type):
    """This metaclass does some funky class method rewriting to generate
    test methods so that one doesn't actually need to do any work to get
    table tests written.  How awesome is that for TDD? :-)
    """
    def __init__(cls, name, bases, dict):
        if dict.has_key('table'):
            monkeypatch(cls, 'test_insert', 'insert')
            
            for k in ['not_nullable', 'unique']:
                if k + 's' in dict:
                    monkeypatch(cls, 'test_' + k, k)

def monkeypatch(cls, test_name, func_name):
    """
    patch the child class with the test_not_nullable function
    now that we know it contains enough data to do so.
    
    rather than do something sensible like use setattr,
    we create a new function and hack the __module__ attribute
    so that when nose runs, it doesn't skip the test because
    it thinks it is in the parent.  This is in
    nose.selector.wantMethod, anytests, and callableInTests.
    
    You can't set __module__ directly because it's a r/o attribute.
    
    The __module__ attribute is set by the new.function method
    from the globals dict, so here we make a shallow copy and
    override the __name__ attribute to point to the module of the
    class we're actually testing.
    
    By this stage, you may think that this is crack.  You're right.
    But at least I don't have to repeat the same code over and
    over in the actual tests ;-)
    """
    g = globals().copy()
    g['__name__'] = cls.__module__
    code = getattr(cls, func_name).im_func.func_code
    # create a new function with:
    # the code of the original function,
    # our patched globals,
    # and the new name of the function
    setattr(cls, test_name, new.function(code, g, test_name))

class TableTestBase(unittest.TestCase):
    """Base class for testing the database schema.

    Derived classes should set the following attributes:

    ``table`` is a string containing the name of the table being tested,
    scoped relative to anchor.model.

    ``attrs`` is a dictionary of columns and their values to use when inserting
    a row into the table.

    ``not_nulls`` is a list of column names that must not be undefined
    in the table.

    ``uniques`` is a list of column names that must uniquely identify
    the object.

    An example using this base class:

    class TestSomeTable(TestTable):
        model = 'module.SomeTable'
        attrs = dict(name='testguy', email_address='test@example.org')
        not_nulls = ['name']
        uniques = ['name', 'email_address']
    """
    __metaclass__ = TableTestGenerator

    def assertRaisesAny(self, callable, *args, **kwargs):
        try:
            callable(*args, **kwargs)
        except:
            pass
        else:
            self.fail("function failed to raise any exception")
        

    def get_table(self):
        """Return the table, coping with scoping.

        Set the ``table`` class variable to the name of the table variable
        relative to anchor.model.
        """
        module = model
        # cope with classes in sub-models
        for m in self.table.split('.'):
            module = getattr(module, m)
        return module
        
    def check_empty_database(self):
        """Check that the database was left empty after the test"""
        r = select([func.count(self.get_table().c.id)]).execute()
        self.assertEqual(0, r.fetchone()[0])

    def insert(self):
        """Test insertion of sample data

        Insert a row into the table, check that it was
        inserted into the database, and then delete it.
    
        Set the attributes for this model object in the ``attrs`` class
        variable.
        """

        t = self.get_table()

        for s in self.sample:
            print "testing insert of s %s" % s
            q = t.insert()
            print q
            q.execute(s)

            for k in s.keys():
                q = select([getattr(t.c, k)])
                print "query", q
                
                r = q.execute()
                print r
                row = r.fetchone()
                print "row", row
                self.assertEqual(s[k], row[0])

            t.delete().execute()

        # do this again to make sure the test data is all able to go into
        # the db, so that we know it's good to do uniqueness tests, for example
        for s in self.sample:
            q = t.insert()
            q.execute(s)

        # get the count of rows
        r = select([func.count(t.c.id)]).execute()
        # check that it's the same length as the sample data
        self.assertEqual(len(self.sample), r.fetchone()[0])

        # ok, delete it
        t.delete().execute()

        self.check_empty_database()
    
    def not_nullable(self):
        """Check that certain columns of a table are not nullable.
    
        Specify the ``not_nullables`` class variable with a list of column names
        that must not be null, and this method will insert into the table rows
        with each set to null and test for an exception from the database layer.
        """

        self.failIf(len(self.sample) < 1, "not enough data to test not-nullable columns")
        
        for col in self.not_nullables:
            print "testing that %s is not nullable" % col
            
            # construct an attribute dictionary without the 'not null' attribute
            coldata = {}
            coldata.update(self.sample[0])
            del coldata[col]
            self.failIf(col in coldata.keys())
    
            # create the model object
            print coldata

            q = self.get_table().insert()
            self.assertRaisesAny(q.execute, coldata)

            self.get_table().delete().execute()

            self.check_empty_database()

    def unique(self):
        """Check that certain attributes of a model object are unique.

        Specify the ``uniques`` class variable with a list of attributes
        that must be unique, and this method will create two copies of the
        model object with that attribute the same and test for an exception
        from the database layer.
        """

        self.failIf(len(self.sample) < 2, "not enough sample data in the self.sample list to test uniqueness")

        for col in self.uniques:

            self.get_table().insert().execute(self.sample[0])

            attr = {}
            attr.update(self.sample[1])

            attr[col] = self.sample[0][col]

            q = self.get_table().insert()
            self.assertRaisesAny(q.execute, attr)

            self.get_table().delete().execute()

            self.check_empty_database()

            
