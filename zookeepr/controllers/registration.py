import datetime
import md5
import warnings

from formencode import validators, compound, variabledecode, schema
from formencode.schema import Schema

from zookeepr.lib.auth import *
from zookeepr.lib.base import *
from zookeepr.lib.crud import *
from zookeepr.lib.mail import *
from zookeepr.lib.validators import BaseSchema, BoundedInt, EmailAddress, DictSet

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
        product_dict = {}
        #for category in c.product_categories:
        #    for product in category.products:
        #        if category.display == 'qty':
        #            product_dict[category.name][product.id] = validators.Int()

    def is_same_person(self):
        return c.signed_in_person == c.registration.person

    def new(self, id):
        able, response = self._able_to_register()
        if not able:
            return response
        errors = {}
        defaults = dict(request.POST)

        if c.signed_in_person:
            schema = self.schemas['edit']
        else:
            schema = self.schemas['new']

        if request.method == 'POST' and defaults:
            result, errors = schema.validate(defaults, self.dbsession)
            if not errors:
                c.registration = model.Registration()
                for k in result['registration']:
                    setattr(c.registration, k, result['registration'][k])
                self.dbsession.save(c.registration)

                if not c.signed_in_person:
                    c.person = model.Person()
                    for k in result['person']:
                        setattr(c.person, k, result['person'][k])

                    self.dbsession.save(c.person)
                else:
                    c.person = c.signed_in_person

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
        registration = self.obj
        # FIXME: Add here the check for paid invoices
        #if registration.person.invoices:
        #    if registration.person.invoices[0].good_payments or registration.person.invoices[0].bad_payments:
        #        c.invoice = registration.person.invoices[0]
        #        return render_response('invoice/already.myt')

        #try:
        return super(RegistrationController, self).edit(id)
        #finally:
        #    try:
        #        self.pay(id, quiet=1) #regenerate the invoice
        #    except:
        #        self.pay(id, quiet=1) #retry once

