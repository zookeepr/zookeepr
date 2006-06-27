from formencode.schema import Schema
from formencode import Invalid

class BaseSchema(Schema):
    allow_extra_fields = True
    filter_extra_fields = True

    def validate(self, input):
        try:
            result = self.to_python(input)
            return result, {}
        except Invalid, e:
            return {}, e.unpack_errors()
