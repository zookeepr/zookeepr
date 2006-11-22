import datetime

class InvoiceItem(object):
    def __init__(self, description=None, cost=None):
        self.description = description
        self.cost = cost

    def __repr__(self):
        return '<InvoiceItem id=%r description=%r cost=%r>' % (self.id, self.description, self.cost)

class Invoice(object):
    def __init__(self, issue_date=None):
        self.issue_date = issue_date

    def __repr__(self):
        return '<Invoice id=%r person=%r>' % (self.id, self.person_id)

class PaymentReceived(object):
    def __init__(self,
                 InvoiceID=None,
                 PaymentID=None,
                 AuthNum=None,
                 Amount=None,
                 RefundKey=None,
                 Status=None,
                 Settlement=None,
                 ErrorString=None,
                 CardName=None,
                 CardType=None,
                 TransID=None,
                 ORIGINAL_AMOUNT=None,
                 ):
        self.invoice_id = InvoiceID
        self.payment_id = PaymentID
        self.auth_num = AuthNum
        self.amount = Amount
        self.refund_key = RefundKey
        self.status = Status
        self.settlement = Settlement
        self.wrror_string = ErrorString
        self.card_name = CardName
        self.card_type = CardType
        self.trans_id = TransID
        self.original_amount = ORIGINAL_AMOUNT

    def map_fields(self, fields):

        mapping = {
            'InvoiceID': 'invoice_id',
            'PaymentID': 'payment_id',
            'AuthNum': 'auth_num',
            'Amount': 'amount',
            'RefundKey': 'refund_key',
            'Status': 'status',
            'Settlement': 'settlement',
            'ErrorString': 'wrror_string',
            'CardName': 'card_name',
            'CardType': 'card_type',
            'TransID': 'trans_id',
            'ORIGINAL_AMOUNT': 'original_amount',
        }

        for key in mapping.keys():
            if key in fields:
                setattr(self, mapping[key], fields[key])


    def __repr__(self):
        return '<PaymentReceived id=%r invoice_id=%r payment_id=%r amount=%r>' % (self.id, self.invoice_id, self.payment_id, self.amount)

class PaymentSent(object):
    def __init__(self):
        pass

    def __repr__(self):
        return '<PaymentSent id=%r>' % (self.id)


