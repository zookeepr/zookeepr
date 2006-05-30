import datetime
import md5

from zookeepr.tests.model import *

class TestRegistrationModel(ModelTest):
    model = 'Registration'
    samples = [dict(timestamp=datetime.datetime.now(),
                    url_hash=md5.new("snuh").hexdigest(),
                    email_address='testguy@example.org',
                    password='password',
                    ),
               ]
    mangles = dict(password=lambda p: md5.new(p).hexdigest())
