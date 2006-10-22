from formencode import validators, compound, variabledecode
from formencode.schema import Schema

from zookeepr.lib.auth import SecureController, AuthRole
from zookeepr.lib.base import *
from zookeepr.lib.crud import Create
from zookeepr.lib.validators import BaseSchema

class RegistrationSchema(Schema):
    rego_type = validators.String()
    miniconfs = validators.String()
    dinner_tickets = validators.Int()
    diet = validators.String()
    tee_size = validators.String()
    open_day_visitors = validators.Int()

    address1 = validators.String()
    address2 = validators.String()
    city = validators.String()
    state = validators.String()
    country = validators.String()
    postcode = validators.String()

    shell = validators.String()
    editor = validators.String()
    distro = validators.String()

    prev_lca = validators.String()
    keysigning = validators.StringBoolean()

    partner = validators.StringBoolean()
    partner_email = validators.String()
    children_0_3 = validators.Int()
    children_4_6 = validators.Int()
    children_7_9 = validators.Int()
    children_10 = validators.Int()

    accommodation = validators.String()
    accommodation_start = validators.String()
    accommodation_end = validators.String()

    la_membership = validators.StringBoolean()
    lca_announce_list = validators.StringBoolean()
    lca_attendees_list = validators.StringBoolean()

    discount_code = validators.String()

class PersonSchema(Schema):
    email_address = validators.String()
    password = validators.String()
    password_confirm = validators.String()
    fullname = validators.String()
    handle = validators.String()
    
class NewRegistrationSchema(BaseSchema):
    person = PersonSchema()
    registration = RegistrationSchema()

    pre_validators = [variabledecode.NestedVariables]
    
class RegistrationController(BaseController, Create):
    individual = 'registration'
    model = model.Registration
    schemas = {'new': NewRegistrationSchema(),
               }
