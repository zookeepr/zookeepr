import datetime
import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import redirect_to, Response, redirect
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill, ForEach, Invalid
from formencode.variabledecode import NestedVariables

from zookeepr.lib.base import BaseController, render
from zookeepr.lib.validators import BaseSchema, ProductValidator, InvoiceItemProductDescription, ExistingPersonValidator
import zookeepr.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zookeepr.lib.mail import email

from zookeepr.model import meta, Invoice, InvoiceItem, Registration, ProductCategory
from zookeepr.model.payment import Payment

from zookeepr.config.lca_info import lca_info, file_paths

import zookeepr.lib.pxpay as pxpay

log = logging.getLogger(__name__)

class InvoiceItemValidator(BaseSchema):
    product = ProductValidator()
    qty = validators.Int(min=1)
    cost = validators.Int(min=0, max=2000000)
    description = validators.String(not_empty=False)
    chained_validators = [InvoiceItemProductDescription()]

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

class InvoiceController(BaseController):
    @authorize(h.auth.is_valid_user)
    def __before__(self, **kwargs):
        pass

    @authorize(h.auth.has_organiser_role)
    @dispatch_on(POST="_new")
    def new(self):
        c.product_categories = ProductCategory.find_all()
        c.item_count = 0;
        return render("/invoice/new.mako")

    @validate(schema=NewInvoiceSchema(), form='new', post_only=True, on_get=True, variable_decode=True)
    def _new(self):
        results = self.form_result['invoice']
        del(results['item_count'])

        items = results['items']
        results['items'] = []
        for i in items:
            item = InvoiceItem()
            if i['description'] != "":
                item.description = i['description']
            else:
                item.product = i['product']
                item.description = i['product'].description
            item.cost = i['cost']
            item.qty = i['qty']
            results['items'].append(item)

        c.invoice = Invoice(**results)
        c.invoice.manual = True
        c.invoice.void = None
        meta.Session.add(c.invoice)
        meta.Session.commit()

        h.flash("Manual invoice created")
        return redirect_to(action='view', id=c.invoice.id)

    def view(self, id):
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_attendee(id), h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()

        c.printable = False
        c.invoice = Invoice.find_by_id(id, True)
        return render('/invoice/view.mako')

    def printable(self, id):
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_attendee(id), h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()

        c.printable = True
        c.invoice = Invoice.find_by_id(id, True)
        return render('/invoice/view_printable.mako')

    def index(self):
        if h.auth.has_organiser_role:
            c.can_edit = True
            c.invoice_collection = Invoice.find_all()
        else:
            c.can_edit = False
            c.invoice_collection = Invoice.find_by_person(h.signed_in_person().id)

        return render('/invoice/list.mako')

    @authorize(h.auth.has_organiser_role)
    def remind(self):
        c.invoice_collection = Invoice.find_all();
        return render('/invoice/remind.mako')

    def _check_invoice(self, person, invoice):
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
        if invoice.overdue():
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

        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_user(person.id), h.auth.has_organiser_role)):
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

        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_user(person.id), h.auth.has_organiser_role)):
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
            'return_url' : lca_info['event_url'] + '/payment/new',
        }

        (valid, uri) = pxpay.generate_request(params)
        if valid != '1':
            c.error_msg = "PxPay Generate Request error: " + uri
            return render("/payment/gateway_error.mako")
        else:
            redirect(uri)

    def pdf(self, id):
        return "Currently disabled." # FIXME: remove PDF invoices work again

        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_attendee(id), h.auth.has_organiser_role)):
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
        #res.headers['Content-type']='application/pdf'
        res.headers['Content-type']='application/octet-stream'
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
        if h.auth.authorized(h.auth.has_organiser_role):
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
