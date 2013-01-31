import datetime
import logging

from pylons import request, response, session, tmpl_context as c
from zkpylons.lib.helpers import redirect_to

from pylons.controllers.util import Response, redirect

from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill, ForEach, Invalid
from formencode.variabledecode import NestedVariables

from zkpylons.lib.base import BaseController, render
from zkpylons.lib.ssl_requirement import enforce_ssl
from zkpylons.lib.validators import BaseSchema, ProductValidator, ExistingPersonValidator, ExistingInvoiceValidator
import zkpylons.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zkpylons.lib.mail import email

from zkpylons.model import meta, Invoice, InvoiceItem, Registration, ProductCategory, Product, URLHash
from zkpylons.model.payment import Payment
from zkpylons.model.payment_received import PaymentReceived

from zkpylons.config.lca_info import lca_info
from zkpylons.config.zkpylons_config import file_paths

import zkpylons.lib.pdfgen as pdfgen
import zkpylons.lib.pxpay as pxpay

log = logging.getLogger(__name__)

class RemindSchema(BaseSchema):
#    message = validators.String(not_empty=True)
    invoices = ForEach(ExistingInvoiceValidator())

class ExistingInvoiceValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        invoice = Invoice.find_by_id(int(value), False)
        if invoice is None:
            raise Invalid("Unknown invoice ID.", value, state)
        else:
            return invoice
    def _from_python(self, value, state):
        return value.id

class InvoiceItemProductDescriptionValidator(validators.FancyValidator):
    def validate_python(self, values, state):
        if (values['product'] is None and values['description'] == "") or (values['product'] is not None and values['description'] != ""):
            message = "You must select a product OR enter a description, not both"
            error_dict = {'description': 'Description must not be blank'}
            raise Invalid(message, values, state, error_dict=error_dict)

class InvoiceItemValidator(BaseSchema):
    product = ProductValidator()
    qty = validators.Int() 
    cost = validators.Int(min=-2000000, max=2000000)
    description = validators.String(not_empty=False)
    chained_validators = [InvoiceItemProductDescriptionValidator()]

class InvoiceSchema(BaseSchema):
    person = ExistingPersonValidator(not_empty=True)
    due_date = validators.DateConverter(month_style='dd/mm/yyyy')
    items = ForEach(InvoiceItemValidator())

    item_count = validators.Int(min=0) # no max, doesn't hit database

class NewInvoiceSchema(BaseSchema):
    invoice = InvoiceSchema()
    pre_validators = [NestedVariables]

class PayInvoiceSchema(BaseSchema):
    payment_id = validators.Int(min=1)

class FakePerson():
    firstname = "John"
    lastname = "Doe"
    email_address = "john.doe@example.com"

class InvoiceController(BaseController):
    @enforce_ssl(required_all=True)
    @authorize(h.auth.Or(h.auth.is_valid_user, h.auth.has_unique_key()))
    def __before__(self, **kwargs):
        pass

    @authorize(h.auth.has_organiser_role)
    def new(self):
        c.product_categories = ProductCategory.find_all()
        return render("/invoice/new.mako")

    def save_new_invoice(self):
        """
        """
        import json
        debug = ""
        data = request.params['invoice']
        data = json.loads(data)

        person_id = int(data['person_id'],10)
        due_date = datetime.datetime.strptime(data['due_date'], '%d/%m/%Y')

        invoice = Invoice(person_id=person_id, due_date=due_date, manual=True, void=None)
        for invoice_item in data['invoice_items']:
            item = InvoiceItem()

            if invoice_item.has_key('description') and invoice_item['description']:
                item.description = invoice_item['description']
            else:
                product = Product.find_by_id(invoice_item['product_id'])
                category = product.category
                item.product = product
                item.description = product.category.name + ' - ' + product.description

            item.cost = float(invoice_item['cost'])
            item.qty = int(invoice_item['qty'],10)
            invoice.items.append(item)

        meta.Session.add(invoice)
        meta.Session.commit()

        debug += str(invoice.id)
        return debug

    @validate(schema=NewInvoiceSchema(), form='new', post_only=True, on_get=True, variable_decode=True)
    def _new(self):
        results = self.form_result['invoice']
        del(results['item_count'])

        items = results['items']
        results['items'] = []
        c.invoice = Invoice(**results)

        for i in items:
            item = InvoiceItem()
            if i['description'] != "":
                item.description = i['description']
            else:
                product = Product.find_by_id(i['product'].id)
                category = product.category
                item.product = i['product']
                item.description = product.category.name + ' - ' + product.description
            item.cost = i['cost']
            item.qty = i['qty']
            c.invoice.items.append(item)

        c.invoice.manual = True
        c.invoice.void = None
        meta.Session.add(c.invoice)
        meta.Session.commit()

        h.flash("Manual invoice created")
        return redirect_to(action='view', id=c.invoice.id)

    def generate_hash(self, id):
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zkpylons_attendee(id), h.auth.has_organiser_role, h.auth.has_unique_key())):
            # Raise a no_auth error
            h.auth.no_role()

        url = h.url_for(action='view', id=id)
        c.hash = URLHash.find_by_url(url=url)
        if c.hash is None:
            c.hash = URLHash()
            c.hash.url = url
            meta.Session.add(c.hash)
            meta.Session.commit()

            # create an entry for the payment page (not needed)
            # TODO: depending on how the gateway works, you may need to make sure you have permissions for the page you get redirected to
            #c.hash = URLHash()
            #c.hash.url = h.url_for(action='pay')
            #meta.Session.add(c.hash)
            #meta.Session.commit()

        return render('/invoice/generate_url.mako')


    def view(self, id):
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zkpylons_attendee(id), h.auth.has_organiser_role, h.auth.has_unique_key())):
            # Raise a no_auth error
            h.auth.no_role()

        c.printable = False
        c.invoice = Invoice.find_by_id(id, True)
        c.payment_received = None
        c.payment = None
        if c.invoice.is_paid and c.invoice.total > 0:
            c.payment_received = c.invoice.good_payments[0]
            c.payment = c.payment_received.payment
        return render('/invoice/view.mako')

    def printable(self, id):
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zkpylons_attendee(id), h.auth.has_organiser_role, h.auth.has_unique_key())):
            # Raise a no_auth error
            h.auth.no_role()

        c.printable = True
        c.invoice = Invoice.find_by_id(id, True)
        c.payment_received = None
        c.payment = None
        if c.invoice.is_paid and c.invoice.total > 0:
            c.payment_received = c.invoice.good_payments[0]
            c.payment = c.payment_received.payment
        return render('/invoice/view_printable.mako')

    @authorize(h.auth.has_organiser_role)
    def index(self):
        c.can_edit = True
        c.invoice_collection = Invoice.find_all()

        return render('/invoice/list.mako')

    @authorize(h.auth.has_organiser_role)
    @dispatch_on(POST="_remind")
    def remind(self):
        c.invoice_collection = meta.Session.query(Invoice).filter(Invoice.is_paid==False).filter(Invoice.is_void==False).all()
        # create dummy person for example:
        c.recipient = FakePerson()
        return render('/invoice/remind.mako')

    @validate(schema=RemindSchema(), form='remind', post_only=True, on_get=True, variable_decode=True)
    def _remind(self):
        results = self.form_result
        for i in results['invoices']:
            c.invoice = i
            c.recipient = i.person
            email(c.recipient.email_address, render('invoice/remind_email.mako'))
            h.flash('Email sent to ' + c.recipient.firstname + ' ' + c.recipient.lastname + ' <' + c.recipient.email_address + '>')
        redirect_to(action='remind')

    def _check_invoice(self, person, invoice, ignore_overdue = False):
        c.invoice = invoice
        if person.invoices:
            if invoice.is_paid or len(invoice.bad_payments) > 0:
                c.status = []
                if invoice.total==0:
                  c.status.append('zero balance')
                if len(invoice.good_payments) > 0:
                  c.status.append('paid')
                  if len(invoice.good_payments)>1:
                    c.status[-1] += ' (%d times)' % len(invoice.good_payments)
                if len(invoice.bad_payments) > 0:
                  c.status.append('tried to pay')
                  if len(invoice.bad_payments)>1:
                    c.status[-1] += ' (%d times)' % len(invoice.bad_payments)
                c.status = ' and '.join(c.status)
                return render('/invoice/already.mako')

        if invoice.is_void:
            c.signed_in_person = h.signed_in_person()
            return render('/invoice/invalid.mako')
        if not ignore_overdue and invoice.is_overdue:
            for ii in invoice.items:
                if ii.product and not ii.product.available():
                    return render('/invoice/expired.mako')

        return None # All fine

    @dispatch_on(POST="_pay")
    def pay(self, id):
        """Request confirmation from user
        """
        invoice = Invoice.find_by_id(id, True)
        person = invoice.person

        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zkpylons_user(person.id), h.auth.has_organiser_role, h.auth.has_unique_key())):
            # Raise a no_auth error
            h.auth.no_role()

        #return render('/registration/really_closed.mako')

        error = self._check_invoice(person, invoice)
        if error is not None:
            return error

        c.payment = Payment()
        c.payment.amount = invoice.total
        c.payment.invoice = invoice

        meta.Session.commit()
        return render("/invoice/payment.mako")

    def pay_invoice(self):
        """
        Pay an invoice via the new angular.js interface

        Expects: and invoice_id. Assumes total amount is to be paid.

        TODO: Validation??
        """
        invoice_id = int(request.params['invoice'],10)
        invoice = Invoice.find_by_id(invoice_id, True)
        person = invoice.person

        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zkpylons_user(person.id), h.auth.has_organiser_role, h.auth.has_unique_key())):
            # Raise a no_auth error
            h.auth.no_role()

        error = self._check_invoice(person, invoice)
        if error is not None:
            raise Exception(error)

        payment = Payment()
        payment.amount = invoice.total
        payment.invoice = invoice

        payment_received = PaymentReceived(
                                    approved=True,
                                    payment=payment,
                                    invoice_id=invoice.id,
                                    success_code='0',
                                    amount_paid=payment.amount,
                                    currency_used='AUD',
                                    response_text='Approved',
                                    client_ip_zookeepr='127.1.0.1',
                                    client_ip_gateway='127.0.0.1',
                                    email_address=person.email_address,
                                    gateway_ref='Rego Desk Cash'
                    )

        meta.Session.add(payment)
        meta.Session.add(payment_received)
        meta.Session.commit()

        return "Payment recorded"

    @validate(schema=PayInvoiceSchema(), form='pay', post_only=True, on_get=True, variable_decode=True)
    def _pay(self, id):
        payment = Payment.find_by_id(self.form_result['payment_id'])
        c.invoice = payment.invoice
        person = c.invoice.person

        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zkpylons_user(person.id), h.auth.has_organiser_role, h.auth.has_unique_key())):
            # Raise a no_auth error
            h.auth.no_role()

        error = self._check_invoice(person, c.invoice)
        if error is not None:
            return error

        client_ip = request.environ['REMOTE_ADDR']
        if 'HTTP_X_FORWARDED_FOR' in request.environ:
            client_ip = request.environ['HTTP_X_FORWARDED_FOR']

        # Prepare fields for PxPay
        params = {
            'payment_id': payment.id,
            'amount': h.integer_to_currency(payment.amount),
            'invoice_id': payment.invoice.id,
            'email_address': payment.invoice.person.email_address,
            'client_ip' : client_ip,
            'return_url' : 'https://conf.linux.org.au/payment/new',
        }

        (valid, uri) = pxpay.generate_request(params)
        if valid != '1':
            c.error_msg = "PxPay Generate Request error: " + uri
            return render("/payment/gateway_error.mako")
        else:
            redirect(uri)

    @authorize(h.auth.has_organiser_role)
    @dispatch_on(POST="_new")
    def refund(self, id):
        invoice = Invoice.find_by_id(id)
        try:
            c.invoice_person = invoice.person.id
        except:
            c.invoice_person = ''

        c.due_date = datetime.date.today().strftime("%d/%m/%Y")

        c.product_categories = ProductCategory.find_all()
        # The form adds one to the count by default, so we need to decrement it
        c.item_count = len(invoice.items) - 1

        defaults = dict()
        defaults['invoice.person' ] = c.invoice_person
        defaults['invoice.due_date'] = c.due_date
        for i in range(len(invoice.items)):
            item = invoice.items[i]
            if item.product:
                defaults['invoice.items-' + str(i) + '.product'] = item.product.id
            else:
                defaults['invoice.items-' + str(i) + '.description'] = item.description
            defaults['invoice.items-' + str(i) + '.qty'] = -item.qty
            defaults['invoice.items-' + str(i) + '.cost'] = item.cost
        form = render("/invoice/new.mako")
        return htmlfill.render(form, defaults, use_all_keys=True)

    @authorize(h.auth.has_organiser_role)
    @dispatch_on(POST="_pay_manual")
    def pay_manual(self, id):
        """Request confirmation from user
        """
        invoice = Invoice.find_by_id(id, True)
        person = invoice.person

        error = self._check_invoice(person, invoice, ignore_overdue=True)
        if error is not None:
            return error

        c.payment = Payment()
        c.payment.amount = invoice.total
        c.payment.invoice = invoice

        meta.Session.commit()
        return redirect_to(controller='payment', id=c.payment.id, action='new_manual')


    def pdf(self, id):
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zkpylons_attendee(id), h.auth.has_organiser_role, h.auth.has_unique_key())):
            # Raise a no_auth error
            h.auth.no_role()

        c.invoice = Invoice.find_by_id(id, True)
        xml_s = render('/invoice/pdf.mako')

        xsl_f = file_paths['zk_root'] + '/zkpylons/templates/invoice/pdf.xsl'
        pdf_data = pdfgen.generate_pdf(xml_s, xsl_f)

        filename = lca_info['event_shortname'] + '_' + str(c.invoice.id) + '.pdf'
        return pdfgen.wrap_pdf_response(pdf_data, filename)


    def void(self, id):
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zkpylons_attendee(id), h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()

        c.invoice = Invoice.find_by_id(id, True)
        if c.invoice.is_void:
            h.flash("Invoice was already voided.")
            return redirect_to(action='view', id=c.invoice.id)
        elif len(c.invoice.payment_received) and h.auth.authorized(h.auth.has_organiser_role):
            h.flash("Invoice has a payment applied to it, do you want to " + h.link_to('Refund', h.url_for(action='refund')) + " instead?")
            return redirect_to(action='view', id=c.invoice.id)
        elif len(c.invoice.payment_received):
            h.flash("Cannot void a paid invoice.")
            return redirect_to(action='view', id=c.invoice.id)
        elif h.auth.authorized(h.auth.has_organiser_role):
            c.invoice.void = "Administration Change"
            meta.Session.commit()
            h.flash("Invoice was voided.")
            return redirect_to(action='view', id=c.invoice.id)
        else:
            c.invoice.void = "User cancellation"
            c.person = c.invoice.person
            meta.Session.commit()
            email(lca_info['contact_email'], render('/invoice/user_voided.mako'))
            h.flash("Previous invoice was voided.")
            return redirect_to(controller='registration', action='pay', id=c.person.registration.id)

    @authorize(h.auth.has_organiser_role)
    def unvoid(self, id):
        c.invoice = Invoice.find_by_id(id, True)
        c.invoice.void = None
        c.invoice.manual = True
        meta.Session.commit()
        h.flash("Invoice was un-voided.")
        return redirect_to(action='view', id=c.invoice.id)

    @authorize(h.auth.has_organiser_role)
    def extend(self, id):
        c.invoice = Invoice.find_by_id(id, True)
        if c.invoice.is_overdue:
            c.invoice.due_date = datetime.datetime.now() + datetime.timedelta(days=1)
        else:
            c.invoice.due_date = c.invoice.due_date + ((c.invoice.due_date - datetime.datetime.now()) * 2)
        meta.Session.commit()
        return redirect_to(action='view')
