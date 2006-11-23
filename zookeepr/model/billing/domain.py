import datetime

class InvoiceItem(object):
    def __init__(self, description=None, qty=None, cost=None):
        self.description = description
        self.qty = qty
        self.cost = cost

    def __repr__(self):
        return '<InvoiceItem id=%r description=%r qty=%r cost=%r>' % (self.id, self.description, self.qty, self.cost)

    def total(self):
        """Return the total cost of this item"""
        return self.cost * self.qty


class Invoice(object):
    def __init__(self, issue_date=None, due_date=None):
        self.issue_date = issue_date
        self.due_date = due_date

        if self.issue_date is None:
            self.issue_date = datetime.datetime.now()
        if self.due_date is None:
            self.due_date = datetime.datetime.now() + datetime.timedelta(14, 0, 0)

    def __repr__(self):
        return '<Invoice id=%r person=%r>' % (self.id, self.person_id)

    def total(self):
        """Return the total value of this invoice"""
        t = 0
        for ii in self.items:
            t += ii.total()
        return t


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
                 HTTP_X_FORWARDED_FOR=None,
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
        self.HTTP_X_FORWARDED_FOR = HTTP_X_FORWARDED_FOR


class Payment(object):
    def __repr__(self):
        return '<Payment id=%r>' % (self.id)
