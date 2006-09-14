import os

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
            if e.errno == 2:
                mkdir(os.path.dirname(dirname))
            else:
                raise e

    print config['moin_data']
    print config['moin_underlay']

    
    mkdir(config['moin_data'])
    mkdir(config['moin_underlay'])
