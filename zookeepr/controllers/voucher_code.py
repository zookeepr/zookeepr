from formencode import validators, variabledecode

from formencode.schema import Schema

from zookeepr.lib.base import *
from zookeepr.lib.auth import *
from zookeepr.lib.crud import *
from zookeepr.lib.validators import BaseSchema, BoundedInt

import os

def generate_code():
    res = os.popen('pwgen -Bnc').read().strip()
    if len(res)<3:
        raise "pwgen call failed"
    return res

class NotExistingVoucherCodeValidator(validators.FancyValidator):
    def validate_python(self, value, state):
        voucher_code = state.query(model.VoucherCode).filter_by(code=value['code']).one()
        if voucher_code is not None:
            raise Invalid("Code already exists!", value, state)

class ExistingPersonValidator(validators.FancyValidator):
    def validate_python(self, value, state):
        leader_id = value['leader_id']
        leader = state.query(model.Person).filter_by(id=leader_id).one()
        if leader is None:
            raise Invalid("Unknown person ID for leader!", value, state)


class VoucherCodeSchema(BaseSchema):
    count = BoundedInt(min=1, max=100)
    leader_id = BoundedInt()
    code = validators.String()
    type = validators.String(not_empty=True)
    percentage = BoundedInt(min=0, max=100)
    comment = validators.String(not_empty=True)

    chained_validators = [NotExistingVoucherCodeValidator, ExistingPersonValidator]

class NewVoucherCodeSchema(BaseSchema):
    voucher_code = VoucherCodeSchema()
    pre_validators = [variabledecode.NestedVariables]



class VoucherCodeController(SecureController, Read, Create, List):
    model = model.VoucherCode
    individual = 'voucher_code'

    schemas = {'new': NewVoucherCodeSchema(),
              }

    permissions = {'new': [AuthRole('organiser')],
                   'view': [AuthRole('organiser')],
                   'list': [AuthTrue()],
                   }

    def __before__(self, **kwargs):
        super(VoucherCodeController, self).__before__(**kwargs)
        c.dbsession = self.dbsession # for the use of list.myt

    def new(self):
        errors = {}
        defaults = dict(request.POST)

        if defaults:
            results, errors = NewVoucherCodeSchema().validate(defaults, self.dbsession)
            print errors

            if errors: #FIXME: make this only print if debug enabled
                if request.environ['paste.config']['app_conf'].get('debug'):
                    warnings.warn("form validation failed: %s" % errors)
            else:
                values = results['voucher_code']
                leader = self.dbsession.query(model.Person).filter_by(id=values['leader_id']).one()
                for i in xrange(values['count']):
                    voucher_code = model.VoucherCode()
                    for k in values:
                        setattr(voucher_code, k, values[k])
                    if voucher_code.code !='':
                      voucher_code.code += '-'
                    voucher_code.code += generate_code()
                    voucher_code.leader = leader
                    self.dbsession.save(voucher_code)

                self.dbsession.flush()

                return redirect_to('/voucher_code')

        return render_response("voucher_code/new.myt", defaults=defaults, errors=errors)

