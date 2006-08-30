import cgi

from formencode import Invalid, validators, schema
from sqlalchemy import create_session

from zookeepr.model import Person, ProposalType

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


class ProposalTypeValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        s = create_session()
        return s.query(ProposalType).get(value)


class FileUploadValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        if isinstance(value, cgi.FieldStorage):
            filename = value.filename
            content = buffer(value.value)
        elif isinstance(value, str):
            filename = None
            content = buffer(value)
        return dict(filename=filename,
                    content=content)
