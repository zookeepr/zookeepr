from zookeepr.tests import *
from zookeepr.models import *

class TestSubmissiontypeController(TestController):
    def test_routing(self):
        """Test url routing for /submissiontype controller"""

        # print to clear output when running verbose
        print
        
        # controller w/o action or id
        u = url_for(controller='/submissiontype')
        print "base controller url: %s" % u
        self.failUnless(u == '/submissiontype')

        # controller w/ index action
        u = url_for(controller='/submissiontype', action='index')
        print "index action url: %s" % u
        self.failUnless(u == '/submissiontype')
        
        # controller w/ new action
        u = url_for(controller='/submissiontype', action='new')
        print "new action url: %s" % u
        self.failUnless(u == '/submissiontype/new')

        # controller w/ view action
        u = url_for(controller='/submissiontype', action='view', id=1)
        print "view action url: %s" % u
        self.failUnless(u == '/submissiontype/1')

        # controller w/ other actions and id
        for action in ['edit', 'update', 'delete']:
            u = url_for(controller='/submissiontype', action=action, id=1)
            print "%s action url: %s" % (action, u)
            self.failUnless(u == '/submissiontype/1/%s' % action)


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
        res.mustcontain('list subtypes')

        # check db
        sub = SubmissionType.get(subid)
        self.failUnless(sub.name == 'Feh fuh')

        ## delete it
        del_url = url_for(controller='/submissiontype', action='delete', id=subid)
        res = self.app.get(del_url)
        res.mustcontain('Delete submission type')
        res.mustcontain('Are you sure?')

        res = self.app.post(del_url, params=dict(id=subid))
        res = res.follow()
        res.mustcontain('list subtypes')

        # check db
        subs = SubmissionType.select_by(name='Asterisk Talk')
        self.failUnless(len(subs) == 0, "still subtypes left in the db")


    def setUp(self):
        objectstore.clear()
        submission_type.delete(exists())
