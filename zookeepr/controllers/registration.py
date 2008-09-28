import datetime
import warnings

from formencode import validators, compound, variabledecode, schema
from formencode.schema import Schema

from zookeepr.lib.auth import *
from zookeepr.lib.base import *
from zookeepr.lib.crud import *
from zookeepr.lib.mail import *
from zookeepr.lib.validators import *

from zookeepr.controllers.person import PersonSchema
from zookeepr.model.billing import ProductCategory, Product, Voucher
from zookeepr.model.registration import Registration

class NotExistingRegistrationValidator(validators.FancyValidator):
    def validate_python(self, value, state):
        rego = None
        if 'signed_in_person_id' in session:
            rego = state.query(model.Registration).filter_by(person_id=session['signed_in_person_id']).first()
        if rego is not None and rego != c.registration:
            raise Invalid("Thanks for your keenness, but you've already registered!", value, state)

class DuplicateVoucherValidator(validators.FancyValidator):
    def validate_python(self, value, state):
        voucher = state.query(Voucher).filter_by(code=value['voucher_code']).first()
        if voucher != None:
            if voucher.registration:
                if not 'signed_in_person_id' in session:
                    raise Invalid("Voucher code already in use! (not logged in)", value, state)
                if voucher.registration.person_id != session['signed_in_person_id']:
                    raise Invalid("Voucher code already in use!", value, state)
        elif value['voucher_code']:
            raise Invalid("Unknown voucher code!", value, state)

class SillyDescriptionChecksum(validators.FancyValidator):
    def validate_python(self, value, state):
        checksum = h.silly_description_checksum(value['silly_description'])
        if value['silly_description_checksum'] != checksum:
            raise Invalid("Smart enough to hack the silly description, not smart enough to hack the checksum.", value, state)

class ExistingPersonSchema(BaseSchema):
    company = validators.String()
    phone = validators.String()
    mobile = validators.String()
    address1 = validators.String(not_empty=True)
    address2 = validators.String()
    city = validators.String(not_empty=True)
    state = validators.String()
    postcode = validators.String(not_empty=True)
    country = validators.String(not_empty=True)

class RegisterSchema(BaseSchema):
    nick = validators.String()
    shell = validators.String()
    shelltext = validators.String()
    editor = validators.String()
    editortext = validators.String()
    distro = validators.String()
    distrotext = validators.String()
    silly_description = validators.String()
    silly_description_checksum = validators.String(strip=True)
    voucher_code = validators.String(if_empty=None)
    diet = validators.String()
    special = validators.String()
    opendaydrag = validators.Int()
    checkin = BoundedInt(min=0)
    checkout = BoundedInt(min=0)
    lasignup = validators.Bool()
    announcesignup = validators.Bool()
    delegatesignup = validators.Bool()
    speaker_record = validators.Bool()
    speaker_video_release = validators.Bool()
    speaker_side_release = validators.Bool()
    prevlca = DictSet(if_missing=None)
    miniconf = DictSet(if_missing=None)

    chained_validators = [SillyDescriptionChecksum(), DuplicateVoucherValidator()]

class NewRegistrationSchema(BaseSchema):
    person = PersonSchema()
    registration = RegisterSchema()

    chained_validators = [NotExistingRegistrationValidator()]
    pre_validators = [variabledecode.NestedVariables]

class UpdateRegistrationSchema(BaseSchema):
    person = ExistingPersonSchema()
    registration = RegisterSchema()

    chained_validators = [NotExistingRegistrationValidator()]
    pre_validators = [variabledecode.NestedVariables]

class RegistrationController(SecureController, Update, List, Read):
    individual = 'registration'
    model = model.Registration
    schemas = {'new': NewRegistrationSchema(),
               'edit': UpdateRegistrationSchema()
            }
    permissions = {'new': True,
                   'edit': [AuthRole('organiser'), AuthFunc('is_same_person')],
                   'view': [AuthRole('organiser'), AuthFunc('is_same_person')],
                   'pay': [AuthRole('organiser'), AuthFunc('is_same_person')],
                   'index': [AuthRole('organiser')],
                   'status': True,
                   'silly_description': True
               }

    def __before__(self, **kwargs):
        super(RegistrationController, self).__before__(**kwargs)
        c.product_categories = self.dbsession.query(ProductCategory).all()
        c.ceilings = {}
        for ceiling in self.dbsession.query(model.Ceiling).all():
            c.ceilings[ceiling.name] = ceiling

        self._generate_product_schema()
        #c.products = self.dbsession.query(Product).all()
        c.product_available = self._product_available
        c.able_to_register = self._able_to_register
        c.able_to_edit = self._able_to_edit

    def _able_to_register(self):
        if c.signed_in_person and c.signed_in_person.registration:
            return False, "Thanks for your keenness, but you've already registered!"
        return True, "You can register"

    def _able_to_edit(self):
        for invoice in c.signed_in_person.invoices:
            if not invoice.void:
                if invoice.paid() and invoice.total() != 0:
                    return False, "Sorry, you've already paid"
        return True, "You can edit"

    def _product_available(self, product, stock=True):
        # bool stock: care about if the product is in stock (ie sold out?)
        if not product.available(stock):
            return False
        if product.auth is not None:
            exec("auth = " + product.auth)
            if not auth:
                return False
        return True

    def _generate_product_schema(self):
        class ProductSchema(BaseSchema):
            pass
        ProductSchema.add_field('partner_email', EmailAddress()) # placed here so prevalidator can refer to it. This means we need a hacky method to save it :S
        for category in c.product_categories:
            if category.display in ('radio', 'select'):
                # min/max can't be calculated on this form. You should only have 1 selected.
                ProductSchema.add_field('category_' + str(category.id), ProductInCategory(category=category, not_empty=True))
                for product in category.products:
                    if product.validate is not None:
                        exec("validator = " + product.validate)
                        ProductSchema.add_pre_validator(validator)
            elif category.display == 'checkbox':
                product_fields = []
                for product in category.products:
                    if self._product_available:
                        ProductSchema.add_field('product_' + str(product.id), validators.Bool(if_missing=False))
                        product_fields.append('product_' + str(product.id))
                        if product.validate is not None:
                            exec("validator = " + product.validate)
                            ProductSchema.add_pre_validator(validator)
                ProductSchema.add_pre_validator(ProductMinMax(product_fields=product_fields, min_qty=category.min_qty, max_qty=category.max_qty, category_name=category.name))
            elif category.display == 'qty':
                # qty
                product_fields = []
                for product in category.products:
                    if self._product_available:
                        ProductSchema.add_field('product_' + str(product.id) + '_qty', BoundedInt())
                        product_fields.append('product_' + str(product.id) + '_qty')
                    if product.validate is not None:
                        exec("validator = " + product.validate)
                        ProductSchema.add_pre_validator(validator)
                ProductSchema.add_pre_validator(ProductMinMax(product_fields=product_fields, min_qty=category.min_qty, max_qty=category.max_qty, category_name=category.name))
                # FIXME: I have spent far too long to try and get this working. Technically this should be a chained validator, not a pre validator but no matter what I do I can't get it to work (read heaps of docs etc etc). The result of being a pre-validator is that if there is an error the pre validator doesn't pick up (like an unfilled field) that the normal validation would pick up it isn't highlighted until the pre-validator doesn't find any errors. For example if you dont' select any shirts and have "asdf" in one of the dinner ticket fields you should see two errors: 1. you have no shirts and 2. tickets need to be integers. Once you select a shirt and resubmit the other error will show up. So it's a usability issue and doesn't make the form less secure, but damn this one is annoying!
        self.schemas['new'].add_field('products', ProductSchema)
        self.schemas['edit'].add_field('products', ProductSchema)

    def is_speaker(self):
        return c.signed_in_person.is_speaker()

    def is_same_person(self):
        return c.signed_in_person == c.registration.person

    def new(self, id):
        able, response = self._able_to_register()
        if not able:
            return render_response("registration/error.myt", error=response)
        errors = {}
        defaults = dict(request.POST)

        if c.signed_in_person:
            current_schema = self.schemas['edit']
        else:
            current_schema = self.schemas['new']

        if request.method == 'POST' and defaults:
            result, errors = current_schema.validate(defaults, self.dbsession)
            if not errors:
                # A blank registration
                c.registration = model.Registration()
                self.save_details(result)

                # Create person<->registration relationship
                c.registration.person = c.person
                self.dbsession.flush()

                email(
                    c.person.email_address,
                    render('registration/response.myt',
                        id=c.person.url_hash, fragment=True))

                self.obj = c.registration
                self.pay(c.registration.id, quiet=1)

                if c.signed_in_person:
                    redirect_to('/registration/status')
                return render_response('registration/thankyou.myt')
        return render_response("registration/new.myt",
                               defaults=defaults, errors=errors)

    def edit(self, id):
        able, response = self._able_to_edit()
        if not able:
            return render_response("registration/error.myt", error=response)
        errors = {}
        defaults = dict(request.POST)

        current_schema = self.schemas['edit']

        if request.method == 'POST' and defaults:
            result, errors = current_schema.validate(defaults, self.dbsession)
            if not errors:
                self.save_details(result)

                self.dbsession.flush()

                self.obj = c.registration
                self.pay(c.registration.id, quiet=1)

                redirect_to('/registration/status')
        return render_response("registration/edit.myt",
                               defaults=defaults, errors=errors)

    def save_details(self, result):
        # Store Registration details
        for k in result['registration']:
            if k in ('shell', 'editor', 'distro'):
                if result['registration'][k] == 'other':
                    setattr(c.registration, k, result['registration'][k + 'text'])
                else:
                    setattr(c.registration, k, result['registration'][k])
            else:
                setattr(c.registration, k, result['registration'][k])
        setattr(c.registration, 'partner_email', result['products']['partner_email']) # hacky method to make validating sane
        self.dbsession.save_or_update(c.registration)

        # Always delete the current products
        c.registration.products = []

        # Store Product details
        for category in c.product_categories:
            if category.display in ('radio', 'select'):
                product = self.dbsession.query(model.Product).get(result['products']['category_' + str(category.id)])
                if product != None:
                    rego_product = model.RegistrationProduct()
                    rego_product.product = product
                    if product.category.name == 'Accomodation':
                        rego_product.qty = c.registration.checkout - c.registration.checkin
                    else:
                        rego_product.qty = 1
                    self.dbsession.save(rego_product)
                    c.registration.products.append(rego_product)
            elif category.display == 'checkbox':
                for product in category.products:
                    if result['products']['product_' + str(product.id)] == True:
                        rego_product = model.RegistrationProduct()
                        rego_product.product = product
                        rego_product.qty = 1
                        self.dbsession.save(rego_product)
                        c.registration.products.append(rego_product)
            elif category.display == 'qty':
                for product in category.products:
                    if result['products']['product_' + str(product.id) + '_qty'] not in [0, None]:
                        rego_product = model.RegistrationProduct()
                        rego_product.product = product
                        rego_product.qty = result['products']['product_' + str(product.id) + '_qty']
                        self.dbsession.save(rego_product)
                        c.registration.products.append(rego_product)

        # Check whether we're already signed in or not, and store person details
        if not c.signed_in_person:
            c.person = model.Person()
        elif c.registration.person:
            c.person = c.registration.person
        else:
            c.person = c.signed_in_person

        for k in result['person']:
            setattr(c.person, k, result['person'][k])

        self.dbsession.save_or_update(c.person)

    def status(self):
        return render_response("registration/status.myt")

    def silly_description(self):
        desc, descChecksum = h.silly_description()
        return descChecksum + ',' + desc

    def pay(self, id, quiet=0):
        registration = self.obj

        invoice = model.Invoice()
        invoice.person = registration.person
        invoice.manual = False

        # Create Invoice
        for rproduct in registration.products:
            ii = model.InvoiceItem(description=rproduct.product.description, qty=rproduct.qty, cost=rproduct.product.cost)
            ii.product = rproduct.product
            product_expires = rproduct.product.available_until() 
            if product_expires != None and product_expires < invoice.due_date:
                invoice.due_date = product_expires
            self.dbsession.save(ii)
            invoice.items.append(ii)

        # Check for included products
        for ii in invoice.items:
            if ii.product and ii.product.included:
                for iproduct in ii.product.included:
                    included_qty = iproduct.include_qty
                    included_category = iproduct.include_category
                    free_qty = 0
                    free_cost = 0
                    for ii2 in invoice.items:
                        if ii2.product and ii2.product.category == included_category:
                            if free_qty + ii2.qty > included_qty:
                                free_cost += (included_qty - free_qty) * ii2.product.cost
                                free_qty += (included_qty - free_qty)
                            else:
                                free_cost += ii2.qty * ii2.product.cost
                                free_qty += ii2.qty

                    # We have included products, create a discount for the cost of them.
                    # This is not perfect, products of different prices can be discounted,
                    # and it can either favor the customer or LCA, depending on the order
                    # of items on the invoice
                    if free_cost > 0:
                        discount_item = model.InvoiceItem(description="Discount for " + str(free_qty) + " included " + included_category.name, qty=1, cost=-free_cost)
                        self.dbsession.save(discount_item)
                        invoice.items.append(discount_item)

        # Voucher code calculation
        if c.registration.voucher:
            voucher = c.registration.voucher
            for vproduct in voucher.products:
                for ii in invoice.items:
                    # if we have a category match
                    if ii.product.category == vproduct.product.category:
                        # The qty we will give
                        if ii.qty < vproduct.qty:
                            qty = ii.qty
                        else:
                            qty = vproduct.qty

                        # the discount we will give
                        max_discount = vproduct.product.cost * vproduct.percentage / 100
                        if ii.product.cost >= max_discount:
                            discount = max_discount
                        else:
                            discount = ii.product.cost
                        discount_item = model.InvoiceItem(description="Discount Voucher (" + voucher.comment + ") for " + vproduct.product.description, qty=qty, cost=-discount)
                        self.dbsession.save(discount_item)
                        invoice.items.append(discount_item)
                        break


        # complicated check to see whether invoices are already in the system
        new_invoice = invoice
        for old_invoice in registration.person.invoices:
            if old_invoice != new_invoice and not old_invoice.manual and not old_invoice.void:
                if self.invoices_identical(old_invoice, new_invoice):
                    for ii in new_invoice.items:
                        self.dbsession.expunge(ii)
                    self.dbsession.expunge(new_invoice)
                    invoice = old_invoice
                else:
                    if old_invoice.due_date < new_invoice.due_date:
                        new_invoice.due_date = old_invoice.due_date
                    ii2 = model.InvoiceItem(description="INVALID INVOICE (Registration Change)", qty=0, cost=0)
                    self.dbsession.save(ii2)
                    old_invoice.items.append(ii2)
                    old_invoice.void = True

        for ii in invoice.items:
            if ii.product and not self._product_available(ii.product):
                ii2 = model.InvoiceItem(description="INVALID INVOICE (Product " + ii.product.description + " is no longer available)", qty=0, cost=0)
                self.dbsession.save(ii2)
                invoice.items.append(ii2)
                invoice.void = True

        invoice.last_modification_timestamp = datetime.datetime.now()
        if invoice.void:
            self.dbsession.expunge(invoice)
            self.dbsession.save_or_update(invoice)
            return render_response("registration/product_unavailable.myt", product=rproduct.product)

        self.dbsession.save_or_update(invoice)
        self.dbsession.flush()

        if quiet: return
        redirect_to(controller='invoice', action='view', id=invoice.id)

    def invoices_identical(self, invoice1, invoice2):
        if invoice1.total() == invoice2.total():
            if len(invoice1.items) == len(invoice2.items):
                matched_products = 0
                for invoice1_item in invoice1.items:
                    for invoice2_item in invoice2.items:
                        if invoice1_item.product == invoice2_item.product and invoice1_item.description == invoice2_item.description and invoice1_item.qty == invoice2_item.qty and invoice1_item.cost == invoice2_item.cost:
                            matched_products += 1
                if len(invoice1.items) == matched_products:
                    return True
        return False
