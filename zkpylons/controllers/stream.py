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
from zkpylons.model.stream import Stream

log = logging.getLogger(__name__)

class NotExistingStreamValidator(validators.FancyValidator):
    def validate_python(self, values, state):
        stream = Stream.find_by_name(values['stream']['name'])
        if stream != None and stream != c.stream:
            message = "Duplicate Stream name"
            error_dict = {'stream.name': "Stream name already in use"}
            raise Invalid(message, values, state, error_dict=error_dict)

class StreamSchema(BaseSchema):
    name = validators.String(not_empty=True)

class NewStreamSchema(BaseSchema):
    stream = StreamSchema()
    pre_validators = [NestedVariables]
    chained_validators = [NotExistingStreamValidator()]

class EditStreamSchema(BaseSchema):
    stream = StreamSchema()
    pre_validators = [NestedVariables]

class StreamController(BaseController):

    @authorize(h.auth.has_organiser_role)
    def __before__(self, **kwargs):
        pass

    @dispatch_on(POST="_new") 
    def new(self):
        return render('/stream/new.mako')

    @validate(schema=NewStreamSchema(), form='new', post_only=True, on_get=True, variable_decode=True)
    def _new(self):
        results = self.form_result['stream']

        c.stream = Stream(**results)
        meta.Session.add(c.stream)
        meta.Session.commit()

        h.flash("Stream created")
        redirect_to(action='index')

    def view(self, id):
        c.stream = Stream.find_by_id(id)
        return render('/stream/view.mako')

    def index(self):
        c.can_edit = True
        c.stream_collection = Stream.find_all()
        return render('/stream/list.mako')

    @dispatch_on(POST="_edit")
    def edit(self, id):
        c.stream = Stream.find_by_id(id)

        defaults = h.object_to_defaults(c.stream, 'stream')

        form = render('/stream/edit.mako')
        return htmlfill.render(form, defaults)

    @validate(schema=EditStreamSchema(), form='edit', post_only=True, on_get=True, variable_decode=True)
    def _edit(self, id):
        stream = Stream.find_by_id(id)

        for key in self.form_result['stream']:
            setattr(stream, key, self.form_result['stream'][key])

        # update the objects with the validated form data
        meta.Session.commit()
        h.flash("The stream has been updated successfully.")
        redirect_to(action='index')

    @dispatch_on(POST="_delete") 
    def delete(self, id):
        """Delete the stream

        GET will return a form asking for approval.

        POST requests will delete the item.
        """
        c.stream = Stream.find_by_id(id)
        return render('/stream/confirm_delete.mako')

    @validate(schema=None, form='delete', post_only=True, on_get=True, variable_decode=True)
    def _delete(self, id):
        c.stream = Stream.find_by_id(id)
        meta.Session.delete(c.stream)
        meta.Session.commit()

        h.flash("Stream has been deleted.")
        redirect_to('index')
