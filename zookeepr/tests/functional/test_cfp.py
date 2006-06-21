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
        st1 = model.SubmissionType('Paper')
        st2 = model.SubmissionType('Scissors')
        self.session.save(st1)
        self.session.save(st2)
        self.session.flush()
        self.stid = (st1.id, st2.id)

    def tearDown(self):
        st1 = self.session.get(model.SubmissionType, self.stid[0])
        st2 = self.session.get(model.SubmissionType, self.stid[1])
        self.session.delete(st1)
        self.session.delete(st2)
        self.session.flush()
        ControllerTest.tearDown(self)
