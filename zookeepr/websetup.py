import os

from paste.deploy import appconfig
from paste.script.copydir import copy_dir

def setup_config(command, filename, section, vars):
    """Set up zookeepr database schema, filesystem requirements.
    """
    app_conf = appconfig('config:' + filename)

    # Import late, otherwise if there's anything wrong in the model,
    # the whole import will fail, and Paste will mistakenly think that
    # websetup doesn't exist.
    from zookeepr.model import create_all
    print "Creating schema"
    create_all(app_conf)
    print "Schema creation done"

    print "Populating data"
    try:
        model.proposal.tables.proposal_type.insert().execute(
            dict(name='Presentation'),
        )
        model.proposal.tables.proposal_type.insert().execute(
            dict(name='Miniconf'),
            )
        model.proposal.tables.proposal_type.insert().execute(
            dict(name='Tutorial'),
            )
        model.schedule.tables.stream.insert().execute(
            dict(name='Free Love and Open Sensual Stimulation'),
            )
        model.core.tables.role.insert().execute(
            dict(name='reviewer'),
            )
    except sqlalchemy.exceptions.SQLError:
        pass

    try:
        model.registration.tables.accommodation_location.insert().execute(
            dict(id=1,
                 name="New College",
                 beds=125,
                 ),
            )
        model.registration.tables.accommodation_option.insert().execute(
            dict(name="no breakfast",
                 cost_per_night=49.50,
                 accommodation_location_id=1,
                 )
            )
        model.registration.tables.accommodation_option.insert().execute(
            dict(name="",
                 cost_per_night=55.00,
                 accommodation_location_id=1,
                 )
            )
        model.registration.tables.accommodation_location.insert().execute(
            dict(id=2,
                 name="Shalom",
                 beds=90,
                 ),
            )
        model.registration.tables.accommodation_option.insert().execute(
            dict(name="",
                 cost_per_night=60.00,
                 accommodation_location_id=2,
                 ),
            )
        model.registration.tables.accommodation_option.insert().execute(
            dict(name="with ensuite",
                 cost_per_night=80.00,
                 accommodation_location_id=2,
                 )
            )
        model.registration.tables.accommodation_location.insert().execute(
            dict(id=3,
                 name="International house",
                 beds=50,
                 ),
            )
        model.registration.tables.accommodation_option.insert().execute(
            dict(name="no breakfast",
                 cost_per_night=35.00,
                 accommodation_location_id=3,
                 )
            )
        model.registration.tables.accommodation_location.insert().execute(
            dict(id=4,
                 name="Warrane",
                 beds=50,
                 )
            )
        model.registration.tables.accommodation_option.insert().execute(
            dict(name="male only",
                 cost_per_night=58.50,
                 accommodation_location_id=4,
                 )
            )
    except sqlalchemy.exceptions.SQLError:
        pass
    print "population done"

    def mkdir(dirname):
        try:
            os.mkdir(dirname)
        except OSError, e:
            # if directory not found, move up a dir
            if e.errno == 2:
                mkdir(os.path.dirname(dirname))
                os.mkdir(dirname)
            else:
                raise e

    try:
        os.symlink(os.path.join(app_conf['moin_data'], 'attachments'), os.path.join(os.path.dirname(__file__), 'public', 'att-data'))
    except OSError, e:
        if e.errno == 17:
            print "skipping, file exists"
        else:
            raise e
    try:
        mkdir(os.path.join(app_conf['moin_data'], 'pages'))
        # copy plugins dir from our egg to the destination
        copy_dir(os.path.join(os.path.dirname(__file__), '..', 'zookeepr.egg-info', 'moin', 'data', 'plugin'), os.path.join(app_conf['moin_data'], 'plugin'), {}, 1, False)
        copy_dir(os.path.join(os.path.dirname(__file__), '..', 'zookeepr.egg-info', 'moin', 'underlay'), os.path.join(app_conf['moin_underlay']), {}, 1, False)
    except OSError, e:
        # skip file-exists
        if e.errno == 17:
            pass
        else:
            raise e
    try:
        mkdir(app_conf['dynamic_html_dir'])
    except OSError, e:
        if e.errno == 17:
            print "dynamic html dir exists"
        else:
            raise e
    f = open(os.path.join(app_conf['dynamic_html_dir'], 'flickr.html'), "ab")
    f.close()

    p = open(os.path.join(app_conf['dynamic_html_dir'], 'planet.html'), "ab")
    p.close()
