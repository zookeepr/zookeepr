from sqlalchemy.orm import mapper, relation, backref
from sqlalchemy.sql import join, and_, select, func, outerjoin

from tables import registration, accommodation_location, accommodation_option, rego_note
from zookeepr.model.billing.tables import voucher_code
from domain import Registration, Accommodation, AccommodationLocation, AccommodationOption, RegoNote
from zookeepr.model.billing.domain import VoucherCode
from zookeepr.model.core import Person

mapper(AccommodationLocation, accommodation_location)

mapper(AccommodationOption, accommodation_option,
       properties = {
    'location': relation(AccommodationLocation)
    }
       )


# The following selectable represents the aggregate sum of registrations
# that have selected a location as their preferred accommodation.
accommodation_location_beds_taken_selectable = \
    select([accommodation_location.c.id.label('loc_id'),
            func.count(registration.c.id).label('beds_taken')],
           from_obj=[outerjoin(outerjoin(accommodation_location,
                                         accommodation_option),
                               registration)],
           group_by=[accommodation_location.c.id]).alias('loc_beds_taken')

# This mapper then joins the options onto the location+registration count above
# so we can determine how many beds are taken for that option.  This is necessary
# as bed count is per location, not per option.
mapper(Accommodation,
       select([accommodation_option.c.id,
               accommodation_location.c.name,
               accommodation_location.c.beds,
               accommodation_option.c.name.label('option'),
               accommodation_option.c.cost_per_night,
               accommodation_location_beds_taken_selectable.c.beds_taken
               ],
              from_obj=[join(join(accommodation_location, accommodation_option),
                             accommodation_location_beds_taken_selectable,
                             accommodation_location_beds_taken_selectable.c.loc_id==accommodation_location.c.id)],
              ).alias('accommodation_selectable'),
       order_by=None,
       )


mapper(Registration, registration,
       properties = {
    'person': relation(Person,
                       backref=backref('registration', cascade="all, delete-orphan",
                                       lazy=True,
                                       uselist=False),
                       ),
    'accommodation': relation(Accommodation, backref='registrations'),
    'voucher': relation(VoucherCode,
                         uselist=False,
                         primaryjoin=registration.c.voucher_code==voucher_code.c.code,
                         foreign_keys=voucher_code.c.code,
        )
    }
       )

mapper(RegoNote, rego_note,
  properties = {
    'rego': relation(Registration,
                     backref=backref('notes', cascade="all, delete-orphan",
                                       lazy=True)),
    'by': relation(Person,
                   backref=backref('notes_made', cascade="all, delete-orphan",
                                       lazy=True)),
  }
)
