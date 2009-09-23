import logging
import datetime

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import redirect_to, abort
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill
from formencode.variabledecode import NestedVariables

from zookeepr.lib.base import BaseController, render
from zookeepr.lib.validators import BaseSchema
import zookeepr.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zookeepr.lib.mail import email

from zookeepr.model import meta, Payment, PaymentReceived

from zookeepr.config.lca_info import lca_info

import zookeepr.lib.pxpay as pxpay

log = logging.getLogger(__name__)

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

        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_user(c.person.id), h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()

        c.is_organiser = False
        if h.auth.authorized(h.auth.has_organiser_role):
            c.is_organiser = True

        c.payment = PaymentReceived.find_by_payment(payment.id)

        c.validation_errors = []
        if c.payment is not None and len(c.payment.validation_errors) > 0:
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
        payment = None
        c.person = None

        fields = dict(request.GET)
        c.response, validation_errors = pxpay.process_response(fields)

        if c.response is None:
            abort(500, ''.join(validation_errors))
        else:
            # Make sure the same browser created the zookeepr payment object and paid by credit card
            #if c.response['client_ip_gateway'] != c.response['client_ip_zookeepr']:
                #validation_errors.append('Mismatch in IP addresses: zookeepr=' + c.response['client_ip_zookeepr'] + ' gateway=' + c.response['client_ip_gateway'])

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
            if c.response['email_address'] != pxpay.munge_email(payment.invoice.person.email_address):
                validation_errors.append('Mismatch between returned email address and invoice object')
            if not c.person.is_from_common_country():
                validation_errors.append('Uncommon country: ' + c.person.country)

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
