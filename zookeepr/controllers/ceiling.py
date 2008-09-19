from formencode import validators, compound, variabledecode, ForEach
from formencode.schema import Schema

from zookeepr.lib.auth import SecureController, AuthRole
from zookeepr.lib.base import *
from zookeepr.lib.crud import Modify, View
from zookeepr.lib.validators import BaseSchema, BoundedInt, ProductValidator
from zookeepr.model import Ceiling, ProductCategory

class NotExistingCeilingValidator(validators.FancyValidator):
    def validate_python(self, value, state):
        ceiling = state.query(Ceiling).filter_by(name=value['name']).first()
        if ceiling != None and ceiling != c.ceiling:
           raise Invalid("Ceiling name already in use", value, state)

class CeilingSchema(BaseSchema):
    name = validators.String(not_empty=True)
    max_sold = BoundedInt(min=0)
    available_from = validators.DateConverter(month_style='dd/mm/yy')
    available_until = validators.DateConverter(month_style='dd/mm/yy')
    products = ForEach(ProductValidator())
    chained_validators = [NotExistingCeilingValidator()]

class NewCeilingSchema(BaseSchema):
    ceiling = CeilingSchema()
    pre_validators = [variabledecode.NestedVariables]

class EditCeilingSchema(BaseSchema):
    ceiling = CeilingSchema()
    pre_validators = [variabledecode.NestedVariables]

class CeilingController(SecureController, View, Modify):
    schemas = {"new" : NewCeilingSchema(),
               "edit" : EditCeilingSchema()}
    permissions = {"view": [AuthRole('organiser')],
                   "index": [AuthRole('organiser')],
                   "edit": [AuthRole('organiser')],
                   "delete": [AuthRole('organiser')],
                   "new": [AuthRole('organiser')],
                   }

    model = Ceiling
    individual = 'ceiling'
    redirect_map = dict(new=dict(action='index'))


    def __before__(self, **kwargs):
        c.product_categories = self.dbsession.query(ProductCategory).all()
        if hasattr(super(CeilingController, self), '__before__'):
            super(CeilingController, self).__before__(**kwargs)
