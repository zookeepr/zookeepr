from zookeepr.tests.functional import *

class TestOpendayController(CRUDControllerTest):
    model = model.openday.Openday
    url = '/openday'
    param_name = 'openday'
    samples = [dict(openday=dict(
                            firstname='Happy',
                            lastname='Teacher',
                                 heardfromtext='School',
                                 opendaydrag=1,
                                 email_address='teacher@example.org',
                                 heardfrom='-',
                                 ),
                    )
               ]
    crud = ['create']

    def test_existing_openday(self):
        p = model.Openday(email_address='teacher@example.org',
                            firstname='Happy',
                            lastname='Teacher',
            )
        self.dbsession.save(p)
        self.dbsession.flush()

        pid = p.id

        resp = self.app.get('/openday/new')
        f = resp.form
        f['openday.heardfromtext'] = 'Moo'
        f['openday.opendaydrag'] = '5'
        f['openday.email_address'] = 'teacher@example.org'
        f['openday.firstname'] = 'Happy'
        f['openday.lastname'] = 'Teacher'

        resp = f.submit()

        resp.mustcontain('You have already registered!')

        # clean up
        self.dbsession.delete(self.dbsession.query(model.Openday).get(pid))
        self.dbsession.flush()

