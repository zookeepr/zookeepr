import pytest
from routes import url_for

from datetime import datetime

from zk.model import DbContent
from .fixtures import DbContentFactory, DbContentTypeFactory

from .crud_helper import CrudHelper

class TestDBContent(CrudHelper):
    @pytest.yield_fixture(autouse=True)
    def prep_types(self, db_session):
        # Some types are expected/required by the system - cause odd 404s if missing
        self.news_type  = DbContentTypeFactory(name="News")
        self.page_type  = DbContentTypeFactory(name="Page")
        self.press_type = DbContentTypeFactory(name="In the press")
        db_session.commit()
        yield

    def test_permissions(self, app, db_session):
        # view removed from get_pages, allowed by public and tested in second pass
        CrudHelper.test_permissions(self, app, db_session, dont_get_pages = 'view', additional_get_pages=('list_files'))


        # These pages can be viewed by the public... any anyone else
        CrudHelper.test_permissions(self, app, db_session, get_pages=('list_news', 'list_press', 'rss_news', 'view'), post_pages=(), good_roles=['public'], bad_roles=[])

        # Special urls for file and folder deletion
        # File and folder doesn't actually have to exist for pages to render ok
        # TODO: calling test_permissions buggers up url_for calls... :(
        upload_url = url_for(controller="db_content", action="upload", folder="test_perms")
        urls = (
                url_for(controller="db_content", action="delete_file", file="dummy.file", folder="test_perms"),
                url_for(controller="db_content", action="delete_folder", current_path="twitchy", folder="test_perms"),
               )

        CrudHelper.test_permissions(self, app, db_session,
                get_pages=urls, post_pages=urls,
        )

        # TODO: Test upload - needs extra post arguments


    def test_new(self, app, db_session):
        start_time = datetime.now()

        data = {
                "title"        : "Bob is here",
                "type"         : self.page_type.id,
                "url"          : "ftp://bobsworld.de/fredlike/steve.bob",
                "body"         : "He made it, at last, it's what's his name",
               }

        def extra_form_check(form):
            assert "db_content.publish_date" in form.fields
            assert "db_content.publish_time" in form.fields

        def extra_form_set(form):
            form["db_content.publish_date"] = "12/05/99"
            form["db_content.publish_time"] = "01:03:05"

        def extra_data_check(new):
            assert getattr(new, 'publish_timestamp').isoformat() == "1999-05-12T01:03:05"
            current_time = datetime.now()
            # Both creation and last_modification timestamp should be between the test start and now
            assert getattr(new, 'creation_timestamp') >= start_time
            assert getattr(new, 'creation_timestamp') <= current_time
            assert getattr(new, 'last_modification_timestamp') >= start_time
            assert getattr(new, 'last_modification_timestamp') <= current_time

        CrudHelper.test_new(self, app, db_session, title="Add a new page", next_url=url_for(controller='db_content', action='view', id=1), data=data, extra_form_check=extra_form_check, extra_form_set=extra_form_set, extra_data_check=extra_data_check)


    def test_view(self, app, db_session):
        target = DbContentFactory()
        # Lots of detail, like timestamps, is not displayed
        expected = [target.title, target.body]

        CrudHelper.test_view(self, app, db_session, title="", target=target, expected=expected)


    def test_index(self, app, db_session):
        # Only get view links for News or Page entries
        content = [DbContentFactory(type=self.news_type) for i in range(10)]
        db_session.commit() # Lock in generated content like id
        entries = { c.id : (c.title, c.type.name, c.url) for c in content }

        CrudHelper.test_index(self, app, db_session, title="List of DB pages", entries=entries)

    def test_edit(self, app, db_session):
        db_content = DbContentFactory(type=self.news_type)
        db_session.commit() # Lock in generated content like id

        start_time = datetime.now()

        initial_values = {
                "type"      : str(db_content.type.id),
                "title"     : db_content.title,
                "url"       : db_content.url,
                }

        new_values = {
                "title"        : "Bob is here",
                "type"         : self.page_type.id,
                "url"          : "ftp://bobsworld.de/fredlike/steve.bob",
                "body"         : "He made it, at last, it's what's his name",
                }

        def extra_form_check(form):
            assert "db_content.publish_date" in form.fields
            assert "db_content.publish_time" in form.fields
            assert form["db_content.publish_date"].value == db_content.publish_timestamp.strftime('%d/%m/%y') # dd/mm/yy
            assert form["db_content.publish_time"].value == db_content.publish_timestamp.strftime('%H:%M:%S') # hh:mm:ss

        def extra_form_set(form):
            form["db_content.publish_date"] = "12/05/99"
            form["db_content.publish_time"] = "01:03:05"

        def extra_data_check(new):
            current_time = datetime.now()
            assert getattr(new, 'publish_timestamp').isoformat() == "1999-05-12T01:03:05"
            # creation timestamp should be before we start the edit process
            # last modification timestamp should be after, and before now
            assert getattr(new, 'creation_timestamp') <= start_time
            assert getattr(new, 'last_modification_timestamp') >= start_time
            assert getattr(new, 'last_modification_timestamp') <= current_time


        CrudHelper.test_edit(self, app, db_session, title="Edit page", initial_values=initial_values, new_values=new_values, extra_form_check=extra_form_check, target=db_content, next_url=url_for(controller='db_content', action='view', id=db_content.id))

    def test_delete(self, app, db_session):
        CrudHelper.test_delete(self, app, db_session, title="Delete Content")
