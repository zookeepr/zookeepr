from zookeepr.tests.functional import *

class TestSubmissionType(ControllerTest):
    model = model.SubmissionType
    name = 'submissiontype'
    url = '/submissiontype'
    samples = [dict(name='Paper'),
               dict(name='BOF')]
    
# #     def test_index(self):
# #         print
# #         print "url for submission type is %s" % url_for(controller='submissiontype')
# #         response = self.app.get(url_for(controller='submissiontype'))
# #         # Test response...
# #         print response

#     def setUp(self):
#         TestController.setUp(self)

#         objectstore.clear()

#         p = Person(handle='root',
#                    password='root',
#                    email_address='')
#         r = Role('admin')
#         p.roles.append(r)

#         objectstore.flush()
#         self.pid = p.id
#         self.rid = r.id

#     def tearDown(self):
#         objectstore.clear()
        
#         p = Person.get(self.pid)
#         r = Role.get(self.rid)
#         p.delete()
#         r.delete()
#         objectstore.flush()

#     def signin(self):
#         signin_u = url_for(controller='/account', action='signin')
#         signin_p = dict(username='root', password='root', go='Submit')
#         res = self.app.post(signin_u, params=signin_p)
#         self.assertEqual(res.request.environ['REMOTE_USER'], 'root')

#     def check(self):
#         self.assertEqual(len(SubmissionType.select()), 0)

#     def test_create(self):
#         """Test create action on /submissiontype"""

#         self.check()

#         self.signin()

#         ## create a new one
#         u = url_for(controller='/submissiontype', action='new')
#         print 'url for create is %s' % u
#         params = {'submissiontype.name': 'Asterisk Talk'}
#         res = self.app.post(u, params)

#         # check that it's in the database
#         sts = SubmissionType.select_by(name='Asterisk Talk')
#         self.assertNotEqual(len(sts), 0)
#         self.assertEqual(len(sts), 1)
#         st = sts[0]

#         # clean up
#         st.delete()
#         objectstore.flush()

#         self.check()

#     def test_edit(self):
#         """Test edit operation on /submissiontype"""

#         self.check()
        
#         self.signin()
        
#         # create something in the db
#         st = SubmissionType(name='paper')
#         objectstore.commit()
#         stid = st.id

#         ## edit it
#         u = url_for(controller='/submissiontype', action='edit', id=stid)
#         res = self.app.post(u,
#                             params={'submissiontype.name': 'lightning talk'})

#         # check db
#         st = SubmissionType.get(stid)
#         self.failUnless(st.name == 'lightning talk', "edit failed")

#         # clean up
#         st.delete()
#         objectstore.commit()

#         self.check()

#     def test_delete(self):
#         """Test delete operation on /submissiontype"""

#         self.check()
        
#         self.signin()

#         # create something
#         st = SubmissionType(name='scissors')
#         objectstore.commit()
#         stid = st.id

#         ## delete it
#         u = url_for(controller='/submissiontype', action='delete', id=stid)
#         #res = self.app.get(del_url)
#         #res.mustcontain('Delete submission type')
#         #res.mustcontain('Are you sure?')

#         res = self.app.post(u)
#         #res = res.follow()
#         #res.mustcontain('List submission types')

#         # check db
#         st = SubmissionType.get(stid)
#         self.failUnless(st is None, "object was not deleted")

#         self.check()

#     def test_invalid_get_on_edit(self):
#         """Test that GET requests on submission type edit don't modify data"""

#         self.check()
        
#         # create some data
#         st = SubmissionType(name='buzz')
#         objectstore.commit()
#         stid = st.id

#         self.signin()

#         u = url_for(controller='/submissiontype', action='edit', id=stid)
#         res = self.app.get(u, params={'submissiontype.name':'feh'})

#         # check db
#         st = SubmissionType.get(stid)
#         self.failUnless(st.name == 'buzz')

#         # clean up
#         st.delete()
#         objectstore.commit()

#         self.check()

#     def test_invalid_get_on_delete(self):
#         """Test that GET requests on submission type delete don't modify data"""

#         self.check()
        
#         # create some data
#         st = SubmissionType(name='buzzd')
#         objectstore.commit()
#         stid = st.id

#         self.signin()

#         u = url_for(controller='/submissiontype', action='delete', id=stid)
#         res = self.app.get(u)
        
#         # check
#         st = SubmissionType.get(stid)
#         self.failIf(st is None, "object was deleted")
        
#         # clean up
#         st.delete()
#         objectstore.commit()

#         self.check()

#     def test_invalid_get_on_new(self):
#         """Test that GET requests on submission type new don't modify data"""

#         self.check()

#         self.signin()
        
#         u = url_for(controller='/submissiontype', action='new')
#         p = {'submissiontype.name': 'buzzn'}
        
#         res = self.app.get(u, params=p)

#         self.check()

#     def test_invalid_delete(self):
#         """Test delete of nonexistent submission types is caught"""

#         # make sure there's nothing in there
#         self.check()

#         self.signin()
        
#         u = url_for(controller='/submissiontype', action='delete', id=1)
#         res = self.app.post(u)

#         self.check()
