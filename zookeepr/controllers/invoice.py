import datetime

import hmac
import sha

from zookeepr.lib.base import *
from zookeepr.lib.auth import *
from zookeepr.lib.crud import *
from zookeepr.lib.validators import *
from formencode import validators, variabledecode, ForEach

from zookeepr.config.lca_info import lca_info

from zookeepr.model.billing import ProductCategory, Product, Voucher

#TODO: Fix validation on new pylons merge

class InvoiceItemValidator(BaseSchema):
    product = ProductValidator()
    qty = BoundedInt(min=1)
    cost = BoundedInt()
    description = validators.String(not_empty=False)
    
    chained_validators = [InvoiceItemProductDescription()]
        
class InvoiceSchema(BaseSchema):
    person = ExistingPersonValidator(not_empty=True)
    due_date = validators.DateConverter(month_style='dd/mm/yy')
    items = ForEach(InvoiceItemValidator())

    item_count = validators.Int()

class NewInvoiceSchema(BaseSchema):
    invoice = InvoiceSchema()
    pre_validators = [variabledecode.NestedVariables]

class InvoiceController(SecureController, Read, List, Create):
    model = model.Invoice
    individual = 'invoice'
    permissions = {'view': [AuthFunc('is_payee'), AuthRole('organiser')],
                   'printable': [AuthFunc('is_payee'), AuthRole('organiser')],
                   'pay': [AuthFunc('is_payee'), AuthRole('organiser')],
                   'remind': [AuthRole('organiser')],
                   'index': [AuthRole('organiser')],
                   'pdf': [AuthFunc('is_payee'), AuthRole('organiser')],
                   'new': [AuthRole('organiser')]
                   }

    schemas = {'new': NewInvoiceSchema()
            }

    def is_payee(self):
        return c.signed_in_person == self.obj.person

    def pay(self, id):
        """Pay an invoice.

        This method bounces the user off to the commsecure website.
        """
        #return render_response('registration/really_closed.myt')
        if c.invoice.person.invoices:
            if c.invoice.paid() or c.invoice.bad_payments:
                return render_response('invoice/already.myt')

        if c.invoice.void:
            return render_response('invoice/invalid.myt')
        if c.invoice.overdue():
            for ii in c.invoice.items:
                if ii.product and not ii.product.available():
                    return render_response('invoice/expired.myt')

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

        res=Response(render('invoice/payment.myt', fields=fields))
        res.headers['Refresh']='300'
        return res

    def printable(self):
        c.printable = True
        res = render('%s/view.myt' % self.individual, fragment=True)
        return Response(res)

    # FIXME There is probably a way to get this to use the List thingy from CRUD
    def remind(self):
        setattr(c, 'invoice_collection', self.dbsession.query(self.model).select(order_by=self.model.c.id))
        return render_response('invoice/remind.myt')

    def pdf(self, id):
        import os, tempfile, libxml2, libxslt

        xml_s = render('%s/pdf.myt' % self.individual, fragment=True)

        xsl_f = request.environ['paste.config']['global_conf']['here'] + '/zookeepr/templates/invoice/pdf.xsl'
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
        res.headers['Content-Disposition']=( 'attachment; filename=%s.pdf'
                                                           % c.invoice.id )

		# We should really remove the pdf file, shouldn't we.
        return res
        
    def new(self):
        errors = {}
        defaults = dict(request.POST)
        c.product_categories = self.dbsession.query(ProductCategory).all()

        c.item_count = 0
        if request.method == 'POST' and defaults:
            result, errors = self.schemas['new'].validate(defaults, self.dbsession)
            c.item_count = int(defaults['invoice.item_count'])
            if not errors:
                values = result['invoice']
                items = values['items']
                del(values['items'], values['item_count'])
                values['items'] = []

                for i in items:
                    item = model.InvoiceItem()
                    if i['description'] != "":
                        item.description = i['description']
                    else:
                        item.product = i['product']
                        item.description = i['product'].description
                    item.cost = i['cost']
                    item.qty = i['qty']
                    values['items'].append(item)
                
                invoice = model.Invoice()
                for k in values:
                    setattr(invoice, k, values[k])
                invoice.manual = True
                invoice.void = False
               
                self.dbsession.save(invoice)
                self.dbsession.flush()
                
                return redirect_to(controller='invoice', action='view', id=invoice.id)

        return render_response("invoice/new.myt",
                               defaults=defaults, errors=errors)
                               
                               
