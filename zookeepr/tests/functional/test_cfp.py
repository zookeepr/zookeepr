import md5

from zookeepr.tests.functional import *

class TestCFP(ControllerTest):
    model = model.CFP
    name = 'cfp'
    url = '/cfp'
    samples = [dict(email_address='testguy@example.org',
                    password='password',
                    password_confirm='password',
                    title='title yo',
                    abstract='abstract yo',
                    type=1,
                    experience="some",
                    url='http://example.org',
                    attachment='foo',
                    ),
               dict(email_address='testgirl@example.org',
                    password='snuh',
                    password_confirm='snuh',
                    title='some title',
                    abstract='some abstract',
                    type=2,
                    experience="none",
                    url='http://example.com',
                    attachment='bar',
                    ),
               ]
    no_test = ['password_confirm']
    mangles = dict(password = lambda p: md5.new(p).hexdigest(),
                   attachment = lambda a: buffer(a),
                   )

    def setUp(self):
        ControllerTest.setUp(self)
        self.subtype = model.SubmissionType('Paper')
        self.session.save(self.subtype)
        self.session.flush()
        print self.subtype

    def tearDown(self):
        self.session.delete(self.subtype)
        self.session.flush()
        ControllerTest.tearDown(self)
