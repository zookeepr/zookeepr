from sqlalchemy import mapper, join, relation, and_, select, func, outerjoin

from zookeepr.model.core import Person
from tables import registration, accommodation_location, accommodation_option
from domain import Registration, Accommodation, AccommodationLocation, AccommodationOption

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
              group_by=[accommodation_option.c.id],
              ).alias('accommodation_selectable'),
       order_by=None,
       )


mapper(Registration, registration,
       properties = {
    'person': relation(Person),
    'accommodation': relation(Accommodation, backref='registrations',
                              ),
    }
       )
