.. _download:

Download Pre built database
===========================

In order to download the required data to create Taxadb database, you can use following command

.. code-block:: bash

   taxadb download -o taxadb

where :code:`-o` refers to an output directory where to download the data.

Available databases
-------------------

The databases used by Taxadb are lengthy to build, therefore we provide pre-built databases.
They are available for download below (**SQLite**).
However, it is possible to build and create your :ref:`own databases <build_own_databases>`

+------+------+----------------+---------------------------------------------------------------+
| Name | Size | Size (gzipped) | download link                                                 |
+======+======+================+===============================================================+
| full | 21G  | 4.4G           | `<http://139.162.178.46/files/taxadb/taxadb_full.sqlite.gz>`_ |
+------+------+----------------+---------------------------------------------------------------+
| nucl | 14G  | 2.9G           | `<http://139.162.178.46/files/taxadb/taxadb_nucl.sqlite.gz>`_ |
+------+------+----------------+---------------------------------------------------------------+
| prot | 7.1G | 1.6G           | `<http://139.162.178.46/files/taxadb/taxadb_prot.sqlite.gz>`_ |
+------+------+----------------+---------------------------------------------------------------+
| gb   | 2.5G | 576M           | `<http://139.162.178.46/files/taxadb/taxadb_gb.sqlite.gz>`_   |
+------+------+----------------+---------------------------------------------------------------+
| wgs  | 8.5G | 1.9G           | `<http://139.162.178.46/files/taxadb/taxadb_wgs.sqlite.gz>`_  |
+------+------+----------------+---------------------------------------------------------------+
| gss  | 880M | 172M           | `<http://139.162.178.46/files/taxadb/taxadb_gss.sqlite.gz>`_  |
+------+------+----------------+---------------------------------------------------------------+
| est  | 1.6G | 320M           | `<http://139.162.178.46/files/taxadb/taxadb_est.sqlite.gz>`_  |
+------+------+----------------+---------------------------------------------------------------+


.. _build_own_databases:

Build you own database
----------------------

* :ref:`SQLite <using_sqlite>`
* :ref:`MySQL <using_mysql>`
* :ref:`PostgreSQL <using_postgres>`

.. _using_sqlite:

SQLite
------

The following command will create an **SQLite** database in the current directory.

.. code-block:: bash

   taxadb create -i taxadb --dbname taxadb

.. _using_mysql:

MySQL
-----

Creating databases is a very vendor specific task. **Peewee**, as most ORMs, can create tables but not databases.
In order to use taxadb with **MySQL**, you'll have to create the database yourself.

.. code-block:: bash

   mysql -u $user -p
   mysql> CREATE DATABASE taxadb;

Then, fill database with data

.. code-block:: bash

   taxadb create -i taxadb --dbname taxadb --dbtype mysql --username user --password secret --port 3306 --hostname localhost`

.. _using_postgres:

PostgreSQL
----------

Creating databases is a very vendor specific task. **Peewee**, as most ORMs, can create tables but not databases.
In order to use taxadb with **PostgreSQL**, you'll have to create the database yourself.

.. code-block:: bash

   psql -U $user -d postgres
   psql> CREATE DATABASE taxadb;

Then, fill database with data

.. code-block:: bash

   taxadb create -i taxadb --dbname taxadb --dbtype postgres --username user --password secret --port 5432 --hostname localhost`

Following options have default value if not set on command line:

* :code:`--port` (:code:`5432` for **PostgreSQL**, :code:`3306` for **MySQL**)
* :code:`--hostname` (localhost)

For more information about available options, please type:

.. code-block:: bash

   taxadb create --help

