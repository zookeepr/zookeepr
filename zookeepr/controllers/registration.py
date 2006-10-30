import smtplib
import warnings

from formencode import validators, compound, variabledecode
from formencode.schema import Schema

from zookeepr.lib.auth import SecureController, AuthRole
from zookeepr.lib.base import *
from zookeepr.lib.crud import Create
from zookeepr.lib.validators import BaseSchema, EmailAddress

class RegistrationSchema(Schema):
    address1 = validators.String(not_empty=True)
    address2 = validators.String()
    city = validators.String(not_empty=True)
    state = validators.String()
    country = validators.String(not_empty=True)
    postcode = validators.String(not_empty=True)

    phone = validators.String()
    
    company = validators.String()

    shell = validators.String()
    shelltext = validators.String()
    editor = validators.String()
    editortext = validators.String()
    distro = validators.String()
    distrotext = validators.String()
    silly_description = validators.String()

    prevlca = validators.Set(if_missing=None)

    type = validators.String(not_empty=True)
    discount_code = validators.String()

    teesize = validators.String(not_empty=True)
    dinner = validators.Int()
    diet = validators.String()
    special = validators.String()
    miniconf = validators.Set(if_missing=None)
    opendaydrag = validators.Int()

    partner_email = EmailAddress(resolve_domain=True)
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
    email_address = EmailAddress(resolve_domain=True, not_empty=True)
    password = validators.String(not_empty=True)
    password_confirm = validators.String(not_empty=True)
    fullname = validators.String(not_empty=True)
    handle = validators.String(not_empty=True)
    pre_validators = [validators.FieldsMatch('password', 'password_confirm')]
    
class NewRegistrationSchema(BaseSchema):
    person = PersonSchema()
    registration = RegistrationSchema()

    pre_validators = [variabledecode.NestedVariables]

class ExistingPersonRegoSchema(BaseSchema):
    registration = RegistrationSchema()

    pre_validators = [variabledecode.NestedVariables]


class RegistrationController(BaseController, Create):
    individual = 'registration'
    model = model.Registration
    schemas = {'new': NewRegistrationSchema(),
               }

    def __before__(self):
        if hasattr(super(RegistrationController, self), '__before__'):
            super(RegistrationController, self).__before__()

        if 'signed_in_person_id' in session:
            c.signed_in_person = Query(model.Person).get_by(id=session['signed_in_person_id'])


    def new(self):

        errors = {}
        defaults = dict(request.POST)

        if defaults:
            if c.signed_in_person:
                results, errors = ExistingPersonRegoSchema().validate(defaults)
            else:
                results, errors = NewRegistrationSchema().validate(defaults)

            if errors: #FIXME: make this only print if debug enabled
                if request.environ['paste.config']['app_conf'].get('debug'):
                    warnings.warn("form validation failed: %s" % errors)
            else:
                c.registration = model.Registration()
                for k in results['registration']:
                    setattr(c.registration, k, results['registration'][k])
                objectstore.save(c.registration)

                if not c.signed_in_person:
                    c.person = model.Person()
                    for k in results['person']:
                        setattr(c.person, k, results['person'][k])

                    objectstore.save(c.person)
                else:
                    c.person = c.signed_in_person

                c.registration.person = c.person
                objectstore.flush()

                s = smtplib.SMTP("localhost")
                body = render('registration/response.myt', id=c.person.url_hash, fragment=True)
                s.sendmail("seven-contact@lca2007.linux.org.au", c.person.email_address, body)
                s.quit()
                
                return render_response('registration/thankyou.myt')

        return render_response("registration/new.myt", defaults=defaults, errors=errors)

