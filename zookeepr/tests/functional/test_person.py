import md5

from zookeepr.tests.functional import *

class TestPerson(ControllerTest):
#     def test_index(self):
#         response = self.app.get(url_for(controller='person'))
#         # Test response...
#         response.mustcontain("person index")
    model = model.Person
    name = 'person'
    url = '/person'
    samples = [dict(handle='testguy',
                    email_address='testguy@example.org',
                    password='p4ssw0rd',
                    password_confirm='p4ssw0rd'),
               dict(handle='testgirl',
                    email_address='testgirl@example.com',
                    password='test',
                    password_confirm='test'),
               ]
    no_test = ['password_confirm']
    mangles = dict(password=lambda p: md5.new(p).hexdigest())
