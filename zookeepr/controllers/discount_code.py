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

class NotExistingDiscountCodeValidator(validators.FancyValidator):
    def validate_python(self, value, state):
        discount_code = state.query(model.DiscountCode).get_by(code=value['code'])
        if discount_code is not None:
            raise Invalid("Code already exists!", value, state)

class PercentageValidator(validators.FancyValidator):
    def validate_python(self, value, state):
        percentage = value['percentage']
        if not (percentage > 0 and percentage <= 100):
            raise Invalid("Invalid percentage!", value, state)


class DiscountCodeSchema(BaseSchema):
    count = BoundedInt(min=1, max=100)
    code = validators.String()
    type = validators.String(not_empty=True)
    percentage = validators.Int(not_empty=True)
    comment = validators.String(not_empty=True)

    chained_validators = [NotExistingDiscountCodeValidator, PercentageValidator]

class NewDiscountCodeSchema(BaseSchema):
    discount_code = DiscountCodeSchema()

    pre_validators = [variabledecode.NestedVariables]



class DiscountCodeController(SecureController, Read, Create, List):
    model = model.DiscountCode
    individual = 'discount_code'

    schemas = {'new': NewDiscountCodeSchema(),
              }

    permissions = {'new': [AuthRole('organiser')],
                   'view': [AuthRole('organiser')],
                   }

    def __before__(self, **kwargs):
        super(DiscountCodeController, self).__before__(**kwargs)


    def new(self):
        errors = {}
        defaults = dict(request.POST)

        if defaults:
            results, errors = NewDiscountCodeSchema().validate(defaults, self.dbsession)
            print errors

            if errors: #FIXME: make this only print if debug enabled
                if request.environ['paste.config']['app_conf'].get('debug'):
                    warnings.warn("form validation failed: %s" % errors)
            else:
	        values = results['discount_code']
	        for i in xrange(values['count']):
		    c.discount_code = model.DiscountCode()
		    for k in values:
			setattr(c.discount_code, k, values[k])
		    if c.discount_code.code !='':
		      c.discount_code.code += '-'
		    c.discount_code.code += generate_code()
		    self.dbsession.save(c.discount_code)

		self.dbsession.flush()

                return redirect_to('/discount_code')

        return render_response("discount_code/new.myt", defaults=defaults, errors=errors)

