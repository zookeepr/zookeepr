import logging

from pylons import request, response, session, tmpl_context as c
from zkpylons.lib.helpers import redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill
from formencode.variabledecode import NestedVariables

from zkpylons.lib.base import BaseController, render
from zkpylons.lib.validators import BaseSchema
import zkpylons.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zkpylons.lib.mail import email

from zkpylons.model import meta
from zkpylons.model import Role

log = logging.getLogger(__name__)

class RoleSchema(BaseSchema):
    name = validators.PlainText()
    pretty_name = validators.String()
    comment = validators.String()
    display_order = validators.Int()

class NewRoleSchema(BaseSchema):
    role = RoleSchema()
    pre_validators = [NestedVariables]

class EditRoleSchema(BaseSchema):
    role = RoleSchema()
    pre_validators = [NestedVariables]

class RoleController(BaseController): # Delete
    @authorize(h.auth.has_organiser_role)
    def __before__(self, **kwargs):
        pass

    @dispatch_on(POST="_edit") 
    def edit(self, id):
        c.form = 'edit'
        c.role = Role.find_by_id(id)
        
        defaults = h.object_to_defaults(c.role, 'role')

        form = render('/role/edit.mako')
        return htmlfill.render(form, defaults)


    @validate(schema=EditRoleSchema(), form='edit', post_only=True, on_get=True, variable_decode=True)
    def _edit(self, id):
        c.role = Role.find_by_id(id)

        for key in self.form_result['role']:
            setattr(c.role, key, self.form_result['role'][key])

        if c.role.pretty_name is not None and c.role.pretty_name == '':
            setattr(c.role, 'pretty_name', None)

        # update the objects with the validated form data
        meta.Session.commit()

        redirect_to(action='view', id=id)


    @dispatch_on(POST="_new") 
    def new(self):
        """Create a new role form. """
        return render('/role/new.mako')

    @validate(schema=NewRoleSchema(), form='new', post_only=True, on_get=True, variable_decode=True)
    def _new(self):
        """Create a new role submit.  """
        results = self.form_result['role']
        c.role = Role(**results)
        meta.Session.add(c.role)
        meta.Session.commit()

        redirect_to('/role')

    def index(self):
        c.role_collection = Role.find_all()
        return render('/role/list.mako')

    def view(self, id):
        c.registration_status = h.config['app_conf'].get('registration_status')
        c.role = Role.find_by_id(id)

        return render('role/view.mako')

    @dispatch_on(POST="_delete") 
    def delete(self, id):
        """Delete the role

        GET will return a form asking for approval.

        POST requests will delete the item.
        """
        c.role = Role.find_by_id(id)
        return render('role/confirm_delete.mako')

    @validate(schema=None, form='delete', post_only=True, on_get=True, variable_decode=True)
    def _delete(self, id):
        c.role = Role.find_by_id(id)
        meta.Session.delete(c.role)
        meta.Session.commit()

        redirect_to('index')
