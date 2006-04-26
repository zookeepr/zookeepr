import unittest

from sqlalchemy import *
from zookeepr.models import *

class TestSubmissionType(unittest.TestCase):
    def test_new(self):
        p = SubmissionType('Paper')

        objectstore.commit()

        assert p.name == 'Paper'

        # verify that it's in the database?
        
