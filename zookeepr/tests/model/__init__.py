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
            monkeypatch(cls, 'test_create', 'create')


class ModelTest(TestBase):
    """Base class for testing the data model.

    Derived classes should set the following attributes:

    ``model`` is a string containing the name of the class being tested,
    scoped relative to the module ``zookeepr.models``.

    ``samples`` is a list of dictionaries of attributes to use when
    creating test model objects.

    An example using this base class:

    class TestSomeModel(TestModel):
        model = 'module.User'
        samples = [dict(name='testguy',
                        email_address='test@example.org')]
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

    def create(self):
        """Create an object of the data model, check that it was
        inserted into the database, and then delete it.
    
        Set the attributes for this model object in the ``attrs`` class
        variable.
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
            for key in self.attrs.keys():
                self.assertEqual(sample[key], getattr(o, key),
                                 "object data invalid")
    
            # deleting object
            session.delete(o)
            session.flush()
    
            # checking db
            self.check_empty_session()

        session.close()
    
#     def not_nullable(self):
#         """Check nullability of certain attributes of a model object.
    
#         Specify the ``not_null`` class variable with a list of attributes
#         that must not be null, and this method will create the model
#         object with each set to null and test for an exception from the
#         database layer.
#         """
    
#         for attr in self.not_null:
#             # construct an attribute dictionary without the 'not null' attribute
#             attrs = {}
#             attrs.update(self.attrs)
#             del attrs[attr]
#             self.failIf(attr in attrs.keys())
    
#             # create the model object
#             o = self.get_model()(**attrs)
    
#             #testing for not null
#             self.assertRaises(SQLError, objectstore.flush)
    
#             # clearing session
#             objectstore.clear()

#         # checking
#         self.check_empty_objectstore()

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
#         self.check_empty_objectstore()
