import unittest

from sqlalchemy import *

from zookeepr.models import *

class TestSubmissionTypeModel(unittest.TestCase):
    def test_new(self):
        """Test basic operations on a SubmissionType"""
        paper = SubmissionType('Paper')

        objectstore.commit()

        assert paper.name == 'Paper'

        paperid = paper.id

        # verify that it's in the database
        paper = SubmissionType.get(paperid)

        assert paper.name == 'Paper'

        paper.delete()
        
        objectstore.commit()

        self.assert_(SubmissionType.get(paperid) is None)

        sts = SubmissionType.select(SubmissionType.c.id>=0)

        assert len(sts) == 0

    def setUp(self):
        objectstore.clear()
