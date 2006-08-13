import md5
import re

from paste.fixture import Dummy_smtplib

from zookeepr.model import Person, Submission, SubmissionType
from zookeepr.tests.functional import *

class TestCFP(ControllerTest):
    def test_index(self):
        res = self.app.get('/cfp')
        
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
                    'type': 1,
                    'experience': 'some',
                    'url': 'http://example.org',
                    'attachment': buffer('foo'),
                    'assistance': True,
                    }
        for k in reg_data.keys():
            form['registration.' + k] = reg_data[k]
        for k in sub_data.keys():
            form['submission.' + k] = sub_data[k]

        form.submit()

        regs = self.objectstore.query(Person).select()
        self.assertEqual(1, len(regs))

        for key in reg_data.keys():
            self.check_attribute(regs[0], key, reg_data[key])

        subs = self.objectstore.query(Submission).select()
        self.assertEqual(1, len(subs))

        for key in sub_data.keys():
            self.check_attribute(subs[0], key, sub_data[key])

        self.objectstore.delete(regs[0])
        self.objectstore.delete(subs[0])
        self.objectstore.flush()

    # FIXME: not testing type
    no_test = ['password_confirm', 'type']
    mangles = dict(password = lambda p: md5.new(p).hexdigest(),
                   attachment = lambda a: buffer(a),
                   #type = lambda t: TestCFP.objectstore.query(SubmissionType).get(1),
                   )

    def setUp(self):
        ControllerTest.setUp(self)
        st1 = SubmissionType('Paper')
        st2 = SubmissionType('Scissors')
        self.objectstore.save(st1)
        self.objectstore.save(st2)
        self.objectstore.flush()
        self.stid = (st1.id, st2.id)

    def tearDown(self):
        st1 = self.objectstore.query(SubmissionType).get(self.stid[0])
        st2 = self.objectstore.query(SubmissionType).get(self.stid[1])
        self.objectstore.delete(st2)
        self.objectstore.delete(st1)
        self.objectstore.flush()
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
             'registration.fullname': 'Testguy McTest',
             'submission.title': 'title',
             'submission.abstract': 'abstract',
             'submission.type': 1,
             'submission.attachment': '',
             'submission.assistance': False,
             }
        for k in d.keys():
            form[k] = d[k]
        res1 = form.submit()

        # thankyou page says what email address got sent to
        res1.mustcontain('testguy@example.org')

        # grab it from the db
        regs = self.objectstore.query(Person).select()
        self.assertEqual(1, len(regs))
        # make sure that it's inactive
        self.assertEqual(False, regs[0].activated)

        # clear this session, we want to reselect this data later
        self.objectstore.clear()
        
        
        # get out the url hash because i don't know how to trap smtplib
        self.failIfEqual(None, Dummy_smtplib.existing, "no message sent from submission")
        
        message = Dummy_smtplib.existing

        print "message: '''%s'''" % message.message

        # check that the message goes to the right place
        self.assertEqual("testguy@example.org", message.to_addresses)

        # check that the message has the to address in it
        to_match = re.match(r'^.*To:.*testguy@example.org.*', message.message, re.DOTALL)
        self.failIfEqual(None, to_match, "to address not in headers")

        # check that the message has the submitter's name
        name_match = re.match(r'^.*Testguy McTest', message.message, re.DOTALL)
        self.failIfEqual(None, name_match, "submitter's name not in headers")

        # check that the message was renderered without HTML, i.e.
        # as a fragment and thus no autohandler crap
        html_match = re.match(r'^.*<!DOCTYPE', message.message, re.DOTALL)
        self.failUnlessEqual(None, html_match, "HTML in message!")
        
        # check that the message has a url hash in it
        match = re.match(r'^.*/register/confirm/(\S+)', message.message, re.DOTALL)
        print "match:", match
        self.failIfEqual(None, match, "url not found")

        # visit the url
        print "match: '''%s'''" % match.group(1)
        res = self.app.get('/register/confirm/%s' % match.group(1))
        print res
        
        # check the rego worked
        regs = self.objectstore.query(Person).select()
        self.assertEqual(1, len(regs))
        print regs[0]
        self.assertEqual(True, regs[0].activated, "registration was not activated!")

        # clean up
        Dummy_smtplib.existing.reset()

        self.objectstore.delete(regs[0])
        self.objectstore.delete(self.objectstore.query(Submission).select()[0])
        self.objectstore.flush()

        self.assertEmptyModel(Submission)
        self.assertEmptyModel(Person)
