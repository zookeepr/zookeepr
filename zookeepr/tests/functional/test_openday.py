import re

from zookeepr.tests.functional import *

class TestOpendayController(ControllerTest):
    model = model.openday.Openday
    url = '/openday'
    param_name = 'openday'
    samples = [dict(openday=dict(
                                      heardfromtext='School',
                                      opendaydrag=1,
                                      email_address='teacher@example.org',
                                      heardfrom='-',
                                      ),
                    )
               ]
#    no_test = ['password_confirm', 'person']
    crud = ['create']

    def setUp(self):
        super(TestOpendayController, self).setUp()

    def tearDown(self):
        ps = Query(model.OpenDay).select()
        for p in ps:
            objectstore.delete(p)
        objectstore.flush()
        super(TestOpendayController, self).tearDown()

class TestOpendayController(ControllerTest):
    def test_existing_openday(self):
        p = model.Openday(email_address='teacher@example.org',
            fullname='Happy teacher',
            )
        objectstore.save(p)
        objectstore.flush()

        pid = p.id

        resp = self.app.get('/openday/new')
        f = resp.form
        sample_data = dict(
            heardfromtext='Moo',
            opendaydrag=5,
            )
        for k in sample_data.keys():
            f['openday.' + k] = sample_data[k]
        f['openday.email_address'] = 'teacher@example.org'
        f['openday.fullname'] = 'Happy Teacher'

        resp = f.submit()

        resp.mustcontain('You have already registered!')

        # clean up
        objectstore.delete(Query(model.Openday).get(pid))
        objectstore.flush()

