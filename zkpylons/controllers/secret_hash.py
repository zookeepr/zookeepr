#####
import sys
import inspect
from pylons import config
import logging
import zkpylons.lib.helpers as h
from pylons import request, response, session, tmpl_context as c
from zkpylons.lib.helpers import redirect_to
from pylons.util import class_name_from_module_name

from zkpylons.model import meta
from pylons.controllers.util import abort

from zkpylons.lib.base import BaseController, render
from zkpylons.model import URLHash

log = logging.getLogger(__name__)


class SecretHashController(BaseController):

    def lookup(self, hash):
        c.hash = URLHash.find_by_hash(hash)
        if c.hash is None:
            abort(404, "Sorry, Invalid Hash.")

        return self.transfer(url=c.hash.url)

    # as per http://www.mail-archive.com/pylons-discuss@googlegroups.com/msg06643.html
    def transfer(controller = None, action = None, url = None, **kwargs):

        """usage:
        1. result = transfer(url = "/someurl/someaction")
        2. result = transfer(controller = "/controller1/sub_controller2",
    action = "test") # kwargs will pass to action.
        """

        if (url != None):
            route_map = config['routes.map']
            match_route= route_map.match(url)
            if (match_route == None):
                raise(Exception("no route matched url '%s'" % url))
            # if
            controller = match_route["controller"].replace("/", ".")
            action = match_route["action"]
            del(match_route["controller"])
            del(match_route["action"])
            kwargs.update(match_route)
        else:
            if (controller == None):
                route_map = config['routes.map']
                match_route = route_map.match("/")
                if (match_route == None):
                    raise(Exception("no route matched url '%s'" % url))
                # if
                controller = match_route["controller"].replace("/", ".")
                if (action == None):
                    action = match_route["action"]
                # if
                del(match_route["controller"])
                del(match_route["action"])
                kwargs.update(match_route)
            else:
                controller = controller.replace("/", ".")
                if (action == None):
                    action = "index"
                # if
            # if
        # if
        full_module_name = config['pylons.package'] + '.controllers.' + controller
        __traceback_hide__ = 'before_and_this'
        try:
            __import__(full_module_name)
        except ImportError, e:
            raise(NotImplementedError("'%s' not found: %s" % (controller, e)))
        # try
        module_name = controller.split('.')[-1]
        class_name = class_name_from_module_name(module_name) + 'Controller'
        controller_class = getattr(sys.modules[full_module_name], class_name)
        controller_inst = controller_class()
        if (hasattr(controller_inst, action)):
            action_method = getattr(controller_inst, action, None)
            #if (not isinstance(action_method, types.MethodType)):
            #    raise(NotImplementedError("action '%s' not found in '%s'" % (action, controller)))
            # if
            if (hasattr(controller_inst, "__before__")):
                before_method = getattr(controller_inst, "__before__", None)
                #if (isinstance(before_method, types.MethodType)):
                #    before_method(action)
                # if
            # if
            action_args_name, action_args, action_kargs, action_defaults = inspect.getargspec(action_method)
            del(action_args_name[0])
            call_kargs = {}
            for k, v in kwargs.iteritems():
                if (k in action_args_name):
                    call_kargs[k] = v
                # if
            # for
            result = action_method(**call_kargs)
            if (hasattr(controller_inst, "__after__")):
                after_method = getattr(controller_inst, "__after__", None)
                #if (isinstance(after_method, types.MethodType)):
                #    after_method(action)
                # if
            # if
            return(result)
        else:
            raise(NotImplementedError("action '%s' not found in '%s'" % (action, controller)))
        # if
    # def

