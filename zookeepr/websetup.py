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

