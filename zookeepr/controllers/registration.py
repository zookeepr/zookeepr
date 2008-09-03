import datetime
import md5
import warnings

from formencode import validators, compound, variabledecode, schema
from formencode.schema import Schema

from zookeepr.lib.auth import *
from zookeepr.lib.base import *
from zookeepr.lib.crud import *
from zookeepr.lib.mail import *
from zookeepr.lib.validators import BaseSchema, BoundedInt, EmailAddress

from zookeepr.controllers.person import PersonSchema
from zookeepr.model.billing import ProductCategory, Product
from zookeepr.model.registration import Registration

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
    checkin = validators.Int()
    checkout = validators.Int()
    lasignup = validators.Bool()
    announcesignup = validators.Bool()
    delegatesignup = validators.Bool()
    speaker_record = validators.Bool()
    speaker_video_release = validators.Bool()
    speaker_side_release = validators.Bool()
    prevlca = validators.String()
    miniconf = validators.String()

class NewRegistrationSchema(BaseSchema):
    person = PersonSchema()
    registration = RegisterSchema()
    pre_validators = [variabledecode.NestedVariables]

class RegistrationController(SecureController):
    individual = 'registration'
    model = model.Registration
    schemas = {'new': NewRegistrationSchema()
              }
    permissions = {'new': True,
               }

    def __before__(self, **kwargs):
        super(RegistrationController, self).__before__(**kwargs)
        c.product_categories = self.dbsession.query(ProductCategory).all()
        c.products = self.dbsession.query(Product).all()

    def _able_to_register(self):
        """ Dummy method until ceilings are integrated """
        return True
        
    def _registrations_closed(self):
        """ Dummy method until ceilings are integrated (will display whether or not regos are closed and the reason why (eg sold out). """
        return "Registrations are closed. (Sold out?)"

    def new(self, id):
        if self._able_to_register() is not True:
            return self._registrations_closed()
        errors = {}
        defaults = dict(request.POST)

        if request.method == 'POST' and defaults:
            result, errors = NewRegistrationSchema().validate(defaults, self.dbsession)
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
                self.pay(c.registration.id, quiet=1)

                if c.signed_in_person:
                    redirect_to('/registration/status')
                return render_response('registration/thankyou.myt')
        return render_response("registration/new.myt",
                           defaults=defaults, errors=errors)
