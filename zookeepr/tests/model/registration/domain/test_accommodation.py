from zookeepr.tests.model import *

class TestAccommodationModel(ModelTest):
    domain = model.registration.Accommodation
    samples = [dict(name="name1",
                    option="o1",
                    cost_per_night=50.50,
                    beds=100,
                    ),
               dict(name="name2",
                    option="o2",
                    cost_per_night=20.20,
                    beds=50,
                    )
               ]

    def test_accommodation_available(self):
        a = model.registration.Accommodation(name="a", option="", cost_per_night=1.0,
                                             beds=1)
        objectstore.save(a)
        objectstore.flush()

        self.assertEqual(1, a.available)

        # register something, use up the bed
        r = model.registration.Registration()
        r.accommodation = a

        objectstore.save(r)
        objectstore.flush()

        self.assertEqual(0, a.available)
