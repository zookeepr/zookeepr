Zookeepr Installation Instructions
==================================

External dependencies
---------------------

Install these with your favourite package manager (eg apt-get).

 * libjpeg-dev
 * libpq-dev
 * libpython-dev
 * libxslt1-dev
 * libxml2-dev
 * postgresql
 * python-virtualenv
 * zlib1g-dev
 * pwgen

Creating a development environment
----------------------------------

1. Create a postgresql database for your ZooKeepr instance.

    ```
    # Create the database zookeepr user
    sudo -u postgres createuser --no-createdb --no-createrole --no-superuser zookeepr

    # Create the zookeepr database, owned by the user
    sudo -u postgres createdb -O zookeepr zookeepr

    # Set the password of the zookeepr user
    sudo -u postgres psql --command "ALTER USER zookeepr with PASSWORD 'zookeepr'"
    ```

2. Create development.ini

    ```
    cp development.ini.sample development.ini
    ```

    The default development.ini file uses the zookeepr database settings set
    in step 1. If you chose to change any of the details in step 1 then you
    must edit the sqlachemy.url in development.ini to match.
    _Note: You must set sqlachemy.url in both the [app:main] and [alembic] sections_


3. Create a virtualenv for your ZooKeepr instance.
    This can be done with virtualenv or virtualenvwrapper.

    ```
    # using only virtualenv
    virtualenv env --no-site-packages
    . ./env/bin/activate # If using bash or zsh, other shells have active.csh etc.

    # using virtualenwrapper
    mkvirtualenv zookeepr
    ```

4. Configure the virtual environment.

    ```
    python setup.py develop
    ```

5. Now we populate the database. Run alembic to create and populate the initial database.

    ```
    alembic --config development.ini upgrade head
    ```

6. Run the development server.

    ```
    pserve --reload development.ini
    ```

7. The default admin account is:

    ```
    email: admin@zookeepr.org
    password: password
    ```

You should now have a development instance of ZooKeepr up and running.

Access it at: <http://0.0.0.0:6543>

*Congratulations*

Developing
----------

Once set up the server must be run within the virtual environment. This can
be done by following just steps 3 and 6.

Testing
-------

Functional and unit tests can be run inside the virtual environment with pytest.

```
# Install dependancies
pip install -r requirements.txt -r test-requirements.txt

py.test # Run all tests
py.test -v zkpylons/tests/functional/test_account.py # Run one test file verbosely
py.test -v zkpylons/tests/functional/test_account.py -k test_create_person # Run one test
```

The automatic integration tests are run by tox and should be run before pushing a commit.

```
tox -r
```
