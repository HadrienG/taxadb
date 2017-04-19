.. _download:

Download and Create a database
==============================

.. _available_databases:

Pre-built databases
-------------------

The databases used by Taxadb are lengthy to build, therefore we provide pre-built databases.
They are available for download below (**SQLite**).
We try to update them on a regular basis.
If you wish, it is also possible to build and create your :ref:`own databases <build_own_databases>`

+------+------+----------------+---------------------------------------------------------------+
| Name | Size | Size (gzipped) | download link                                                 |
+======+======+================+===============================================================+
| full | 40G  | 8.1G           | `<http://139.162.178.46/files/taxadb/taxadb_full.sqlite.gz>`_ |
+------+------+----------------+---------------------------------------------------------------+
| nucl | 25G  | 5.0G           | `<http://139.162.178.46/files/taxadb/taxadb_nucl.sqlite.gz>`_ |
+------+------+----------------+---------------------------------------------------------------+
| prot | 15G  | 3.2G           | `<http://139.162.178.46/files/taxadb/taxadb_prot.sqlite.gz>`_ |
+------+------+----------------+---------------------------------------------------------------+
| gb   | 4.4G | 962M           | `<http://139.162.178.46/files/taxadb/taxadb_gb.sqlite.gz>`_   |
+------+------+----------------+---------------------------------------------------------------+
| wgs  | 17G  | 3.2G           | `<http://139.162.178.46/files/taxadb/taxadb_wgs.sqlite.gz>`_  |
+------+------+----------------+---------------------------------------------------------------+
| gss  | 1.6M | 316M           | `<http://139.162.178.46/files/taxadb/taxadb_gss.sqlite.gz>`_  |
+------+------+----------------+---------------------------------------------------------------+
| est  | 2.9G | 599M           | `<http://139.162.178.46/files/taxadb/taxadb_est.sqlite.gz>`_  |
+------+------+----------------+---------------------------------------------------------------+


.. _build_own_databases:

Build you own database
----------------------

In order to create your own database, you first need to download the required data from
the ncbi ftp. The following command does it for you:

.. code-block:: bash

   taxadb download -o taxadb

where :code:`-o` refers to an output directory where to download the data.


.. _using_sqlite:

SQLite
^^^^^^

The following command will create an **SQLite** database in the current directory.

.. code-block:: bash

   taxadb create -i taxadb --dbname taxadb

.. _using_mysql:

MySQL
^^^^^

Creating databases is a very vendor specific task. **Peewee**, as most ORMs, can create tables but not databases.
In order to use taxadb with **MySQL**, you'll have to create the database yourself.

.. code-block:: bash

   mysql -u $user -p
   mysql> CREATE DATABASE taxadb;

Then, fill database with data

.. code-block:: bash

   taxadb create -i taxadb --dbname taxadb --dbtype mysql --username user --password secret --port 3306 --hostname localhost

.. _using_postgres:

PostgreSQL
^^^^^^^^^^

Creating databases is a very vendor specific task. **Peewee**, as most ORMs, can create tables but not databases.
In order to use taxadb with **PostgreSQL**, you'll have to create the database yourself.

.. code-block:: bash

   psql -U $user -d postgres
   psql> CREATE DATABASE taxadb;

Then, fill database with data

.. code-block:: bash

   taxadb create -i taxadb --dbname taxadb --dbtype postgres --username user --password secret --port 5432 --hostname localhost


The following options have default value if not set on the command line:

* :code:`--port` (:code:`5432` for **PostgreSQL**, :code:`3306` for **MySQL**)
* :code:`--hostname` (localhost)

For more information about all the available options, please type:

.. code-block:: bash

   taxadb create --help

.. warning::

   When building your database with downloaded data, you can increase the speed
   of data loading by using --fast option. This option avoid checking existence
   of each accession id in the database before loading related info. In certain
   case this may lead to duplicate entries in table accession when loading
   the same file twice for example.
