from zookeepr.tests.model import *

class TestSubmissionTypeModel(TestModel):
    model = 'SubmissionType'
    attrs = dict(name='example')
    not_null = ['name']

    def test_create(self):
        self.create()

    def test_not_nullable(self):
        self.not_nullable()
