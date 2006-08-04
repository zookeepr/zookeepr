from formencode import validators, compound, schema, variabledecode

from zookeepr.lib.base import BaseController, c
from zookeepr.lib.crud import Modify, View
from zookeepr.lib.validators import BaseSchema
from zookeepr.models import Submission, SubmissionType

class SubmissionValidator(schema.Schema):
    title = validators.String()
    abstract = validators.String()
    experience = validators.String()

class NewSubmissionValidator(BaseSchema):
    submission = SubmissionValidator()
    pre_validators = [variabledecode.NestedVariables]

class EditSubmissionValidator(BaseSchema):
    submission = SubmissionValidator()
    pre_validators = [variabledecode.NestedVariables]

class SubmissionController(BaseController, View, Modify):
    validators = {"new" : NewSubmissionValidator(),
                  "edit" : EditSubmissionValidator()}

    model = Submission
    individual = 'submission'

    def edit(self, id):
        c.submission_types = self.objectstore.query(SubmissionType).select()
        return Modify.edit(self, id)
