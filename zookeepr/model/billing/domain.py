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

    def qty_invoiced(self):
        qty = 0
        for p in self.products:
            qty += p.qty_invoiced()
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
        return self.qty_invoiced() >= self.max_sold
        #return self.qty_sold() >= self.max_sold

    def available(self):
        if self.soldout():
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

    def __reprt__(self):
        return '<ProductCategory id=%r name=%r description=%r display=%r min_qty=%r max_qty=%r>' % (self.id, self.name, self.description, self.display, self.min_qty, self.max_qty)

    def available_products(self, person):
        products = []
        for product in self.products:
            if product.available():
                products.append(product)
        return products

    def qty_person_sold(self, person):
        qty = 0
        for i in person.invoices:
            for ii in i.invoice_items:
                if ii.product.category == self:
                    qty += ii.qty
        return qty

    def can_i_sell(self, person, qty):
        if self.qty_person_sold(person) + qty <= self.max_qty:
            return True
        else:
            return False

class ProductInclude(object):
    def __init__(self, include_qty=None):
        self.include_qty = include_qty

    def __repr__(self):
        return '<ProductInclude product_id=%r include_product_id=%r include_qty=%r>' % (self.product_id, self.include_product_id, self.include_qty)

class Product(object):
    def __init__(self, active=False, description=None, cost=None, auth=None, validate=None):
        self.active = active
        self.description = description
        self.cost = cost
        self.auth = auth
        self.validate = validate

    def __repr__(self):
        return '<Product id=%r active=%r description=%r cost=%r auth=%r validate%r>' % (self.id, self.active, self.description, self.cost, self.auth, self.validate)

    def qty_sold(self):
        qty = 0
        for ii in self.invoice_items:
            if ii.invoice.paid():
                if self.category.name == 'Accomodation':
                    qty += 1
                else:
                    qty += ii.qty
        return qty

    def qty_invoiced(self):
        qty = 0
        for ii in self.invoice_items:
            if ii.invoice.void == False and ii.invoice.due_date >= datetime.datetime.now():
                if self.category.name == 'Accomodation':
                    qty += 1
                else:
                    qty += ii.qty
        return qty

    def remaining(self):
        max_ceiling = None
        for c in self.ceilings:
            if c.remaining() > max_ceiling:
                max_ceiling = c.remaining
        return max_ceiling

    def available(self):
        if self.active:
           for c in self.ceilings:
                if not c.available():
                    return False
           return True
        else:
            return False

    def can_i_sell(self, person, qty):
        if not self.available():
            return False
        if not self.category.can_i_sell(person, qty):
            return False
        for c in self.ceiling:
            if not c.can_i_sell(qty):
                return False
        return True

    def available_until(self):
        until = []
        for ceiling in self.ceilings:
            if ceiling.available_until != None:
                until.append(ceiling.available_until)
        if len(until) > 0:
            return max(until)

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
    def __init__(self, void=False, issue_date=None, due_date=None):
        self.void = void
        self.issue_date = issue_date
        self.due_date = due_date

        if self.issue_date is None:
            self.issue_date = datetime.datetime.now()
        if self.due_date is None:
            self.due_date = datetime.datetime.now() + datetime.timedelta(14, 0, 0)

    def __repr__(self):
        return '<Invoice id=%r void=%r person=%r>' % (self.id, self.void, self.person_id)

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
        if self.void == True:
            return "Invalid"
        elif self.paid():
            return "Paid"
        else:
            return "Unpaid"

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


class VoucherCode(object):
    def __repr__(self):
        return '<VoucherCode id=%r code=%r type=%r percentage=%r comment=%r>' % (self.id, self.code, self.type, self.percentage, self.comment)

    def __init__(self,
                 code=None,
                 percentage=None,
                 comment=None,
                 ):
        self.code = code
        self.percentage = percentage
        self.comment = comment


