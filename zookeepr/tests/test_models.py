import unittest

from sqlalchemy import *
from zookeepr.models import *

class TestPersonModel(unittest.TestCase):
    def test_new(self):
        p = Person('testguy')
        objectstore.commit()

        assert p.handle == 'testguy'
        
        # verify that it's in the database?
        
