import formencode
from formencode.validators import *

from contentstor import FormSchema

class PersonSchema(FormSchema):
    handle = PlainText(not_empty=True)
    email_address = String()
    password = String()
    password_confirm = String()
    
    firstname = String(maxlength=1024)
    lastname = String(maxlength=1024)
    phone = String(maxlength=32)
    fax = String(maxlength=32)

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
    url = URL()
    attachment = FieldStorageUploadConverter()
    
class RoleSchema(FormSchema):
    name = String()
