<div id="randoms">
    <img src="<% random_pic('location') %>" alt="" height="100" width="100" title="Random Location Image"/>
    <img src="<% random_pic('people') %>" alt="" height="100" width="100" title="Random People Image"/>
    <img src="<% random_pic('misc') %>" alt="" height="100" width="100" title="Random Misc Image"/>
    <strong></strong>
</div>

<%init>
from glob import glob
import os.path, random
def random_pic(subdir):
    fileprefix = '/srv/zookeepr/zookeepr/public/random-pix/'
    htmlprefix = '/random-pix/'
    file = os.path.basename(random.choice(glob(fileprefix + subdir + '/*')))
    return htmlprefix+subdir+'/'+file
</%init>
