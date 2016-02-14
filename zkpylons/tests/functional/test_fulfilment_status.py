from .crud_helper import CrudHelper
from .fixtures import FulfilmentStatusFactory, FulfilmentTypeFactory

class TestFulfilmentStatus(CrudHelper):
    def test_new(self, app, db_session):
        types = [FulfilmentTypeFactory() for i in range(10)]
        db_session.commit()

        data = {
                "name"      : "Jhonny",
                "void"      : True,
                "completed" : True,
                "locked"    : True,
                'types'     : [types[0].id, types[3].id, types[8].id],
               }

        CrudHelper.test_new(self, app, db_session, data=data)

    def test_view(self, app, db_session):
        types = [FulfilmentTypeFactory() for i in range(3)]
        target = FulfilmentStatusFactory(types=types)

        expected = [target.name, types[0].name, types[1].name, types[2].name]

        CrudHelper.test_view(self, app, db_session, target=target, expected=expected)

    def test_edit(self, app, db_session):
        types = [FulfilmentTypeFactory() for i in range(10)]
        target = FulfilmentStatusFactory(types=types)
        db_session.commit()

        initial_values = {
                "name"      : target.name,
                "void"      : None,
                "completed" : None,
                "locked"    : None,
                "types"     : [str(t.id) for t in types],
                }

        new_types = [types[0].id, types[3].id, types[8].id]
        new_values = {
                "name"      : "Jhonny",
                "void"      : True,
                "completed" : True,
                "locked"    : True,
                "types"     : [types[0].id, types[3].id, types[8].id],
               }

        CrudHelper.test_edit(self, app, db_session, initial_values=initial_values, new_values=new_values, target=target)
