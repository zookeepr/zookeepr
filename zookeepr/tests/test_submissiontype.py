import os
import unittest

from sqlalchemy import *

from zookeepr.models import *

class TestSubmissionTypeModel(unittest.TestCase):
    def check(self):
        self.assertEqual(len(SubmissionType.select()), 0)
        
    def test_basic(self):
        """Test basic operations on SubmissionType model"""

        # assert that the table is empty
        self.check()

        # create
        st = SubmissionType('Paper')
        objectstore.commit()
        self.failUnless(st.name == 'Paper', "did not set object name")
        stid = st.id
        # verify that it's in the database
        st = SubmissionType.get(stid)
        self.failIf(st is None, "object not in database")
        self.failUnless(st.name == 'Paper', "object name not correct")

        # delete it
        st.delete()
        objectstore.commit()
        st = SubmissionType.get(stid)
        self.failUnless(st is None, "did not delete submissinotype")

        # check table is empty when we leave
        self.check()

    def test_name_not_null(self):
        """Test that submission_type.name is not null"""

        self.check()
        
        st = SubmissionType()

        self.assertRaises(SQLError, objectstore.flush)
        
        objectstore.clear()
        self.check()

    def setUp(self):
        objectstore.clear()
