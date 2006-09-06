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
