import hmac
import sha
import pytest

def fake_payment_params():
    return dict(
            invoice_id      = 1,
            payment_amount  = 69001,
            bank_reference  = 5261,
            payment_number  = 'SimProxy 54021550',
            card_mac        = 'fake',
            card_name       = 'joe',
            card_number     = '1234',
            card_type       = 'TestCard',
            card_expiry     = '1/1/1',
            currency        = 'USD',
            payment_id      = '23',
            receipt_address = 'here',
            remote_ip       = '127.0.0.1',
            response_amount = '55',
            response_code   = 'HELP',
            response_text   = 'Approved',
            summary_code    = 'a test entry',
            )


class TestPaymentController(object):
    """Test that when we pump data into the payment, it does the right thing.  """

    def gen_mac(self, fields):
        """Generate a HMAC for the fields"""
        keys = fields.keys()
        keys.sort()
        string_to_mac = '&'.join(['%s=%s' % (key, fields[key]) for key in keys if key != 'MAC'])
        mac = hmac.new('foo', string_to_mac, sha).hexdigest()
        fields['MAC'] = mac
        return fields

    @pytest.mark.xfail # Reported as #415
    def test_no_payment(self, app, smtplib):
        """ a random hit on the page """

        resp = app.get('/payment/new', params=fake_payment_params(), extra_environ=dict(REMOTE_ADDR='0.0.0.0'))

        print resp
        assert "Invalid HMAC" in smtplib.existing.message

        assert resp.header('location') == '/Errors/InvalidPayment'


    @pytest.mark.xfail # Reported as #415
    def test_valid_hmac_no_payment(self, app, smtplib):
        """ form has a valid HMAC but nonexistent payment """

        resp = app.get('/payment/new', params=self.gen_mac(fake_payment_params()), extra_environ=dict(REMOTE_ADDR='0.0.0.0'))

        print resp

        print smtplib.existing.message

        assert "Nonexistent Payment" in smtplib.existing.message
        assert resp.header('location') == "/Errors/MissingPayment"


