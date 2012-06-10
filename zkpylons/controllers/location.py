import logging

from pylons import request, response, session, tmpl_context as c
from zookeepr.lib.helpers import redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill, ForEach, Invalid
from formencode.variabledecode import NestedVariables

from zookeepr.lib.base import BaseController, render
from zookeepr.lib.ssl_requirement import enforce_ssl
from zookeepr.lib.validators import BaseSchema
import zookeepr.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zookeepr.lib.mail import email

from zookeepr.model import meta
from zookeepr.model.location import Location

from zookeepr.config.lca_info import lca_info

log = logging.getLogger(__name__)

class LocationSchema(BaseSchema):
    display_name = validators.String(not_empty=True)
    display_order = validators.Int()
    capacity = validators.Int()

class NewLocationSchema(BaseSchema):
    location = LocationSchema()
    pre_validators = [NestedVariables]

class EditLocationSchema(BaseSchema):
    location = LocationSchema()
    pre_validators = [NestedVariables]

class LocationController(BaseController):

    @enforce_ssl(required_all=True)
    @authorize(h.auth.has_organiser_role)
    def __before__(self, **kwargs):
        c.can_edit = True

    @dispatch_on(POST="_new")
    def new(self):
        return render('/location/new.mako')

    @validate(schema=NewLocationSchema(), form='new', post_only=True, on_get=True, variable_decode=True)
    def _new(self):
        results = self.form_result['location']

        c.location = Location(**results)
        meta.Session.add(c.location)
        meta.Session.commit()

        h.flash("Location created")
        redirect_to(action='index', id=None)

    def view(self, id):
        c.location = Location.find_by_id(id)
        return render('/location/view.mako')

    def index(self):
        c.location_collection = Location.find_all()
        return render('/location/list.mako')

    @dispatch_on(POST="_edit")
    def edit(self, id):
        c.location = Location.find_by_id(id)

        defaults = h.object_to_defaults(c.location, 'location')

        form = render('/location/edit.mako')
        return htmlfill.render(form, defaults)

    @validate(schema=EditLocationSchema(), form='edit', post_only=True, on_get=True, variable_decode=True)
    def _edit(self, id):
        location = Location.find_by_id(id)

        for key in self.form_result['location']:
            setattr(location, key, self.form_result['location'][key])

        # update the objects with the validated form data
        meta.Session.commit()
        h.flash("The Location has been updated successfully.")
        redirect_to(action='index', id=None)

    @dispatch_on(POST="_delete")
    def delete(self, id):
        """Delete the location

        GET will return a form asking for approval.

        POST requests will delete the item.
        """
        c.location = Location.find_by_id(id)
        return render('/location/confirm_delete.mako')

    @validate(schema=None, form='delete', post_only=True, on_get=True, variable_decode=True)
    def _delete(self, id):
        c.location = Location.find_by_id(id)
        meta.Session.delete(c.location)
        meta.Session.commit()

        h.flash("Location has been deleted.")
        redirect_to('index')
