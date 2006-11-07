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
