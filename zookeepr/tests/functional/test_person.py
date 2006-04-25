from zookeepr.tests import *

class TestPersonController(TestController):
    def test_index(self):
        response = self.app.get(url_for(controller='person'))
        # Test response...
        response.mustcontain("person index")

    def test_new(self):
        res = self.app.get(url_for(controller='person', action='new'))
        res.mustcontain("you're creating a person")

        res = self.app.post(url_for(controller='person', action='new'),
                            params=dict(handle='testguy'))

        res = res.follow()
        res.mustcontain("you're viewing person testguy")

    def test_view(self):
        response = self.app.get(url_for(controller='person', action='view', id='jaq'))
        response.mustcontain("you're viewing person jaq")

    def test_edit(self):
        response = self.app.get(url_for(controller='person', action='edit', id='jaq'))
        response.mustcontain("you're editing person jaq")

    def test_delete(self):
        response = self.app.get(url_for(controller='person', action='delete', id='jaq'))
        response.mustcontain("you're deleting person jaq")

    def test_list(self):
        response = self.app.get(url_for(controller='person', action='list'))
        response.mustcontain("you're getting the list of persons")

