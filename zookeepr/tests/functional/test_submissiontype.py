from zookeepr.tests import *
from zookeepr.models import *

class TestSubmissionTypeController(TestController):
    def test_routing(self):
        """Test url routing for /submissiontype controller"""

        # print to clear output when running verbose
        print
        
        # controller w/o action or id
        u = url_for(controller='submissiontype')
        print u
        self.failUnless(u == '/submissiontype')
        
        # controller w/ new action
        u = url_for(controller='submissiontype', action='new')
        print u
        self.failUnless(u == '/submissiontype/new')

        # controller w/ view action
        u = url_for(controller='submissiontype', action='view', id=1)
        print u
        self.failUnless(u == '/submissiontype/1')

        # controller w/ other actions and id
        for action in ['edit', 'update', 'delete']:
            u = url_for(controller='submissiontype', action=action, id=1)
            print u
            self.failUnless(u == '/submissiontype/1/%s' % action)


#     def test_index(self):
#         print
#         print "url for submission type is %s" % url_for(controller='submissiontype')
#         response = self.app.get(url_for(controller='submissiontype'))
#         # Test response...
#         print response

#     def test_new(self):
#         """Test basic operations on /submissiontype controller"""
#         res = self.app.get(url_for(controller='submissiontype', action='new'))
#         res.mustcontain('New submission type')
#         res.mustcontain('Name:')

#         res = self.app.get(url_for(controller='submissiontype', action='new'), params=dict(name='Asterisk Talk'))

#         # follow redirect
#         res = res.follow()

#         # viewing a subtype
#         res.mustcontain('view subtype')

#         # check that it's in the database!
#         subs = SubmissionType.select_by(name='Asterisk Talk')
#         assert len(subs) == 1
#         sub = subs[0]

#         subid = sub.id

#         # check that we're viewing the correct id!
#         res.mustcontain('view subtype %d' % subid)

#         # delete it
#         res = self.app.get(url_for(controller='submissiontype', action='delete', id=subid))
#         res.mustcontain('Delete submission type')
#         res.mustcontain('Are you sure?')

#         res = self.app.post(url_for(controller='submissiontype', action='delete', id=subid), params=dict(id=subid, submit='Submit'))
#         res = res.follow()
#         res.mustcontain('subtype list')
        

#     def setUp(self):
#         objectstore.clear()
#         submission_type.delete(exists())
