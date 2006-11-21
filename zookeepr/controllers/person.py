# from formencode import validators
# from formencode.schema import Schema
# from formencode.variabledecode import NestedVariables

# from zookeepr.lib.auth import *
# from zookeepr.lib.base import *
# from zookeepr.lib.crud import *
# from zookeepr.lib.validators import BaseSchema
# from zookeepr.model import Person

# class PersonSchema(Schema):
#     password = validators.PlainText()
#     password_confirm = validators.PlainText()    
#     email_address = validators.Email()

#     handle = validators.PlainText()
#     phone = validators.String()
#     fax = validators.String()
#     firstname = validators.String()
#     lastname = validators.String()

# class NewPersonSchema(BaseSchema):
#     person = PersonSchema()
#     pre_validators = [NestedVariables]

# class EditPersonSchema(BaseSchema):
#     person = PersonSchema()
#     pre_validators = [NestedVariables]

# class PersonController(SecureController, Update):
#     schemas = {#"new" : NewPersonSchema(),
#                "edit" : EditPersonSchema()}
#     permissions = {#"view": [],
#                    #"new": [],
#                    "edit": [AuthFunc('is_same_person')],
#                    #"delete": [],
#                    #"index": [],
#                    }

#     model = Person
#     individual = 'person'

#     def is_same_person(self):
#         return c.person == c.signed_in_person
