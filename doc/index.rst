.. taxadb documentation master file, created by
   sphinx-quickstart on Thu Mar 1 19:09:27 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Taxadb
======

Taxadb is a application to locally query the ncbi taxonomy. Taxadb is written in python, and access its database using
the `peewee <http://peewee.readthedocs.io>`_ library.

.. image:: biobook_taxonomy_graphik_6.png
   :scale: 50

..   :height: 246
..   :width: 200

* A small tool to query `NCBI <https://ncbi.nlm.nih.gov/taxonomy>`_ taxonomy.
* Written in python 3.5.
* Built-in support for `SQLite <https://www.sqlite.org>`_, `MySQL <https://www.mysql.com>`_ and
  `PostgreSQL <https://www.postgresql.org>`_.
* Available pre-built SQLite databases (:ref:`Download build databases <download>`).
* `API documentation <api>`_.

.. image:: postgresql.png
    :target: taxadb/download.html#using-postgres
    :alt: postgresql

.. image:: mysql.png
    :target: taxadb/download.html#using-mysql
    :alt: mysql

.. image:: sqlite.png
    :target: taxadb/download.html#using-sqlite
    :alt: sqlite

Taxadb's source code hosted on `GitHub <https://github.com/HadrienG/taxadb.git>`_.

* :ref:`Installation guide <install>` explains how to install Taxadb.
* :ref:`Download or build data <download>` explain how to build Taxadb database(s).
* :ref:`Test the application <tests>` allow to run several tests for supported databases.
* :ref:`Querying taxadb <query>` shows some example on how to use Taxadb application.
* :ref:`API reference <api>` describes available classes and methods to use Taxadb.

Note
----

If you find any bugs, odd behavior, or have an idea for a new feature please don't hesitate to `open an issue <https://github.com/Hadien/taxadb/issues?state=open>`_ .

Contents:
---------

.. toctree::
   :maxdepth: 2
   :glob:

   taxadb/install
   taxadb/download
   taxadb/tests
   taxadb/query
   taxadb/api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. |date| date::
.. |time| date:: %H:%M

*This documentation was generated on* |date| *at* |time|.