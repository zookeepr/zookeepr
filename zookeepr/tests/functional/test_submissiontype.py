from zookeepr.tests import *
from zookeepr.models import *

class TestSubmissiontypeController(TestController):
    def test_index(self):
        response = self.app.get(url_for(controller='submissiontype'))
        # Test response...

    def test_new(self):
        res = self.app.get(url_for(controller='submissiontype', action='new'))

        res.mustcontain('Name:')

        res = self.app.get(url_for(controller='submissiontype', action='new'), params=dict(name='Asterisk Talk'))

        # follow redirect
        res = res.follow()

        # viewing a subtype
        res.mustcontain('view subtype')

        # check that it's in the database!
        subs = SubmissionType.select_by(name='Asterisk Talk')
        assert len(subs) == 1
        sub = subs[0]

        # check that we're viewing the correct id!
        res.mustcontain('view subtype %d' % sub.id)
