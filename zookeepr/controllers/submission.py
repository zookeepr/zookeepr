from formencode import validators, compound, schema, variabledecode

from zookeepr.lib.auth import SecureController, AuthFunc, AuthTrue, AuthFalse
from zookeepr.lib.base import c, g, redirect_to, request, render_response
from zookeepr.lib.crud import Modify, View
from zookeepr.lib.validators import BaseSchema, PersonValidator, SubmissionTypeValidator
from zookeepr.model import Submission, SubmissionType

class SubmissionSchema(schema.Schema):
    title = validators.String()
    abstract = validators.String()
    experience = validators.String()
    url = validators.String()
    type = SubmissionTypeValidator()
    #person_id = 

class NewSubmissionSchema(BaseSchema):
    submission = SubmissionSchema()
    pre_validators = [variabledecode.NestedVariables]

class EditSubmissionSchema(BaseSchema):
    submission = SubmissionSchema()
    pre_validators = [variabledecode.NestedVariables]

class SubmissionController(SecureController, View, Modify):
    model = Submission
    individual = 'submission'

    schemas = {"new" : NewSubmissionSchema(),
               "edit" : EditSubmissionSchema()}
    permissions = {"edit": [AuthFunc('is_submitter')],
                   "view": [AuthFunc('is_submitter')],
                   "delete": [AuthFunc('is_submitter')],
                   "index": [],
                   }

    def __before__(self, **kwargs):
        super(SubmissionController, self).__before__(**kwargs)

        c.submission_types = g.objectstore.query(SubmissionType).select()

    def new(self, id):
        self.obj = self.model()
        errors = {}
        defaults = dict(request.POST)
        if defaults:
            result, errors = self.schemas['new'].validate(defaults)

            if not errors:
                for k in result['submission']:
                    setattr(self.obj, k, result['submission'][k])

                self.obj.people.append(c.person)

                g.objectstore.save(self.obj)
                g.objectstore.flush()

                redirect_to(action='view', id=self.obj.id)

        c.submission = self.obj

        good_errors = {}
        for key in errors.keys():
            try:
                for subkey in errors[key].keys():
                    good_errors[key + "." + subkey] = errors[key][subkey]
            except AttributeError:
                good_errors[key] = errors[key]

        return render_response('submission/new.myt', defaults=defaults, errors=good_errors)

    def is_submitter(self):
        return c.person in self.obj.people
