"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper

def make_map():
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE

    # the top level controller is named home
    map.connect('home', '/', controller='home')

    map.connect('/media/news',         controller='db_content', action='list_news', id=None)
    map.connect('/media/news/rss',     controller='db_content', action='rss_news', id=None)
    map.connect('/media/news/{id}',    controller='db_content', action='view')
    map.connect('/media/in_the_press', controller='db_content', action='list_press', id=None)

    # DB content
    map.connect('/db_content/list_files',    controller='db_content', action='list_files', id=None)
    map.connect('/db_content/delete_file',   controller='db_content', action='delete_file', id=None)
    map.connect('/db_content/delete_folder', controller='db_content', action='delete_folder', id=None)
    map.connect('/db_content/upload',        controller='db_content', action='upload', id=None)

    # Schedule
    map.connect('/schedule/{day}', controller='schedule', day=None)

    # Review
    map.connect('/proposal/review_index', controller='proposal', action='review_index', id=None)
    map.connect('/proposal/summary',      controller='proposal', action='summary', id=None)
    map.connect('/review/summary',        controller='review', action='summary', id=None)

    # The CFP named routes
    map.connect('/programme/edit_submission',           controller='proposal', action='index')
    map.connect('/programme/edit_submission/{id}',      controller='proposal', action='view')
    map.connect('/programme/edit_submission/{id}/edit', controller='proposal', action='edit')
    map.connect('/programme/submit_a_presentation',     controller='proposal', action='submit')
    map.connect('/programme/submit_a_miniconf',         controller='proposal', action='submit_mini')

    # schedule routes
    map.connect('/programme/schedule/{day}',           controller='schedule', action='index', day=None)
    map.connect('/programme/schedule/view_talk/{id}', controller='schedule', action='view_talk', id=None)

    # Invoice Reminder
    map.connect('/invoice/pdf/{id}',               controller='invoice', action='pdf', id=None)
    #map.connect('/invoice/remind',                 controller='invoice', action='remind', id=None)
    #map.connect('/registration/remind',            controller='registration', action='remind', id=None)
    map.connect('/register/status',                controller='registration', action='status', id=None)
    map.connect('/registration/silly_description', controller='registration', action='silly_description', id=None)
    map.connect('/registration/generate_badges',   controller='registration', action='generate_badges', id=None)

    # account confirmation named route
    map.connect('acct_confirm', '/person/confirm/{confirm_hash}', controller='person', action='confirm')
    map.connect('/person/signin',                    controller='person', action='signin')
    map.connect('/person/signout',                   controller='person', action='signout')
    map.connect('/person/forgotten_password',        controller='person', action='forgotten_password')
    map.connect('/person/reset_password/{url_hash}', controller='person', action='reset_password')

    # admin controller
    map.connect('/admin/{action}', controller='admin')

    # OpenDay
    #map.connect('openday', '/OpenDay', controller='openday', action='new')
    #map.connect('/Openday', controller='openday', action='new')
    #map.connect('/openday', controller='openday', action='new')
    #map.connect('/openDay', controller='openday', action='new')

    #HACK: links from 08 keep on going to /openday and currently the controller is broken... Simply send a 404
    map.connect('openday', '/OpenDay', controller='not_found', action='page')
    map.connect('/Openday', controller='not_found', action='page')
    map.connect('/openday', controller='not_found', action='page')
    map.connect('/openDay', controller='not_found', action='page')

    #HACK: Alias' for db_content pages. Due to the news route the menu will display the wrong thing. These are only here incase somebody mis-links.
    #HACK: this is because of an incorrect link in the press release
    map.connect('/become_a_sponsor', controller='db_content', action='view', id=8)
    map.connect('/review/help', controller='db_content', action='view', id=25)
    map.connect('/sponsors/google_diversity_programme', controller='db_content', action='view', id=66)
    map.connect('/sponsors', controller='db_content', action='view', id=61)
    map.connect('/register', controller='db_content', action='view', id=45)
    map.connect('/programme', controller='db_content', action='view', id=3)

    # special case the wiki controller so that it's not gobbled by the
    # usual {controller} rules...
    #map.connect('/wiki', controller='wiki', action='view', url='/wiki')
    #map.connect('/wiki/*sfx', controller='wiki', action='view_wiki')

    # route rego_notes with ID's
    map.connect('registration/{rego_id}/new_note', controller='rego_note', action='new', id=None)

    # Note to wary travellers; an ID can never be 'new' because of this
    # routing rule
    map.connect('/{controller}/new', action='new')
    map.connect('/{controller}/new_submit', action='new_submit')
    map.connect('/{controller}', action='index')

    # default action when not specified is 'view'
    map.connect('/{controller}/{id}', action='view')
    # default url scheme
    map.connect('/{controller}/{id}/{action}')

    # map.connect('*url', controller='wiki', action='view')
    #FIXME map.connect('*url', controller='db_content', action='page', id=None)
    #map.connect('/db_content/view', controller='db_content', action='view', id=None)
    #FIXME map.connect('*url', controller='not_found', action='page')

    return map
