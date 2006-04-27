from zookeepr.tests import *
from zookeepr.models import *

class TestSubmissiontypeController(TestController):
#     def test_index(self):
#         print
#         print "url for submission type is %s" % url_for(controller='submissiontype')
#         response = self.app.get(url_for(controller='submissiontype'))
#         # Test response...
#         print response

    def test_new(self):
        """Test basic operations on /submissiontype controller"""
        print

        ## create a new one
        new_url = url_for(controller='/submissiontype', action='new')
        res = self.app.get(new_url)
        res.mustcontain('New submission type')
        res.mustcontain('Name:')

        res = self.app.post(new_url,
                            params=dict(name='Asterisk Talk'))

        # follow redirect
        res = res.follow()
        # check that we're viewing the correct id!
        res.mustcontain('View submission type')
        res.mustcontain('Name:')
        res.mustcontain('Asterisk Talk')

        # check that it's in the database!
        subs = SubmissionType.select_by(name='Asterisk Talk')
        assert len(subs) == 1
        sub = subs[0]

        subid = sub.id

        ## edit it
        ed_url = url_for(controller='/submissiontype', action='edit', id=subid)
        res = self.app.get(ed_url)
        res.mustcontain('Edit submission type')
        res.mustcontain('Name:')
        res = self.app.post(ed_url,
                            params=dict(name='Feh fuh'))

        # follow redirect?
        res = res.follow()
        res.mustcontain('List submission types')
        res.mustcontain('Feh fuh')

        # check db
        sub = SubmissionType.get(subid)
        self.failUnless(sub.name == 'Feh fuh')

        ## delete it
        del_url = url_for(controller='/submissiontype', action='delete', id=subid)
        res = self.app.get(del_url)
        res.mustcontain('Delete submission type')
        res.mustcontain('Are you sure?')

        res = self.app.post(del_url, params=dict(delete='ok', id=subid))
        res = res.follow()
        res.mustcontain('List submission types')

        # check db
        subs = SubmissionType.select_by(name='Asterisk Talk')
        self.failUnless(len(subs) == 0, "still subtypes left in the db")

    def test_invalid_get_on_edit(self):
        """Test that GET requests on edit action don't modify data"""
        # create some data
        sub = SubmissionType(name='buzz')
        objectstore.commit()

        u = url_for(controller='/submissiontype', action='edit', id=sub.id)
        res = self.app.get(u, params=dict(name='feh'))
        res.mustcontain('Edit submission type')

        self.failUnless(sub.name == 'buzz')

        # clean up
        sub.delete()
        objectstore.commit()
        # doublecheck
        subs = SubmissionType.select()
        assert len(subs) == 0

    def test_invalid_get_on_delete(self):
        """Test that GET requests on delete action don't modify data"""
        # create some data
        sub = SubmissionType(name='buzzd')
        objectstore.commit()

        subid = sub.id
        u = url_for(controller='/submissiontype', action='delete', id=subid)
        res = self.app.get(u, params=dict(delete='ok', id=subid))
        res.mustcontain('Delete submission type')

        sub = SubmissionType.get(subid)
        self.failUnless(sub is not None)
        
        # clean up
        sub.delete()
        objectstore.commit()
        # doublecheck
        subs = SubmissionType.select()
        assert len(subs) == 0

    def test_invalid_get_on_new(self):
        """Test that GET requests on new action don't modify data"""

        u = url_for(controller='/submissiontype', action='new')
        res = self.app.get(u, params=dict(name='buzzn'))
        res.mustcontain('New submission type')

        subs = SubmissionType.select()
        assert len(subs) == 0
    

    def setUp(self):
        objectstore.clear()
        submission_type.delete(exists())
