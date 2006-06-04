import unittest

from zookeepr.lib.validators import Strip

class TestStripValidator(unittest.TestCase):
    def test_strip(self):
        value_dict = dict(something='something',
                          foo=37,
                          commit='ok')

        result = Strip("commit").to_python(value_dict, None)

        self.failIf("commit" in result.keys(), "key not stripped")
