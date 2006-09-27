from zookeepr.tests.functional import *
from zookeepr.lib.base import session, g
from paste.fixture import AppError

from sqlalchemy import create_session

class TestTemplateController(ControllerTest):
    """Tests the Template controller and wiki integration."""

    # Implementation

    def setUp(self):
        ControllerTest.setUp(self)

        self.logged_in = False

        # create a user
        self.p = model.core.Person(email_address='testguy@example.org',
                         password='p4ssw0rd')
        self.p.activated = True
        self.p.handle = 'Foomongler'

        objectstore.save(self.p)
        objectstore.flush()
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

        objectstore.delete(Query(model.Person).get(self.p.id))
        objectstore.flush()

        ControllerTest.tearDown(self)

    def assertNotLoggedIn(self):
        # confirm we aren't logged in 
        resp = self.app.get(url_for(controller='/NobodyExpectsTheSpanishInquisition'), status=200)
        self.assertEquals(-1, resp.body.find('Foomongler'))

    def _login(self):
        if not self.logged_in:
            # log in
            resp = self.app.get(url_for(controller='account',
                                    action='signin'))
            f = resp.form
            f['email_address'] = 'testguy@example.org'
            f['password'] = 'p4ssw0rd'
            resp = f.submit()
            self.logged_in = True


    # Tests

    def test_moin_on_404(self):
        resp = self.app.get(url_for(controller='/idontexistlollollol'), status=200)
        resp.mustcontain('/idontexistlollollol?action=edit')

    # I have no idea how to test this. 
    #    def test_moin_disabled_if_no_moin(self):

    # well we changed that today, so this won't work anymore! :)    
    #def test_moin_login(self):
    #    self._login()
    #    
    #    # see if we are logged in now
    #    resp = self.app.get(url_for(controller='/NobodyExpectsTheSpanishInquisition'), status=200)
    #    resp.mustcontain('Foomongler')

    def test_moin_edit(self):
        # make sure we're not logged in
        self.assertNotLoggedIn()

        # check to make sure the page doesn't exist already
        resp = self.app.get('/NobodyExpectsTheSpanishInquisition', status=200)
        self.assertEquals(-1, resp.body.find('Always look at the bright side of life.'))

        # make sure we can't edit without logging in
        resp = self.app.get('/NobodyExpectsTheSpanishInquisition?action=edit', status=200)
        resp.mustcontain('You are not allowed to edit this page.')

        # login
        self._login()

        # make sure we can get the edit page up when we are logged in
        resp = self.app.get('/NobodyExpectsTheSpanishInquisition?action=edit', status=200)
        resp.mustcontain('<textarea')
        resp.mustcontain('editor-textarea')
        resp.mustcontain('you are editing this page')

        # edit and save the page
        f = resp.forms[0]
        f['savetext'] = 'Always look at the bright side of life.'
        resp = f.submit('button_save')

        # make sure our edit was successful
        resp.mustcontain('Always look at the bright side of life.')
        resp.mustcontain('Thank you for your changes')
        
        # refetch a fresh copy without having just been edited
        resp = self.app.get('/NobodyExpectsTheSpanishInquisition', status=200)
        
        # extra pendantic checks
        resp.mustcontain('last edited')
        resp.mustcontain('Always look at the bright side of life.')

        # delete the page
        f = resp.forms[0]
        f['action'] = 'DeletePage'
        resp = f.submit()

        resp.mustcontain('Really delete this page?')

        # answer yes on the confirmation page
        f = resp.forms[0]
        f.submit('delete')

    def test_clean_html(self):
        resp = self.app.get('/NobodyExpectsTheSpanishInquisition', status=200)
        self.assertEquals(1, resp.body.count('<html'))
        self.assertEquals(1, resp.body.count('<body'))
        self.assertEquals(1, resp.body.count('<head'))
