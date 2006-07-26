#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='zookeepr',
    version="0.1",
    #description="",
    #author="",
    #author_email="",
    #url="",
    install_requires=["Pylons==0.8.2",
                      "Paste==0.9.3-zookeepr2",
                      "SQLAlchemy>=0.2.3",
                      "FormEncode==0.5.1",
                      ],
    dependency_links=["http://gnaw.yi.org/~ycros/zookeepr-deps/"],
    packages=find_packages(),
    include_package_data=True,
    test_suite = 'nose.collector',
    package_data={'zookeepr': ['i18n/*/LC_MESSAGES/*.mo',
                               'templates/autohandler',
                               'templates/*.myt',
                               'templates/*/*.myt',
                               'public/*.css',
                               'public/*.png',
                               'public/*.pdf',
                               'public/*.gif']},
    entry_points="""
    [paste.app_factory]
    main=zookeepr:make_app
    [paste.app_install]
    main=paste.script.appinstall:Installer
    """,
)
