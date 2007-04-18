from zookeepr.tests.model import *

class TestOpenday(CRUDModelTest):
    domain = model.openday.Openday
    samples = [dict(firstname='fullname1',
                    lastname="moo",
                    email_address='partneremail1',
                    heardfrom='heardfrom1',
                    heardfromtext='heardfromtext1',
                    opendaydrag=1,
                    ),
               dict(firstname='fullname2',
                    lastname="moo2",
                    email_address='partneremail2',
                    heardfrom='heardfrom2',
                    heardfromtext='heardfewromtext2',
                    opendaydrag=2,
                    )]
