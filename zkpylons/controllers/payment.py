import logging
import datetime

from pylons import request, response, session, tmpl_context as c
from zkpylons.lib.helpers import redirect_to
from pylons.controllers.util import abort
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill
from formencode.variabledecode import NestedVariables

from zkpylons.lib.base import BaseController, render
from zkpylons.lib.validators import BaseSchema, ExistingPaymentValidator
import zkpylons.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zkpylons.lib.mail import email

from zkpylons.model import meta, Payment, PaymentReceived, Invoice

from zkpylons.config.lca_info import lca_info

import zkpylons.lib.pxpay as pxpay

log = logging.getLogger(__name__)

class PaymentSchema(BaseSchema):
    approved = validators.Int(min=0, max=1, not_empty=True)
    amount_paid = validators.Int(max=2000000)
    currency_used = validators.String()
    gateway_ref = validators.String()
    email_address = validators.String(not_empty=False)
    success_code = validators.String()

class NewPaymentSchema(BaseSchema):
    payment = PaymentSchema()

class SecurePayPingSchema(BaseSchema):
    payment_id = validators.Int(not_empty=True)
    invoice_id = validators.Int(not_empty=True)
    summary_code = validators.String(not_empty=True)
    response_amount = validators.Int(not_empty=True)
    currency = validators.String(not_empty=True)
    card_name = validators.String(not_empty=False)
    card_type = validators.String(not_empty=False)
    card_number = validators.String(not_empty=False)
    card_expiry = validators.String(not_empty=False)
    card_mac = validators.String(not_empty=False)
    response_code = validators.String(not_empty=True)
    bank_reference = validators.String(not_empty=True)
    response_text = validators.String(not_empty=True)
    remote_ip = validators.String(not_empty=True)
    receipt_address = validators.String(not_empty=True)

class PaymentController(BaseController):
    """This controller receives payment advice from the payment gateway.

    the url /payment/new receives the advice
    """

    @authorize(h.auth.has_organiser_role)
    def index(self):
        c.payment_collection = Payment.find_all()
        return render('/payment/list.mako')

    @authorize(h.auth.is_valid_user)
    def view(self, id):

        payment = Payment.find_by_id(id, abort_404=True)
        c.person = payment.invoice.person

        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zkpylons_user(c.person.id), h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()

        c.is_organiser = False
        if h.auth.authorized(h.auth.has_organiser_role):
            c.is_organiser = True

        c.payment = PaymentReceived.find_by_payment(payment.id)

        c.validation_errors = []
        if c.payment is not None and c.payment.validation_errors is not None and len(c.payment.validation_errors) > 0:
            c.validation_errors = c.payment.validation_errors.split(';')

        same_invoice = PaymentReceived.find_by_invoice(payment.invoice.id)
        same_email   = PaymentReceived.find_by_email(c.person.email_address)
        if c.payment is not None:
            same_invoice = same_invoice.filter("payment_id <> " + str(payment.id))
            same_email = same_email.filter("payment_id <> " + str(payment.id))
        c.related_payments = same_invoice.union(same_email)

        return render('/payment/view.mako')

    # No authentication because it's called directly by the payment gateway
    def new(self):
        schema = SecurePayPingSchema()
        try:
            form_result = schema.to_python(request.params)
        except validators.Invalid, error:
            return 'Invalid: %s' % error

        payment = None
        c.person = None

        fields = form_result
        c.response = {
            'payment_id': fields['payment_id'],
            'invoice_id': fields['invoice_id'],
            'success_code': fields['summary_code'],
            'amount_paid': fields['response_amount'],
            'currency_used': fields['currency'],
            'card_name': fields['card_name'],
            'card_type': fields['card_type'],
            'card_number': fields['card_number'],
            'card_expiry': fields['card_number'],
            'card_mac': fields['card_mac'],
            'auth_code': fields['response_code'],
            'gateway_ref': fields['bank_reference'],
            'response_text': fields['response_text'],
            'client_ip_gateway': fields['remote_ip'],
            'client_ip_zookeepr': request.environ.get('REMOTE_ADDR'),
            'email_address': fields['receipt_address']
       }

        if 'Approved' in c.response['response_text']:
            c.response['approved'] = True
        else:
            c.response['approved'] = False

        validation_errors = []

        if c.response is None:
            abort(500, ''.join(validation_errors))
        else:
            # Make sure the same browser created the zkpylons payment object and paid by credit card
            #if c.response['client_ip_gateway'] != c.response['client_ip_zookeepr']:
                #validation_errors.append('Mismatch in IP addresses: zkpylons=' + c.response['client_ip_zookeepr'] + ' gateway=' + c.response['client_ip_gateway'])

            # Get the payment object associated with this transaction
            payment = Payment.find_by_id(c.response['payment_id'])

        if payment is None:
            validation_errors.append('Invalid payment ID from the payment gateway')
        else:
            c.person = payment.invoice.person

            # Check whether a payment has already been received for this payment object
            received = PaymentReceived.find_by_payment(payment.id)
            if received is not None:
                # Ignore repeat payment
                return redirect_to(action='view', id=payment.id)

            # Extra validation
            if c.response['amount_paid'] != payment.amount:
                validation_errors.append('Mismatch between amounts paid and invoiced')
            if c.response['invoice_id'] != payment.invoice.id:
                validation_errors.append('Mismatch between returned invoice ID and payment object')
            #if c.response['email_address'] != pxpay.munge_email(payment.invoice.person.email_address):
            #    validation_errors.append('Mismatch between returned email address and invoice object')
            if not c.person.is_from_common_country():
                if c.person.country:
                    validation_errors.append('Uncommon country: ' + c.person.country)
                else:
                    validation_errors.append('Unknown country')

        c.pr = PaymentReceived(**c.response)
        c.pr.validation_errors = ';'.join(validation_errors)
        meta.Session.add(c.pr)
        meta.Session.commit()

        if len(validation_errors) > 0 and c.response['approved']:
            # Suspiciously approved transaction which needs to be checked manually
            email(lca_info['contact_email'], render('/payment/suspicious_payment.mako'))

        if c.person is not None:
            email(c.person.email_address, render('/payment/response.mako'))

        # OK we now have a valid transaction, we redirect the user to the view page
        # so they can see if their transaction was accepted or declined
        return redirect_to(action='view', id=payment.id)

    @authorize(h.auth.has_organiser_role)
    @dispatch_on(POST="_new_manual")
    def new_manual(self, id):
        c.payment = Payment.find_by_id(id)
        payment = None
        c.person = c.payment.invoice.person


        defaults = {
            'payment.approved': 1,
            'payment.email_address': c.person.email_address,
            'payment.success_code': 'Received',
            'payment.amount_paid': c.payment.amount,
            'payment.currency_used': 'AUD',
        }

        form = render('/payment/new.mako')
        return htmlfill.render(form, defaults)

    @authorize(h.auth.has_organiser_role)
    @validate(schema=NewPaymentSchema(), form='new_manual', post_only=True, on_get=True, variable_decode=True)
    def _new_manual(self, id):
        """Create a new payment."""
        results = self.form_result['payment']

        # Check whether a payment has already been received for this payment object
        payment = Payment.find_by_id(id)
        received = PaymentReceived.find_by_payment(payment.id)
        if received is not None:
            print "WTF"
            # Ignore repeat payment
            return redirect_to(action='view', id=payment.id)

        client_ip = request.environ['REMOTE_ADDR']
        if 'HTTP_X_FORWARDED_FOR' in request.environ:
            client_ip = request.environ['HTTP_X_FORWARDED_FOR']

        results['response_text'] = 'Manual payment processed by ' + h.signed_in_person().fullname()
        results['client_ip_zookeepr'] = client_ip
        results['client_ip_gateway'] = client_ip
        results['payment'] = payment

        c.payment_received = PaymentReceived(**results)
        c.payment_received.email_address.lower()

        if results['approved'] == 1:
            setattr(c.payment_received, 'approved', True)
        else:
            setattr(c.payment_received, 'approved', False)

        setattr(c.payment_received, 'validation_errors', '')
        setattr(c.payment_received, 'invoice', payment.invoice)


        meta.Session.add(c.payment_received)
        meta.Session.commit()

        return redirect_to(action='view', id=payment.id)

