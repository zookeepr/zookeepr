import logging
import datetime

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

from zkpylons.model import meta, Person, FulfilmentGroup, Fulfilment, FulfilmentItem

from zkpylons.config.lca_info import lca_info

log = logging.getLogger(__name__)

class CheckinController(BaseController):
    @authorize(h.auth.Or(h.auth.has_organiser_role, h.auth.HasZookeeprRole('checkin')))
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

    @jsonify
    def person_data(self):
        """
	Return the fulfilment data for a person in json format.

	Use direct sql queries because I am too lazy to work out how James' magic queries work.
	"""

        id = request.params['id']
	id = int(id)
        # Assume that the SQL library sanitizes this somehow somewhere

	person_qry_text = """select p.*
	                     from person p
			     where p.id = %d
			  """ % id

	notes_qry = """select rn.* 
	               from rego_note rn
		       join registration r on rn.rego_id = r.id
		       where r.person_id = %d
		    """ % id

	fulfilments_qry = """select f.*, fs.name fulfilment_status, ft.name fulfilment_type
	                     from fulfilment f, 
			          fulfilment_status fs ,
				  fulfilment_type ft
		             where person_id = %d
			       and fs.id = f.status_id
			       and ft.id = f.type_id
			  """ % id

	fulfilment_items_qry = """
	                       select fi.*, p.description
			       from fulfilment_item fi,
			            product p
			       where fulfilment_id = %d
			         and fi.product_id = p.id
			       """ 

	person_qry = sa.sql.text(person_qry_text)
        row = meta.Session.execute(person_qry).fetchone()


	person = {}
	person.update(row)
	for k in person.keys():
  	    if isinstance(person[k], datetime.datetime):
                person[k] = person[k].strftime('%d/%m/%Y')


        notes = []
	for n_row in meta.Session.execute(notes_qry):

	    note = {}
	    note.update(n_row)
	    for k in note.keys():
  	        if isinstance(note[k], datetime.datetime):
                    note[k] = note[k].strftime('%d/%m/%Y')

	    notes.append(note)

	person['notes'] = notes

	fulfilments = []
	for f_row in meta.Session.execute(fulfilments_qry):
	    fulfilment = {}
	    fulfilment.update(f_row)
	    for k in fulfilment.keys():
  	        if isinstance(fulfilment[k], datetime.datetime):
                    fulfilment[k] = fulfilment[k].strftime('%d/%m/%Y')


            fulfilment_items = []
	    for fi_row in meta.Session.execute(fulfilment_items_qry % fulfilment['id']):
	        fulfilment_item = {}
	        fulfilment_item.update(fi_row)
	        for k in fulfilment_item.keys():
  	            if isinstance(fulfilment_item[k], datetime.datetime):
                        fulfilment_item[k] = fulfilment_item[k].strftime('%d/%m/%Y')

                fulfilment_items.append(fulfilment_item)



	    fulfilment['fulfilment_items'] = fulfilment_items 

            fulfilments.append(fulfilment)

	person['fulfilments'] = fulfilments

        return person


    #@jsonify
    def update_fulfilments(self):
        """
	Allow the updating of fulfilment data via json.

	Only allow a subset of the columns in the tables to be updated.  In particular do 
	not allow the primary keys or the fulfilment_id on the fulfilmment_item table to be changed.

	TODO:

	If we don't get all of the fulfilment_items for a fulfilment then throw an error

	If qty for an item is zero then we should delete it.
	"""

        import json

	debug = ""

        data = request.params['data']

	data = json.loads(data)


	for fulfilment in data['fulfilments']:
            db_fulfilment = Fulfilment.find_by_id(int(fulfilment['id']), abort_404=False)
	    db_fulfilment.type_id = fulfilment['type_id'] 
	    db_fulfilment.status_id = fulfilment['status_id'] 
	    db_fulfilment.code = fulfilment['code']

            meta.Session.add(db_fulfilment)

	    for fulfilment_item in fulfilment['fulfilment_items']:
                db_fulfilment_item = FulfilmentItem.find_by_id(fulfilment_item['id'], abort_404=False)

                db_fulfilment_item.product_id = fulfilment_item['product_id']
                db_fulfilment_item.product_text = fulfilment_item['product_text']
                db_fulfilment_item.qty = int(fulfilment_item['qty'])

                meta.Session.add(db_fulfilment_item)


        meta.Session.commit()
	debug += "Committed changes\n"
	return debug


	raise Exception( 'Success')


