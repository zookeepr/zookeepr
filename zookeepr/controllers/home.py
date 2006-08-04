from zookeepr.lib.base import *
from zookeepr.lib.auth import SecureController

class HomeController(BaseController):

    def index(self):
        """The home page of the website.

        If the user has not signed in, then they are presented with the default page.

        Otherwise, they're shown the customised page.

        We rely on `c.person` containing the Person object for the currently signed
        in user, but we don't want to redirect to the signin action if we're not signed
        in so we duplicate the __before__ code from SecureController here.
        """

        if 'person_id' in session:
            c.person = self.objectstore.get(Person, session['person_id'])

            resp = render_response('home.myt')

        else:
            resp = render_response('about/index.myt')

        return resp
