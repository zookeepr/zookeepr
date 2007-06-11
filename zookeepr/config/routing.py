"""
Setup your Routes options here
"""
import sys, os
from routes import Mapper

def make_map():
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    m = Mapper(directory=os.path.join(root_path, 'controllers'))
    
    # Define your routes. The more specific and detailed routes should be defined first,
    # so they may take precedent over the more generic routes. For more information, refer
    # to the routes manual @ http://routes.groovie.org/docs/

    # the top level controller is named home
    m.connect('home', '', controller='home')

    # hack the old error handler back in, using the style of the old
    # routes controller.  this is necessary to get the error handler
    # to not 404 when calling itself
    m.connect('/error/:action/:id', controller='error')

    # The CFP named routes
    m.connect('cfp', '/cfp', controller='cfp', action='index')
    m.connect('submit_cfp', '/cfp/submit', controller='cfp', action='submit')
    m.connect('/cfp/thankyou', controller='cfp', action='thankyou')

    # account confirmation named route
    m.connect('acct_confirm', '/account/confirm/:id',
              controller='account',
              action='confirm')

    # Verify stuff from commsecure
    m.connect('/invoice/verify', controller='invoice', action='verify', id=None)

    # Invoice Reminder
    m.connect('/invoice/remind', controller='invoice', action='remind', id=None)
    m.connect('/registration/remind', controller='registration', action='remind', id=None)

    # special case for account controller, again in the style of the
    # original routes controller
    m.connect('/account/:action', controller='account')
    m.connect('/account/reset_password/:url_hash', controller='account', action='reset_password')

    # OpenDay
    m.connect('openday', '/OpenDay', controller='openday', action='new')
    m.connect('/Openday', controller='openday', action='new')
    m.connect('/openday', controller='openday', action='new')
    m.connect('/openDay', controller='openday', action='new')
    
    m.connect('/proposal/summary', controller='proposal', action='summary', id=None)

    # Note to wary travellers; an ID can never be 'new' because of this
    # routing rule
    m.connect(':controller/new', action='new', id=None)
    m.connect(':controller', action='index', id=None)
    # default action when not specified is 'view'
    m.connect(':controller/:id', action='view')
    # default url scheme
    m.connect(':controller/:id/:action', action='index', id=None)

    m.connect('*url', controller='template', action='view')

    return m
