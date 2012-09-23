import logging

from pylons import request, response, session, tmpl_context as c
from zkpylons.lib.helpers import redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill, ForEach
from formencode.variabledecode import NestedVariables

from zkpylons.lib.base import BaseController, render
from zkpylons.lib.ssl_requirement import enforce_ssl
from zkpylons.lib.validators import BaseSchema, ProductCategoryValidator, CeilingValidator
import zkpylons.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zkpylons.model import meta
from zkpylons.model.ceiling import Ceiling
from zkpylons.model.product import Product, ProductInclude
from zkpylons.model.product_category import ProductCategory

from zkpylons.config.lca_info import lca_info

log = logging.getLogger(__name__)

class ProductSchema(BaseSchema):
    category = ProductCategoryValidator()
    display_order = validators.Int(not_empty=True)
    active = validators.Bool()
    description = validators.String(not_empty=True)
    cost = validators.Int(min=0, max=20000000)
    auth = validators.String(if_empty=None)
    validate = validators.String(if_empty=None)
    ceilings = ForEach(CeilingValidator())

class NewProductSchema(BaseSchema):
    product = ProductSchema()
    pre_validators = [NestedVariables]

class EditProductSchema(BaseSchema):
    product = ProductSchema()
    pre_validators = [NestedVariables]

class ProductController(BaseController):

    @enforce_ssl(required_all=True)
    @authorize(h.auth.has_organiser_role)
    def __before__(self, **kwargs):
        c.product_categories = ProductCategory.find_all()
        c.ceilings = Ceiling.find_all()

    @dispatch_on(POST="_new") 
    def new(self, cat_id=None):
        form=render('/product/new.mako')
        if cat_id is None:
            return form
        else:
            return htmlfill.render(form, {
                'product.category': cat_id,
                'product.category_id': cat_id})

    @validate(schema=NewProductSchema(), form='new', post_only=True, on_get=True, variable_decode=True)
    def _new(self):
        results = self.form_result['product']

        c.product = Product(**results)
        meta.Session.add(c.product)
        meta.Session.commit()

        h.flash("Product created")
        redirect_to(action='view', id=c.product.id)

    def view(self, id):
        c.can_edit = True
        c.product = Product.find_by_id(id)
        return render('/product/view.mako')

    def index(self):
        c.can_edit = True
        return render('/product/list.mako')

    @dispatch_on(POST="_edit") 
    def edit(self, id):
        c.product = Product.find_by_id(id)

        defaults = h.object_to_defaults(c.product, 'product')
        defaults['product.category'] = c.product.category.id

        defaults['product.ceilings'] = []
        for ceiling in c.product.ceilings:
            defaults['product.ceilings'].append(ceiling.id)

        form = render('/product/edit.mako')
        return htmlfill.render(form, defaults)

    @validate(schema=EditProductSchema(), form='edit', post_only=True, on_get=True, variable_decode=True)
    def _edit(self, id):
        product = Product.find_by_id(id)

        for key in self.form_result['product']:
            setattr(product, key, self.form_result['product'][key])

        # update the objects with the validated form data
        meta.Session.commit()
        h.flash("The product has been updated successfully.")
        redirect_to(action='view', id=id)

    @dispatch_on(POST="_delete") 
    def delete(self, id):
        """Delete the product

        GET will return a form asking for approval.

        POST requests will delete the item.
        """
        c.product = Product.find_by_id(id)
        return render('/product/confirm_delete.mako')

    @validate(schema=None, form='delete', post_only=True, on_get=True, variable_decode=True)
    def _delete(self, id):
        c.product = Product.find_by_id(id)
        for include in ProductInclude.find_by_product(id):
            meta.Session.delete(include)
        meta.Session.commit()
        meta.Session.delete(c.product)
        meta.Session.commit()

        h.flash("Product has been deleted.")
        redirect_to('index')
