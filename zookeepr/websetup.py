import os

from paste.script.copydir import copy_dir

def setup_config(command, filename, section, vars):
    """
    Place any commands to setup zookeepr here.
    """
    from paste.deploy import appconfig
    config = appconfig('config:' + filename)

#     print "command", command
#     print "filename", filename
#     print "section", section
#     print "vars", vars
#     print "config", config

    import sqlalchemy
    from zookeepr import model
    sqlalchemy.default_metadata.connect(config['dburi'])#, echo=True)
    sqlalchemy.default_metadata.create_all()
#    print "created thingies"
    

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
                 beds=100
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
                 beds=100,
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
                 beds=100,
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
                 beds=100,
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
        os.symlink(os.path.join(config['moin_data'], 'attachments'), os.path.join(os.path.dirname(__file__), 'public', 'att-data'))
        mkdir(os.path.join(config['moin_data'], 'pages'))
        # copy plugins dir from our egg to the destination
        copy_dir(os.path.join(os.path.dirname(__file__), '..', 'zookeepr.egg-info', 'moin', 'data', 'plugin'), os.path.join(config['moin_data'], 'plugin'), {}, 1, False)
        copy_dir(os.path.join(os.path.dirname(__file__), '..', 'zookeepr.egg-info', 'moin', 'underlay'), os.path.join(config['moin_underlay']), {}, 1, False)
    except OSError, e:
        # skip file-exists
        if e.errno == 17:
            pass
        else:
            raise e
