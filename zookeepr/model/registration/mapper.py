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

mapper(Accommodation,
       select([accommodation_option.c.id,
               accommodation_location.c.name,
               accommodation_location.c.beds,
               accommodation_option.c.name.label('option'),
               accommodation_option.c.cost_per_night,
               func.count(registration.c.id).label('beds_taken'),
               ],
              from_obj=[outerjoin(join(accommodation_location, accommodation_option),
                                  registration)],
              group_by=[accommodation_option.c.id,
                        accommodation_option.c.name,
                        accommodation_option.c.cost_per_night,
                        accommodation_location.c.name,
                        accommodation_location.c.beds],
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
