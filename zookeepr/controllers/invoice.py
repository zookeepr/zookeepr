import datetime
import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import redirect_to, Response, redirect
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill, ForEach, Invalid
from formencode.variabledecode import NestedVariables

from zookeepr.lib.base import BaseController, render
from zookeepr.lib.ssl_requirement import enforce_ssl
from zookeepr.lib.validators import BaseSchema, ProductValidator, ExistingPersonValidator, ExistingInvoiceValidator
import zookeepr.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zookeepr.lib.mail import email

from zookeepr.model import meta, Invoice, InvoiceItem, Registration, ProductCategory, Product, URLHash
from zookeepr.model.payment import Payment

from zookeepr.config.lca_info import lca_info
from zookeepr.config.zookeepr_config import file_paths

import zookeepr.lib.pxpay as pxpay

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
    cost = validators.Int(min=0, max=2000000)
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
    @dispatch_on(POST="_new")
    def new(self):
        try:
            c.invoice_person = request.GET['person_id']
        except:
            c.invoice_person = ''

        c.due_date = datetime.date.today().strftime("%d/%y/%Y")

        c.product_categories = ProductCategory.find_all()
        c.item_count = 0;
        return render("/invoice/new.mako")

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
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_attendee(id), h.auth.has_organiser_role, h.auth.has_unique_key())):
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
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_attendee(id), h.auth.has_organiser_role, h.auth.has_unique_key())):
            # Raise a no_auth error
            h.auth.no_role()

        c.printable = False
        c.invoice = Invoice.find_by_id(id, True)
        c.payment_received = None
        c.payment = None
        if c.invoice.paid() and c.invoice.total() > 0:
            c.payment_received = c.invoice.good_payments()[0]
            c.payment = c.payment_received.payment
        return render('/invoice/view.mako')

    def printable(self, id):
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_attendee(id), h.auth.has_organiser_role, h.auth.has_unique_key())):
            # Raise a no_auth error
            h.auth.no_role()

        c.printable = True
        c.invoice = Invoice.find_by_id(id, True)
        c.payment_received = None
        c.payment = None
        if c.invoice.paid() and c.invoice.total() > 0:
            c.payment_received = c.invoice.good_payments()[0]
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
        c.invoice_collection = Invoice.find_all()
        #c.invoice = c.invoice_collection[0]
        #c.recipient = c.invoice.person
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
            if invoice.paid() or invoice.bad_payments().count() > 0:
                c.status = []
                if invoice.total()==0:
                  c.status.append('zero balance')
                if invoice.good_payments().count() > 0:
                  c.status.append('paid')
                  if invoice.good_payments().count()>1:
                    c.status[-1] += ' (%d times)' % invoice.good_payments().count()
                if invoice.bad_payments().count() > 0:
                  c.status.append('tried to pay')
                  if invoice.bad_payments().count()>1:
                    c.status[-1] += ' (%d times)' % invoice.bad_payments().count()
                c.status = ' and '.join(c.status)
                return render('/invoice/already.mako')

        if invoice.is_void():
            c.signed_in_person = h.signed_in_person()
            return render('/invoice/invalid.mako')
        if not ignore_overdue and invoice.overdue():
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

        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_user(person.id), h.auth.has_organiser_role, h.auth.has_unique_key())):
            # Raise a no_auth error
            h.auth.no_role()

        #return render('/registration/really_closed.mako')

        error = self._check_invoice(person, invoice)
        if error is not None:
            return error

        c.payment = Payment()
        c.payment.amount = invoice.total()
        c.payment.invoice = invoice

        meta.Session.commit()
        return render("/invoice/payment.mako")

    @validate(schema=PayInvoiceSchema(), form='pay', post_only=True, on_get=True, variable_decode=True)
    def _pay(self, id):
        payment = Payment.find_by_id(self.form_result['payment_id'])
        c.invoice = payment.invoice
        person = c.invoice.person

        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_user(person.id), h.auth.has_organiser_role, h.auth.has_unique_key())):
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
            'amount': "%#.*f" % (2, payment.amount / 100.0),
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
        c.payment.amount = invoice.total()
        c.payment.invoice = invoice

        meta.Session.commit()
        return redirect_to(controller='payment', id=c.payment.id, action='new_manual')


    def pdf(self, id):
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_attendee(id), h.auth.has_organiser_role, h.auth.has_unique_key())):
            # Raise a no_auth error
            h.auth.no_role()

        import os, tempfile, libxml2, libxslt

        c.invoice = Invoice.find_by_id(id, True)

        xml_s = render('/invoice/pdf.mako')

        xsl_f = file_paths['zk_root'] + '/zookeepr/templates/invoice/pdf.xsl'
        xsl_s = libxml2.parseFile(xsl_f)
        xsl = libxslt.parseStylesheetDoc(xsl_s)

        xml = libxml2.parseDoc(xml_s)
        svg_s = xsl.applyStylesheet(xml, None)

        (svg_fd, svg) = tempfile.mkstemp('.svg')
        xsl.saveResultToFilename(svg, svg_s, 0)

        xsl.freeStylesheet()
        xml.freeDoc()
        svg_s.freeDoc()

        (pdf_fd, pdf) = tempfile.mkstemp('.pdf')

        os.close(svg_fd); os.close(pdf_fd)

        os.system('inkscape -z -f %s -A %s' % (svg, pdf))

        pdf_f = file(pdf)
        res = Response(pdf_f.read())
        pdf_f.close()
        res.headers['Content-type']='application/pdf'
        #res.headers['Content-type']='application/octet-stream'
        #res.headers['Content-type']='text/plain; charset=utf-8'
        filename = lca_info['event_shortname'] + '_' + str(c.invoice.id) + '.pdf'
        res.headers['Content-Disposition']=( 'attachment; filename=%s' % filename )

        # We should really remove the pdf file, shouldn't we.
        return res

    def void(self, id):
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_attendee(id), h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()

        c.invoice = Invoice.find_by_id(id, True)
        if c.invoice.is_void():
            h.flash("Invoice was already voided.")
            return redirect_to(action='view', id=c.invoice.id)

        if h.auth.authorized(h.auth.has_organiser_role):
            c.invoice.void = "Administration Change"
            meta.Session.commit()
            h.flash("Invoice was voided.")
            return redirect_to(action='view', id=c.invoice.id)
        else:
            if c.invoice.paid():
                h.flash("Cannot void a paid invoice.")
                return redirect_to(action='view', id=c.invoice.id)
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
