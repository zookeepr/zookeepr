import datetime

import hmac
import sha

from zookeepr.lib.base import *
from zookeepr.lib.auth import *
from zookeepr.lib.crud import *

from zookeepr.config.lca_info import lca_info

class InvoiceController(SecureController, Read, List):
    model = model.Invoice
    individual = 'invoice'
    permissions = {'view': [AuthFunc('is_payee'), AuthRole('organiser')],
                   'printable': [AuthFunc('is_payee'), AuthRole('organiser')],
                   'pay': [AuthFunc('is_payee'), AuthRole('organiser')],
                   'remind': [AuthRole('organiser')],
                   'index': [AuthRole('organiser')],
                   'pdf': [AuthFunc('is_payee'), AuthRole('organiser')],
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

        age = datetime.datetime.now() - c.invoice.last_modification_timestamp
        if age > datetime.timedelta(hours=1):
            return render_response('invoice/expired.myt')
        if c.invoice.total() % 5 != 0:
            return render_response('invoice/invalid.myt')

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

    def pdf(self):
        import os, tempfile

        res = render('%s/pdf.myt' % self.individual, fragment=True)

        xsl = request.environ['paste.config']['global_conf']['here']
        xsl += '/templates/invoice/pdf.xsl'

        (xml_fd, xml) = tempfile.mkstemp('.xml')
        (svg_fd, svg) = tempfile.mkstemp('.svg')
        (pdf_fd, pdf) = tempfile.mkstemp('.pdf')

        xml_f = os.fdopen(xml_fd, 'w')
        xml_f.write(res)
        xml_f.close()

        os.close(svg_fd); os.close(pdf_fd)

        os.system('saxon %s %s > %s' % (xml, xsl, svg))
        os.system('inkscape -z -f %s -A %s' % (svg, pdf))

        pdf_f = file(pdf)
        res = Response(pdf_f.read())
        pdf_f.close()
        #res.headers['Content-type']='application/pdf'
        res.headers['Content-type']='application/octet-stream'
        #res.headers['Content-type']='text/plain; charset=utf-8'
        res.headers['Content-Disposition']=( 'attachment; filename=%s.pdf'
                                                           % c.invoice.id )
        return res
