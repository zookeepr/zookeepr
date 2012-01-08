import os, sys
from paste.script.util.logging_config import fileConfig

sys.path.append('/home/zookeepr/livecheckout')
os.environ['PYTHON_EGG_CACHE'] = '/home/zookeepr/livecheckout/zookeepr.egg-info'
#os.environ['PYTHONIOENCODING'] = 'ascii'

fileConfig('/home/zookeepr/livecheckout/config.ini')

from paste.deploy import loadapp

application = loadapp('config:/home/zookeepr/livecheckout/config.ini')
