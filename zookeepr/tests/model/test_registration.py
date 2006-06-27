import datetime
import md5

from zookeepr.tests.model import *

class TestRegistrationModel(ModelTest):
    model = 'Registration'
    samples = [dict(timestamp=datetime.datetime.now(),
                    url_hash=md5.new("snuh").hexdigest(),
                    email_address='testguy@example.org',
                    password='password',
                    activated=True,
                    ),
               dict(timestamp=datetime.datetime(2006, 6, 25, 10, 11, 37),
                    url_hash=md5.new("buh").hexdigest(),
                    email_address='testgirl@example.org',
                    password='password1',
                    activated=False,
                    ),
               ]
    mangles = dict(password=lambda p: md5.new(p).hexdigest())
