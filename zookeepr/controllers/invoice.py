import datetime

import hmac
import sha

import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import redirect_to, Response
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
from zookeepr.model.payment import PaymentOptions

from zookeepr.config.lca_info import lca_info, file_paths

log = logging.getLogger(__name__)

class InvoiceItemValidator(BaseSchema):
    product = ProductValidator()
    qty = validators.Int(min=1)
    cost = validators.Int(min=0, max=2000000)
    description = validators.String(not_empty=False)
    chained_validators = [InvoiceItemProductDescription()]
        
class InvoiceSchema(BaseSchema):
    person = ExistingPersonValidator(not_empty=True)
    due_date = validators.DateConverter(format='%d/%m/%y')
    items = ForEach(InvoiceItemValidator())

    item_count = validators.Int(min=0) # no max, doesn't hit database

class NewInvoiceSchema(BaseSchema):
    invoice = InvoiceSchema()
    pre_validators = [NestedVariables]

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

    @validate(schema=NewInvoiceSchema(), form='new', post_only=True)
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
        c.invoice = Invoice.find_by_id(id)
        # TODO: remove these once payment works
        c.invoice.good_payments = False
        c.invoice.bad_payments = False
        return render('/invoice/view.mako')

    def printable(self, id):
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_attendee(id), h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()

        c.printable = True
        c.invoice = Invoice.find_by_id(id)
        return render('/invoice/view_printable.mako')

    def index(self):
        if h.auth.has_organiser_role:
            c.can_edit = True
            c.invoice_collection = Invoice.find_all()
        else:
            c.can_edit = False
            c.invoice_collection = Invoice.find_by_person(h.signed_in_person().id)

        # TODO: the payment stuff is not yet implemented
        for i in c.invoice_collection:
            i.good_payments = False
            i.bad_payments = False
        return render('/invoice/list.mako')

    @authorize(h.auth.has_organiser_role)
    def remind(self):
        c.invoice_collection = Invoice.find_all();
        c.payment_options = PaymentOptions();
        
        # TODO: this is a temporary hack until registration is ported
        for i in c.invoice_collection:
            i.person.registration = Registration()
        
        return render('/invoice/remind.mako')

    def pay(self, id):
        return "TODO: pay (needs payment controller)"
        """Pay an invoice.

        This method bounces the user off to the commsecure website.
        """
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_attendee(id), h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()

        c.invoice = Invoice.find_by_id(id)

        #return render('/registration/really_closed.mako')
        if c.invoice.person.invoices:
            if c.invoice.paid() or c.invoice.bad_payments:
                c.status = []
                if c.invoice.total()==0:
                  c.status.append('zero balance')
                if c.invoice.good_payments:
                  c.status.append('paid')
                  if len(c.invoice.good_payments)>1:
                    c.status[-1] += ' (%d times)' % len(c.invoice.good_payments)
                if c.invoice.bad_payments:
                  c.status.append('tried to pay')
                  if len(c.invoice.bad_payments)>1:
                    c.status[-1] += ' (%d times)' % len(c.invoice.bad_payments)
                c.status = ' and '.join(c.status)
                return render('/invoice/already.mako')

        if c.invoice.is_void():
            c.signed_in_person = h.signed_in_person()
            return render('/invoice/invalid.mako')
        if c.invoice.overdue():
            for ii in c.invoice.items:
                if ii.product and not ii.product.available():
                    return render('/invoice/expired.mako')

        # get our merchant id and secret
        merchant_id = lca_info['commsecure_merchantid']
        secret = lca_info['commsecure_secret']

        # create payment entry
        payment = model.Payment()
        payment.invoice = c.invoice
        # not sure why we do this anymore, convenience i guess
        payment.amount = c.invoice.total()

        self.dbsession.save(payment)
        self.dbsession.flush()

        fields = {
            'MerchantID': merchant_id,
            'PaymentID': payment.id,
            'Amount': payment.amount,
            'InvoiceID': payment.invoice.id,
            }

        # Generate HMAC
        keys = fields.keys()
        keys.sort()     # keys in alphabetical order

        # key1=value1&key2=value2&key3=value3 ...
        stringToMAC = '&'.join(['%s=%s' % (key, fields[key]) for key in keys])
        mac = hmac.new(secret, stringToMAC, sha).hexdigest()
        fields['MAC'] = mac

        res=Response(render('/invoice/payment.mako', fields=fields))
        res.headers['Refresh']='300'
        return res

    def pdf(self, id):
        if not h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_attendee(id), h.auth.has_organiser_role)):
            # Raise a no_auth error
            h.auth.no_role()

        import os, tempfile, libxml2, libxslt

        c.invoice = Invoice.find_by_id(id)
        # TODO: remove these once payment works
        c.invoice.good_payments = False
        c.invoice.bad_payments = False
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

    @authorize(h.auth.has_organiser_role)
    def void(self, id):
        c.invoice = Invoice.find_by_id(id)
        c.invoice.void = "Administration Change"
        meta.Session.commit()
        h.flash("Invoice was voided.")
        return redirect_to(action='view', id=c.invoice.id)

    @authorize(h.auth.has_organiser_role)    
    def unvoid(self, id):
        c.invoice = Invoice.find_by_id(id)
        c.invoice.void = None
        c.invoice.manual = True
        meta.Session.commit()
        h.flash("Invoice was un-voided.")
        return redirect_to(action='view', id=c.invoice.id)
