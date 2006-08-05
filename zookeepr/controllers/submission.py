from formencode import validators, compound, schema, variabledecode

from zookeepr.lib.auth import SecureController
from zookeepr.lib.base import c
from zookeepr.lib.crud import Modify, View
from zookeepr.lib.validators import BaseSchema
from zookeepr.models import Submission, SubmissionType

class SubmissionSchema(schema.Schema):
    title = validators.String()
    abstract = validators.String()
    experience = validators.String()
    url = validators.String()
    submission_type_id = validators.Int()

class NewSubmissionSchema(BaseSchema):
    submission = SubmissionSchema()
    pre_validators = [variabledecode.NestedVariables]

class EditSubmissionSchema(BaseSchema):
    submission = SubmissionSchema()
    pre_validators = [variabledecode.NestedVariables]

class SubmissionController(SecureController, View, Modify):
    validators = {"new" : NewSubmissionSchema(),
                  "edit" : EditSubmissionSchema()}

    model = Submission
    individual = 'submission'

    def __before__(self, **kwargs):
        SecureController.__before__(self, **kwargs)
        
        c.submission_types = self.objectstore.query(SubmissionType).select()
