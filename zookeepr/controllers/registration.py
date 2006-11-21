import smtplib
import warnings

from formencode import validators, compound, variabledecode
from formencode.schema import Schema

from zookeepr.lib.auth import *
from zookeepr.lib.base import *
from zookeepr.lib.crud import *
from zookeepr.lib.validators import BaseSchema, EmailAddress

class DictSet(validators.Set):
    def _from_python(self, value):
        value = super(DictSet, self)._from_python(value, state)
        return dict(zip(value, [1]*len(value)))
        
    def _to_python(self, value, state):
        value = value.keys()
        return super(DictSet, self)._to_python(value, state)


# FIXME: merge with account.py controller and move to validators
class NotExistingAccountValidator(validators.FancyValidator):
    def validate_python(self, value, state):
        account = state.query(model.Person).get_by(email_address=value['email_address'])
        if account is not None:
            raise Invalid("This account already exists.  Please try signing in first.  Thanks!", value, state)

        account = state.query(model.Person).get_by(handle=value['handle'])
        if account is not None:
            raise Invalid("This display name has been taken, sorry.  Please use another.", value, state)

class NotExistingRegistrationValidator(validators.FancyValidator):
    def validate_python(self, value, state):
        rego = None
        if 'signed_in_person_id' in session:
            rego = state.query(model.Registration).get_by(person_id=session['signed_in_person_id'])
        if rego is not None:
            raise Invalid("Thanks for your keenness, but you've already registered!", value, state)


class AccommodationValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        if value == 'own':
            return None
        return state.query(model.Accommodation).get(value)

    def _from_python(self, value):
        return value.id


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

    prevlca = DictSet(if_missing=None)

    type = validators.String(not_empty=True)
    discount_code = validators.String()

    teesize = validators.String(not_empty=True)
    dinner = validators.Int()
    diet = validators.String()
    special = validators.String()
    miniconf = DictSet(if_missing=None)
    opendaydrag = validators.Int()

    partner_email = EmailAddress(resolve_domain=True)
    kids_0_3 = validators.Int()
    kids_4_6 = validators.Int()
    kids_7_9 = validators.Int()
    kids_10 = validators.Int()

    accommodation = AccommodationValidator()
    
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

    chained_validators = [NotExistingAccountValidator(), validators.FieldsMatch('password', 'password_confirm')]


class NewRegistrationSchema(BaseSchema):
    person = PersonSchema()
    registration = RegistrationSchema()

    chained_validators = [NotExistingRegistrationValidator()]
    pre_validators = [variabledecode.NestedVariables]


class ExistingPersonRegoSchema(BaseSchema):
    registration = RegistrationSchema()

    chained_validators = [NotExistingRegistrationValidator()]
    pre_validators = [variabledecode.NestedVariables]


class EditRegistrationSchema(BaseSchema):
    registration = RegistrationSchema()

    #chained_validators = [NotExistingRegistrationValidator()]
    pre_validators = [variabledecode.NestedVariables]


class RegistrationController(BaseController, Create, Update):
    individual = 'registration'
    model = model.Registration
    schemas = {'new': NewRegistrationSchema(),
               'edit': EditRegistrationSchema(),
               }
    permissions = {'edit': [AuthFunc('is_same_person')],
                   }
    redirect_map = {'edit': dict(controller='/profile', action='index'),
                    }

    def is_same_person(self):
        c.signed_in_person == c.registration.person

    def __before__(self, **kwargs):
        if hasattr(super(RegistrationController, self), '__before__'):
            super(RegistrationController, self).__before__(**kwargs)

        if 'signed_in_person_id' in session:
            c.signed_in_person = self.dbsession.query(model.Person).get_by(id=session['signed_in_person_id'])

        as = self.dbsession.query(model.Accommodation).select()
        c.accommodation_collection = filter(lambda a: a.get_available_beds() >= 1, as)

    def new(self):
        errors = {}
        defaults = dict(request.POST)

        if defaults:
            if c.signed_in_person:
                results, errors = ExistingPersonRegoSchema().validate(defaults, self.dbsession)
            else:
                results, errors = NewRegistrationSchema().validate(defaults, self.dbsession)

            if errors: #FIXME: make this only print if debug enabled
                if request.environ['paste.config']['app_conf'].get('debug'):
                    warnings.warn("form validation failed: %s" % errors)
            else:
                c.registration = model.Registration()
                for k in results['registration']:
                    setattr(c.registration, k, results['registration'][k])
                self.dbsession.save(c.registration)

                if not c.signed_in_person:
                    c.person = model.Person()
                    for k in results['person']:
                        setattr(c.person, k, results['person'][k])

                    self.dbsession.save(c.person)
                else:
                    c.person = c.signed_in_person

                c.registration.person = c.person
                self.dbsession.flush()

                s = smtplib.SMTP("localhost")
                body = render('registration/response.myt', id=c.person.url_hash, fragment=True)
                s.sendmail("seven-contact@lca2007.linux.org.au", c.person.email_address, body)
                s.quit()
                
                return render_response('registration/thankyou.myt')

        return render_response("registration/new.myt", defaults=defaults, errors=errors)
