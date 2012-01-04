import os, sys
from paste.script.util.logging_config import fileConfig

sys.path.append('/home/zookeepr/git/zookeepr')
os.environ['PYTHON_EGG_CACHE'] = '/home/zookeepr/git/zookeepr/zookeepr.egg-info'
#os.environ['PYTHONIOENCODING'] = 'ascii'

fileConfig('/home/zookeepr/git/zookeepr/config.ini')

from paste.deploy import loadapp

application = loadapp('config:/home/zookeepr/git/zookeepr/config.ini')
