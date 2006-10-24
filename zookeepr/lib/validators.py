import cgi

from formencode import Invalid, validators, schema
from sqlalchemy import Query

from zookeepr.model import Person, ProposalType, Stream

class BaseSchema(schema.Schema):
    allow_extra_fields = True
    filter_extra_fields = True

    def validate(self, input):
        try:
            result = self.to_python(input)
            return result, {}
        except Invalid, e:
            errors = e.unpack_errors()
            # e.unpack_errors() doesn't necessarily return a nice dictionary
            # for formfill to use, so re-mangle it
            good_errors = {}
            try:
                for key in errors.keys():
                    try:
                        for subkey in errors[key].keys():
                            good_errors[key + "." + subkey] = errors[key][subkey]
                    except AttributeError:
                        good_errors[key] = errors[key]
            except AttributeError:
                good_errors['x'] = errors
                
            return {}, good_errors


class PersonValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        return Person.get(value)


class ProposalTypeValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        return Query(ProposalType).get(value)


class FileUploadValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        if isinstance(value, cgi.FieldStorage):
            filename = value.filename
            content = value.value
        elif isinstance(value, str):
            filename = None
            content = value
        return dict(filename=filename,
                    content=content)


class StreamValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        return Query(Stream).get(value)


class ReviewSchema(schema.Schema):
    familiarity = validators.Int()
    technical = validators.Int()
    experience = validators.Int()
    coolness = validators.Int()
    stream = StreamValidator()
    comment = validators.String()
