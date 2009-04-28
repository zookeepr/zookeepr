import logging, os

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill
from formencode.variabledecode import NestedVariables

from zookeepr.lib.base import BaseController, render
from zookeepr.lib.validators import BaseSchema, ExistingPersonValidator
import zookeepr.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zookeepr.lib.mail import email

from zookeepr.model import meta
from zookeepr.model import Voucher, ProductCategory

from zookeepr.config.lca_info import lca_info

log = logging.getLogger(__name__)

def generate_code():
    res = os.popen('pwgen -Bnc').read().strip()
    if len(res)<3:
        raise "pwgen call failed"
    return res

class NotExistingVoucherValidator(validators.FancyValidator):
    def validate_python(self, value, state):
        voucher = Voucher.find_by_code(value['code'])
        if voucher is not None:
            raise Invalid("Code already exists!", value, state)

class VoucherSchema(BaseSchema):
    count = validators.Int(min=1, max=100)
    leader = ExistingPersonValidator(not_empty=True)
    code = validators.String()
    comment = validators.String(not_empty=True)

    chained_validators = [NotExistingVoucherValidator()]

class NewVoucherSchema(BaseSchema):
    voucher = VoucherSchema()
    pre_validators = [NestedVariables]

class ProductSchema(BaseSchema):
    pass

class VoucherController(BaseController):
    @authorize(h.auth.is_valid_user)
    def __before__(self, **kwargs):
        c.product_categories = ProductCategory.find_all()

    def _generate_product_schema(self):
        for category in c.product_categories:
            if category.name in ['Ticket', 'Accommodation']:
                if category.display == 'radio':
                    # min/max can't be calculated on this form. You should only have 1 selected.
                    ProductSchema.add_field('category_' + str(category.id), ProductInCategory(category=category, if_missing=None))
                    ProductSchema.add_field('category_' + str(category.id) + '_percentage', validators.Int(min=0, max=100, if_empty=0))
                elif category.display == 'checkbox':
                    for product in category.products:
                        ProductSchema.add_field('product_' + str(product.id), validators.Bool(if_missing=False))
                        ProductSchema.add_field('product_' + str(product.id) + '_percentage', validators.Int(min=0, max=100, if_empty=0))
                elif category.display in ('select', 'qty'):
                    for product in category.products:
                        ProductSchema.add_field('product_' + str(product.id) + '_qty', validators.Int(min=0, max=100, if_empty=0))
                        ProductSchema.add_field('product_' + str(product.id) + '_percentage', validators.Int(min=0, max=100, if_empty=0))

    @dispatch_on(POST="_new")
    @authorize(h.auth.has_organiser_role)
    def new(self):
        self._generate_product_schema()

        defaults = {
            'voucher.count': '1',
            'voucher.percentage': '100',
            'voucher.type': 'Professional',
        }
        form = render("/voucher/new.mako")
        return htmlfill.render(form, defaults)

    @validate(schema=NewVoucherSchema(), form='new', post_only=True, on_get=True, variable_decode=True)
    @authorize(h.auth.has_organiser_role)
    def _new(self):
        results = self.form_result['voucher']
        count = results['count']
        del(results['count'])

        for i in xrange(count):
            c.voucher = Voucher(**results)
            if c.voucher.code !='':
                c.voucher.code += '-'
            c.voucher.code += generate_code()
            meta.Session.add(c.voucher)

            c.product_categories = [] # TODO: remove this and fix the for loop!
            for category in c.product_categories:
                if category.name in ['Ticket', 'Accommodation']:
                    if category.display == 'radio':
                        if results['products']['category_' + str(category.id)]:
                            vproduct = VoucherProduct()
                            vproduct.product = meta.Session.query(model.Product).get(results['products']['category_' + str(category.id)])
                            vproduct.qty = 1
                            vproduct.percentage = results['products']['category_' + str(category.id) + '_percentage']
                            meta.Session.add(vproduct)
                            c.voucher.products.append(vproduct)
                    elif category.display == 'checkbox':
                        for product in category.products:
                            if results['products']['product_' + str(product.id)]:
                                vproduct = VoucherProduct()
                                vproduct.product = product
                                vproduct.qty = 1
                                vproduct.percentage = results['products']['product_' + str(product.id) + '_percentage']
                                meta.Session.add(vproduct)
                                c.voucher.products.append(vproduct)
                    else:
                        for product in category.products:
                            if results['products']['product_' + str(product.id) + '_qty'] not in (0, None):
                                vproduct = VoucherProduct()
                                vproduct.product = product
                                vproduct.qty = results['products']['product_' + str(product.id) + '_qty']
                                vproduct.percentage = results['products']['product_' + str(product.id) + '_percentage']
                                meta.Session.add(vproduct)
                                c.voucher.products.append(vproduct)

        meta.Session.commit()
        h.flash("Voucher created")
        return redirect_to(controller='voucher', action='index')

    def index(self):
        c.admin = h.auth.has_organiser_role
        if c.admin:
            c.vouchers = Voucher.find_all()
        else:
            c.vouchers = h.signed_in_person().vouchers

        # TODO: remove this once registration is done
        for v in c.vouchers:
            v.registration = False
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
        # TODO: remove this once registration is done
        c.voucher.registration = False

        if not c.voucher.registration:
            meta.Session.delete(c.voucher)
            meta.Session.commit()
            h.flash("Voucher has been deleted.")
        else:
            h.flash("Cannot delete a voucher which has already been used.", 'error')

        redirect_to('index')
