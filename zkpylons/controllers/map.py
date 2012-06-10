import logging
import zkpylons.lib.helpers as h
from pylons import request, response, session, tmpl_context as c

from zkpylons.model import meta
from zkpylons.model.db_content import DbContent, DbContentType

from zkpylons.lib.base import BaseController, render

log = logging.getLogger(__name__)


class MapController(BaseController):

    def index(self):
        """A Google map on website.
        """

        return render('map/view.mako')
