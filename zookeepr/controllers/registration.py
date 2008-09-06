import datetime
import md5
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
    editor = validators.String()
    distro = validators.String()
    silly_description = validators.String()
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

class NewRegistrationSchema(BaseSchema):
    person = PersonSchema()
    registration = RegisterSchema()
    pre_validators = [variabledecode.NestedVariables]

class UpdateRegistrationSchema(BaseSchema):
    person = ExistingPersonSchema()
    registration = RegisterSchema()
    pre_validators = [variabledecode.NestedVariables]

class RegistrationController(SecureController, Update, Read):
    individual = 'registration'
    model = model.Registration
    schemas = {'new': NewRegistrationSchema(),
               'edit': UpdateRegistrationSchema()
            }
    permissions = {'new': True,
                   'edit': [AuthRole('organiser'), AuthFunc('is_same_person')],
                   'view': [AuthRole('organiser'), AuthFunc('is_same_person')],
                   'status': True
               }

    def __before__(self, **kwargs):
        super(RegistrationController, self).__before__(**kwargs)
        c.product_categories = self.dbsession.query(ProductCategory).all()
        self._generate_product_schema()
        #c.products = self.dbsession.query(Product).all()

    def _able_to_register(self):
        """ Dummy method until ceilings are integrated. Returns boolean and message/reason if you can't register (eg sold out) """
        return True, "You can register"

    def _able_to_edit(self):
        """ Dummy method until ceilings are integrated. Returns boolean and message/reason if you can't edit (eg already paid) """
        return True, "You can edit"

    def _generate_product_schema(self):
        class ProductSchema(BaseSchema):
            pass
        for category in c.product_categories:
            if category.display == 'radio':
                # min/max can't be calculated on this form. You should only have 1 selected.
                ProductSchema.add_field('category_' + str(category.id), BoundedInt())
            elif category.display == 'options':
                product_fields = []
                for product in category.products:
                    ProductSchema.add_field('product_' + str(product.id), validators.Bool(if_missing=False))
                    product_fields.append('options' + str(category.id) + '_product_' + str(product.id))
                ProductSchema.add_pre_validator(ProductMinMax(product_fields=product_fields, min_qty=category.min_qty, max_qty=category.max_qty, category_name=category.name))
            elif category.display == 'qty':
                # qty
                product_fields = []
                for product in category.products:
                    ProductSchema.add_field('qty' + str(category.id) + '_product_' + str(product.id), BoundedInt())
                    product_fields.append('qty' + str(category.id) + '_product_' + str(product.id))
                ProductSchema.add_pre_validator(ProductMinMax(product_fields=product_fields, min_qty=category.min_qty, max_qty=category.max_qty, category_name=category.name))
                # FIXME: I have spent far too long to try and get this working. Technically this should be a chained validator, not a pre validator but no matter what I do I can't get it to work (read heaps of docs etc etc). The result of being a pre-validator is that if there is an error the pre validator doesn't pick up (like an unfilled field) that the normal validation would pick up it isn't highlighted until the pre-validator doesn't find any errors. For example if you dont' select any shirts and have "asdf" in one of the dinner ticket fields you should see two errors: 1. you have no shirts and 2. tickets need to be integers. Once you select a shirt and resubmit the other error will show up. So it's a usability issue and doesn't make the form less secure, but damn this one is annoying!
        self.schemas['new'].add_field('products', ProductSchema)
        self.schemas['edit'].add_field('products', ProductSchema)

    def is_same_person(self):
        return c.signed_in_person == c.registration.person

    def new(self, id):
        able, response = self._able_to_register()
        if not able:
            return response
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
            setattr(c.registration, k, result['registration'][k])
        self.dbsession.save_or_update(c.registration)

        for rego_product in c.registration.products:
            self.dbsession.delete(rego_product)

        # Store Product details
        for category in c.product_categories:
            if category.display == 'radio':
                product = self.dbsession.query(model.Product).get(result['products']['category_' + str(category.id)])
                if product != None:
                    rego_product = model.RegistrationProduct()
                    rego_product.product = product
                    rego_product.qty = 1
                    self.dbsession.save(rego_product)
                    c.registration.products.append(rego_product)
                else:
                    raise Exception
            elif category.display == 'options':
                for product in category.products:
                    if result['products']['options' + str(category.id) + '_product_' + str(product.id)] == True:
                        rego_product = model.RegistrationProduct()
                        rego_product.product = product
                        rego_product.qty = 1
                        self.dbsession.save(rego_product)
                        c.registration.products.append(rego_product)
            elif category.display == 'qty':
                for product in category.products:
                    if result['products']['qty' + str(category.id) + '_product_' + str(product.id)] not in [0, None]:
                        rego_product = model.RegistrationProduct()
                        rego_product.product = product
                        rego_product.qty = result['products']['qty' + str(category.id) + '_product_' + str(product.id)]
                        self.dbsession.save(rego_product)
                        c.registration.products.append(rego_product)

        # Check whether we're already signed in or not, and store person details
        if not c.signed_in_person:
            c.person = model.Person()
            for k in result['person']:
                setattr(c.person, k, result['person'][k])

            self.dbsession.save(c.person)
        else:
            c.person = c.signed_in_person




    def status(self):
        c.ceilings = {}
        c.ceilings['conference'] = self.dbsession.query(model.Ceiling).filter_by(name='conference').one()
        c.ceilings['earlybird'] = self.dbsession.query(model.Ceiling).filter_by(name='earlybird').one()
        return render_response("registration/status.myt")
