"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper

def make_map(config):
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'], explicit=False)
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
    map.connect('/about/map',          controller='map')
    map.connect('/brisbane/map',       controller='map')

    map.connect('/sitemap',            controller='sitemap', action='view')

    # DB content
    map.connect('/db_content/list_files',    controller='db_content', action='list_files', id=None)
    map.connect('/db_content/delete_file',   controller='db_content', action='delete_file', id=None)
    map.connect('/db_content/delete_folder', controller='db_content', action='delete_folder', id=None)
    map.connect('/db_content/upload',        controller='db_content', action='upload', id=None)

    # Schedule
    map.connect('/programme/schedule',                controller='schedule', action='table', day=None)
    map.connect('/programme/schedule/ical',           controller='schedule', action='ical')
    map.connect('/programme/schedule/json',           controller='schedule', action='json')
    map.connect('/programme/schedule/{day}',          controller='schedule', action='table', day=None)
    map.connect('/programme/schedule/view_talk/{id}', controller='schedule', action='table_view', id=None)
    map.connect('/programme/schedule/video',          controller='schedule', action='video_room', room=None)
    map.connect('/programme/schedule/video/{room}',   controller='schedule', action='video_room', room=None)
    map.connect('/event/new_proposals',               controller='event', action='new_proposals')

    # Proposal submission
    map.connect('/programme/submit_a_miniconf', controller='miniconf_proposal', action='new')
    map.connect('/programme/submit_a_proposal',    controller='proposal', action='new')

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

    # registration and invoicing
    map.connect('/invoice/{id}/pdf',               controller='invoice', action='pdf', id=None)
    map.connect('/invoice/remind',                 controller='invoice', action='remind', id=None)
    map.connect('/invoice/save_new_invoice',       controller='invoice', action='save_new_invoice', id=None)
    map.connect('/invoice/pay_invoice',            controller='invoice', action='pay_invoice', id=None)
    map.connect('/registration/remind',            controller='registration', action='remind', id=None)
    map.connect('/register/status',                controller='registration', action='status')
    map.connect('/registration/silly_description', controller='registration', action='silly_description')
    map.connect('/registration/generate_badges',   controller='registration', action='generate_badges')

    map.connect('/invoice/generate_hash/{id}',     controller='invoice', action='generate_hash', id=None)
    map.connect('/secret/{hash}',                  controller='secret_hash', action='lookup', hash=None)

    # account confirmation named route
    map.connect('acct_confirm', '/person/confirm/{confirm_hash}', controller='person', action='confirm')
    map.connect('/person/signin',                    controller='person', action='signin')
    map.connect('/person/signout',                   controller='person', action='signout')
    map.connect('/person/signout_confirm',           controller='person', action='signout_confirm')
    map.connect('/person/forgotten_password',        controller='person', action='forgotten_password')
    map.connect('/person/reset_password/{url_hash}', controller='person', action='reset_password')
    map.connect('/person/persona_login',             controller='person', action='persona_login')
    map.connect('/person/finish_signup',             controller='person', action='finish_signup')
    map.connect('/person/new_incomplete',            controller='person', action='new_incomplete')

    # booklet
    map.connect('/registration/professionals_latex', controller='registration', action='professionals_latex')
    map.connect('/proposal/latex',                  controller='proposal', action='latex')

    # product
    map.connect('/product/new/{cat_id}', controller='product', action='new')

    # checkin
    map.connect('/checkin/{action}', controller='checkin')

    # admin controller
    map.connect('/admin/{action}', controller='admin')

    # route rego_notes with ID's
    map.connect('/registration/{rego_id}/new_note', controller='rego_note', action='new', id=None)

    # photocomp
    map.connect('/photocomp/edit', controller='photocomp', action='edit', id=None)
    map.connect('/photocomp/', controller='photocomp', action='index')
    map.connect('/photocomp/photo/{filename}', controller='photocomp', action='photo')

    # UML Graphs
    map.connect('/uml_graph.{format}',
            controller='uml_graph', action='dotmodel',
            requirements=dict(format='(png|jpeg|jpg|svg|dot)'),
            conditions=dict(method='GET'))
            
    # boarding pass
    map.connect('/boardingpass/{id}', controller='boardingpass', action='pdf')

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
