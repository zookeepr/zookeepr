from .crud_helper import CrudHelper
from .fixtures import RegoNoteFactory, CompletePersonFactory, RegistrationFactory

class TestRegoNote(CrudHelper):
    def test_new(self, app, db_session):
        # NOTE: Manually specifying the ids on the form is crazy
        pers = CompletePersonFactory()
        rego = RegistrationFactory()
        db_session.commit()

        data = {
                "rego"    : rego.id,
                "note"    : "The red pill is a lie",
                "block"   : True,
                "by"      : pers.id,
               }

        CrudHelper.test_new(self, app, db_session, data=data, title="Add a new note")

    def test_view(self, app, db_session):
        target = RegoNoteFactory(by=CompletePersonFactory())
        db_session.commit()
        expected = [target.rego.person.fullname, target.by.fullname, target.note]
        CrudHelper.test_view(self, app, db_session, target=target, expected=expected, title="Viewing note")

    def test_index(self, app, db_session):
        groups = [RegoNoteFactory(by=CompletePersonFactory()) for i in range(10)]
        db_session.commit()
        entries = { s.id : [str(s.id), s.rego.person.fullname, s.by.fullname] for s in groups }

        CrudHelper.test_index(self, app, db_session, entries = entries, title="List of Registration Notes")

    def test_edit(self, app, db_session):
        peeps = [CompletePersonFactory() for i in range(10)]
        regos = [RegistrationFactory() for i in range(10)]
        target = RegoNoteFactory()
        db_session.commit()

        initial_values = {
                "rego"    : str(target.rego.id),
                "note"    : target.note,
                "block"   : target.block,
                "by"      : str(target.by.id),
                }

        new_values = {
                "rego"    : regos[7].id,
                "note"    : "The red pill is a lie",
                "block"   : True,
                "by"      : peeps[4].id,
               }

        CrudHelper.test_edit(self, app, db_session, new_values=new_values, initial_values=initial_values, target=target)
