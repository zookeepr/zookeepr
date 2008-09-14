from formencode import validators, compound, variabledecode
from formencode.schema import Schema

from zookeepr.lib.auth import SecureController, AuthRole
from zookeepr.lib.base import *
from zookeepr.lib.crud import Modify, View
from zookeepr.lib.validators import BaseSchema, BoundedInt
from zookeepr.model import Product, ProductCategory

class ProductCategoryValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        return state.query(model.ProductCategory).get(value)

    def _from_python(self, value):
        return value.id

class ProductSchema(BaseSchema):
    category = ProductCategoryValidator()
    active = validators.Bool()
    description = validators.String(not_empty=True)
    cost = BoundedInt(min=0)
    auth = validators.String()
    validate = validators.String()

class NewProductSchema(BaseSchema):
    product = ProductSchema()
    pre_validators = [variabledecode.NestedVariables]

class EditProductSchema(BaseSchema):
    product = ProductSchema()
    pre_validators = [variabledecode.NestedVariables]

class ProductController(SecureController, View, Modify):
    schemas = {"new" : NewProductSchema(),
               "edit" : EditProductSchema()}
    permissions = {"view": [AuthRole('organiser')],
                   "index": [AuthRole('organiser')],
                   "edit": [AuthRole('organiser')],
                   "delete": [AuthRole('organiser')],
                   "new": [AuthRole('organiser')],
                   }

    model = Product
    individual = 'product'
    redirect_map = dict(new=dict(action='index'))

    def __before__(self, **kwargs):
        if hasattr(super(ProductController, self), '__before__'):
            super(ProductController, self).__before__(**kwargs)

        c.product_categories = self.dbsession.query(ProductCategory).all()
