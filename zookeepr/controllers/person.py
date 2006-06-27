from formencode import validators, compound, schema, variabledecode

from zookeepr.lib.base import BaseController
from zookeepr.lib.crud import View, Modify
from zookeepr.models import Person
from zookeepr.lib.validators import Strip

class PersonValidator(schema.Schema):
    password = validators.PlainText()
    password_confirm = validators.PlainText()    
    email_address = validators.Email()

    handle = validators.PlainText()
    phone = validators.String()
    fax = validators.String()
    firstname = validators.String()
    lastname = validators.String()

class NewPersonValidator(schema.Schema):
    person = PersonValidator()
    pre_validators = [Strip("commit"), variabledecode.NestedVariables]

class EditPersonValidator(schema.Schema):
    person = PersonValidator()
    pre_validators = [Strip('commit'), variabledecode.NestedVariables]

class PersonController(BaseController, View, Modify):
    validator = {"new" : NewPersonValidator(),
                 "edit" : EditPersonValidator()}

    model = Person
    individual = 'person'
    key = 'handle'
