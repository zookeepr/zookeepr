from .crud_helper import CrudHelper
from .fixtures import FulfilmentStatusFactory, FulfilmentTypeFactory

class TestFulfilmentType(CrudHelper):
    def test_new(self, app, db_session):
        statie = [FulfilmentStatusFactory() for i in range(10)]
        db_session.commit()

        data = {
                "name"           : "Jhonny",
                "initial_status" : statie[5].id,
                'status'         : [statie[0].id, statie[3].id, statie[8].id]
               }

        CrudHelper.test_new(self, app, db_session, data=data)

    def test_view(self, app, db_session):
        statie = [FulfilmentStatusFactory() for i in range(3)]
        target = FulfilmentTypeFactory(status=statie)
        db_session.commit()

        expected = [target.name, statie[0].name, statie[1].name, statie[2].name]
        CrudHelper.test_view(self, app, db_session, target=target, expected=expected)

    def test_edit(self, app, db_session):
        statie = [FulfilmentStatusFactory() for i in range(10)]
        target = FulfilmentTypeFactory(initial_status=statie[2], status=statie)
        db_session.commit()

        initial_values = {
                "name"      : target.name,
                "initial_status" : str(statie[2].id),
        }

        new_status = [statie[0].id, statie[3].id, statie[8].id]
        new_values = {
                "name"      : "Jhonny",
                "initial_status" : statie[7].id,
               }

        def extra_form_check(form):
            assert 'fulfilment_type.status' in form.fields
            assert len(form['fulfilment_type.status'].value) == len(statie)
            assert form['fulfilment_type.status'].value.sort() == [str(s.id) for s in statie].sort()

        def extra_form_set(form):
            form['fulfilment_type.status'] = new_status

        def extra_data_check(new):
            new_stat_ids = [t.id for t in new.status]
            assert len(new_stat_ids) == len(new_status)
            for id in new_status:
                assert id in new_stat_ids

        CrudHelper.test_edit(self, app, db_session, initial_values=initial_values, new_values=new_values, extra_form_check=extra_form_check, extra_form_set=extra_form_set, extra_data_check=extra_data_check, target=target)
