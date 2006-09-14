#!/usr/bin/python2.3

import os.path
import os
import sys

try:
    __file__
except NameError:
    __file__ = '?'

print """Content-type: text/html

<html><head><title>Python Exploration</title></head><body>
<table border=1>
<tr><th colspan=2>1. System Information</th></tr>
<tr><td>Python</td><td>%s</td></tr>
<tr><td>Platform</td><td>%s</td></tr>
<tr><td>Absolute path of this script</td><td>%s</td></tr>
<tr><td>Filename</td><td>%s</td></tr>
""" % (sys.version,
       sys.platform,
       os.path.abspath('.'),
       __file__)
print "<th colspan=2>2. Environment Variables</th>\n"
for variable in os.environ:
    print "<tr><td>%s</td><td>%s</td></tr>\n" % (variable, os.environ[variable])
print "</table></body></html>"
