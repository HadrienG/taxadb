.. _query:


Querying the database
=====================

Firstly make sure you have :ref:`downloaded <download>` or :ref:`build <build_own_databases>` the database.

Below you can find basic examples. For more complex examples, please refer to the complete :ref:`documentation <api>`.
Play with taxonimc identifiers:

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