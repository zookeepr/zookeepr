import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill, ForEach, Invalid
from formencode.variabledecode import NestedVariables

from zookeepr.lib.base import BaseController, render
from zookeepr.lib.validators import BaseSchema, ProductValidator
import zookeepr.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zookeepr.lib.mail import email

from zookeepr.model import meta
from zookeepr.model.product_category import ProductCategory

from zookeepr.config.lca_info import lca_info

log = logging.getLogger(__name__)

class NotExistingProductCategoryValidator(validators.FancyValidator):
    def validate_python(self, value, state):
        product_category = ProductCategory.find_by_name(value['product_category']['name'])
        if product_category != None and product_category != c.product_category:
           raise Invalid("Category name already in use", value, state)

class ProductCategorySchema(BaseSchema):
    name = validators.String(not_empty=True)
    description = validators.String(not_empty=True)
    display = validators.String(not_empty=True)
    min_qty = validators.Int(min=0, max=2000000)
    max_qty = validators.Int(min=0, max=2000000)
    # TODO: check that min_qty <= max_qty

class NewProductCategorySchema(BaseSchema):
    product_category = ProductCategorySchema()
    pre_validators = [NestedVariables]
    chained_validators = [NotExistingProductCategoryValidator()]

class EditProductCategorySchema(BaseSchema):
    product_category = ProductCategorySchema()
    pre_validators = [NestedVariables]

class ProductCategoryController(BaseController):

    @authorize(h.auth.has_organiser_role)
    def __before__(self, **kwargs):
        pass

    @dispatch_on(POST="_new") 
    def new(self):
        return render('/product_category/new.mako')

    @validate(schema=NewProductCategorySchema(), form='new', post_only=True)
    def _new(self):
        results = self.form_result['product_category']

        c.product_category = ProductCategory(**results)
        meta.Session.add(c.product_category)
        meta.Session.commit()

        h.flash("Category created")
        redirect_to(action='view', id=c.product_category.id)

    def view(self, id):
        c.product_category = ProductCategory.find_by_id(id)
        return render('/product_category/view.mako')

    def index(self):
        c.can_edit = True
        c.product_category_collection = ProductCategory.find_all()
        return render('/product_category/list.mako')

    @dispatch_on(POST="_edit")
    def edit(self, id):
        c.product_category = ProductCategory.find_by_id(id)

        defaults = h.object_to_defaults(c.product_category, 'product_category')

        form = render('/product_category/edit.mako')
        return htmlfill.render(form, defaults)

    @validate(schema=EditProductCategorySchema(), form='edit', post_only=True)
    def _edit(self, id):
        product_category = ProductCategory.find_by_id(id)

        for key in self.form_result['product_category']:
            setattr(product_category, key, self.form_result['product_category'][key])

        # update the objects with the validated form data
        meta.Session.commit()
        h.flash("The product_category has been updated successfully.")
        redirect_to(action='view', id=id)

    @dispatch_on(POST="_delete") 
    def delete(self, id):
        """Delete the product_category

        GET will return a form asking for approval.

        POST requests will delete the item.
        """
        c.product_category = ProductCategory.find_by_id(id)
        return render('/product_category/confirm_delete.mako')

    @validate(schema=None, form='delete', post_only=True, on_get=True, variable_decode=True)
    def _delete(self, id):
        c.product_category = ProductCategory.find_by_id(id)
        meta.Session.delete(c.product_category)
        meta.Session.commit()

        h.flash("Category has been deleted.")
        redirect_to('index')
