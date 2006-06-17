from unittest import TestCase

from zookeepr.lib.crud import CRUDBase, Create

class TestCRUD(TestCase):
    def test_redirect_to(self):

        target = dict(controller='pants', action='index')

        class A(CRUDBase):
            pass
        
        class B(CRUDBase):
            redirect_map = dict(new=target)

        default_redirect = dict(controller='a', action='view', id=1)
        a = A()
        result = a.redirect_to('new', default_redirect)

        print "a", result
        
        c = C()
        result = c.redirect_to('new', default_redirect)
        print "c", result

    def test_create(self):
        pass
