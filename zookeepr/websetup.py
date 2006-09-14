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
