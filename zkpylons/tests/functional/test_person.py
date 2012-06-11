# import md5

# from zkpylons.tests.functional import *

# class TestPerson(SignedInCRUDControllerTest):
#     model = model.Person
#     name = 'person'
#     url = '/person'
#     samples = [dict(handle='testguy',
#                     email_address='testguy@example.org',
#                     password='p4ssw0rd',
#                     password_confirm='p4ssw0rd',
#                     fullname='Testy Guy',
#                     phone='37373737',
#                     mobile='42424242'
#                     ),
#                dict(handle='testgirl',
#                     email_address='testgirl@example.com',
#                     password='test',
#                     password_confirm='test',
#                     fullname='Ytset Girl',
#                     phone='12121212',
#                     mobile='23232323'
#                     ),
#                ]
#     no_test = ['password_confirm']
#     mangles = dict(password=lambda p: md5.new(p).hexdigest())
#     crud = ['edit']
