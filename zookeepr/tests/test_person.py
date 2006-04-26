import unittest
import md5

from sqlalchemy import *
from zookeepr.models import *

class TestPersonModel(unittest.TestCase):
    def test_new(self):
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
        
