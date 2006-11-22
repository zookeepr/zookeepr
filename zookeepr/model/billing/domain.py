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


class Payment(object):
    def __repr__(self):
        return '<Payment id=%r>' % (self.id)
