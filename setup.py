from setuptools import setup, find_packages

setup(
    name='zookeepr',
    version="",
    #description="",
    #author="",
    #author_email="",
    #url="",
    install_requires=["Pylons==0.9",
                      "SQLAlchemy>=0.2.5"],
    packages=find_packages(),
    include_package_data=True,
    test_suite = 'nose.collector',
    package_data={'zookeepr': ['i18n/*/LC_MESSAGES/*.mo']},
    entry_points="""
    [paste.app_factory]
    main=zookeepr:make_app
    [paste.app_install]
    main=paste.script.appinstall:Installer
    """,
)
