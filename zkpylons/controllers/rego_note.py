import logging

from pylons import request, response, session, tmpl_context as c
from zkpylons.lib.helpers import redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill
from formencode.variabledecode import NestedVariables

from zkpylons.lib.base import BaseController, render
from zkpylons.lib.ssl_requirement import enforce_ssl
from zkpylons.lib.validators import BaseSchema, ExistingRegistrationValidator, ExistingPersonValidator
import zkpylons.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zkpylons.lib.mail import email

from zkpylons.model import meta
from zkpylons.model.rego_note import RegoNote

log = logging.getLogger(__name__)

class RegoNoteSchema(BaseSchema):
    rego = ExistingRegistrationValidator(not_empty=True)
    note = validators.String(not_empty=True)
    block = validators.Bool(if_empty=False)
    by = ExistingPersonValidator(not_empty=True)

class NewNoteSchema(BaseSchema):
    rego_note = RegoNoteSchema()
    pre_validators = [NestedVariables]

class UpdateNoteSchema(BaseSchema):
    rego_note = RegoNoteSchema()
    pre_validators = [NestedVariables]

class RegoNoteController(BaseController):
    @enforce_ssl(required_all=True)
    @authorize(h.auth.has_organiser_role)
    def __before__(self, **kwargs):
        pass

    @dispatch_on(POST="_new") 
    def new(self):
        defaults = {
            'rego_note.by': h.signed_in_person().id
        }
        raw_params = request.params
        if 'rego_id' in raw_params:
            c.rego_id = int(raw_params['rego_id'])
            defaults['rego_note.rego'] = c.rego_id

        form = render('/rego_note/new.mako')
        return htmlfill.render(form, defaults)

    @validate(schema=NewNoteSchema(), form='new', post_only=True, on_get=True, variable_decode=True)
    def _new(self):
        results = self.form_result['rego_note']

        c.rego_note = RegoNote(**results)
        meta.Session.add(c.rego_note)
        meta.Session.commit()

        h.flash("Rego note created")
        redirect_to(action='view', id=c.rego_note.id)

    def view(self, id):
        c.rego_note = RegoNote.find_by_id(id)
        return render('rego_note/view.mako')

    def index(self):
        c.rego_note_collection = RegoNote.find_all()
        return render('rego_note/list.mako')

    @dispatch_on(POST="_edit")
    def edit(self, id):
        c.rego_note = RegoNote.find_by_id(id)

        defaults = h.object_to_defaults(c.rego_note, 'rego_note')

        # Rename some fields to match form names
        defaults["rego_note.rego"] = defaults["rego_note.rego_id"]
        defaults["rego_note.by"] = defaults["rego_note.by_id"]

        form = render('rego_note/edit.mako')
        return htmlfill.render(form, defaults)

    @validate(schema=UpdateNoteSchema(), form='edit', post_only=True, on_get=True, variable_decode=True)
    def _edit(self, id):
        rego_note = RegoNote.find_by_id(id)

        for key in self.form_result['rego_note']:
            setattr(rego_note, key, self.form_result['rego_note'][key])

        # update the objects with the validated form data
        meta.Session.commit()
        h.flash("The note has been updated successfully.")
        redirect_to(action='view', id=id)

    @dispatch_on(POST="_delete") 
    def delete(self, id):
        """Delete the rego note

        GET will return a form asking for approval.

        POST requests will delete the item.
        """
        c.rego_note = RegoNote.find_by_id(id)
        return render('rego_note/confirm_delete.mako')

    @validate(schema=None, form='delete', post_only=True, on_get=True, variable_decode=True)
    def _delete(self, id):
        c.rego_note = RegoNote.find_by_id(id)
        meta.Session.delete(c.rego_note)
        meta.Session.commit()

        h.flash("Rego note has been deleted.")
        redirect_to('index')
