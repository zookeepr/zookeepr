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
    from zookeepr.model import create_all, populate_data
    print "Creating schema"
    create_all(app_conf)
    print "Schema creation done"

    print "Populating data"
    populate_data()
    print "Data population done"

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
        mkdir(os.path.join(app_conf['moin_data'], 'pages'))
        mkdir(os.path.join(app_conf['moin_data'], 'attachments'))
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

    try:
        if os.path.exists(app_conf['dynamic_html_dir']):
            print "ok!"
        else:
            print "boo"
        os.symlink(os.path.join(app_conf['moin_data'], 'attachments'),
                   os.path.join(app_conf['dynamic_html_dir'], 'att-data'))
    except OSError, e:
        if e.errno == 17:
            print "skipping, file exists"
        else:
            raise e
