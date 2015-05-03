import logging

from pylons import request, response, session, tmpl_context as c, app_globals
from zkpylons.lib.helpers import redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill, ForEach, Invalid
from formencode.variabledecode import NestedVariables

from zkpylons.lib.base import BaseController, render
from zkpylons.lib.ssl_requirement import enforce_ssl
from zkpylons.lib.validators import BaseSchema, FulfilmentTypeValidator, ExistingPersonValidator
import zkpylons.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zkpylons.lib.mail import email

from zkpylons.model import meta, FulfilmentGroup, FulfilmentType
from zkpylons.model.config import Config

import zkpylons.lib.pdfgen as pdfgen

log = logging.getLogger(__name__)

class FulfilmentGroupSchema(BaseSchema):
    person = ExistingPersonValidator(not_empty=False)
    code = validators.String(not_empty=True)

class NewFulfilmentGroupSchema(BaseSchema):
    fulfilment_group = FulfilmentGroupSchema()
    pre_validators = [NestedVariables]

class EditFulfilmentGroupSchema(BaseSchema):
    fulfilment_group = FulfilmentGroupSchema()
    pre_validators = [NestedVariables]

class FulfilmentGroupController(BaseController):

    @enforce_ssl(required_all=True)
    @authorize(h.auth.has_organiser_role)
    def __before__(self, **kwargs):
        c.can_edit = True
        c.fulfilment_types = FulfilmentType.find_all()

    @dispatch_on(POST="_new")
    def new(self):
        return render('/fulfilment_group/new.mako')

    @validate(schema=NewFulfilmentGroupSchema(), form='new', post_only=True, on_get=True, variable_decode=True)
    def _new(self):
        results = self.form_result['fulfilment_group']

        c.fulfilment_group = FulfilmentGroup(**results)
        meta.Session.add(c.fulfilment_group)
        meta.Session.commit()

        h.flash("Fulfilment Group created")
        redirect_to(action='index', id=None)

    def view(self, id):
        c.fulfilment_group = FulfilmentGroup.find_by_id(id)
        return render('/fulfilment_group/view.mako')

    def pdf(self, id):
        c.fulfilment_group = FulfilmentGroup.find_by_id(id, True)

        xml_s = render('/fulfilment_group/pdf.mako')
        xsl_f = app_globals.mako_lookup.get_template('/fulfilment_group/pdf.xsl').filename
        pdf_data = pdfgen.generate_pdf(xml_s, xsl_f)

        filename = Config.get('event_shortname') + '_' + str(c.fulfilment_group.id) + '.pdf'
        return pdfgen.wrap_pdf_response(pdf_data, filename)

    def index(self):
        c.fulfilment_group_collection = FulfilmentGroup.find_all()
        return render('/fulfilment_group/list.mako')

    @dispatch_on(POST="_edit")
    def edit(self, id):
        c.fulfilment_group = FulfilmentGroup.find_by_id(id)

        defaults = h.object_to_defaults(c.fulfilment_group, 'fulfilment_group')
        defaults['fulfilment_group.person'] = c.fulfilment_group.person_id

        form = render('/fulfilment_group/edit.mako')
        return htmlfill.render(form, defaults)

    @validate(schema=EditFulfilmentGroupSchema(), form='edit', post_only=True, on_get=True, variable_decode=True)
    def _edit(self, id):
        fulfilment_group = FulfilmentGroup.find_by_id(id)

        for key in self.form_result['fulfilment_group']:
            setattr(fulfilment_group, key, self.form_result['fulfilment_group'][key])

        # update the objects with the validated form data
        meta.Session.commit()
        h.flash("The Fulfilment Group has been updated successfully.")
        redirect_to(action='index', id=None)

    @dispatch_on(POST="_delete")
    def delete(self, id):
        """Delete the fulfilment_group

        GET will return a form asking for approval.

        POST requests will delete the item.
        """
        c.fulfilment_group = FulfilmentGroup.find_by_id(id)
        return render('/fulfilment_group/confirm_delete.mako')

    @validate(schema=None, form='delete', post_only=True, on_get=True, variable_decode=True)
    def _delete(self, id):
        c.fulfilment_group = FulfilmentGroup.find_by_id(id)
        meta.Session.delete(c.fulfilment_group)
        meta.Session.commit()

        h.flash("Fulfilment Group has been deleted.")
        redirect_to('index', id=None)
