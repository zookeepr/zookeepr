from zookeepr.tests import *
from zookeepr.models import *

class TestSubmissiontypeController(TestController):
#     def test_index(self):
#         print
#         print "url for submission type is %s" % url_for(controller='submissiontype')
#         response = self.app.get(url_for(controller='submissiontype'))
#         # Test response...
#         print response

    def test_create(self):
        """Test create action on /submissiontype"""

        ## create a new one
        u = url_for(controller='/submissiontype', action='new')
        print 'url for create is %s' % u
        res = self.app.post(u,
                            params={'submissiontype.name': 'Asterisk Talk'})

        # check that it's in the database
        sts = SubmissionType.select_by(name='Asterisk Talk')
        self.failIf(len(sts) == 0, "object not in database")
        self.failUnless(len(sts) == 1, "too many objects in database")
        st = sts[0]

        # clean up
        st.delete()
        objectstore.commit()
        # check
        sts = SubmissionType.select()
        self.failUnless(len(sts) == 0, "database is not empty")

    def test_edit(self):
        """Test edit operation on /submissiontype"""

        # create something in the db
        st = SubmissionType(name='paper')
        objectstore.commit()
        stid = st.id

        ## edit it
        u = url_for(controller='/submissiontype', action='edit', id=stid)
        res = self.app.post(u,
                            params={'submissiontype.name': 'lightning talk'})

        # check db
        st = SubmissionType.get(stid)
        self.failUnless(st.name == 'lightning talk', "edit failed")

        # clean up
        st.delete()
        objectstore.commit()
        # check
        sts = SubmissionType.select()
        print 'remaining in db: %s' % sts
        self.failUnless(len(sts) == 0, "database is not empty")

    def test_delete(self):
        """Test delete operation on /submissiontype"""

        # create something
        st = SubmissionType(name='scissors')
        objectstore.commit()
        stid = st.id

        ## delete it
        u = url_for(controller='/submissiontype', action='delete', id=stid)
        #res = self.app.get(del_url)
        #res.mustcontain('Delete submission type')
        #res.mustcontain('Are you sure?')

        res = self.app.post(u)
        #res = res.follow()
        #res.mustcontain('List submission types')

        # check db
        st = SubmissionType.get(stid)
        self.failUnless(st is None, "object was not deleted")
        # check
        sts = SubmissionType.select()
        self.failUnless(len(sts) == 0, "database is not empty")

#     def test_invalid_get_on_edit(self):
#         """Test that GET requests on edit action don't modify data"""
#         # create some data
#         sub = SubmissionType(name='buzz')
#         objectstore.commit()

#         u = url_for(controller='/submissiontype', action='edit', id=sub.id)
#         res = self.app.get(u, params=dict(name='feh'))
#         res.mustcontain('Edit submission type')

#         self.failUnless(sub.name == 'buzz')

#         # clean up
#         sub.delete()
#         objectstore.commit()
#         # doublecheck
#         subs = SubmissionType.select()
#         assert len(subs) == 0

#     def test_invalid_get_on_delete(self):
#         """Test that GET requests on delete action don't modify data"""
#         # create some data
#         sub = SubmissionType(name='buzzd')
#         objectstore.commit()

#         subid = sub.id
#         u = url_for(controller='/submissiontype', action='delete', id=subid)
#         res = self.app.get(u, params=dict(delete='ok', id=subid))
#         res.mustcontain('Delete submission type')

#         sub = SubmissionType.get(subid)
#         self.failIf(sub is None)
        
#         # clean up
#         sub.delete()
#         objectstore.commit()
#         # doublecheck
#         subs = SubmissionType.select()
#         assert len(subs) == 0

#     def test_invalid_get_on_new(self):
#         """Test that GET requests on new action don't modify data"""

#         u = url_for(controller='/submissiontype', action='new')
#         res = self.app.get(u, params=dict(name='buzzn'))
#         #res.mustcontain('New submission type')

#         subs = SubmissionType.select()
#         self.failUnless(len(subs) == 0, "database is not empty")

    def test_invalid_delete(self):
        """Test that deletes of nonexistent subtypes are handled gracefully"""

        # make sure there's nothing in there
        subs = SubmissionType.select()
        self.failUnless(len(subs) == 0, "database was not empty")
        
        u = url_for(controller='/submissiontype', action='delete', id=1)
        res = self.app.post(u, status=302)
