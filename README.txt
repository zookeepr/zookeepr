This file is for you to describe the zookeepr application. Typically
you would include information such as the information below:

Installation and Setup
======================

Install ``zookeepr`` using easy_install::

    easy_install zookeepr

Make a config file as follows::

    paster make-config zookeepr config.ini
    
Tweak the config file as appropriate and then setup the applicaiton::

    paster setup-app config.ini
    
Then you are ready to go.