import datetime

class InvoiceItem(object):
    def __init__(self, description=None, qty=None, cost=None):
        self.description = description
        self.qty = qty
        self.cost = cost

    def __repr__(self):
        return '<InvoiceItem id=%r description=%r qty=%r cost=%r>' % (self.id, self.description, self.qty, self.cost)

class Invoice(object):
    def __init__(self, issue_date=None):
        self.issue_date = issue_date

    def __repr__(self):
        return '<Invoice id=%r person=%r>' % (self.id, self.person_id)

    # FIXME: remove when mapped to payment object
    def _get_payment(self):
        return None

    payment = property(_get_payment)


class PaymentReceived(object):
    def __init__(self, invoice_id=None, auth_num=None, amount=None, refund_key=None, merchant_id=None, status=None, settlement=None, error_string=None, card_name=None, requested_page=None, card_type=None, mac=None, card_number=None, payment_id=None, trans_id=None, original_amount=None, surcharge=None):
        self.invoice_id = invoice_id
        self.auth_num = auth_num
        self.amount = amount
        self.refund_key = refund_key
        self.merchant_id = merchant_id
        self.status = status
        self.settlement = settlement
        self.error_string = error_string
        self.card_name = card_name
        self.requested_page = requested_page
        self.card_type = card_type
        self.mac = mac
        self.card_number = card_number
        self.payment_id = payment_id
        self.trans_id = trans_id
        self.original_amount = original_amount
        self.surcharge = surcharge

    def __repr__(self):
        return '<PaymentReceived id=%r invoice_id=%r payment_id=%r amount=%r status=%r>' % (self.id, self.invoice_id, self.payment_id, self.amount, self.status)
