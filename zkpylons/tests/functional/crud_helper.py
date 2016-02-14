from routes import url_for

import sqlalchemy
from BeautifulSoup import BeautifulSoup

import re
from random import randint

import zk.model

from . import fixtures
from .fixtures import PersonFactory, RoleFactory
from .utils import do_login

camel2snake_re = re.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')
def camel2snake(camel):
    # From http://stackoverflow.com/a/12867228/2438650
    return camel2snake_re.sub(r'_\1', camel).lower()

def snake2camel(snake):
    camel = snake.replace("_", " ")
    camel = camel.title() # Titles every word
    return camel.replace(" ", "")

def get_simple_columns(base):
    # Get simple columns
    # Base can be either a SQLAlchemy class or object
    columns = []
    for c in base.__table__.columns:
        if len(c.foreign_keys): continue # No foreign key ids
        if c.name == 'id': continue # Our id typically isn't included
        # Checking against parent/category types
        if (
            isinstance(c.type, sqlalchemy.sql.sqltypes.String) or
            isinstance(c.type, sqlalchemy.types.Integer) or
            isinstance(c.type, sqlalchemy.types.Boolean)
           ):
            columns.append(c)
        else:
            print "Skipping", c.name, str(c.type), type(c.type), c.type.__dict__
    return columns

def get_target_entries(target):
    columns = get_simple_columns(target)
    target_entries = []
    for c in columns:
        val = getattr(target, c.name)
        if val is None:
            pass # Ignore
        elif isinstance(c.type, sqlalchemy.sql.sqltypes.String):
            target_entries.append(val)
        elif isinstance(c.type, sqlalchemy.types.Integer):
            target_entries.append(str(val))
        elif isinstance(c.type, sqlalchemy.types.Boolean):
            pass # booleans are often rendered as checkboxes, so we ignore
    return target_entries

class CrudHelper(object):
    @classmethod
    def _get_insert_role(self, name):
        # Often want to use a specific role, typically by creating it
        # But as the name is unique this causes a db clash and failure
        # This function returns the requested role, inserting if required

        # NOTE: This function is designed to protect against repeated crud function calls
        #       It will not protect against multiple calls within the same function.
        #       Specifically, commit() must be run between calls to be safe
        role = zk.model.Role.find_by_name(name, abort_404=False)
        if role is None:
            role = RoleFactory(name=name)
        return role

    def _conv_data(self, data):
        if not isinstance(data, (basestring, bytes)):
            try:
                return [self._conv_data(entry) for entry in data]
            except TypeError:
                pass # Not iterable

        try:
            sqlalchemy.inspection.inspect(data) # Will throw exception if not SQLAlchemy object
            # Is SQLAlchemy object, comparison is done based on the id
            return data.id
        except:
            pass

        return data

    
    def test_permissions(self, app, db_session,
            controller = None, page_id = None, target=None, target_class=None,
            good_roles = ['organiser'], bad_roles = None,
            get_pages = ('new', 'view', 'index', 'edit', 'delete'),
            post_pages = ('new', 'edit', 'delete'),
            additional_get_pages = None, additional_post_pages = None,
            dont_get_pages = None, dont_post_pages = None,
            good_pers = None, bad_pers = None,
        ):

        if controller is None:
            # Set controller based on name of child class
            class_name = self.__class__.__name__
            assert class_name.startswith("Test") # Check it is of correct form
            controller = camel2snake(class_name[4:])

        # TODO: Verbose failure messages
        all_roles = ['organiser', 'team', 'reviewer',
                     'miniconf', 'proposals_chair', 'late_submitter',
                     'funding_reviewer', 'press', 'miniconfsonly',
                     'public'
                    ]

        if bad_roles is None:
            bad_roles = [n for n in all_roles if n not in good_roles]

        # Public is a special role, for non-logged in users
        if 'public' in good_roles and 'public' in bad_roles:
            raise Exception("public role cannot be both good and bad")
        elif 'public' in good_roles:
            good_roles.remove('public')
            public_good = True
        elif 'public' in bad_roles:
            bad_roles.remove('public')
            public_good = False
        else:
            public_good = None # Skip test

        if good_pers is None:
            good_pers = PersonFactory(roles = [self._get_insert_role(name=n) for n in good_roles])
        if bad_pers is None:
            bad_pers = PersonFactory(roles = [self._get_insert_role(name=n) for n in bad_roles])

        db_session.commit()

        if page_id is None:
            if target is None:
                # Base class off controller
                target = eval("fixtures." + snake2camel(controller) + "Factory()")
                db_session.commit()
            page_id = target.id

        if additional_get_pages is not None:
            if isinstance(additional_get_pages, basestring):
                get_pages = get_pages + (additional_get_pages,)
            else:
                get_pages = get_pages + additional_get_pages

        if additional_post_pages is not None:
            if isinstance(additional_post_pages, basestring):
                post_pages = post_pages + (additional_post_pages,)
            else:
                post_pages = post_pages + additional_post_pages

        if dont_get_pages is not None:
            if isinstance(dont_get_pages, basestring):
                dont_get_pages = [dont_get_pages]
            get_pages = [p for p in get_pages if p not in dont_get_pages]
        
        if dont_post_pages is not None:
            if isinstance(dont_post_pages, basestring):
                dont_post_pages = [dont_post_pages]
            post_pages = [p for p in post_pages if p not in dont_post_pages]
        

        db_session.commit()

        def do_page(page, method, status=None, **kwargs):
            if "/" in page:
                url = page
            else:
                url = url_for(controller=controller, action=page, id=page_id)
            if method == "GET":
                resp = app.get(url, status="*", **kwargs)
            elif method == "POST":
                resp = app.post(url, status="*", **kwargs)
            print method, url, "want", ("good" if status is None else status), "got", resp.status_code

            status_response = resp.status_code
            if resp.status_code == 200 and "Otherwise enter your credentials in the following form." in unicode(resp.body, 'utf-8'):   
                # Not logged in, log in required - should really be a 401
                status_response = 401

            if status is None:
                # Allow 2XX or 3XX response - same as WebTest default
                assert status_response >= 200
                assert status_response < 400
            else:
                assert status_response == status


        if len(good_roles):
            do_login(app, good_pers)
            for page in get_pages:
                do_page(page=page, method="GET")
            for page in post_pages:
                do_page(page=page, method="POST")

        if len(bad_roles):
            do_login(app, bad_pers)
            for page in get_pages:
                do_page(page=page, method="GET", status=403)
            for page in post_pages:
                do_page(page=page, method="POST", status=403)

        if public_good is not None:
            # Override cookies to disable login state
            for page in get_pages:
                do_page(page=page, method="GET", headers={'Cookie':''}, status=(None if public_good else 401))
            for page in post_pages:
                do_page(page=page, method="POST", headers={'Cookie':''}, status=(None if public_good else 401))
            
    def test_new(self, app, db_session,
            data = None, controller = None, user = None,
            target_class = None, title = None, form_prefix = None, next_url = None,
            do_form_check = True, do_form_set = True, do_data_check = True,
            extra_form_check = None, extra_form_set = None, extra_data_check = None
        ):

        if user is None:
            # Don't care about permissions, just run as organiser
            user = PersonFactory(roles = [self._get_insert_role('organiser')])

        if controller is None:
            # Set controller based on name of child class
            class_name = self.__class__.__name__
            assert class_name.startswith("Test") # Check it is of correct form
            controller = camel2snake(class_name[4:])

        if target_class is None:
            # Base class off controller
            target_class = eval("zk.model." + snake2camel(controller))

        if title is None:
            # Generate title from controller name
            title = "New " + controller.replace("_", " ").title()

        if form_prefix is None:
            # Could base off target_class or controller
            # Using controller for now as it is easier
            form_prefix = controller

        if len(form_prefix):
            # Len check allows us to set form_prefix to '' and do it manually
            form_prefix = form_prefix + "."

        if data is None:
            # Generate data based on table data
            columns = get_simple_columns(target_class)

            data = {}
            for c in columns:
                rand = randint(1,1000)
                if isinstance(c.type, sqlalchemy.sql.sqltypes.String):
                    data[c.name] = "Gen%i" % rand
                elif isinstance(c.type, sqlalchemy.types.Integer):
                    data[c.name] = rand
                elif isinstance(c.type, sqlalchemy.types.Boolean):
                    data[c.name] = (rand%2 == 2)
                else:
                    print "WARNING: Unknown type %s" % str(c.type)
                    # Try string...
                    data[c.name] = "Unk%i" % rand
            print "Generated data", data

        if next_url is None:
            # Default is to go back to the index
            next_url = url_for(controller=controller, action='index', id=None)

        db_session.commit()
        start_count = len(target_class.find_all())

        do_login(app, user)

        resp = app.get(url_for(controller=controller, action='new'))
        
        assert title in unicode(resp.body, 'utf-8')
        f = resp.form
        assert f.action == url_for(controller=controller, action='new')

        if do_form_check:
            for k in data:
                assert form_prefix+k in f.fields

        if extra_form_check is not None:
            extra_form_check(f)

        if do_form_set:
            for k in data:
                f[form_prefix+k] = data[k]

        if extra_form_set is not None:
            extra_form_set(f)

        post_resp = f.submit()
        assert post_resp.status_code == 302, BeautifulSoup(post_resp.body).find(id="flash")
        assert next_url in post_resp.location

        db_session.expunge_all()

        assert start_count + 1 == len(target_class.find_all())
        new = sorted(target_class.find_all(), key=lambda o: o.id)[-1]

        if do_data_check:
            for k in data:
                val = getattr(new, k)
                val = self._conv_data(val)
                assert val == data[k], "%s == %s, %s" % (val, data[k], k)

        if extra_data_check is not None:
            extra_data_check(new)
        
        return resp

    def test_index(self, app, db_session,
                controller = None, title = None, user = None,
                target_class = None, entries = None,
                entry_actions = ('view', 'edit', 'delete'), page_actions = ('new',)
            ):

        # Entries - is a dictionary, key is page id, value is text to search for

        if user is None:
            # Don't care about permissions, just run as organiser
            user = PersonFactory(roles = [self._get_insert_role('organiser')])

        if controller is None:
            # Set controller based on name of child class
            class_name = self.__class__.__name__
            assert class_name.startswith("Test") # Check it is of correct form
            controller = camel2snake(class_name[4:])

        if title is None:
            # Generate title from controller name
            title = "List " + controller.replace("_", " ").title()

        # Extract and test for the easy to process data
        if True:
        #if entries is None:
            # We only use target_class to generate entries
            if target_class is None:
                # Base class off controller
                target_class = eval("zk.model." + snake2camel(controller))


            columns = get_simple_columns(target_class)

            print "TEST COLUMNS", [(c.name, str(c.type)) for c in columns]

            if entries is None:
                factory = eval("fixtures." + target_class.__name__ + "Factory")
                targets = [factory() for i in range(10)]

                db_session.commit()

                entries = { t.id : get_target_entries(t) for t in targets }
                print "Generated entries", entries

        db_session.commit()

        do_login(app, user)
        resp = app.get(url_for(controller=controller, action='index'))
        assert title in unicode(resp.body, 'utf-8')

        for pageid in entries:
            if isinstance(entries[pageid], basestring):
                assert entries[pageid] in unicode(resp.body, 'utf-8')
            else:
                for expected in entries[pageid]:
                    assert expected in unicode(resp.body, 'utf-8')
            for act in entry_actions:
                assert url_for(controller=controller, action=act,   id=pageid) in unicode(resp.body, 'utf-8')
        for act in page_actions:
            assert url_for(controller=controller, action=act) in unicode(resp.body, 'utf-8')

        return resp


    def test_view(self, app, db_session,
            expected=None, url=None, target=None, controller=None, title=None, user=None):

        if user is None:
            # Don't care about permissions, just run as organiser
            user = PersonFactory(roles = [self._get_insert_role('organiser')])

        if controller is None:
            # Set controller based on name of child class
            class_name = self.__class__.__name__
            assert class_name.startswith("Test") # Check it is of correct form
            controller = camel2snake(class_name[4:])

        if title is None and controller is not None:
            # Generate title from controller name
            title = "View " + controller.replace("_", " ").title()

        # Don't always need a target
        if target is None and (expected is None or url is None):
            # Base class off controller
            target = eval("fixtures." + snake2camel(controller) + "Factory()")

        db_session.commit()

        # Extract and test for the easy to process data
        if expected is None:
            expected = get_target_entries(target)
            print "Gen expected", expected

        if url is None:
            url = url_for(controller=controller, action='view', id=target.id)

        do_login(app, user)
        resp = app.get(url)
        print resp

        if title is not None:
            assert title in unicode(resp.body, 'utf-8')
        for entry in expected:
            assert str(entry) in unicode(resp.body, 'utf-8')

        return resp


    def test_edit(self, app, db_session,
            initial_values = None, new_values = None,
            controller = None, pageid = None, target = None,
            title = None, target_class = None, form_prefix = None,
            next_url = None, user = None,
            do_form_check = True, do_form_set = True, do_data_check = True,
            extra_form_check = None, extra_form_set = None, extra_data_check = None,
            ):

        if user is None:
            # Don't care about permissions, just run as organiser
            user = PersonFactory(roles = [self._get_insert_role('organiser')])

        if controller is None:
            # Set controller based on name of child class
            class_name = self.__class__.__name__
            assert class_name.startswith("Test") # Check it is of correct form
            controller = camel2snake(class_name[4:])

        if title is None:
            # Generate title from controller name
            title = "Edit " + controller.replace("_", " ").title()
        
        if target_class is None:
            # Base class off controller
            target_class = eval("zk.model." + snake2camel(controller))

        if form_prefix is None:
            # Could base off target_class or controller
            # Using controller for now as it is easier
            form_prefix = controller

        if len(form_prefix):
            # Len check allows us to set form_prefix to '' and do it manually
            form_prefix = form_prefix + "."

        if next_url is None:
            # Default is to go back to the index
            next_url = url_for(controller=controller, action='index', id=None)

        if initial_values is None or new_values is None:
            columns = get_simple_columns(target_class)

        if target is None and initial_values is None:
            # Generate initial values based on target - need a target
            target = eval("fixtures." + target_class.__name__ + "Factory()")
            db_session.commit()

        if initial_values is None:
            # Generate initial values based on target
            initial_values = { c.name : str(getattr(target, c.name)) for c in columns }
            for k in initial_values:
                if initial_values[k] == 'None':  initial_values[k] = ''
                if initial_values[k] == 'True':  initial_values[k] = '1'
                if initial_values[k] == 'False': initial_values[k] = None
            print "Generated initial values", initial_values

        if new_values is None:
            # Note code is duplicated with test_new
            data = {}
            for c in columns:
                rand = randint(1,1000)
                if isinstance(c.type, sqlalchemy.sql.sqltypes.String):
                    data[c.name] = "Gen%i" % rand
                elif isinstance(c.type, sqlalchemy.types.Integer):
                    data[c.name] = rand
                elif isinstance(c.type, sqlalchemy.types.Boolean):
                    data[c.name] = (rand%2 == 2)
                else:
                    print "WARNING: Unknown type %s" % str(c.type)
                    # Try string...
                    data[c.name] = "Unk%i" % rand
            new_values = data
            print "Generated new values", new_values

        if pageid is None:
            pageid = target.id

        db_session.commit()
        start_count = len(target_class.find_all())

        do_login(app, user)

        resp = app.get(url_for(controller=controller, action='edit', id=pageid))
        
        assert title in unicode(resp.body, 'utf-8')
        f = resp.form
        assert f.action == url_for(controller=controller, action='edit', id=pageid)

        if do_form_check:
            for k in initial_values:
                assert form_prefix + k in f.fields

            for k in initial_values:
                if isinstance(initial_values[k], bool):
                    assert f[form_prefix+k].value == ('1' if initial_values[k] else None)
                elif isinstance(initial_values[k], list):
                    assert f[form_prefix+k].value.sort() == initial_values[k].sort()
                else:
                    assert f[form_prefix+k].value == initial_values[k]

        if extra_form_check is not None:
            extra_form_check(f)

        if do_form_set:
            for k in new_values:
                f[form_prefix+k] = new_values[k]

        if extra_form_set is not None:
            extra_form_set(f)

        resp = f.submit()
        assert resp.status_code == 302, BeautifulSoup(resp.body).find(id="flash")

        db_session.expunge_all()
        assert start_count == len(target_class.find_all())
        new = sorted(target_class.find_all(), key=lambda o: o.id)[-1]
        assert next_url in resp.location

        if do_data_check:
            for k in new_values:
                val = getattr(new, k)
                val = self._conv_data(val)
                assert val == new_values[k], "%s == %s, %s" % (val, new_values[k], k)

        if extra_data_check is not None:
            extra_data_check(new)

        return resp

    def test_delete(self, app, db_session,
            controller = None, target = None,
            title = None, target_class = None, next_url = None, user = None,
            ):

        if user is None:
            # Don't care about permissions, just run as organiser
            user = PersonFactory(roles = [self._get_insert_role('organiser')])

        if controller is None:
            # Set controller based on name of child class
            class_name = self.__class__.__name__
            assert class_name.startswith("Test") # Check it is of correct form
            controller = camel2snake(class_name[4:])

        if title is None:
            # Generate title from controller name
            title = "Delete " + controller.replace("_", " ").title()

        if target_class is None:
            if target is None:
                # Base class off controller
                target_class = eval("zk.model." + snake2camel(controller))
            else:
                # Base class off target
                target_class = eval("zk.model." + target.__class__.__name__)

        if target is None:
            target = eval("fixtures." + target_class.__name__ + "Factory()")

        if next_url is None:
            # Default is to go back to the index
            next_url = url_for(controller=controller, action='index', id=None)
        
        db_session.commit()
        start_count = len(target_class.find_all())

        do_login(app, user)
        resp = app.get(url_for(controller=controller, action='delete', id=target.id))

        assert title in unicode(resp.body, 'utf-8')
        assert "Are you sure" in unicode(resp.body, 'utf-8')

        f = resp.form
        post_resp = f.submit()
        assert post_resp.status_code == 302, BeautifulSoup(post_resp.body).find(id="flash")
        assert next_url in post_resp.location

        db_session.expunge_all()
        assert start_count-1 == len(target_class.find_all())

        return resp
