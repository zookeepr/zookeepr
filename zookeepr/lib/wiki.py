"""MoinMoin wiki integration."""

from exceptions import ImportError
from paste.httpexceptions import HTTPException

from zookeepr.lib.base import *
from zookeepr.model import Person

try:
    from MoinMoin.server.wsgi import moinmoinApp
    from MoinMoin.request import RequestWSGI
    import cgi

    class RequestZookeepr(RequestWSGI):
        def __init__(self, request):
            self.requestZookeepr = request
            RequestWSGI.__init__(self, request.environ)
            
        def setup_args(self, form=None):
            formvars = self.requestZookeepr.POST
            getvars = self.requestZookeepr.GET
            vars = [formvars, getvars]
            args = {}

            for var in vars:
                for key in var:
                    values = var.getall(key)
                    fixedResult = []
                    for item in values:
                       if isinstance(item, cgi.FieldStorage) and item.filename:
                           args[key + '__filename__'] = item.filename
                           fixedResult.append(item.value)
                       else:
                           fixedResult.append(item)
                    args[key] = fixedResult

            return self.decodeArgs(args)
    
    has_moin = True
except ImportError:
    has_moin = False

import re

cleaner_regexp = re.compile(r'<body.*?>(.*?)</body>', re.S)

def get_wiki_response(request, start_response):
    from zookeepr.lib.base import abort
    if not has_moin:
        abort(404)
        return

    if 'signed_in_person_id' in session:
        people = g.objectstore.query(Person).select_by(id=session['signed_in_person_id'])
        if len(people) > 0:
            request.environ['AUTH_TYPE'] = 'Basic'
            request.environ['REMOTE_USER'] = people[0].handle
        
    moinReq = RequestZookeepr(request)
    moinReq.run()
    start_response(moinReq.status, moinReq.headers)
    return [moinReq.output()]

def wiki_here():
    from zookeepr.lib.base import request
    def start_response(status, headers, exc_info=None):
        pass

    try:
        wiki_content = ''.join(get_wiki_response(request, start_response))
        match = cleaner_regexp.search(wiki_content)
        if match:
            return match.groups()[0]
    except HTTPException:
        return ''
