.. _query:


Querying the database
=====================

Firstly make sure you have :ref:`downloaded <download>` or :ref:`built <build_own_databases>` the database.

Below you can find basic examples. For more complex examples, please refer to the complete :ref:`documentation <api>`.

.. _useconfig:

Using configuration file or environment variable
------------------------------------------------

Taxadb can now take profit of configuration file or environment variable to
set database connection parameters.

* Using configuration file

You can pass a configuration file when building your object:

.. code-block:: python

   >>> from taxadb.taxid import TaxID

   >>> taxid = TaxID(config='/path/to/taxadb.cfg')
   >>> name = taxid.sci_name(33208)
   >>> ...

* Configuration file format

The configuration file must use syntax supported by `configparser object
<https://docs.python.org/3.5/library/configparser.html>`_.
You must set database connection parameters in a section called
:code:`DBSETTINGS` as below:

.. code-block:: bash

   [DBSETTINGS]
   dbtype=<sqlite|postgres|mysql>
   dbname=taxadb
   hostname=taxadb.domain.org
   username=admin
   password=s3cr3T
   port=

Some value will default it they are not set.

**hostname** will be set to value :code:`localhost` and **port** is set to
:code:`5432` for :code:`dbtype=postgres` and :code:`3306` for
:code:`dbtype=mysql`.

* Using environment variable

Taxadb can as well use an environment variable to automatically point the
application to a configuration file. To take profit of it, just set
:code:`TAXADB_CONFIG` to the path of your configuration file:

.. code-block:: bash

   (bash) export TAXADB_CONFIG='/path/to/taxadb.cfg'
   (csh) set TAXADB_CONFIG='/path/to/taxadb.cfg'

Then, just create your object as follow:

.. code-block:: python

   >>> from taxadb.taxid import TaxID

   >>> taxid = Taxid()
   >>> name = taxid.sci_name(33208)
   >>> ...

.. note::

   Arguments passed to object initiation will always overwrite default values
   as well as values that might have been set by configuration file or
   environment variable :code:`TAXADB_CONFIG`.

.. _taxids:

taxids
------

Several operations on taxids are available in taxadb:

.. code-block:: python

   >>> from taxadb.taxid import TaxID

   >>> taxid = TaxID(dbype='sqlite', dbname='taxadb.sqlite')
   >>> name = taxid.sci_name(33208)
   >>> print(name)
   Metazoa

   >>> lineage = taxid.lineage_name(33208)
   >>> print(lineage)
   ['Metazoa', 'Opisthokonta', 'Eukaryota', 'cellular organisms']
   >>> lineage = taxid.lineage_name(33208, reverse=True)
   >>> print(lineage)
   ['cellular organism', 'Eukaryota', 'Opisthokonta', 'Metazoa']

If you are using MySQL or postgres, you'll have to provide your username and password
(and optionally the port and hostname):

.. code-block:: python

    >>> from taxadb.taxid import TaxID

    >>> taxid = TaxID(dbype='postgres', dbname='taxadb',
                        username='taxadb', password='*****')
    >>> name = taxid.sci_name(33208)
    >>> print(name)
    Metazoa

.. _accessions:

accession numbers
-----------------

Get taxonomic information from accession number(s).

.. code-block:: python

   >>> from taxadb.accessionid import AccessionID

   >>> my_accessions = ['X17276', 'Z12029']
   >>> accession = AccessionID(dbtype='sqlite', dbname='taxadb.sqlite')
   >>> taxids = accession.taxid(my_accessions)
   >>> taxids
   <generator object taxid at 0x1051b0830>

   >>> for tax in taxids:
           print(tax)
   ('X17276', 9646)
   ('Z12029', 9915)
