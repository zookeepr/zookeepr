from setuptools import setup, find_packages

setup(
    name='zookeepr',
    version="0.2.5",
    #description="",
    #author="",
    #author_email="",
    #url="",
    install_requires=[
        # our champion wsgi stack
        "Pylons>=0.9.1",
        # our champion ORM
        "SQLAlchemy>=0.3",
        # nose as test runner
        "nose>=0.9.0",
        # FormEncode used to do form input validation
        "FormEncode>=0.5.1",
        # Explicit depends on PasteScript as we use it in setup-app
        "PasteScript>=0.9.8",
        # URL auto_link fixes in 0.2.1
        "WebHelpers>=0.2.1",
        # DNS for email address validation
        "dnspython",
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
