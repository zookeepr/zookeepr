import re

from paste.fixture import Dummy_smtplib

from zookeepr.tests.functional import *

class TestRegistrationController(ControllerTest):
    model = model.registration.Registration
    url = '/registration'
    param_name = 'registration'
    samples = [dict(registration=dict(address1='a1',
                                      address2='a2',
                                      city='city',
                                      state='state1',
                                      country='country1',
                                      postcode='postcode1',
                                      phone='37',
                                      company='company1',
                                      shelltext='shelltext1',
                                      editortext='editortext1',
                                      distrotext='distrotext1',
                                      type='Professional',
                                      discount_code='discount_code1',
                                      teesize='M_M',
                                      diet='diet1',
                                      special='special1',
                                      opendaydrag=1,
                                      partner_email='partner@example.org',
                                      kids_0_3=1,
                                      kids_4_6=1,
                                      kids_7_9=1,
                                      kids_10=1,
                                      checkin=14,
                                      checkout=20,
                                      lasignup=True,
                                      announcesignup=True,
                                      delegatesignup=False,
                                      editor='-',
                                      distro='-',
                                      shell='-',
                                      accommodation='own',
                                      ),
                    person=dict(email_address='testguy@example.org',
                                password='test',
                                password_confirm='test',
                                handle='testguy',
                                fullname='testguy mctest',
                                )
                    )
               ]
    no_test = ['password_confirm', 'person']
    crud = ['create']
    
    def setUp(self):
        super(TestRegistrationController, self).setUp()
        Dummy_smtplib.install()

    def tearDown(self):
        Dummy_smtplib.existing.reset()

        ps = Query(model.Person).select()
        for p in ps:
            objectstore.delete(p)
        objectstore.flush()
        super(TestRegistrationController, self).tearDown()

class TestSignedInRegistrationController(SignedInControllerTest):

    def test_existing_account_registration(self):
        """Test that someone with an existing account can register.

        """
        resp = self.app.get('/registration/new')
        f = resp.form
        print f.fields.keys()
        self.failIf('person.fullname' in f.fields.keys(), "form asking for person details of signed in person")
        sample_data = dict(address1='a1',
            city='Sydney',
            state='NSW',
            country='Australia',
            postcode='2001',
            type='Professional',
            teesize='M_M',
            checkin=14,
            checkout=20,
            accommodation='own',
            )
        for k in sample_data.keys():
            f['registration.' + k] = sample_data[k]
        resp = f.submit()
        self.failIf('Missing value' in resp, "form validation failed")
        resp.mustcontain('testguy@example.org')

        self.failIfEqual(None, Dummy_smtplib.existing, "no message sent from registration")

        message = Dummy_smtplib.existing

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

        # test that we have a registration
        regs = Query(model.Registration).select()
        self.failIfEqual([], regs)
        self.assertEqual(self.person.id, regs[0].person.id)

        # clean up
        objectstore.delete(regs[0])
        objectstore.flush()
