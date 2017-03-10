.. _tests:


Testing Taxadb
==============

You can easily run some tests. To do so proceed as follow:

.. code-block:: bash

   cd /path/to/taxadb
   nosetests

This simple command will run tests against an `SQLite` test database called `test_db.sqlite` located in `taxadb/test`
directory.

It is also possible to only run tests related to accessionid or taxid as follow

.. code-block:: bash

   nosetests -a 'taxid'
   nosetests -a 'accessionid'

You can also use the configuration file located in root distribution `taxadb.ini` as follow. This file should contains
database connection settings:

.. code-block:: bash

   nosetests --tc-file taxadb.ini

You can override configuration file settings using command line options `--tc` such as:

.. code-block:: bash

   nosetest --tc-file taxadb.ini --tc=sql.dbname:another_dbname

More info at `nose-testconfig <https://pypi.python.org/pypi/nose-testconfig>`_.


Running tests against PostgreSQL or MySQL
-----------------------------------------

**First create a test database to insert test data**

* PostgreSQL

.. code-block:: bash

   createdb <test_db>

or from PostgreSQL client `psql`

.. code-block:: bash

   psql -U postgres
   psql> CREATE DATABASE <test_db>;

* MySQL

.. code-block:: bash

   mysql -u root
   mysql> CREATE DATABASE <test_db>;

**Load test data**

* PostgreSQL

.. code-block:: bash

   gunzip -c /path/to/taxadb/taxadb/test/test_mypg_db.sql.gz | psql -d <test_db> -U <user>

* MySQL

.. code-block:: bash

   gunzip -c /path/to/taxadb/taxadb/test/test_mypg_db.sql.gz | mysql -D <test_db> -u <user> -p

**Run tests**

Either edit `taxadb.ini` to fit database configuration or use `--tc` command line option and set appropriate values like
`username, password, port, hostname, dbtype(postgres or mysql), dbname`.

1. PostgreSQL

.. code-block:: bash

   nosetests --tc-file taxadb.ini

.. code-block:: bash

   nosetests -tc-file taxadb.ini --tc=sql.dbtype:postgres --tc=sql.username:postgres --tc=sql.dbname:test_db2


2. MySQL

.. code-block:: bash

   nosetests --tc-file taxadb.ini

.. code-block:: bash

   nosetests -tc-file taxadb.ini --tc=sql.dbtype:mysql --tc=sql.username:root --tc=sql.dbname:newdbname
