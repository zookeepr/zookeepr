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


class PaymentReceived(object):
    def __repr__(self):
        return '<PaymentReceived id=%r invoice_id=%r payment_id=%r amount=%r status=%r>' % (self.id, self.InvoiceID, self.PaymentID, self.Amount, self.Status)

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
                 RequestedPage=None,
                 MAC=None,
                 CardNumber=None,
                 MerchantID=None,
                 Surcharge=None,
                 ):
        self.InvoiceID = InvoiceID
        self.PaymentID = PaymentID
        self.AuthNum = AuthNum
        self.Amount = Amount
        self.RefundKey = RefundKey
        self.Status = Status
        self.Settlement = Settlement
        self.ErrorString = ErrorString
        self.CardName = CardName
        self.CardType = CardType
        self.TransID = TransID
        self.ORIGINAL_AMOUNT = ORIGINAL_AMOUNT
        self.RequestedPage = RequestedPage
        self.MAC = MAC
        self.CardNumber = CardNumber
        self.MerchantID = MerchantID
        self.Surcharge = Surcharge

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
            'RequestedPage': 'requested_page',
            'MAC': 'mac',
            'CardNumber': 'card_number',
            'MerchantID': 'merchant_id',
            'Surcharge': 'surcharge',
        }

        for key in mapping.keys():
            if key in fields:
                setattr(self, mapping[key], fields[key])


class Payment(object):
    def __repr__(self):
        return '<Payment id=%r>' % (self.id)
