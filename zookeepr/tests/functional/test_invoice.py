import datetime

from zookeepr.tests.functional import *

class TestInvoiceController(SignedInCRUDControllerTest):
    def setUp(self):
        super(TestInvoiceController, self).setUp()
                                                 
        self.invoice = model.Invoice(issue_date=datetime.datetime(2006,11,21))
        self.dbsession.save(self.invoice)
        self.person.invoices.append(self.invoice)

        ii1 = model.InvoiceItem(description='line 1', qty=2, cost=100)
        self.invoice.items.append(ii1)
        self.dbsession.save(ii1)
        
        ii2 = model.InvoiceItem(description="awesomeness", qty=1, cost=250)
        self.invoice.items.append(ii2)
        self.dbsession.save(ii2)
        
        self.dbsession.flush()
        self.iid = self.invoice.id

    def tearDown(self):
        invoice = self.dbsession.query(model.Invoice).get(self.iid)
        self.dbsession.delete(invoice)
        self.dbsession.flush()

        super(TestInvoiceController, self).tearDown()

    def test_invoice_view(self):
        resp = self.app.get('/invoice/%d' % self.iid)
        print resp

        resp.mustcontain("Linux Australia")
        resp.mustcontain("ABN")
        resp.mustcontain("line 1")
        resp.mustcontain("$2.00")
        resp.mustcontain("$4.50")


    def test_registration_invoice_gen(self):
        # testing that we can generate an invoice from a registration
        al = model.registration.AccommodationLocation(name='FooPlex', beds=100)
        ao = model.registration.AccommodationOption(name='snuh', cost_per_night=37.00)
        ao.location = al
        self.dbsession.save(al)
        self.dbsession.save(ao)
        self.dbsession.flush()

        accom = self.dbsession.query(model.Accommodation).get(ao.id)
        rego = model.Registration(type='Professional',
                                  checkin=14,
                                  checkout=20,
                                  dinner=1,
                                  partner_email='foo',
                                  kids_0_3=9,
                                  )
        self.dbsession.save(rego)
        rego.person = self.person
        rego.accommodation = accom

        self.dbsession.flush()
        self.dbsession.clear()

        resp = self.app.get('/profile/%d' % self.person.id)

        resp = resp.click('(confirm invoice and pay)', index=1)

        # get a redirect from confirm once invoice is built
        resp = resp.follow()

        print resp

        inv = self.dbsession.query(model.Invoice).get_by(person_id=self.person.id)


        print "items:", inv.items
        
        for d in ('Professional Registration', 'Accommodation - FooPlex (snuh)', 'Additional Penguin Dinner Tickets', "Partner's Programme"):
            self.failUnless(d in [ii.description for ii in inv.items],
                            "Can't find %r in items" % d)
        


        self.fail("not really")
        # clean up
        
        
