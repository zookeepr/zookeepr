from zookeepr.tests import *
from zookeepr.models import *

class TestSubmissionController(TestController):
#     def test_index(self):
#         response = self.app.get(url_for(controller='submission'))
#         # Test response...
#         print response

    def test_create(self):
        """Test create action on /submission"""

        ## create a new one
        u = url_for(controller='/submission', action='new')
        print 'url for create is %s' % u
        res = self.app.post(u,
                            params={'submission.title': 'create'})

        # check that it's in the database
        ss = Submission.select_by(title='create')
        self.failIf(len(ss) == 0, "object not in database")
        self.failUnless(len(ss) == 1, "too many objects in database")
        s = ss[0]

        # clean up
        s.delete()
        objectstore.commit()
        # check
        ss = Submission.select()
        self.failUnless(len(ss) == 0, "database is not empty")

    def test_edit(self):
        """Test edit operation on /submission"""

        # create something in the db
        s = Submission(title='edit')
        objectstore.commit()
        sid = s.id

        ## edit it
        u = url_for(controller='/submission', action='edit', id=sid)
        params = {'submission.title': 'edited'}
        res = self.app.post(u, params=params)

        # check db
        s = Submission.get(sid)
        self.failUnless(s.title == 'edited', "edit failed")

        # clean up
        s.delete()
        objectstore.commit()
        # check
        ss = Submission.select()
        print 'remaining in db: %s' % ss
        self.failUnless(len(ss) == 0, "database is not empty")

    def test_delete(self):
        """Test delete operation on /submission"""

        # create something
        s = Submission(title='delete')
        objectstore.commit()
        sid = s.id

        ## delete it
        u = url_for(controller='/submission', action='delete', id=sid)
        res = self.app.post(u)

        # check db
        s = Submission.get(sid)
        self.failUnless(s is None, "object was not deleted")
        # check
        ss = Submission.select()
        self.failUnless(len(ss) == 0, "database is not empty")

    def test_edit_invalid_get(self):
        """Test GET requests on submission edit are idempotent"""
        # create some data
        s = Submission(title='edit')
        objectstore.commit()
        sid = s.id

        u = url_for(controller='/submission', action='edit', id=sid)
        params = {'submission.title': 'invalid edit'}
        res = self.app.get(u, params=params)

        # check db
        st = Submission.get(sid)
        self.failUnless(s.title == 'edit')

        # clean up
        s.delete()
        objectstore.commit()
        # doublecheck
        ss = Submission.select()
        self.failUnless(len(ss) == 0, "dtabase is not empty")

    def test_delete_invalid_get(self):
        """Test GET requests on submission delete are idempotent"""
        # create some data
        s = Submission(title='delete')
        objectstore.commit()
        sid = s.id

        u = url_for(controller='/submission', action='delete', id=sid)
        res = self.app.get(u)
        # check
        s = Submission.get(sid)
        self.failIf(s is None, "object was deleted")
        
        # clean up
        s.delete()
        objectstore.commit()
        # doublecheck
        ss = Submission.select()
        self.failUnless(len(ss) == 0, "database is not empty")

    def test_create_invalid_get(self):
        """Test GET requests on submission new are idempotent"""

        # verify there's nothing in there
        ss = Submission.select()
        self.failUnless(len(ss) == 0, "database was not empty")
        
        u = url_for(controller='/submission', action='new')
        params = {'submission.title': 'create'}
        res = self.app.get(u, params=params)
        
        # check
        ss = Submission.select()
        self.failUnless(len(ss) == 0, "database is not empty")

    def test_delete_nonexistent(self):
        """Test delete of nonexistent submission types is caught"""

        # make sure there's nothing in there
        ss = Submission.select()
        self.failUnless(len(ss) == 0, "database was not empty")
        
        u = url_for(controller='/submission', action='delete', id=1)
        res = self.app.post(u)

        # check
        ss = Submission.select()
        self.failUnless(len(ss) == 0, "database is not empty")
        
