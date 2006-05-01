import md5
import os
import unittest

from sqlalchemy import *

from zookeepr.models import *

class TestPersonModel(unittest.TestCase):
    def test_new(self):
        """Test simple creation of a Person object"""

        # first let's assert that theres nothing in there
        ps = Person.select()
        self.failUnless(len(ps) == 0, "database is not empty")

        p = Person('testguy',
                   'testguy@example.org',
                   'p4ssw0rd',
                   'Testguy',
                   'McTest',
                   '+61295555555')

        objectstore.commit()

        assert p.handle == 'testguy'
        assert p.email_address == 'testguy@example.org'

        # check password was hashed:
        hasher = md5.new('p4ssw0rd')
        assert p.password_hash == hasher.hexdigest()

        assert p.firstname == 'Testguy'
        assert p.lastname == 'McTest'

        assert p.phone == '+61295555555'
        
        # verify that it's in the database?

        pid = p.id
        p = Person.get(pid)
        self.failUnless(p.handle == 'testguy')

        # clean up
        p.delete()
        objectstore.commit()
        # check
        ps = Person.select()
        assert len(ps) == 0

    def test_unique_handle(self):
        """Test that the handle attribute of Person is unique"""

        # assert that the database is empty so as not to fuck us up
        ps = Person.select()
        self.failIf(len(ps) > 0, "database is not empty")
        
        p1 = Person('test_unique_handle',
                    'test_uq_h1@example.org',
                    'p4ssw0rd',
                    'Testguy',
                    'McTest',
                    '37')
        objectstore.commit()
        p1id = p1.id
        
        p2 = Person('test_unique_handle',
                    'test_uq_h2@example.org',
                    'p4ssw0rd',
                    'Testguy',
                    'McTest',
                    '37')
        # handle is the same, so throw integrityerror
        self.assertRaises(SQLError, objectstore.commit)

        # clean up
        del p2
        objectstore.clear()
        p1 = Person.get(p1id)
        p1.delete()
        objectstore.commit()
        # check
        ps = Person.select()
        self.failUnless(len(ps) == 0, "database was not left clean")

#     def test_too_long_handle(self):
#         # this doesn't work with sqlite due to this FAQ:
#         # http://www.sqlite.org/faq.html#q11
#         p = Person('a'*42,
#                    'test_too_long@example.org',
#                    'p4ssw0rd',
#                    'Testguy',
#                    'McTest',
#                    '+61295555555')

#         objectstore.commit()

#         p1 = Person.mapper.select_by(email_address='test_too_long@example.org')
#         assert p1[0].handle == 'a'*40
