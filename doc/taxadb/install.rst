.. _install:

Installing Taxadb
=================

Taxadb requires :code:`python 3.5` to work. Taxadb can work with `SQLite`, `PostgreSQL` and `MySQL`. By default Taxadb
works with `SQLite` as it comes with modern Python distributions.

To install it, simply type one of the following in a terminal:

* Using pip

.. code-block:: bash

   pip install taxadb

Installing Taxadb for `PostgreSQL` and/or `MySQL`

.. code-block:: bash

    pip install -e .[postgres, mysql] taxadb

This should install `psycopg2` and `PyMySQL` Python packages


* Using :code:`python setup.py install`


.. code-block:: bash

   python setup.py install

Installing Taxadb for `PostgreSQL` and/or `MySQL`

.. code-block:: bash

   pip install psycopg2 PyMySQL
   python setup.py install
