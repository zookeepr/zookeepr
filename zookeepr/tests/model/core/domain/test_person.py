import md5

from zookeepr.tests.model import *

class TestPerson(ModelTest):
    model = 'core.Person'

    samples = [dict(handle='testguy',
                    email_address='testguy@example.org',
                    password='p4ssw0rd',
                    firstname='Testguy',
                    lastname='McTest',
                    phone='+61295555555',
                    ),
               dict(handle='testgirl',
                    email_address='testgrrl@example.com',
                    password='foobar',
                    firstname='Testgirl',
                    lastname='Von Test',
                    phone="37",
                    fax="42",
                    ),
               ]

    mangles = dict(password=lambda p: md5.new(p).hexdigest())
