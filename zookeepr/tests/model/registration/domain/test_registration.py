from zookeepr.tests.model import *

class TestRegistration(CRUDModelTest):
    domain = model.registration.Registration
    samples = [dict(address1='a1',
                    address2='a2',
                    city='city',
                    state='state1',
                    country='country1',
                    postcode='postcode1',
                    phone='+61 2 37',
                    company='company1',
                    shell='shell1',
                    shelltext='shelltext1',
                    editor='editor1',
                    editortext='editortext1',
                    distro='distro1',
                    distrotext='distrotext1',
                    type='type1',
                    voucher_code='voucher_code1',
                    teesize='teesize1',
		    extra_tee_count=1,
		    extra_tee_sizes='extra_tee_sizes1',
                    dinner=1,
                    diet='diet1',
                    special='special1',
                    opendaydrag=1,
                    partner_email='partneremail1',
                    kids_0_3=1,
                    kids_4_6=1,
                    kids_7_9=1,
                    checkin=1,
                    checkout=1,
                    lasignup=1,
                    announcesignup=1,
                    delegatesignup=1,
                    prevlca=[99],
                    miniconf=['Debian'],
                    )]

    def setUp(self):
        super(TestRegistration, self).setUp()
        self.person = model.Person(email_address='testguy@example.org')
        self.dbsession.save(self.person)
        self.dbsession.flush()
        self.pid = self.person.id

    def tearDown(self):
        self.dbsession.delete(self.dbsession.query(model.Person).get(self.pid))
        self.dbsession.flush()
        super(TestRegistration, self).tearDown()

    def additional(self, rego):
        rego.person = self.person
        return rego

    def test_person_mapping(self):
        # person.registration should point to a single registration object
        r = model.Registration(**self.samples[0])
        p = model.Person(email_address='testguy+map@example.org')

        r.person = p
        self.dbsession.save(r)
        self.dbsession.save(p)

        self.dbsession.flush()
        
        rid = r.id
        pid = p.id

        # clear it
        self.dbsession.clear()

        
        p = self.dbsession.query(model.Person).get(pid)
        r = self.dbsession.query(model.Registration).get(rid)

        # test that p is mapped to r properly
        self.assertEqual(r, p.registration)

        self.assertEqual(p, r.person)

        # clean up, assert that r is deleted when p is
        self.dbsession.delete(p)
        self.dbsession.flush()

        self.assertEqual(None, self.dbsession.query(model.Registration).get(rid))
