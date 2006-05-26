import datetime
import md5

from zookeepr.tests.model import *

class TestRegistrationModel(TestModel):
    model = 'Registration'
    attrs = dict(timestamp=datetime.datetime.now(),
                 url_hash=md5.new("snuh").hexdigest())
    not_null = ['timestamp', 'url_hash']

    def test_create(self):
        self.create()

    def test_not_nullable(self):
        self.not_nullable()
