import logging

from pylons import request, response, session, tmpl_context as c
from zkpylons.lib.helpers import redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill, ForEach, Invalid
from formencode.variabledecode import NestedVariables

from zkpylons.lib.base import BaseController, render
from zkpylons.lib.ssl_requirement import enforce_ssl
from zkpylons.lib.validators import BaseSchema, ProductValidator
import zkpylons.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zkpylons.lib.mail import email

from zkpylons.model import meta
from zkpylons.model.product import Product, ProductInclude
from zkpylons.model.product_category import ProductCategory

log = logging.getLogger(__name__)

class NotExistingProductCategoryValidator(validators.FancyValidator):
    def validate_python(self, values, state):
        product_category = ProductCategory.find_by_name(values['product_category']['name'])
        if product_category != None and product_category != c.product_category:
            message = "Duplicate product category name"
            error_dict = {'product_category.name': "Category name already in use"}
            raise Invalid(message, values, state, error_dict=error_dict)

class ProductCategorySchema(BaseSchema):
    name = validators.String(not_empty=True)
    description = validators.String(not_empty=True)
    note = validators.String()
    display = validators.String(not_empty=True)
    display_mode = validators.String()
    display_order = validators.Int(min=0, max=2000000, not_empty=True)
    invoice_free_products = validators.Bool(if_missing=False)
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

    @enforce_ssl(required_all=True)
    @authorize(h.auth.has_organiser_role)
    def __before__(self, **kwargs):
        pass

    @dispatch_on(POST="_new") 
    def new(self):
        return render('/product_category/new.mako')

    @validate(schema=NewProductCategorySchema(), form='new', post_only=True, on_get=True, variable_decode=True)
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

    def stats(self, id):
        c.can_edit = True
        c.product_category = ProductCategory.find_by_id(id)
        c.product_categories = ProductCategory.find_all()
        return render('/product_category/stats.mako')

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

    @validate(schema=EditProductCategorySchema(), form='edit', post_only=True, on_get=True, variable_decode=True)
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
        # For some reason cascading isn't working for me. Likely I just don't understand SA so I'll do it this way:
        # first delete all of the products
        for product in c.product_category.products:
            # We also delete all of the productincludes for the products
            for include in ProductInclude.find_by_product(product.id):
                meta.Session.delete(include)
            meta.Session.commit()
            meta.Session.delete(product)
        meta.Session.commit()
        # Also delete any includes of the category
        for include in ProductInclude.find_by_category(id):
            meta.Session.delete(include)
        meta.Session.commit()
        meta.Session.delete(c.product_category)
        meta.Session.commit()

        h.flash("Category has been deleted.")
        redirect_to('index')
