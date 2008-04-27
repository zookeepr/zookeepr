import warnings

from formencode import validators, compound, variabledecode
from formencode.schema import Schema

from zookeepr.lib.base import *
from zookeepr.lib.crud import Create
from zookeepr.lib.validators import BaseSchema, EmailAddress

class NotExistingOpendayValidator(validators.FancyValidator):
    def validate_python(self, value, state):
        openday = state.query(model.Openday).filter_by(email_address=value['email_address']).one()
        if openday is not None:
            raise Invalid("You have already registered!", value, state)


class OpendaySchema(Schema):
    firstname = validators.String(not_empty=True)
    lastname = validators.String(not_empty=True)
    email_address = EmailAddress(resolve_domain=True, not_empty=True)

    opendaydrag = validators.Int(not_empty=True)

    heardfrom = validators.String()
    heardfromtext = validators.String()

    chained_validators = [NotExistingOpendayValidator()]


class NewOpendaySchema(BaseSchema):
    openday = OpendaySchema()

    pre_validators = [variabledecode.NestedVariables]


class OpendayController(BaseController, Create):
    individual = 'openday'
    model = model.Openday
    schemas = {'new': NewOpendaySchema(),
               }

    def __before__(self):
        if hasattr(super(OpendayController, self), '__before__'):
            super(OpendayController, self).__before__()


    def new(self):

        errors = {}
        defaults = dict(request.POST)

        if defaults:
            results, errors = NewOpendaySchema().validate(defaults, self.dbsession)

            if errors: #FIXME: make this only print if debug enabled
                if request.environ['paste.config']['app_conf'].get('debug'):
                    warnings.warn("form validation failed: %s" % errors)
            else:
                c.openday = model.Openday()
                for k in results['openday']:
                    setattr(c.openday, k, results['openday'][k])
                self.dbsession.save(c.openday)

                self.dbsession.flush()

                return render_response('openday/thankyou.myt')

        return render_response("openday/new.myt", defaults=defaults, errors=errors)

