from formencode import validators, variabledecode

from formencode.schema import Schema

from zookeepr.lib.base import *
from zookeepr.lib.auth import *
from zookeepr.lib.crud import *
from zookeepr.lib.validators import *

import os

def generate_code():
    res = os.popen('pwgen -Bnc').read().strip()
    if len(res)<3:
        raise "pwgen call failed"
    return res

class NotExistingVoucherValidator(validators.FancyValidator):
    def validate_python(self, value, state):
        voucher = state.query(model.Voucher).filter_by(code=value['code']).first()
        if voucher is not None:
            raise Invalid("Code already exists!", value, state)

class ExistingPersonValidator(validators.FancyValidator):
    def _to_python(self, value, state):
        leader = state.query(model.Person).filter_by(id=value).first()
        if leader is None:
            raise Invalid("Unknown person ID for leader!", value, state)
        else:
            return leader
    def _from_python(self, value, state):
        return valud.id

class VoucherSchema(BaseSchema):
    count = BoundedInt(min=1, max=100)
    leader = ExistingPersonValidator(not_empty=True)
    code = validators.String()
    comment = validators.String(not_empty=True)

    chained_validators = [NotExistingVoucherValidator()]

class NewVoucherSchema(BaseSchema):
    voucher = VoucherSchema()
    pre_validators = [variabledecode.NestedVariables]



class VoucherController(SecureController, Read, Create, List):
    model = model.Voucher
    individual = 'voucher'

    schemas = {'new': NewVoucherSchema(),
              }

    permissions = {'new': [AuthRole('organiser')],
                   'index': [AuthTrue()],
                   }

    def __before__(self, **kwargs):
        super(VoucherController, self).__before__(**kwargs)
        c.dbsession = self.dbsession # for the use of list.myt
        c.product_categories = self.dbsession.query(model.ProductCategory).all()

    def _generate_product_schema(self):
        class ProductSchema(BaseSchema):
            pass
        for category in c.product_categories:
            if category.name in ['Ticket', 'Accomodation']:
                if category.display == 'radio':
                    # min/max can't be calculated on this form. You should only have 1 selected.
                    ProductSchema.add_field('category_' + str(category.id), ProductInCategory(category=category, if_missing=None))
                    ProductSchema.add_field('category_' + str(category.id) + '_percentage', BoundedInt(min=0, max=100, if_empty=0))
                elif category.display == 'checkbox':
                    for product in category.products:
                        ProductSchema.add_field('product_' + str(product.id), validators.Bool(if_missing=False))
                        ProductSchema.add_field('product_' + str(product.id) + '_percentage', BoundedInt(min=0, max=100, if_empty=0))
                elif category.display in ('select', 'qty'):
                    for product in category.products:
                        ProductSchema.add_field('product_' + str(product.id) + '_qty', BoundedInt(min=0))
                        ProductSchema.add_field('product_' + str(product.id) + '_percentage', BoundedInt(min=0, max=100, if_empty=0))
        self.schemas['new'].add_field('products', ProductSchema)

    def new(self):
        self._generate_product_schema()
        errors = {}
        defaults = dict(request.POST)

        if defaults:
            results, errors = self.schemas['new'].validate(defaults, self.dbsession)
            print errors

            if errors: #FIXME: make this only print if debug enabled
                if request.environ['paste.config']['app_conf'].get('debug'):
                    warnings.warn("form validation failed: %s" % errors)
            else:
                values = results['voucher']
                for i in xrange(values['count']):
                    voucher = model.Voucher()
                    for k in values:
                        setattr(voucher, k, values[k])
                    if voucher.code !='':
                      voucher.code += '-'
                    voucher.code += generate_code()
                    self.dbsession.save(voucher)

                    for category in c.product_categories:
                        if category.name in ['Ticket', 'Accomodation']:
                            if category.display == 'radio':
                                if results['products']['category_' + str(category.id)]:
                                    vproduct = model.VoucherProduct()
                                    vproduct.product = self.dbsession.query(model.Product).get(results['products']['category_' + str(category.id)])
                                    vproduct.qty = 1
                                    vproduct.percentage = results['products']['category_' + str(category.id) + '_percentage']
                                    self.dbsession.save(vproduct)
                                    voucher.products.append(vproduct)
                            elif category.display == 'checkbox':
                                for product in category.products:
                                    if results['products']['product_' + str(product.id)]:
                                        vproduct = model.VoucherProduct()
                                        vproduct.product = product
                                        vproduct.qty = 1
                                        vproduct.percentage = results['products']['product_' + str(product.id) + '_percentage']
                                        self.dbsession.save(vproduct)
                                        voucher.products.append(vproduct)

                            else:
                                for product in category.products:
                                    if results['products']['product_' + str(product.id) + '_qty'] not in (0, None):
                                        vproduct = model.VoucherProduct()
                                        vproduct.product = product
                                        vproduct.qty = results['products']['product_' + str(product.id) + '_qty']
                                        vproduct.percentage = results['products']['product_' + str(product.id) + '_percentage']
                                        self.dbsession.save(vproduct)
                                        voucher.products.append(vproduct)

                self.dbsession.flush()

                return redirect_to('/voucher')

        return render_response("voucher/new.myt", defaults=defaults, errors=errors)

