import formencode
from formencode.validators import *

from contentstor import FormSchema

class PersonSchema(FormSchema):
    handle = String(not_empty=True)
    email_address = String()
    password = String()

    firstname = String()
    lastname = String()
    phone = String()
    fax = String()

class SubmissionTypeSchema(FormSchema):
    name = String(maxlength=40)

class SubmissionSchema(FormSchema):
    title = String()
    abstract = String()
    submission_type = String()
    person = String()
    experience = String()
    url = String()
