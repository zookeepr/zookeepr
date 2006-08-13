from zookeepr.lib.base import *
from zookeepr.model import Person

class RegisterController(BaseController):

    def confirm(self, id):
        """Confirm a registration with the given ID.

        `id` is a md5 hash of the email address of the registrant, the time
        they regsitered, and a nonce.

        """
        r = g.objectstore.query(Person).select_by(_url_hash=id)

        if len(r) < 1:
            abort(404)

        r[0].activated = True

        g.objectstore.save(r[0])
        g.objectstore.flush()

        return render_response('register/confirmed.myt')
