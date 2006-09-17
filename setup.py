from setuptools import setup, find_packages

setup(
    name='zookeepr',
    version="0.1.8",
    #description="",
    #author="",
    #author_email="",
    #url="",
    install_requires=[
        "Pylons>=0.9.1",
        "SQLAlchemy>=0.2.8",
        "nose>=0.9.0",
        "FormEncode>=0.5.1",
        "PasteScript>=0.9.8",
    ],
    packages=find_packages(),
    include_package_data=True,
    test_suite = 'nose.collector',
    package_data={'zookeepr': ['i18n/*/LC_MESSAGES/*.mo',
        'templates/autohandler',
        'templates/*.myt',
        'templates/*/*.myt',
        'public/*.css',
        'public/*.png',
        'public/*.gif',
        'public/*.pdf',
        'public/sponsors/*.gif',
        ]}, 
    entry_points="""
    [paste.app_factory]
    main=zookeepr:make_app
    [paste.app_install]
    main=paste.script.appinstall:Installer
    """,
)
