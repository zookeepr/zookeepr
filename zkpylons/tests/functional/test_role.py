from routes import url_for

from zk.model.role import Role

from .fixtures import PersonFactory, RoleFactory
from .utils import do_login


class TestRole(object):

    def test_create(self, app, db_session):
        p = PersonFactory(
                roles = [RoleFactory(name="organiser")],
                # Set full set of detail to avoid incomplete profile flag
                firstname = 'Testguy',
                lastname  = 'McTest',
                i_agree   = True,
                activated = True,
                address1  = 'Somewhere',
                city      = 'Over the rainbow',
                postcode  = 'Way up high',
                )
        db_session.commit()

        do_login(app, p)
        resp = app.get(url_for(controller='role', action='new'))
        f = resp.form
        f['role.name']          = 'newrole'
        f['role.pretty_name']   = 'Test created role'
        f['role.comment']       = 'I understand why people generate this'
        f['role.display_order'] = 23
        resp = f.submit()
        resp = resp.follow() # Failure indicates form validation error

        assert 'Missing value' not in unicode(resp.body, 'utf-8')

        # Test creation
        db_session.expunge_all()

        roles = Role.find_all()
        assert len(roles) == 2 # organiser and created one

        new_role = roles[1] if roles[0].name == "organiser" else roles[0]

        assert new_role.name == 'newrole'
        assert new_role.pretty_name == 'Test created role'
        assert new_role.comment == 'I understand why people generate this'
        assert new_role.display_order == 23

    def test_index(self, app, db_session):
        p = PersonFactory(
                roles = [RoleFactory(name="organiser")],
                # Set full set of detail to avoid incomplete profile flag
                firstname = 'Testguy',
                lastname  = 'McTest',
                i_agree   = True,
                activated = True,
                address1  = 'Somewhere',
                city      = 'Over the rainbow',
                postcode  = 'Way up high',
                )
        r2 = RoleFactory()
        r3 = RoleFactory()
        r4 = RoleFactory()
        r5 = RoleFactory()
        db_session.commit()

        do_login(app, p)
        resp = app.get(url_for(controller='role', action='index'))

        assert "organiser" in unicode(resp.body, 'utf-8')
        assert r2.name in unicode(resp.body, 'utf-8')
        assert r3.name in unicode(resp.body, 'utf-8')
        assert r4.name in unicode(resp.body, 'utf-8')
        assert r5.name in unicode(resp.body, 'utf-8')
