.. _query:


Querying the database
=====================

Firstly make sure you have :ref:`downloaded <download>` or :ref:`built <build_own_databases>` the database.

Below you can find basic examples. For more complex examples, please refer to the complete :ref:`documentation <api>`.

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
