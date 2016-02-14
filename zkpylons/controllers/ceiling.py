import logging
from collections import namedtuple


from pylons import request, response, session, tmpl_context as c
from zkpylons.lib.helpers import redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill, ForEach, Invalid
from formencode.variabledecode import NestedVariables

from zkpylons.lib.base import BaseController, render
from zkpylons.lib.ssl_requirement import enforce_ssl
from zkpylons.lib.validators import BaseSchema, ProductValidator, CeilingValidator
import zkpylons.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zkpylons.lib.mail import email

from zkpylons.model import meta
from zkpylons.model.ceiling import Ceiling
from zkpylons.model.product_category import ProductCategory

log = logging.getLogger(__name__)

class NotExistingCeilingValidator(validators.FancyValidator):
    def validate_python(self, values, state):
        ceiling = Ceiling.find_by_name(values['ceiling']['name'])
        if ceiling != None and ceiling != c.ceiling:
            message = "Duplicate Ceiling name"
            error_dict = {'ceiling.name': "Ceiling name already in use"}
            raise Invalid(message, values, state, error_dict=error_dict)

class CeilingSchema(BaseSchema):
    parent = CeilingValidator()
    name = validators.String(not_empty=True)
    max_sold = validators.Int(min=0, max=2000000)
    available_from = validators.DateConverter(month_style='dd/mm/yyyy')
    available_until = validators.DateConverter(month_style='dd/mm/yyyy')
    products = ForEach(ProductValidator())

class NewCeilingSchema(BaseSchema):
    ceiling = CeilingSchema()
    pre_validators = [NestedVariables]
    chained_validators = [NotExistingCeilingValidator()]

class EditCeilingSchema(BaseSchema):
    ceiling = CeilingSchema()
    pre_validators = [NestedVariables]

class CeilingController(BaseController):

    @enforce_ssl(required_all=True)
    @authorize(h.auth.has_organiser_role)
    def __before__(self, **kwargs):
        c.product_categories = ProductCategory.find_all()

    @dispatch_on(POST="_new")
    def new(self):
        c.ceilings = Ceiling.find_all()
        return render('/ceiling/new.mako')

    @validate(schema=NewCeilingSchema(), form='new', post_only=True, on_get=True, variable_decode=True)
    def _new(self):
        results = self.form_result['ceiling']

        c.ceiling = Ceiling(**results)
        meta.Session.add(c.ceiling)
        meta.Session.commit()

        h.flash("Ceiling created")
        redirect_to(action='view', id=c.ceiling.id)

    def view(self, id):
        c.ceiling = Ceiling.find_by_id(id)
        c.specials = []
        SpecStruct = namedtuple('Special', 'id person_id reg_id fullname product is_paid diet special u18 notes')
        for product in c.ceiling.products:
            for invoice_item in product.invoice_items:
                if not invoice_item.invoice.status == 'Invalid':
                    person = invoice_item.invoice.person
                    rego = person.registration
                    c.specials.append(SpecStruct(
                        id=person.id,
                        person_id=person.id,
                        reg_id=rego.id,
                        fullname=person.fullname,
                        product=invoice_item.description,
                        is_paid=invoice_item.invoice.is_paid,
                        diet=rego.diet,
                        special=rego.special,
                        u18=not(rego.over18),
                        notes=rego.notes,
                    ))

        return render('/ceiling/view.mako')

    def index(self):
        c.can_edit = True
        c.ceiling_collection = Ceiling.find_all()
        return render('/ceiling/list.mako')

    @dispatch_on(POST="_edit")
    def edit(self, id):
        c.ceilings = Ceiling.find_all()
        c.ceiling = Ceiling.find_by_id(id)

        defaults = h.object_to_defaults(c.ceiling, 'ceiling')

        if c.ceiling.parent:
            defaults['ceiling.parent'] = c.ceiling.parent.id

        defaults['ceiling.products'] = []
        for product in c.ceiling.products:
            defaults['ceiling.products'].append(product.id)
        if c.ceiling.available_from:
            defaults['ceiling.available_from'] = c.ceiling.available_from.strftime('%d/%m/%y')
        if c.ceiling.available_until:
            defaults['ceiling.available_until'] = c.ceiling.available_until.strftime('%d/%m/%y')

        form = render('/ceiling/edit.mako')
        return htmlfill.render(form, defaults)

    @validate(schema=EditCeilingSchema(), form='edit', post_only=True, on_get=True, variable_decode=True)
    def _edit(self, id):
        ceiling = Ceiling.find_by_id(id)

        for key in self.form_result['ceiling']:
            setattr(ceiling, key, self.form_result['ceiling'][key])

        # update the objects with the validated form data
        meta.Session.commit()
        h.flash("The ceiling has been updated successfully.")
        redirect_to(action='view', id=id)

    @dispatch_on(POST="_delete")
    def delete(self, id):
        """Delete the ceiling

        GET will return a form asking for approval.

        POST requests will delete the item.
        """
        c.ceiling = Ceiling.find_by_id(id)
        return render('/ceiling/confirm_delete.mako')

    @validate(schema=None, form='delete', post_only=True, on_get=True, variable_decode=True)
    def _delete(self, id):
        c.ceiling = Ceiling.find_by_id(id)
        meta.Session.delete(c.ceiling)
        meta.Session.commit()

        h.flash("Ceiling has been deleted.")
        redirect_to('index')
