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
        self.dbsession.save(self.al)
        self.dbsession.save(self.ao)
        self.dbsession.flush()

        self.alid = self.al.id
        self.aoid = self.ao.id
        
    def tearDown(self):
        self.dbsession.clear()

        self.dbsession.delete(self.dbsession.query(model.Person).get_by(email_address='testguy@example.org'))

        self.ao = self.dbsession.query(model.registration.AccommodationOption).get(self.aoid)
        self.al = self.dbsession.query(model.registration.AccommodationLocation).get(self.alid)
        self.dbsession.delete(self.ao)
        self.dbsession.delete(self.al)
        self.dbsession.flush()
        
        if Dummy_smtplib.existing:
            Dummy_smtplib.existing.reset()

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
        regs = self.dbsession.query(model.Registration).select()
        self.failIfEqual([], regs)
        self.assertEqual(self.person.id, regs[0].person.id)

        # clean up
        self.dbsession.delete(regs[0])
        self.dbsession.flush()

    def test_edit_registration(self):
        # testing that we can generate an invoice from a registration
        al = model.registration.AccommodationLocation(name='FooPlex', beds=100)
        ao = model.registration.AccommodationOption(name='snuh', cost_per_night=37.00)
        ao.location = al
        self.dbsession.save(al)
        self.dbsession.save(ao)
        self.dbsession.flush()
        alid = al.id
        aoid = ao.id

        accom = self.dbsession.query(model.Accommodation).get(ao.id)
        rego = model.Registration(type='Professional',
                                  checkin=14,
                                  checkout=20,
                                  dinner=1,
                                  partner_email='foo',
                                  kids_0_3=9,
                                  lasignup=True,
                                  miniconf=['Debian', 'OpenOffice.org'],
                                  prevlca=['06', '99'],
                                  )
        self.dbsession.save(rego)
        rego.person = self.person
        rego.accommodation = accom

        self.dbsession.flush()
        rid = rego.id
        self.dbsession.clear()

        resp = self.app.get('/registration/1/edit')

        #print resp.form.fields

        print "*** dumping field contents"
        for k, v in resp.form.fields.items():
            print "%s: %r" % (k, v[0].value)

        print "registration.lasignup:", resp.form.fields['registration.lasignup'][0].value
        self.assertEqual('1', resp.form.fields['registration.lasignup'][0].value)
        self.assertEqual('14', resp.form.fields['registration.checkin'][0].value)
        self.assertEqual('1', resp.form.fields['registration.dinner'][0].value)
        self.assertEqual('1', resp.form.fields['registration.miniconf.Debian'][0].value)
        self.assertEqual('1', resp.form.fields['registration.miniconf.OpenOffice.org'][0].value)
        self.assertEqual('1', resp.form.fields['registration.prevlca.06'][0].value)
        self.assertEqual('1', resp.form.fields['registration.prevlca.99'][0].value)

        # clean up
        self.dbsession.delete(self.dbsession.query(model.Registration).get(rid))
        self.dbsession.delete(self.dbsession.query(model.registration.AccommodationOption).get(aoid))
        self.dbsession.delete(self.dbsession.query(model.registration.AccommodationLocation).get(alid))
        self.dbsession.flush()
        

class TestNotSignedInRegistrationController(ControllerTest):
    def test_not_signed_in_existing_registration(self):
        p = model.Person(email_address='testguy@example.org',
            fullname='testguy mctest',
            )
        p.activated = True
        self.dbsession.save(p)
        self.dbsession.flush()

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
        self.dbsession.delete(self.dbsession.query(model.Person).get(pid))
        self.dbsession.flush()

    def test_not_signed_in_existing_handle(self):
        p = model.Person(email_address='testguy@example.org',
            fullname='testguy mctest',
            handle='testguy',
            )
        p.activated = True
        self.dbsession.save(p)
        self.dbsession.flush()

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
        self.dbsession.delete(self.dbsession.query(model.Person).get(pid))
        self.dbsession.flush()
