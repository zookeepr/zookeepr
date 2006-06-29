import datetime
import md5

from zookeepr.tests.model import *

class TestRegistrationModel(ModelTest):
    model = 'Registration'
    samples = [dict(
                    email_address='testguy@example.org',
                    password='password',
                    activated=True,
                    ),
               dict(timestamp=datetime.datetime(2006, 6, 25, 10, 11, 37),
                    email_address='testgirl@example.org',
                    password='password1',
                    activated=False,
                    ),
               ]
    mangles = dict(password=lambda p: md5.new(p).hexdigest())
