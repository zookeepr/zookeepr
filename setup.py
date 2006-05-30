#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='zookeepr',
    version="0.1",
    #description="",
    #author="",
    #author_email="",
    #url="",
    install_requires=["Pylons==0.8.1",
                      "SQLAlchemy==0.2.1",
                      "FormEncode==0.5.1"],
    packages=find_packages(),
    include_package_data=True,
    test_suite = 'nose.collector',
    package_data={'zookeepr': ['i18n/*/LC_MESSAGES/*.mo',
                               'templates/*.myt',
                               'templates/*/*.myt',
                               'public/*.css',
                               'public/*.png',
                               'public/*.gif']},
    entry_points="""
    [paste.app_factory]
    main=zookeepr:make_app
    [paste.app_install]
    main=paste.script.appinstall:Installer
    """,
)
