import new

from zookeepr.lib.base import *

class SubExec:
    """This class is used to return a callabled that subexec-s a
    given file."""
    
    def _orig(self):
        """_orig is a really nasty hack. Here is why, pylons when it
        does its magic introspection stuff excepts real python functions,
        not callables like SubExec. (because it calles inspect.getargspec
        internally). But is also supports decorated function in the way
        such that it first checks if there is an _orig member on the callable
        and instead calls ispect.getargspec on the _orig member. So what
        we do here is provide an _orig that it can happily run inspect.getargspec
        on. I like the way I have now written more explanation that the
        duplicated code I saved implementing this, but thats really not the point."""
        pass

    def __init__(self, filename):
        """Create a new SubExec object, that will m.subexec a given
        filename when called."""
        self.filename = filename
        
    def __call__(self, _self):
        """This is the actual overloaded method which
        makes subexec callable."""
        m.subexec(self.filename)

class AboutController(BaseController):
    templates = ["whatson", "programme", "dates",
                 "press", "sydney", "contact",
                 "sponsors"]

    def index(self):
        h.redirect_to(action='whatson')

    def __getattr__(self, name):
        if name in self.templates:
            return new.instancemethod(SubExec("about/%s.myt" % name), self)
        else:
            raise AttributeError, name
