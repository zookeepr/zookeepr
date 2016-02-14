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
from zkpylons.model.rego_room import RegoRoom

log = logging.getLogger(__name__)

class RegoRoomSchema(BaseSchema):
    rego = ExistingRegistrationValidator(not_empty=True)
    room = validators.String(not_empty=True)
    by = ExistingPersonValidator(not_empty=True)

class NewRoomSchema(BaseSchema):
    rego_room = RegoRoomSchema()
    pre_validators = [NestedVariables]

class UpdateRoomSchema(BaseSchema):
    rego_room = RegoRoomSchema()
    pre_validators = [NestedVariables]

class RegoRoomController(BaseController):
    @enforce_ssl(required_all=True)
    @authorize(h.auth.has_organiser_role)
    def __before__(self, **kwargs):
        pass

    @dispatch_on(POST="_new") 
    def new(self):
        defaults = {
            'rego_room.by': h.signed_in_person().id
        }
        raw_params = request.params
        if 'rego_id' in raw_params:
            c.rego_id = int(raw_params['rego_id'])
            defaults['rego_room.rego'] = c.rego_id

        form = render('/rego_room/new.mako')
        return htmlfill.render(form, defaults)

    @validate(schema=NewRoomSchema(), form='new', post_only=True, on_get=True, variable_decode=True)
    def _new(self):
        results = self.form_result['rego_room']

        c.rego_room = RegoRoom(**results)
        meta.Session.add(c.rego_room)
        meta.Session.commit()

        h.flash("Rego room created")
        redirect_to(action='view', id=c.rego_room.id)

    def view(self, id):
        c.rego_room = RegoRoom.find_by_id(id)
        return render('rego_room/view.mako')

    def index(self):
        c.rego_room_collection = RegoRoom.find_all()
        return render('rego_room/list.mako')

    @dispatch_on(POST="_edit")
    def edit(self, id):
        c.rego_room = RegoRoom.find_by_id(id)

        defaults = h.object_to_defaults(c.rego_room, 'rego_room')

        # Rename some fields to match form names
        defaults["rego_room.rego"] = defaults["rego_room.rego_id"]
        defaults["rego_room.by"] = defaults["rego_room.by_id"]

        form = render('rego_room/edit.mako')
        return htmlfill.render(form, defaults)

    @validate(schema=UpdateRoomSchema(), form='edit', post_only=True, on_get=True, variable_decode=True)
    def _edit(self, id):
        rego_room = RegoRoom.find_by_id(id)

        for key in self.form_result['rego_room']:
            setattr(rego_room, key, self.form_result['rego_room'][key])

        # update the objects with the validated form data
        meta.Session.commit()
        h.flash("The room has been updated successfully.")
        redirect_to(action='view', id=id)

    @dispatch_on(POST="_delete") 
    def delete(self, id):
        """Delete the rego room

        GET will return a form asking for approval.

        POST requests will delete the item.
        """
        c.rego_room = RegoRoom.find_by_id(id)
        return render('rego_room/confirm_delete.mako')

    @validate(schema=None, form='delete', post_only=True, on_get=True, variable_decode=True)
    def _delete(self, id):
        c.rego_room = RegoRoom.find_by_id(id)
        meta.Session.delete(c.rego_room)
        meta.Session.commit()

        h.flash("Rego room has been deleted.")
        redirect_to('index')
