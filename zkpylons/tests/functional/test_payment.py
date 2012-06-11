import hmac
import sha

from paste.fixture import Dummy_smtplib

from zkpylons.tests.functional import *

class TestPaymentController(ControllerTest):
    """Test that when we pump data into the payment, it does the right thing.
    """

    def setUp(self):
        super(TestPaymentController, self).setUp()
        Dummy_smtplib.install()
        print Dummy_smtplib.existing

        self.params = dict(invoice_id=1,
                           payment_amount=69001,
                           bank_reference=5261,
                           payment_number='SimProxy 54021550')

    def tearDown(self):
        if Dummy_smtplib.existing:
            Dummy_smtplib.existing.reset()

        self.dbsession.delete(self.dbsession.query(model.PaymentReceived).select()[0])
        self.dbsession.flush()

        super(TestPaymentController, self).tearDown()

#    def test_no_payment(self):
        # a random hit on the page

        # FIXME fi this test once code gets fixed
        #resp = self.app.get('/payment/new', params=self.params)

        #print resp
        #self.failUnless("Invalid HMAC" in  Dummy_smtplib.existing.message)

        #self.assertEqual('/Errors/InvalidPayment', resp.header('location'))

    def gen_mac(self, fields):
        """Generate a HMAC for the fields"""
        keys = fields.keys()
        keys.sort()
        string_to_mac = '&'.join(['%s=%s' % (key, fields[key]) for key in keys if key != 'MAC'])
        mac = hmac.new('foo', string_to_mac, sha).hexdigest()
        fields['MAC'] = mac
        return fields

    #def test_valid_hmac_no_payment(self):
        # form has a valid HMAC but nonexistent payment

        #resp = self.app.get('/payment/new', params=self.gen_mac(self.params))

        #print resp

        #print Dummy_smtplib.existing.message

        #self.failUnless("Nonexistent Payment" in Dummy_smtplib.existing.message)
        #self.assertEqual("/Errors/MissingPayment", resp.header('location'))


#     def test_valid_payment_wrong_invoice(self):
#         invoice = model.Invoice()
#         self.dbsession.save(invoice)
#         ii = model.InvoiceItem('foo', 1, 100)
#         self.dbsession.save(ii)
        
#         invoice.items.append(ii)

#         # do stuff
        
#         self.fail("not really")
        
        
        
