from zookeepr.lib.base import BaseController, render_response
#from zookeepr.lib.crud import Edit

class ReviewController(BaseController):
    def new(self):
        return render_response("review/new.myt", defaults={}, errors={})
