from .fixtures import ProposalFactory, EventFactory, EventTypeFactory, ProposalStatusFactory
from .crud_helper import CrudHelper


class TestEvent(CrudHelper):
    def test_permissions(self, app, db_session):
        CrudHelper.test_permissions(self, app, db_session, additional_get_pages = 'new_proposals')

# TODO: new_proposals page

    def test_new(self, app, db_session):
        # Proposals must be accepted but without event
        accepted = ProposalStatusFactory(name='Accepted')
        props = [ProposalFactory(status = accepted, event = None) for i in range(10)]
        types = [EventTypeFactory() for i in range(10)]

        data = {
                "type"      : types[8].id,
                "proposal"  : props[3].id,
                "title"     : "test_new",
                "url"       : "http://rickroll.com",
                "publish"   : True,
                "exclusive" : True,
               }

        def extra_form_check(form):
            # Both have an initial extra "None" field
            assert len(form.fields['event.type'][0].options) == 10+1
            assert len(form.fields['event.proposal'][0].options) == 10+1

        CrudHelper.test_new(self, app, db_session, data=data, extra_form_check = extra_form_check)

        # TODO: Invalid content


    def test_view(self, app, db_session):
        accepted = ProposalStatusFactory(name='Accepted')
        event = EventFactory(proposal = ProposalFactory(status = accepted), title="Here is Johnny", url="http://where.is.wally?")

        # TODO: Timeslot, location, schedule

        expected = [event.type.name, event.title, event.url]
        print expected

        view1 = CrudHelper.test_view(self, app, db_session, expected=expected, target=event)

    def test_index(self, app, db_session):
        events = [EventFactory(title = "test_index %i banananas" % i) for i in range(10)]
        db_session.commit()
        entries = { ev.id : [ev.title, ev.type.name] for ev in events }

        CrudHelper.test_index(self, app, db_session, entries = entries)

    def test_edit(self, app, db_session):
        # TODO: Invalid content

        accepted = ProposalStatusFactory(name='Accepted')
        props = [ProposalFactory(status = accepted, event = None) for i in range(10)]
        types = [EventTypeFactory() for i in range(10)]
        event = EventFactory(proposal = props[9], type = types[8], title="Here is Johnny", url="http://where.is.wally?")

        db_session.commit()

        initial_values = {
            "type"      : str(event.type.id),
            "proposal"  : str(event.proposal.id),
            "title"     : event.title,
            "url"       : event.url,
            "publish"   : "1" if event.publish else "0",
            "exclusive" : str(int(event.exclusive)),
        }

        new_values = {
            "type"      : types[6].id,
            "proposal"  : props[3].id,
            "title"     : "test_new",
            "url"       : "http://rickroll.com",
            "publish"   : True,
            "exclusive" : True,
        }

        def extra_form_check(form):
            # Both have an initial extra "None" field
            assert len(form.fields['event.type'][0].options) == 10+1
            assert len(form.fields['event.proposal'][0].options) == 10+1

        CrudHelper.test_edit(self, app, db_session, initial_values=initial_values, new_values=new_values, extra_form_check=extra_form_check, target=event)
