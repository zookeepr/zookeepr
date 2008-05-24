from zookeepr.tests.functional import *

class TestTemplateController(ControllerTest):
    """Tests the Template controller and wiki integration."""

    # Implementation

    def setUp(self):
        super(TestTemplateController, self).setUp()

        self.logged_in = False

        # create a user
        self.p = model.core.Person(email_address='testguy@example.org',
                         password='p4ssw0rd')
        self.p.activated = True
        self.p.handle = 'Foomongler'

        self.dbsession.save(self.p)
        self.dbsession.flush()
        self.pid = self.p.id

    def tearDown(self):
        # clean up
        self._login()

        resp = self.app.get('/NobodyExpectsTheSpanishInquisition', status=200)
        if resp.body.find('bright side of life') > -1:
            f = resp.forms[0]
            f['action'] = 'DeletePage'
            resp = f.submit()
            resp.mustcontain('Really delete this page?')
            f = resp.forms[0]
            f.submit('delete')

        self.dbsession.delete(self.dbsession.query(model.Person).get(self.p.id))
        self.dbsession.flush()

        super(TestTemplateController, self).tearDown()

    def assertNotLoggedIn(self):
        # confirm we aren't logged in 
        resp = self.app.get(url_for(controller='/NobodyExpectsTheSpanishInquisition'), status=200)
        self.assertEquals(-1, resp.body.find('Foomongler'))

    def _login(self):
        if not self.logged_in:
            # log in
            resp = self.app.get(url_for(controller='person',
                                    action='signin'))
            f = resp.form
            f['email_address'] = 'testguy@example.org'
            f['password'] = 'p4ssw0rd'
            resp = f.submit()
            self.logged_in = True

    def test_clean_html(self):
        resp = self.app.get('/NobodyExpectsTheSpanishInquisition', status=200)
        self.assertEquals(1, resp.body.count('<html'))
        self.assertEquals(1, resp.body.count('<body'))
        self.assertEquals(1, resp.body.count('<head'))
