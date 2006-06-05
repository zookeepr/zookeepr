from pylons import h
from sqlalchemy import create_session

from zookeepr.models import Person

def profile_url(email_address):
    """Retrieve the url for a person's profile, given only their email address"""
    session = create_session()
    users = session.query(Person).select_by(email_address=email_address)
    user = users[0]

    if user.handle is not None:
        key = user.handle
    else:
        key = user.id

    return h.url_for(controller='person', action='view', id=key)
