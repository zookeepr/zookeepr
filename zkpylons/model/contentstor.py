"""ContenStor Model"""

import formencode
from sqlalchemy import *

class FormSchema(formencode.schema.Schema):
    filter_extra_fields = True
    allow_extra_fields = True
        
    def validate(self, input):
        try :
            result = self.to_python(input)
            return result, {}
        except formencode.Invalid, e:
            return {}, e.unpack_errors()

def update(self, **kargs):
    for key in kargs.keys():
        if hasattr(kargs[key], 'value'):
            setattr(self, key, kargs[key].value)
        else:
            setattr(self, key, kargs[key])

def validate(self, input=None):
    validate_self = bool(input)
    if not input:
        keys = self._managed_attributes.keys()
        input = dict([(k, getattr(self, k)) for k in keys])
    newvals, errors = self._form_schema().validate(input)
    if validate_self:
        self.update(**newvals)
        self.errors = errors
        return errors
    else:
        return newvals, errors

def modelise(class_, table, form, **kwargs):
    #class._table = table
    class_._form_schema = form
    # Use assign_mapper to monkeypatch the classes with useful methods
    assign_mapper(class_, table, **kwargs)
    # monkeypatch a validator and updater method
    class_.validate = validate
    class_.update = update
    class_.errors = {}
