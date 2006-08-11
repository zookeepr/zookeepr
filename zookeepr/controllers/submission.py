from formencode import validators, compound, schema, variabledecode

from zookeepr.lib.auth import BaseController
from zookeepr.lib.base import c
from zookeepr.lib.crud import Modify, View
from zookeepr.lib.validators import BaseSchema, SubmissionTypeValidator
from zookeepr.model import Submission, SubmissionType

class SubmissionSchema(schema.Schema):
    title = validators.String()
    abstract = validators.String()
    experience = validators.String()
    url = validators.String()
    type = SubmissionTypeValidator

class NewSubmissionSchema(BaseSchema):
    submission = SubmissionSchema()
    pre_validators = [variabledecode.NestedVariables]

class EditSubmissionSchema(BaseSchema):
    submission = SubmissionSchema()
    pre_validators = [variabledecode.NestedVariables]

class SubmissionController(BaseController, View, Modify):
    validators = {"new" : NewSubmissionSchema(),
                  "edit" : EditSubmissionSchema()}

    model = Submission
    individual = 'submission'

    def __before__(self, **kwargs):
        BaseController.__before__(self, **kwargs)
        
        c.submission_types = SubmissionType.select()
