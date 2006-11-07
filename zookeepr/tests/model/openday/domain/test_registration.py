from zookeepr.tests.model import *

class TestOpenday(ModelTest):
    domain = model.registration.Registration
    samples = [dict(fullname='fullname1',
                    partner_email='partneremail1',
                    heardfrom='heardfrom1',
                    heardfromtext='heardfromtext1',
                    opendaydrag=1,
                    )]
