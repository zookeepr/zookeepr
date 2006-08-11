from formencode import Invalid, validators, schema

from zookeepr.model import SubmissionType

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
        return SubmissionType.get(value)
