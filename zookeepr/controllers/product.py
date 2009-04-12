import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill
from formencode.variabledecode import NestedVariables

from zookeepr.lib.base import BaseController, render
from zookeepr.lib.validators import BaseSchema, ProductCategoryValidator
import zookeepr.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zookeepr.model import meta
from zookeepr.model.product import Product

from zookeepr.config.lca_info import lca_info

log = logging.getLogger(__name__)

class ProductSchema(BaseSchema):
    category = ProductCategoryValidator()
    active = validators.Bool()
    description = validators.String(not_empty=True)
    cost = BoundedInt(min=0)
    auth = validators.String(if_empty=None)
    validate = validators.String(if_empty=None)

class NewProductSchema(BaseSchema):
    product = ProductSchema()
    pre_validators = [NestedVariables]

class EditProductSchema(BaseSchema):
    product = ProductSchema()
    pre_validators = [NestedVariables]

class ProductController(BaseController):
    permissions = {"view": [AuthRole('organiser')],
                   "index": [AuthRole('organiser')],
                   "edit": [AuthRole('organiser')],
                   "delete": [AuthRole('organiser')],
                   "new": [AuthRole('organiser')],
                   }

    model = Product
    individual = 'product'
    redirect_map = dict(new=dict(action='index'))

    @authorize(h.auth.has_organiser_role)
    def __before__(self, **kwargs):
        c.product_categories = self.dbsession.query(ProductCategory).all()
        c.ceilings = self.dbsession.query(Ceiling).all()
        if hasattr(super(ProductController, self), '__before__'):
            super(ProductController, self).__before__(**kwargs)

    
