zookeepr conference management
==============================

[![Build Status](https://travis-ci.org/zookeepr/zookeepr.svg)](https://travis-ci.org/zookeepr/zookeepr)

zookeepr Readme
---------------

This document details how running zookeepr, how to run tests, and where to start hacking.

It assumes that you have the necessary dependencies installed and the development environment up and running. Please refer to INSTALL if you do not have your environment set up.

Running zookeepr
----------------

See [INSTALL.md](INSTALL.md)

 * Run `paster serve -v --reload development.ini`
 * Point your browser to http://localhost:5000/

Where to start hacking
----------------------

 * Refer to the docstrings to familiarise yourself with the code
 * PEP-8 is your new god. PyLint can be used to enforce it. Refer to http://www.python.org/dev/peps/pep-0008/
   * Check the code against pep8 with `tox -e pep8`
 * Run tests with `tox`
 * Add yourself to the AUTHORS file if you think you're contributions are worthy :-)

