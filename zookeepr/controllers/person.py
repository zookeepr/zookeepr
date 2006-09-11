from formencode import validators
from formencode.schema import Schema
from formencode.variabledecode import NestedVariables

from zookeepr.lib.auth import SecureController, AuthFunc
from zookeepr.lib.base import c, session
from zookeepr.lib.crud import View, Modify
from zookeepr.lib.validators import BaseSchema
from zookeepr.model import Person

class PersonSchema(Schema):
    password = validators.PlainText()
    password_confirm = validators.PlainText()    
    email_address = validators.Email()

    handle = validators.PlainText()
    phone = validators.String()
    fax = validators.String()
    firstname = validators.String()
    lastname = validators.String()

class NewPersonSchema(BaseSchema):
    person = PersonSchema()
    pre_validators = [NestedVariables]

class EditPersonSchema(BaseSchema):
    person = PersonSchema()
    pre_validators = [NestedVariables]

class PersonController(SecureController, View, Modify):
    schemas = {"new" : NewPersonSchema(),
               "edit" : EditPersonSchema()}
    permissions = {"view": [],
                   "new": [],
                   "edit": [],
                   "delete": [],
                   "index": [],
                   }

    model = Person
    individual = 'person'
    key = 'handle'

    def is_same_person(self):
        return c.person.id == session['signed_in_person_id']
