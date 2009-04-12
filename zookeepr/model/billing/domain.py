from __future__ import division
import datetime

class Ceiling(object):
    def __init__(self, name=None, max_sold=None, available_from=None, available_until=None):
        self.name = name
        self.max_sold = max_sold
        self.available_from = available_from
        self.available_until = available_until

    def __repr__(self):
        return '<Ceiling id=%r name=%r max_sold=%r available_from=%r, available_until=%r' % (self.id, self.name, self.max_sold, self.available_from, self.available_until)

    def qty_sold(self):
        qty = 0
        for p in self.products:
            qty += p.qty_sold()
        return qty

    def qty_invoiced(self, date=True):
        # date: bool? only count items that are not overdue
        qty = 0
        for p in self.products:
            qty += p.qty_invoiced(date)
        return qty

    def percent_sold(self):
        if self.max_sold == None:
            return 0
        else:
            return self.qty_sold() / self.max_sold * 100

    def percent_invoiced(self):
        if self.max_sold == None:
            return 0
        else:
            return self.qty_invoiced() / self.max_sold * 100

    def remaining(self):
        return self.max_sold - self.qty_sold()

    def soldout(self):
        if self.max_sold != None:
            return self.qty_invoiced() >= self.max_sold
            #return self.qty_sold() >= self.max_sold

    def available(self, stock=True):
        # bool stock: care about if the product is in stock (ie sold out?)
        if stock and self.soldout():
            return False
        elif self.available_from is not None and self.available_from >= datetime.datetime.now():
            return False
        elif self.available_until is not None and self.available_until <= datetime.datetime.now():
            return False
        else:
            return True

    def can_i_sell(self, qty):
        if not self.soldout() and self.remaining() > qty:
            return True
        else:
            return False


class ProductCategory(object):
    def __init__(self, name=None, description=None, display='qty', min_qty=0, max_qty=100):
        self.name = name
        self.description = description
        self.display = display
        self.min_qty = min_qty
        self.max_qty = max_qty

class ProductInclude(object):
    def __init__(self, include_qty=None):
        self.include_qty = include_qty

    def __repr__(self):
        return '<ProductInclude product_id=%r include_product_id=%r include_qty=%r>' % (self.product_id, self.include_product_id, self.include_qty)

class InvoiceItem(object):
    def __init__(self, description=None, qty=None, cost=None):
        self.description = description
        self.qty = qty
        self.cost = cost

    def __repr__(self):
        return '<InvoiceItem id=%r description=%r qty=%r cost=%r>' % (self.id, self.description, self.qty, self.cost)

    def total(self):
        """Return the total cost of this item"""
        return (self.cost or 0) * self.qty

class Invoice(object):
    def __init__(self, void=None, issue_date=None, due_date=None):
        self.void = void
        self.issue_date = issue_date
        self.due_date = due_date

        if self.issue_date is None:
            self.issue_date = datetime.datetime.now()
        if self.due_date is None:
            self.due_date = datetime.datetime.now()

    def __repr__(self):
        return '<Invoice id=%r void=%r person=%r>' % (self.id, self.void, self.person_id)

    def is_void(self):
        return (self.void is not None)

    def total(self):
        """Return the total value of this invoice"""
        t = 0
        for ii in self.items:
            t += ii.total()
        return t

    def paid(self):
        """Return whether the invoice is paid (or zero-balance) """
        return bool(self.good_payments or self.total()==0)

    def status(self):
        if self.is_void() == True:
            return "Invalid"
        elif self.paid():
            return "Paid"
        else:
            return "Unpaid"

    def overdue(self):
        return self.due_date < datetime.datetime.now()

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


class Voucher(object):
    def __repr__(self):
        return '<Voucher id=%r code=%r comment=%r leader_id=%r>' % (self.id, self.code, self.comment, self.leader_id)

    def __init__(self, code=None, comment=None):
        self.code = code
        self.comment = comment


class VoucherProduct(object):
    def __repr__(self):
        return '' % ()
    def __init__(self, qty=None, percentage=None):
        self.qty = qty
        self.percentage = percentage
