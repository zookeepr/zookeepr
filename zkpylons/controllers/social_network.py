import logging

from pylons import request, response, session, tmpl_context as c
from zkpylons.lib.helpers import redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill, ForEach, Invalid
from formencode.variabledecode import NestedVariables

from zkpylons.lib.base import BaseController, render
from zkpylons.lib.validators import BaseSchema, ProductValidator
import zkpylons.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zkpylons.lib.mail import email

from zkpylons.model import meta
from zkpylons.model.social_network import SocialNetwork

log = logging.getLogger(__name__)

class NotExistingSocialNetworkValidator(validators.FancyValidator):
    def validate_python(self, values, state):
        name = values['social_network']['name']
        social_network = SocialNetwork.find_by_name(name, abort_404=False)
        if social_network != None and social_network.name == name:
	    message = "Duplicate Social Network name"
	    error_dict = {'social_network.name': "Social Network name already in use"}
            raise Invalid(message, values, state, error_dict=error_dict)

class SocialNetworkSchema(BaseSchema):
    name = validators.String(not_empty=True)
    logo = validators.String(not_empty=True)
    url = validators.URL(add_http=True, check_exists=False)

class NewSocialNetworkSchema(BaseSchema):
    social_network = SocialNetworkSchema()
    pre_validators = [NestedVariables]
    chained_validators = [NotExistingSocialNetworkValidator()]

class EditSocialNetworkSchema(BaseSchema):
    social_network = SocialNetworkSchema()
    pre_validators = [NestedVariables]

class SocialNetworkController(BaseController):

    @authorize(h.auth.has_organiser_role)
    def __before__(self, **kwargs):
        pass

    @dispatch_on(POST="_new")
    def new(self):
        return render('/social_network/new.mako')

    @validate(schema=NewSocialNetworkSchema(), form='new', post_only=True, on_get=True, variable_decode=True)
    def _new(self):
        results = self.form_result['social_network']

        print "Gonna make a new SocialNetwork"
        c.social_network = SocialNetwork(**results)
        print "New social_network %s" % c.social_network
        meta.Session.add(c.social_network)
        meta.Session.commit()

        h.flash("Social Network created")
        redirect_to(action='view', id=c.social_network.id)

    def view(self, id):
        c.social_network = SocialNetwork.find_by_id(id)
        return render('/social_network/view.mako')

    def index(self):
        c.can_edit = True
        c.social_networks = SocialNetwork.find_all()
        return render('/social_network/list.mako')

    @dispatch_on(POST="_edit")
    def edit(self, id):
        c.social_network = SocialNetwork.find_by_id(id)

        defaults = h.object_to_defaults(c.social_network, 'social_network')

        form = render('/social_network/edit.mako')
        return htmlfill.render(form, defaults)

    @validate(schema=EditSocialNetworkSchema(), form='edit', post_only=True, on_get=True, variable_decode=True)
    def _edit(self, id):
        social_network = SocialNetwork.find_by_id(id)

        for key in self.form_result['social_network']:
            setattr(social_network, key, self.form_result['social_network'][key])

        # update the objects with the validated form data
        meta.Session.commit()
        h.flash("The social_network has been updated successfully.")
        redirect_to(action='view', id=id)

    @dispatch_on(POST="_delete")
    def delete(self, id):
        """Delete the social_network

        GET will return a form asking for approval.

        POST requests will delete the item.
        """
        c.social_network = SocialNetwork.find_by_id(id)
        return render('/social_network/confirm_delete.mako')

    @validate(schema=None, form='delete', post_only=True, on_get=True, variable_decode=True)
    def _delete(self, id):
        c.social_network = SocialNetwork.find_by_id(id)
        meta.Session.delete(c.social_network)
        meta.Session.commit()

        h.flash("Social Network has been deleted.")
        redirect_to('index')
