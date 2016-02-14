import logging, os

from pylons import request, response, session, tmpl_context as c
from zkpylons.lib.helpers import redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill
from formencode.variabledecode import NestedVariables

from zkpylons.lib.base import BaseController, render
from zkpylons.lib.ssl_requirement import enforce_ssl
from zkpylons.lib.validators import BaseSchema, ExistingPersonValidator
import zkpylons.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zkpylons.lib.mail import email

from zkpylons.model import meta
from zkpylons.model import Voucher, VoucherProduct, ProductCategory, Product

log = logging.getLogger(__name__)

def generate_code():
    res = os.popen('pwgen -BnA').read().strip()
    if len(res)<3:
        raise StandardError("pwgen call failed")
    return res

class NotExistingVoucherValidator(validators.FancyValidator):
    def validate_python(self, values, state):
        # TODO: This doesn't work, code is randomly generated - this doesn't search for prefixes
        voucher = Voucher.find_by_code(values['voucher']['code'])
        error_dict = {}
        if voucher is not None:
            message = "Duplicate Voucher Code"
            error_dict = {'voucher.code': "Code already exists!"}
            raise Invalid(message, values, state, error_dict=error_dict)

class VoucherSchema(BaseSchema):
    count = validators.Int(min=1, max=100)
    leader = ExistingPersonValidator(not_empty=True)
    code = validators.String()
    comment = validators.String(not_empty=True)

class NewVoucherSchema(BaseSchema):
    voucher = VoucherSchema()
    pre_validators = [NestedVariables]
    chained_validators = [NotExistingVoucherValidator()]

new_schema = NewVoucherSchema()

class VoucherController(BaseController):
    @enforce_ssl(required_all=True)
    @authorize(h.auth.is_valid_user)
    def __before__(self, **kwargs):
        c.product_categories = ProductCategory.find_nonfree()
        self._generate_product_schema()

    def _generate_product_schema(self):
        # This function is similar to zkpylons.registration.RegistrationController._generate_product_schema
        # Since the form is arbitrarily defined by what product types there are, the validation
        #   (aka schema) also needs to be dynamic.
        # Thus, this function generates a dynamic schema to validate a given set of products.
        #
        pschema = BaseSchema()
        for category in c.product_categories:
            # handle each form input type individually as the validation is unique.
            if category.display == 'radio':
                # min/max can't be calculated on this form. You should only have 1 selected.
                pschema.add_field('category_' + str(category.id), validators.Int(if_missing=None))
                pschema.add_field('category_' + str(category.id) + '_percentage', validators.Int(min=0, max=100, if_empty=0))
            else:
                for product in category.products_nonfree:
                    pschema.add_field('product_' + str(product.id) + '_qty', validators.Int(min=0, max=100, if_empty=0))
                    pschema.add_field('product_' + str(product.id) + '_percentage', validators.Int(min=0, max=100, if_empty=0))
        new_schema.add_field('products', pschema)

    @dispatch_on(POST="_new")
    @authorize(h.auth.has_organiser_role)
    def new(self):
        defaults = {
            'voucher.count': '1',
        }
        form = render("/voucher/new.mako")
        return htmlfill.render(form, defaults)

    @validate(schema=new_schema, form='new', post_only=True, on_get=True, variable_decode=True)
    @authorize(h.auth.has_organiser_role)
    def _new(self):
        results = self.form_result['voucher']
        count = results['count'] # Number of voucher codes to generate
        del(results['count'])

        for i in xrange(count):
            if 'products' in results:
                del(results['products'])
            c.voucher = Voucher(**results)
            if c.voucher.code !='':
                c.voucher.code += '-' #add a dash between prefix and random
            c.voucher.code += generate_code()
            meta.Session.add(c.voucher) # save voucher to DB

            results['products'] = self.form_result['products']

            for category in c.product_categories:
                # depending on "display" type of product, handle the input appropriately
                if category.display == 'radio':
                    if 'category_' + str(category.id) in results['products'] and results['products']['category_' + str(category.id)] != None:
                        product = Product.find_by_id(results['products']['category_' + str(category.id)])
                        vproduct = VoucherProduct()
                        vproduct.voucher = c.voucher
                        vproduct.product = product
                        vproduct.qty = 1
                        vproduct.percentage = results['products']['category_' + str(category.id) + '_percentage']
                        meta.Session.add(vproduct) # Save product to DB
                        c.voucher.products.append(vproduct) # Assign individual product discount to voucher
                else:
                    for product in category.products_nonfree:
                        if 'product_' + str(product.id) + '_qty' in results['products']:
                            if results['products']['product_' + str(product.id) + '_qty'] not in (0, None):
                                vproduct = VoucherProduct()
                                vproduct.voucher = c.voucher
                                vproduct.product = product
                                vproduct.qty = results['products']['product_' + str(product.id) + '_qty']
                                vproduct.percentage = results['products']['product_' + str(product.id) + '_percentage']
                                meta.Session.add(vproduct)
                                c.voucher.products.append(vproduct)

        meta.Session.commit() #save all updates
        h.flash("Voucher created")
        return redirect_to(controller='voucher', action='index')

    def index(self):
        c.admin = h.auth.authorized(h.auth.has_organiser_role)
        if c.admin:
            c.vouchers = Voucher.find_all()
        else:
            c.vouchers = h.signed_in_person().vouchers

        return render('/voucher/list.mako')

    @dispatch_on(POST="_delete")
    @authorize(h.auth.has_organiser_role)
    def delete(self, id):
        """Delete the voucher

        GET will return a form asking for approval.

        POST requests will delete the item.
        """
        c.voucher = Voucher.find_by_id(id)
        return render('/voucher/confirm_delete.mako')

    @validate(schema=None, form='delete', post_only=True, on_get=True, variable_decode=True)
    @authorize(h.auth.has_organiser_role)
    def _delete(self, id):
        c.voucher = Voucher.find_by_id(id)

        if not c.voucher.registration:
            meta.Session.delete(c.voucher)
            meta.Session.commit()
            h.flash("Voucher has been deleted.")
        else:
            h.flash("Cannot delete a voucher which has already been used.", 'error')

        redirect_to('index')
