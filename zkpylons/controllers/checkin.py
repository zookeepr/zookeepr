import logging

from pylons import request, response, session, tmpl_context as c
from zkpylons.lib.helpers import redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on
from pylons.decorators import jsonify

from formencode import validators, htmlfill, ForEach, Invalid
from formencode.variabledecode import NestedVariables

from zkpylons.lib.base import BaseController, render
from zkpylons.lib.validators import BaseSchema, ProductValidator
import zkpylons.lib.helpers as h

import sqlalchemy as sa
from sqlalchemy.sql.expression import cast

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zkpylons.lib.mail import email

from zkpylons.model import meta, Person, FulfilmentGroup, Fulfilment

from zkpylons.config.lca_info import lca_info

log = logging.getLogger(__name__)

class CheckinController(BaseController):
    @authorize(h.auth.has_organiser_role)
    def __before__(self, **kwargs):
        pass

    def index(self):
        return render('/checkin/index.mako')

    @jsonify
    def lookup(self):
        q = request.params['q']
        # Assume that the SQL library handles the SQL attack vectors

        person_query =  meta.Session.query(Person.id, sa.func.concat(Person.fullname, " - ", Person.email_address).label("pretty")).filter(sa.or_(
            Person.lastname.ilike(q + '%'),
            Person.fullname.ilike(q + '%'),
            Person.email_address.ilike(q + '%'),
        ))

        personid_query = meta.Session.query(Person.id, cast(Person.id, sa.String).label("pretty")).filter(
            cast(Person.id, sa.String).like(q + '%'),
        )

        boarding_query = meta.Session.query(FulfilmentGroup.person_id, FulfilmentGroup.code.label("pretty")).filter( 
            FulfilmentGroup.code.like(q + '%')
        )

        badge_query = meta.Session.query(Fulfilment.person_id, Fulfilment.code.label("pretty")).filter( 
            Fulfilment.code.like(q + '%')
        )

        union_query = person_query.union(personid_query, boarding_query, badge_query).order_by("pretty").limit(5)

        return dict(r=list(union_query.all()))
