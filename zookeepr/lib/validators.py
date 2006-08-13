from formencode import Invalid, validators, schema
from sqlalchemy import create_session

from zookeepr.model import Person, SubmissionType

class BaseSchema(schema.Schema):
    allow_extra_fields = True
    filter_extra_fields = True

    def validate(self, input):
        try:
            result = self.to_python(input)
            return result, {}
        except Invalid, e:
            return {}, e.unpack_errors()


class PersonValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        return Person.get(value)


class SubmissionTypeValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        s = create_session()
        return s.query(SubmissionType).get(value)
