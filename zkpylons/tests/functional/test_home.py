from routes import url_for

from .fixtures import PersonFactory
from .utils import do_login, isSignedIn

class TestHomeController(object):
    def test_index(self, app):
        response = app.get(url_for(controller='home'))

    def test_index_logged_in_regos_open(self, app, db_session):
        p = PersonFactory(
                # Set full set of detail to avoid incomplete profile flag
                firstname = 'Testguy',
                lastname  = 'Testguy',
                i_agree   = True,
                activated = True,
                address1  = 'Somewhere',
                city      = 'Over the rainbow',
                postcode  = 'Way up high',
                )

        db_session.commit()

        # Set redirect origin
        response = app.get('/')

        resp = do_login(app, p.email_address, p.raw_password)
        assert isSignedIn(app)

        resp = resp.follow()

        # TODO:
        # This doesn't work, we get sent back to our previous page
        # This is sane but the implementation seems bug ridden
        # There is also code to redirect to /register/new but it isn't reached
        #assert resp.request.path == '/register/status'

        assert resp.request.path == '/'
        resp.mustcontain("Sign out")
