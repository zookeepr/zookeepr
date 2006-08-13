from formencode import validators, compound, schema, variabledecode

from zookeepr.lib.auth import SecureController, AuthFunc, AuthTrue, AuthFalse
from zookeepr.lib.base import c
from zookeepr.lib.crud import Modify, View
from zookeepr.lib.validators import BaseSchema, PersonValidator, SubmissionTypeValidator
from zookeepr.model import Submission, SubmissionType

class SubmissionSchema(schema.Schema):
    title = validators.String()
    abstract = validators.String()
    experience = validators.String()
    url = validators.String()
    type = SubmissionTypeValidator
    #person_id = validators.Int()

class NewSubmissionSchema(BaseSchema):
    submission = SubmissionSchema()
    pre_validators = [variabledecode.NestedVariables]

class EditSubmissionSchema(BaseSchema):
    submission = SubmissionSchema()
    pre_validators = [variabledecode.NestedVariables]

class SubmissionController(SecureController, View, Modify):
    schemas = {"new" : NewSubmissionSchema(),
               "edit" : EditSubmissionSchema()}
    permissions = {"edit": [AuthFunc('is_submitter')],
                   "view": [AuthFunc('is_submitter')],
                   "delete": [AuthFunc('is_submitter')],
                   "index": [],
                   }

    model = Submission
    individual = 'submission'

    def __before__(self, **kwargs):
        super(SubmissionController, self).__before__(**kwargs)
        
        c.submission_types = SubmissionType.select()

    def is_submitter(self):
        return c.person in c.submission.people
