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
    m.connect('/media/news', controller='db_content', action='list_news', id=None)
    m.connect('/media/news/rss', controller='db_content', action='rss_news', id=None)
    m.connect('/media/news/:id', controller='db_content', action='view')
    m.connect('/media/in_the_press', controller='db_content', action='list_press', id=None)

    # DB content
    m.connect('/db_content/list_files', controller='db_content', action='list_files', id=None)
    m.connect('/db_content/delete_file', controller='db_content', action='delete_file', id=None)
    m.connect('/db_content/delete_folder', controller='db_content', action='delete_folder', id=None)
    m.connect('/db_content/upload', controller='db_content', action='upload', id=None)

    # Review
    m.connect('/proposal/review_index', controller='proposal', action='review_index', id=None)
    m.connect('/proposal/summary', controller='proposal', action='summary', id=None)
    m.connect('/review/summary', controller='review', action='summary', id=None)


    # hack the old error handler back in, using the style of the old
    # routes controller.  this is necessary to get the error handler
    # to not 404 when calling itself
    m.connect('/error/:action/:id', controller='error')

    # The CFP named routes
    #m.connect('cfp', '/cfp', controller='cfp', action='index')
    #m.connect('presentations', '/presentations', controller='cfp', action='index')
    #m.connect('submit_cfp', '/papers/submit_a_paper', controller='cfp', action='submit')
    #m.connect('submit_cfp', '/papers/submit_a_presentation', controller='cfp', action='submit')
    #m.connect('submit_cfp', '/presentations/submit_a_presentation', controller='cfp', action='submit')
    #m.connect('/papers/thankyou', controller='cfp', action='thankyou')
    #m.connect('/presentations/thankyou', controller='cfp', action='thankyou')
    #m.connect('submit_mini', '/mini-confs/submit_mini-conf_proposal', controller='cfp', action='submit_mini')
    #m.connect('/presentations/edit/:id', controller='proposal', action='edit')
    m.connect('/programme/edit_submission', controller='proposal', action='index')
    m.connect('/programme/edit_submission/:id', controller='proposal', action='view')
    m.connect('/programme/edit_submission/:id/edit', controller='proposal', action='edit')
    m.connect('/programme/submit_a_presentation', controller='proposal', action='submit')
    m.connect('/programme/submit_a_miniconf', controller='proposal', action='submit_mini')

    # Verify stuff from commsecure

    m.connect('/invoice/verify', controller='invoice', action='verify', id=None)

    # Invoice Reminder
    m.connect('/invoice/remind', controller='invoice', action='remind', id=None)
    m.connect('/registration/remind', controller='registration', action='remind', id=None)
    m.connect('/registration/status', controller='registration', action='status', id=None)
    m.connect('/registration/silly_description', controller='registration', action='silly_description', id=None)
    m.connect('/registration/volunteer', controller='registration', action='volunteer_redirect', id=None)
    m.connect('/registration/professional', controller='registration', action='professional', id=None)
    m.connect('/registration/list_miniconf_orgs', controller='registration', action='list_miniconf_orgs', id=None)

    # account confirmation named route
    m.connect('acct_confirm', '/person/confirm/:confirm_hash', controller='person', action='confirm')
    m.connect('/person/signin', controller='person', action='signin')
    m.connect('/person/signout', controller='person', action='signout')
    m.connect('/person/forgotten_password', controller='person', action='forgotten_password', id=None)
    m.connect('/person/reset_password/:url_hash', controller='person', action='reset_password')

    # admin controller
    m.connect('/admin/:action', controller='admin')
    m.connect('/programme/mini-confs/recorded', controller='admin', action='recorded_miniconf_talks')

    # OpenDay
    #m.connect('openday', '/OpenDay', controller='openday', action='new')
    #m.connect('/Openday', controller='openday', action='new')
    #m.connect('/openday', controller='openday', action='new')
    #m.connect('/openDay', controller='openday', action='new')
   
    #HACK: links from 08 keep on going to /openday and currently the controller is broken... Simply send a 404
    m.connect('openday', '/OpenDay', controller='not_found', action='page')
    m.connect('/Openday', controller='not_found', action='page')
    m.connect('/openday', controller='not_found', action='page')
    m.connect('/openDay', controller='not_found', action='page')

    #HACK: this is because of an incorrect link in the press release
    m.connect('/become_a_sponsor', controller='db_content', action='view', id=8)
    m.connect('/review/help', controller='db_content', action='view', id=25)

    # special case the wiki controller so that it's not gobbled by the
    # usual :controller rules...
    #m.connect('/wiki', controller='wiki', action='view', url='/wiki')
    #m.connect('/wiki/*sfx', controller='wiki', action='view_wiki')


    # Note to wary travellers; an ID can never be 'new' because of this
    # routing rule
    m.connect(':controller/new', action='new', id=None)
    m.connect(':controller', action='index', id=None)
    # default action when not specified is 'view'
    m.connect(':controller/:id', action='view')
    # default url scheme
    m.connect(':controller/:id/:action', action='index', id=None)

    # m.connect('*url', controller='wiki', action='view')
    m.connect('*url', controller='db_content', action='page', id=None)
    #m.connect('/db_content/view', controller='db_content', action='view', id=None)
    m.connect('*url', controller='not_found', action='page')

    return m
