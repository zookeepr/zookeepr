import re

from paste.fixture import Dummy_smtplib

from zookeepr.tests.functional import *

class TestRegistrationController(CRUDControllerTest):
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
                                      silly_description='foo',
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
                                      prevlca={'99': '1'},
                                      miniconf={'Debian': '1'},
                                      accommodation=1,
                                      ),
                    person=dict(email_address='testguy@example.org',
                                password='test',
                                password_confirm='test',
                                handle='testguy',
                                fullname='testguy mctest',
                                )
                    )
               ]
    # FIXME: not testing accommodation object
    no_test = ['password_confirm', 'person', 'accommodation']
    crud = ['create']
    mangles = dict(miniconf = lambda m: m.keys(),
                   prevlca = lambda p: p.keys(),
                   #accommodation = lambda p: None,
                   )

    def setUp(self):
        super(TestRegistrationController, self).setUp()
        Dummy_smtplib.install()

        # create some accommodation
        self.al = model.registration.AccommodationLocation(name='foo', beds=1)
        self.ao = model.registration.AccommodationOption(name='', cost_per_night=1)
        self.ao.location = self.al
        objectstore.save(self.al)
        objectstore.save(self.ao)
        objectstore.flush()

        self.alid = self.al.id
        self.aoid = self.ao.id
        
    def tearDown(self):
        self.ao = Query(model.registration.AccommodationOption).get(self.aoid)
        self.al = Query(model.registration.AccommodationLocation).get(self.alid)
        objectstore.delete(self.ao)
        objectstore.delete(self.al)
        objectstore.flush()
        
        if Dummy_smtplib.existing:
            Dummy_smtplib.existing.reset()

        ps = Query(model.Person).select()
        for p in ps:
            objectstore.delete(p)
        objectstore.flush()
        super(TestRegistrationController, self).tearDown()

class TestSignedInRegistrationController(SignedInCRUDControllerTest):

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
            accommodation='0',
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

class TestNotSignedInRegistrationController(ControllerTest):
    def test_not_signed_in_existing_registration(self):
        p = model.Person(email_address='testguy@example.org',
            fullname='testguy mctest',
            )
        p.activated = True
        objectstore.save(p)
        objectstore.flush()

        pid = p.id

        resp = self.app.get('/registration/new')
        f = resp.form
        sample_data = dict(address1='a1',
            city='Sydney',
            state='NSW',
            country='Australia',
            postcode='2001',
            type='Professional',
            teesize='M_M',
            checkin=14,
            checkout=20,
            accommodation=0,
            )
        for k in sample_data.keys():
            f['registration.' + k] = sample_data[k]
        f['person.email_address'] = 'testguy@example.org'
        f['person.fullname'] = 'testguy mctest'
        f['person.handle']= 'testguy'
        f['person.password'] = 'test'
        f['person.password_confirm'] = 'test'

        resp = f.submit()

        resp.mustcontain('This account already exists.')

        # clean up
        objectstore.delete(Query(model.Person).get(pid))
        objectstore.flush()

    def test_not_signed_in_existing_handle(self):
        p = model.Person(email_address='testguy@example.org',
            fullname='testguy mctest',
            handle='testguy',
            )
        p.activated = True
        objectstore.save(p)
        objectstore.flush()

        pid = p.id

        resp = self.app.get('/registration/new')
        f = resp.form
        sample_data = dict(address1='a1',
            city='Sydney',
            state='NSW',
            country='Australia',
            postcode='2001',
            type='Professional',
            teesize='M_M',
            checkin=14,
            checkout=20,
            accommodation=0,
            )
        for k in sample_data.keys():
            f['registration.' + k] = sample_data[k]
        f['person.email_address'] = 'testguy2@example.org'
        f['person.fullname'] = 'testguy mctest'
        f['person.handle']= 'testguy'
        f['person.password'] = 'test'
        f['person.password_confirm'] = 'test'

        resp = f.submit()

        resp.mustcontain('This display name has been taken, sorry.  Please use another.')

        # clean up
        objectstore.delete(Query(model.Person).get(pid))
        objectstore.flush()
