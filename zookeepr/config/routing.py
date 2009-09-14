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

    map.connect('/media/news',         controller='db_content', action='list_news')
    map.connect('/media/news/rss',     controller='db_content', action='rss_news')
    map.connect('/media/news/{id}',    controller='db_content', action='view')
    map.connect('/media/in_the_press', controller='db_content', action='list_press')

    map.connect('/sitemap',            controller='sitemap', action='view')

    # DB content
    map.connect('/db_content/list_files',    controller='db_content', action='list_files', id=None)
    map.connect('/db_content/delete_file',   controller='db_content', action='delete_file', id=None)
    map.connect('/db_content/delete_folder', controller='db_content', action='delete_folder', id=None)
    map.connect('/db_content/upload',        controller='db_content', action='upload', id=None)

    # Schedule
    map.connect('/schedule/{day}', controller='schedule', day=None)

    # Proposal submission
    map.connect('/programme/submit_a_miniconf', controller='miniconf_proposal', action='new')
    map.connect('/programme/submit_a_paper',    controller='proposal', action='new')

    # Review
    map.connect('/proposal/review_index', controller='proposal', action='review_index')
    map.connect('/proposal/summary',      controller='proposal', action='summary')
    map.connect('/proposal/approve', controller='proposal', action='approve')
    map.connect('/review/summary',        controller='review', action='summary')

    # Funding Review
    map.connect('/funding/review_index', controller='funding', action='review_index')
    map.connect('/funding/summary',      controller='funding', action='summary')
    map.connect('/funding/approve',      controller='funding', action='approve')
    map.connect('/funding_review/summary', controller='funding_review', action='summary')

    # schedule routes
    map.connect('/programme/schedule',                controller='schedule', action='index', day='monday')
    map.connect('/programme/schedule/{day}',          controller='schedule', action='index', day=None)
    map.connect('/programme/schedule/view_talk/{id}', controller='schedule', action='view_talk', id=None)

    # registration and invoicing
    map.connect('/invoice/pdf/{id}',               controller='invoice', action='pdf', id=None)
    map.connect('/invoice/remind',                 controller='invoice', action='remind', id=None)
    map.connect('/registration/remind',            controller='registration', action='remind', id=None)
    map.connect('/register/status',                controller='registration', action='status')
    map.connect('/registration/silly_description', controller='registration', action='silly_description')
    map.connect('/registration/generate_badges',   controller='registration', action='generate_badges')

    # account confirmation named route
    map.connect('acct_confirm', '/person/confirm/{confirm_hash}', controller='person', action='confirm')
    map.connect('/person/signin',                    controller='person', action='signin')
    map.connect('/person/signout',                   controller='person', action='signout')
    map.connect('/person/signout_confirm',           controller='person', action='signout_confirm')
    map.connect('/person/forgotten_password',        controller='person', action='forgotten_password')
    map.connect('/person/reset_password/{url_hash}', controller='person', action='reset_password')

    # admin controller
    map.connect('/admin/{action}', controller='admin')

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
    map.connect('*url', controller='db_content', action='page', id=None)
    #map.connect('/db_content/view', controller='db_content', action='view', id=None)
    map.connect('*url', controller='not_found', action='view')

    return map
