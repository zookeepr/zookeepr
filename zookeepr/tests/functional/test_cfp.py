import md5

from paste.fixture import Dummy_smtplib

from zookeepr.models import Registration, Submission
from zookeepr.tests.functional import *

class TestCFP(ControllerTest):
    def test_create(self):
        response = self.app.get('/cfp/submit')
        form = response.form

        print form.text
        print form.fields

        reg_data = {'email_address': 'testguy@example.org',
                    'password': 'password',
                    'password_confirm': 'password',
                   }
        sub_data = {'title': 'title',
                    'abstract': 'abstract',
                    #'type': 1,
                    'experience': 'some',
                    'url': 'http://example.org',
                    'attachment': 'foo',
                    'assistance': True,
                    }
        for k in reg_data.keys():
            form['registration.' + k] = reg_data[k]
        for k in sub_data.keys():
            form['submission.' + k] = sub_data[k]

        form.submit()

        regs = self.session.query(Registration).select()
        self.assertEqual(1, len(regs))

        for key in reg_data.keys():
            self.check_attribute(regs[0], key, reg_data[key])

        subs = self.session.query(Submission).select()
        self.assertEqual(1, len(subs))

        for key in sub_data.keys():
            self.check_attribute(subs[0], key, sub_data[key])

        self.session.delete(regs[0])
        self.session.delete(subs[0])
        self.session.flush()

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
                           
        
    def test_cfp_registration(self):
        # set up the smtp catcher
        Dummy_smtplib.install()
        
        # submit to the cfp
        res = self.app.get('/cfp/submit')
        form = res.form
        d = {'registration.email_address': 'testguy@example.org',
             'registration.password': 'test',
             'registration.password_confirm': 'test',
             'submission.title': 'title',
             'submission.abstract': 'abstract',
             'submission.attachment': '',
             'submission.assistance': False,
             }
        for k in d.keys():
            form[k] = d[k]
        res1 = form.submit()
        res1 = res1.follow() # expecting a redirect to a thankyou page
        #print "form submit result", res1
        
        # get out the url hash because i don't know how to trap smtplib
        self.failIfEqual(None, Dummy_smtplib.existing, "no message sent from submission")
        
        #message = Dummy_smtplib.existing
        #print Dummy_smtplib.existing.message
        
        # visit the url
        # check the rego worked
        pass
