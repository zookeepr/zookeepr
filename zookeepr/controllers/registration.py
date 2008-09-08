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
from zookeepr.model.billing import ProductCategory, Product
from zookeepr.model.registration import Registration

class NotExistingRegistrationValidator(validators.FancyValidator):
    def validate_python(self, value, state):
        rego = None
        if 'signed_in_person_id' in session:
            rego = state.query(model.Registration).filter_by(person_id=session['signed_in_person_id']).first()
        if rego is not None and rego != c.registration:
            raise Invalid("Thanks for your keenness, but you've already registered!", value, state)

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
    #voucher_code = validators.String()
    diet = validators.String()
    special = validators.String()
    opendaydrag = validators.Int()
    partner_email = EmailAddress()
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

    chained_validators = [SillyDescriptionChecksum()]

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
        self._generate_product_schema()
        #c.products = self.dbsession.query(Product).all()

    def _able_to_register(self):
        if c.signed_in_person and c.signed_in_person.registration:
            return False, "Thanks for your keenness, but you've already registered!"
        """ Dummy method until ceilings are integrated. Returns boolean and message/reason if you can't register (eg sold out) """
        return True, "You can register"

    def _able_to_edit(self):
        """ Dummy method until ceilings are integrated. Returns boolean and message/reason if you can't edit (eg already paid) """
        return True, "You can edit"

    def _generate_product_schema(self):
        class ProductSchema(BaseSchema):
            pass
        for category in c.product_categories:
            if category.display in ('radio', 'select'):
                # min/max can't be calculated on this form. You should only have 1 selected.
                ProductSchema.add_field('category_' + str(category.id), ProductInCategory(category=category, not_empty=True))
            elif category.display == 'checkbox':
                product_fields = []
                for product in category.products:
                    if product.is_available():
                        ProductSchema.add_field('product_' + str(product.id), validators.Bool(if_missing=False))
                        product_fields.append('product_' + str(product.id))
                ProductSchema.add_pre_validator(ProductMinMax(product_fields=product_fields, min_qty=category.min_qty, max_qty=category.max_qty, category_name=category.name))
            elif category.display == 'qty':
                # qty
                product_fields = []
                for product in category.products:
                    if product.is_available():
                        ProductSchema.add_field('product_' + str(product.id) + '_qty', BoundedInt())
                        product_fields.append('product_' + str(product.id) + '_qty')
                ProductSchema.add_pre_validator(ProductMinMax(product_fields=product_fields, min_qty=category.min_qty, max_qty=category.max_qty, category_name=category.name))
                # FIXME: I have spent far too long to try and get this working. Technically this should be a chained validator, not a pre validator but no matter what I do I can't get it to work (read heaps of docs etc etc). The result of being a pre-validator is that if there is an error the pre validator doesn't pick up (like an unfilled field) that the normal validation would pick up it isn't highlighted until the pre-validator doesn't find any errors. For example if you dont' select any shirts and have "asdf" in one of the dinner ticket fields you should see two errors: 1. you have no shirts and 2. tickets need to be integers. Once you select a shirt and resubmit the other error will show up. So it's a usability issue and doesn't make the form less secure, but damn this one is annoying!
        self.schemas['new'].add_field('products', ProductSchema)
        self.schemas['edit'].add_field('products', ProductSchema)

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
                #self.pay(c.registration.id, quiet=1)

                if c.signed_in_person:
                    redirect_to('/registration/status')
                return render_response('registration/thankyou.myt')
        return render_response("registration/new.myt",
                               defaults=defaults, errors=errors)

    def edit(self, id):
        able, response = self._able_to_edit()
        if not able:
            return response
        errors = {}
        defaults = dict(request.POST)

        current_schema = self.schemas['edit']

        if request.method == 'POST' and defaults:
            result, errors = current_schema.validate(defaults, self.dbsession)
            if not errors:
                self.save_details(result)

                self.dbsession.flush()

                self.obj = c.registration
                #self.pay(c.registration.id, quiet=1)

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
        self.dbsession.save_or_update(c.registration)

        # Always delete the current products
        for rego_product in c.registration.products:
            self.dbsession.delete(rego_product)

        # Store Product details
        for category in c.product_categories:
            if category.display in ('radio', 'select'):
                product = self.dbsession.query(model.Product).get(result['products']['category_' + str(category.id)])
                if product != None:
                    rego_product = model.RegistrationProduct()
                    rego_product.product = product
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
        c.ceilings = {}
        c.ceilings['conference'] = self.dbsession.query(model.Ceiling).filter_by(name='conference').one()
        c.ceilings['earlybird'] = self.dbsession.query(model.Ceiling).filter_by(name='earlybird').one()
        return render_response("registration/status.myt")

    def silly_description(self):
        desc, descChecksum = h.silly_description()
        return descChecksum + ',' + desc

    def pay(self, id, quiet=0):
        registration = self.obj
        if registration.person.invoices:
            for invoice in registration.person.invoices:
                if invoice.good_payments or invoice.bad_payments:
                    c.invoice = invoice
                    if quiet: return
                    return render_response('invoice/already.myt')
                else:
                    invoice.void = True

        invoice = model.Invoice()
        invoice.person = registration.person

        # Check for voucher
        #voucher_result, errors = self.check_voucher()

        for rproduct in registration.products:
            ii = model.InvoiceItem(description=rproduct.product.description, qty=rproduct.qty, cost=rproduct.product.cost)
            ii.product = rproduct.product
            self.dbsession.save(ii)
            invoice.items.append(ii)

        invoice.last_modification_timestamp = datetime.datetime.now()

        self.dbsession.save(invoice)
        self.dbsession.flush()

        if quiet: return
        redirect_to(controller='invoice', action='view', id=invoice.id)
