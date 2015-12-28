from datetime import datetime

from .crud_helper import CrudHelper
from .fixtures import FulfilmentFactory, FulfilmentTypeFactory, FulfilmentStatusFactory, PersonFactory, CompletePersonFactory


class TestFulfilment(CrudHelper):
    def test_permissions(self, app, db_session):
        # Some pages reference fulfilment statuses, by id
        for i in range(10):
            try:
                FulfilmentStatusFactory(id=i)
                db_session.commit()
            except:
                pass # id already exists - that's all we need

        # Manually inserting ids trips up the postgresql serial type, so we manually fix it
        # Hit sequence directly as it's easier to handle unset entries
        curr_id = db_session.execute("SELECT last_value FROM fulfilment_status_id_seq").scalar();
        if curr_id < 10:
            db_session.execute("SELECT setval('fulfilment_status_id_seq', 10)")

        # Can't test badge_pdf as it returns a non-html document
        # Can't test person as it uses a person id, not fulfilment
        CrudHelper.test_permissions(self, app, db_session, good_roles=['checkin'], get_pages=('badge_print', 'swag_give'), post_pages=[])
        CrudHelper.test_permissions(self, app, db_session)

    def test_new(self, app, db_session):
        types = [FulfilmentTypeFactory() for i in range(10)]
        statie = [FulfilmentStatusFactory(types=types) for i in range(10)]
        person = PersonFactory()
        db_session.commit()

        data = {
                "person" : person.id,
                "type"   : types[3].id,
                "status" : statie[6].id,
               }

        start_time = datetime.now()

        def extra_data_check(new):
            current_time = datetime.now()
            # Both creation and last_modification timestamp should be between the test start and now
            assert getattr(new, 'creation_timestamp') >= start_time
            assert getattr(new, 'creation_timestamp') <= current_time
            assert getattr(new, 'last_modification_timestamp') >= start_time
            assert getattr(new, 'last_modification_timestamp') <= current_time

        CrudHelper.test_new(self, app, db_session, data=data, extra_data_check=extra_data_check)

    def test_view(self, app, db_session):
        types = [FulfilmentTypeFactory() for i in range(10)]
        statie = [FulfilmentStatusFactory(types=types) for i in range(10)]
        ful = FulfilmentFactory(type=types[1], status=statie[9], code="idkfa", person=PersonFactory(firstname="John", lastname="23"))
        db_session.commit()
        expected = [ ful.person.fullname, ful.code, ful.status.name ]

        # TODO: Additional, item list

        CrudHelper.test_view(self, app, db_session, target=ful, expected=expected)

    def test_index(self, app, db_session):
        ff = [FulfilmentFactory(person=CompletePersonFactory()) for i in range(10)]
        db_session.commit()
        entries = { f.id : [f.person.fullname, str(f.id), f.type.name, f.status.name] for f in ff }

        CrudHelper.test_index(self, app, db_session, entries = entries)

    def test_edit(self, app, db_session):
        types = [FulfilmentTypeFactory() for i in range(10)]
        statie = [FulfilmentStatusFactory(types=types) for i in range(10)]
        p1 = PersonFactory()
        p2 = PersonFactory()
        ful = FulfilmentFactory(type=types[1], status=statie[9], person=p1)
        db_session.commit()

        initial_values = {
                "person"    : str(ful.person.id),
                "type"      : str(ful.type.id),
                "status"    : str(ful.status.id),
                }

        new_values = {
                "person" : p2.id,
                "type"   : types[3].id,
                "status" : statie[6].id,
               }

        start_time = datetime.now()

        def extra_data_check(new):
            current_time = datetime.now()
            # creation timestamp should be before we start the edit process
            # last modification timestamp should be after, and before now
            assert getattr(new, 'creation_timestamp') <= start_time
            assert getattr(new, 'last_modification_timestamp') >= start_time
            assert getattr(new, 'last_modification_timestamp') <= current_time

        CrudHelper.test_edit(self, app, db_session, initial_values=initial_values, new_values=new_values, target=ful, extra_data_check=extra_data_check)
