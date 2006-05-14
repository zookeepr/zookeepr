import formencode
from formencode.validators import *

from contentstor import FormSchema

class PersonSchema(FormSchema):
    handle = PlainText(not_empty=True)
    email_address = String()
    password = String()
    password_confirm = String()
    
    firstname = String()
    lastname = String()
    phone = String()
    fax = String()

    chained_validators = [
        FieldsMatch('password', 'password_confirm')
        ]

class SubmissionTypeSchema(FormSchema):
    name = String(maxlength=40)

class SubmissionSchema(FormSchema):
    title = String()
    abstract = String()
    submission_type = String()
    person = String()
    experience = String()
    url = String()
