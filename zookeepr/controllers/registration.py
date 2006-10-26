import warnings

from formencode import validators, compound, variabledecode
from formencode.schema import Schema

from zookeepr.lib.auth import SecureController, AuthRole
from zookeepr.lib.base import *
from zookeepr.lib.crud import Create
from zookeepr.lib.validators import BaseSchema

class RegistrationSchema(Schema):
    address1 = validators.String(not_empty=True)
    address2 = validators.String()
    city = validators.String(not_empty=True)
    state = validators.String()
    country = validators.String(not_empty=True)
    postcode = validators.String(not_empty=True)

    company = validators.String()

    shell = validators.String()
    shelltext = validators.String()
    editor = validators.String()
    editortext = validators.String()
    distro = validators.String()
    distrotext = validators.String()

    prevlca = validators.Set(if_missing=None)

    type = validators.String(not_empty=True)
    discount_code = validators.String()

    teesize = validators.String(not_empty=True)
    dinner = validators.Int()
    diet = validators.String()
    special = validators.String()
    miniconf = validators.Set(if_missing=None)
    opendaydrag = validators.Int()

    partner_email = validators.String()
    kids_0_3 = validators.Int()
    kids_4_6 = validators.Int()
    kids_7_9 = validators.Int()
    kids_10 = validators.Int()

    accommodation = validators.String()
    checkin = validators.Int()
    checkout = validators.Int()

    lasignup = validators.Bool()
    announcesignup = validators.Bool()
    delegatesignup = validators.Bool()

class PersonSchema(Schema):
    email_address = validators.String(not_empty=True)
    password = validators.String(not_empty=True)
    password_confirm = validators.String(not_empty=True)
    fullname = validators.String(not_empty=True)
    handle = validators.String(not_empty=True)
    pre_validators = [validators.FieldsMatch('password', 'password_confirm')]
    
class NewRegistrationSchema(BaseSchema):
    person = PersonSchema()
    registration = RegistrationSchema()

    pre_validators = [variabledecode.NestedVariables]
    
class RegistrationController(BaseController, Create):
    individual = 'registration'
    model = model.Registration
    schemas = {'new': NewRegistrationSchema(),
               }

    def new(self):

        errors = {}
        defaults = dict(request.POST)

        print "d", defaults

        if defaults:
            results, errors = NewRegistrationSchema().validate(defaults)

            print "r, e", results, errors

            if errors:
                warnings.warn("form validation failed: %s" % errors)
            else:
                c.registration = model.Registration()
                c.person = model.Person()
                for k in results['person']:
                    setattr(c.person, k, results['person'][k])
                for k in results['registration']:
                    setattr(c.registration, k, results['registration'][k])

                c.registration.person = c.person

        return render_response("registration/new.myt", defaults=defaults, errors=errors)

