import sqlalchemy

import zookeepr.models as model
from zookeepr.tests import TestBase, monkeypatch

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
    scoped relative to the module ``zookeepr.models``.

    ``samples`` is a list of dictionaries of columns and their values to use
    when inserting a row into the table.

    ``not_nullables`` is a list of column names that must not be undefined
    in the table.

    ``uniques`` is a list of column names that must uniquely identify
    the object.

    An example using this base class:

    class TestSomeTable(TestTable):
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
        """Test insertion of sample data

        Insert a row into the table, check that it was
        inserted into the database, and then delete it.
    
        Set the attributes for this model object in the ``attrs`` class
        variable.
        """

        self.failIf(len(self.samples) < 1, "not enough sample data, stranger")
        
        for sample in self.samples:
            print "testing insert of s %s" % sample
            query = self.get_table().insert()
            query.execute(sample)

            for key in sample.keys():
                col = getattr(self.get_table().c, key)
                query = sqlalchemy.select([col])
                result = query.execute()
                print result
                row = result.fetchone()
                print "row", row
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
            print "testing that %s is not nullable" % col
            
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

__all__ = ['TableTest', 'model']
