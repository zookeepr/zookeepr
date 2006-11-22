# import md5

# from zookeepr.tests.functional import *

# class TestPerson(SignedInCRUDControllerTest):
#     model = model.Person
#     name = 'person'
#     url = '/person'
#     samples = [dict(handle='testguy',
#                     email_address='testguy@example.org',
#                     password='p4ssw0rd',
#                     password_confirm='p4ssw0rd',
#                     firstname='Testy',
#                     lastname='Guy',
#                     phone='37373737',
#                     fax='42424242'
#                     ),
#                dict(handle='testgirl',
#                     email_address='testgirl@example.com',
#                     password='test',
#                     password_confirm='test',
#                     firstname='Ytset',
#                     lastname='Girl',
#                     phone='12121212',
#                     fax='23232323'
#                     ),
#                ]
#     no_test = ['password_confirm']
#     mangles = dict(password=lambda p: md5.new(p).hexdigest())
#     crud = ['edit']
