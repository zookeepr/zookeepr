import new
import os
from unittest import TestCase

class TestBase(TestCase):
    def assertRaisesAny(self, callable_obj, *args, **kwargs):
        """Assert that the ``callable_obj`` raises any exception."""
        try:
            callable_obj(*args, **kwargs)
        except:
            pass
        else:
            self.fail("callable %s failed to raise an exception" % callable_obj)

def monkeypatch(cls, test_name, func_name):
    """Create a method on a class with a different name.

    This method patches ``cls`` with a method called ``test_name``, which
    is bound to the actual callable ``func_name``.

    In order to make sure test cases get run in children of the assortment
    of test base classes in this module, we do not name the worker methods
    with the prefix 'test_'.  Instead they are named otherwise, and we
    alias them in the metaclass of the test class.

    However, due to the behaviour of ``nose`` to not run tests that are
    defined outside of the module of the current test class being run, we
    need to create these test aliases with the model of the child class,
    rather than simply calling ``setattr``.

    (Curious readers can study ``node.selector``, in particular the
    ``wantMethod``, ``callableInTests``, and ``anytests`` methods (as of
    this writing).)

    You can't set __module__ directly because it's a r/o attribute, so we
    call ``new.function`` to create a new function with the same code as
    the original.  The __module__ attribute is set by the new.function
    method from the globals dict that it is passed, so here we make a
    shallow copy of the original and override the __name__ attribute to
    point to the module of the class we're actually testing.
    
    By this stage, you may think that this is crack.  You're right.
    But at least I don't have to repeat the same code over and
    over in the actual tests ;-)
    """
    # get the code
    code = getattr(cls, func_name).im_func.func_code
    # get the function globals so we can overwrite the module
    g = getattr(cls, func_name).im_func.func_globals.copy()
    g['__name__'] = cls.__module__
    # create a new function with:
    # the code of the original function,
    # our patched globals,
    # and the new name of the function
    setattr(cls, test_name, new.function(code, g, test_name))


def setup():
    try:
        os.unlink('test.db')
    except OSError:
        pass

    from zookeepr.model import create_all
    create_all({'dburi': 'sqlite:///test.db',
                'echo_queries': 'true'})

__all__ = ['TestBase', 'monkeypatch']
