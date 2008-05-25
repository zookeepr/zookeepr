from zookeepr.tests.model import *

class TestAccommodationLocationModel(CRUDModelTest):
    """Test the AccommodationLocation crud object, that maps straight on
    top of the accommodation_location table.
    """
    domain = model.registration.AccommodationLocation
    samples = [dict(name="nam1",
                    beds=1,
                    ),
               dict(name="name2",
                    beds=2,
                    )
               ]


class TestAccommodationOptionModel(CRUDModelTest):
    """Test the AccommodationOption crud object, that maps straight
    on top of the accommopation_option table.
    """
    domain = model.registration.AccommodationOption
    samples = [dict(name="opt1",
                    cost_per_night=1,
                    ),
               dict(name="opt2",
                    cost_per_night=2,
                    )
               ]

    def setUp(self):
        super(TestAccommodationOptionModel, self).setUp()
        
        self.location = model.registration.AccommodationLocation(name='foo', beds=1)
        self.dbsession.save(self.location)
        self.dbsession.flush()
        self.lid = self.location.id
        
    def additional(self, ao):
        """Create location objects for the samples before they're saved.
        """
        ao.location = self.location
        return ao

    def tearDown(self):
        self.location = self.dbsession.query(model.registration.AccommodationLocation).get_by(id=self.lid)
        self.dbsession.delete(self.location)
        self.dbsession.flush()

        super(TestAccommodationOptionModel, self).tearDown()


class TestAccommodationModel(ModelTest):

    def test_accommodation_available(self):
        al = model.registration.AccommodationLocation(name='a', beds=1)
        self.dbsession.save(al)
        self.dbsession.flush()
        ao = model.registration.AccommodationOption(name='buh', cost_per_night=1.00)
        ao.location = al
        self.dbsession.save(ao)
        self.dbsession.flush()

        print "accommodations:", self.dbsession.query(model.registration.Accommodation).all()

        a = self.dbsession.query(model.registration.Accommodation).filter_by(id=1).one()
        self.failIfEqual(None, a)

        print "registrations using this accommodation:", a.registrations

        self.assertEqual([], a.registrations)

        self.assertEqual(1, a.get_available_beds())

        p = model.Person(email_address='testguy@example.org')
        self.dbsession.save(p)
        # register something, use up the bed
        r = model.registration.Registration()
        r.accommodation = a

        p.registration = r

        self.dbsession.save(r)
        self.dbsession.flush()
        
        # we want to force a reload of the beds_taken field
        self.dbsession.refresh(a)
        #self.dbsession.expire(r)
        
        print "registrations using this accommodation:", a.registrations
        self.failIfEqual([], a.registrations)
        self.assertEqual(r, a.registrations[0])

        print "beds taken:", a.beds_taken
        self.assertEqual(1, a.beds_taken)
        self.assertEqual(1, a.beds)
        print "available beds:", a.get_available_beds()
        self.assertEqual(0, a.get_available_beds())

        # add a second accommodation option
        ao1 = model.registration.AccommodationOption(name='snuh', cost_per_night=2)
        ao1.location = al
        self.dbsession.save(ao1)
        self.dbsession.flush()

        # assert that there are two accommodations now
        as = self.dbsession.query(model.Accommodation).all()
        print "accommodations 2:", as
        self.assertEqual(2, len(as))

        a1 = self.dbsession.query(model.registration.Accommodation).filter_by(id=ao1.id).one()
        
        print "a beds available:", a.get_available_beds()
        print "a1 beds available:", a1.get_available_beds()

        # both options should have no beds because the first registration filled them all
        self.assertEqual(0, a1.get_available_beds(), "accommodation options should both have no beds available")

        as = self.dbsession.query(model.Accommodation).all()
        print 'as:', as
        self.assertEqual(2, len(as))

        available_as = filter(lambda a: a.get_available_beds() >= 1, as)
        print 'available_as:', available_as
        self.assertEqual(0, len(available_as))

        self.dbsession.delete(p)
        self.dbsession.flush()
        model.registration.tables.registration.delete().execute()
        model.registration.tables.accommodation_option.delete().execute()
        model.registration.tables.accommodation_location.delete().execute()
