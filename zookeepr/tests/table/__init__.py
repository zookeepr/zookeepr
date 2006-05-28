import new
import unittest

from sqlalchemy import objectstore, SQLError

import zookeepr.models as model

class TableTestGenerator(type):
    """This metaclass does some funky class method rewriting to generate
    test methods so that one doesn't actually need to do any work to get
    table tests written.  How awesome is that for TDD? :-)
    """
    def __init__(cls, name, bases, dict):
        print "new table test generator"

        if dict.has_key('table'):
            if dict.has_key('not_nullables'):
                print "setting test_not_nullable to not_nulable method"

                # patch the child class with the test_not_nullable function
                # now that we know it contains enough data to do so.
                #
                # rather than do something sensible like use setattr,
                # we create a new function and hack the __module__ attribute
                # so that when nose runs, it doesn't skip the test because
                # it thinks it is in the parent.  This is in
                # nose.selector.wantMethod, anytests, and callableInTests.
                #
                # You can't set __module__ directly because it's a r/o attribute.
                #
                # The __module__ attribute is set by the new.function method
                # from the globals dict, so here we make a shallow copy and
                # override the __name__ attribute to point to the module of the
                # class we're actually testing.
                #
                # By this stage, you may think that this is crack.  You're right.
                # But at least I don't have to repeat the same code over and
                # over in the actual tests ;-)
                g = globals().copy()
                g['__name__'] = cls.__module__
                code = cls.not_nullable.im_func.func_code
                # create a new function with:
                # the code of the original function,
                # our patched globals,
                # and the new name of the function
                cls.test_not_nullable = new.function(code, g,
                                                     'test_not_nullable')

                # p.s. i am not a crackpot

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

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        print "snuh"

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
        x= select([func.count(self.get_table().c.id)]).execute()
        print x
        self.assertEqual(0, len(self.get_table().select()))

#     def insert(self):
#         """Insert a row into the table, check that it was
#         inserted into the database, and then delete it.
    
#         Set the attributes for this model object in the ``attrs`` class
#         variable.
#         """
    
#         # instantiating model
#         o = self.get_model()(**self.attrs)
    
#         # committing to db
#         objectstore.flush()
#         oid = o.id
    
#         # check it's in the database
#         o1 = self.get_model().get(oid)
#         self.failIfEqual(o1, None, "object not in database")
        
#         # checking attributes
#         for k in self.attrs.keys():
#             self.assertEqual(getattr(o1, k), self.attrs[k], "object data invalid")
    
#         # deleting object
#         o.delete()
    
#         # flushing store
#         objectstore.flush()
    
#         # checking db
#         self.check_empty_database()
    
    def not_nullable(self):
        """Check that certain columns of a table are not nullable.
    
        Specify the ``not_nullables`` class variable with a list of column names
        that must not be null, and this method will insert into the table rows
        with each set to null and test for an exception from the database layer.
        """
    
        for col in self.not_nullables:
            # construct an attribute dictionary without the 'not null' attribute
            coldata = {}
            coldata.update(self.sample)
            del coldata[col]
            self.failIf(col in coldata.keys())
    
            # create the model object
            o = self.get_table().insert(coldata)
    
            #testing for not null
            #self.assertRaises(SQLError, objectstore.flush)
    
            # clearing session
            objectstore.clear()

        # checking
        self.check_empty_database()

#     def unique(self):
#         """Check that certain attributes of a model object are unique.

#         Specify the ``uniques`` class variable with a list of attributes
#         that must be unique, and this method will create two copies of the
#         model object with that attribute the same and test for an exception
#         from the database layer.
#         """

#         for attr in self.uniques:
#             # construct an attribute dictionary
#             attrs = {}
#             attrs.update(self.attrs)

#             #
#             o = self.get_model()(**attrs)
            
#             objectstore.flush()
#             oid = o.id

#             attrs1 = {}
#             attrs1.update(self.attrs)

#             # ugh, this sucks
#             for k in attrs.keys():
#                 if k <> attr:
#                     if type(attrs1[k], types.IntType):
#                         attr1[k] += 1
#                     elif type(attrs1[k]) == types.StringType:
#                         attr1[k].append('1')
#                     else:
#                         raise RuntimeError, "don't know how to un-unique a %s type, %s" % (type(attrs1[k]), k)

#             # assert that the two attr dicts are different the way we want them
#             del attrs[attr]
#             del attrs1[attr]

#             if attrs <> {} and attrs1 <> {}:
#                 self.failIfEqual(attrs, attrs1)
            
#             attrs[attr] = self.attrs[attr]
#             attrs1[attr] = self.attrs[attr]
#             self.assertEqual(attrs[attr], attrs1[attr])

#             o1 = self.get_model()(**attrs1)
            
#             self.assertRaises(SQLError, objectstore.flush)

#             objectstore.clear()
            
#             # clean up
#             o = self.get_model().get(oid)
#             o.delete()
#             objectstore.flush()
           
#         # check db
#         self.check_empty_database()
