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
                    discount_code='discount_code1',
                    teesize='teesize1',
                    dinner=1,
                    diet='diet1',
                    special='special1',
                    opendaydrag=1,
                    partner_email='partneremail1',
                    kids_0_3=1,
                    kids_4_6=1,
                    kids_7_9=1,
                    kids_10=1,
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
        objectstore.save(self.person)
        objectstore.flush()
        self.pid = self.person.id

    def tearDown(self):
        objectstore.delete(Query(model.Person).get(self.pid))
        objectstore.flush()
        super(TestRegistration, self).tearDown()

    def additional(self, rego):
        rego.person = self.person
        return rego

    def test_person_mapping(self):
        # person.registration should point to a single registration object
        r = model.Registration(**self.samples[0])
        p = model.Person(email_address='testguy+map@example.org')

        r.person = p
        objectstore.save(r)
        objectstore.save(p)

        objectstore.flush()
        
        rid = r.id
        pid = p.id

        # clear it
        objectstore.clear()

        
        p = Query(model.Person).get(pid)
        r = Query(model.Registration).get(rid)

        # test that p is mapped to r properly
        self.assertEqual(r, p.registration)

        self.assertEqual(p, r.person)

        # clean up, assert that r is deleted when p is
        objectstore.delete(p)
        objectstore.flush()

        self.assertEqual(None, Query(model.Registration).get(rid))
