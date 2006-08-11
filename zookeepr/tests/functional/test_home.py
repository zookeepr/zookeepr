from zookeepr.model import Person, Submission
from zookeepr.tests.functional import *

class TestHomeController(ControllerTest):
    def test_index(self):
        response = self.app.get(url_for(controller='home'))

#     def test_index_logged_in(self):
#         p = Person(email_address='testguy@testguy.org',
#                    password='test',
#                    firstname='Testguy')
#         p.save()
#         print p
#         #s = Submission(title='foo')
#         # s.save()
#         # p.submissions.append(s)
#         objectstore.flush()

#         print p

# #         resp = self.app.get(url_for(controller='account',action='signin'))
# #         f = resp.form
# #         f['email_address'] = 'testguy@example.org'
# #         f['password'] = 'test'
# #         resp = f.submit()
# #         self.failUnless('person_id' in resp.session)
# #         resp = resp.follow()
# #         self.assertEqual('/', resp.url)
# #         resp.mustcontain("Welcome, <strong>Testguy</strong>!")
# #         resp.mustcontain("foo")
        
        
#         p.delete()
# #         s.delete()
#         objectstore.flush()
