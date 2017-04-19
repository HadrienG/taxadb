# Taxadb

[![Build Status](https://travis-ci.org/HadrienG/taxadb.svg?branch=master)](https://travis-ci.org/HadrienG/taxadb)
[![PyPI](https://img.shields.io/badge/python-3.5-blue.svg)]()
[![LICENSE](https://img.shields.io/badge/license-MIT-lightgrey.svg)]()

Taxadb is an application to locally query the ncbi taxonomy. Taxadb is written in python, and access its database using the [peewee](http://peewee.readthedocs.io) library.

In brief Taxadb:

* is a small tool to query the [ncbi](https://ncbi.nlm.nih.gov/taxonomy) taxonomy.
* is written in python >= 3.5.
* has built-in support for [SQLite](https://www.sqlite.org), [MySQL](https://www.mysql.com) and [PostgreSQL](https://www.postgresql.org).
* has available pre-built SQLite databases.
* has a comprehensive API documentation.


## Installation

Taxadb requires python >= 3.5 to work. To install taxadb with sqlite support, simply type the following in your terminal:

    pip3 install taxadb

If you wish to use MySQL or PostgreSQL, please refer to the full [documentation](http://taxadb.readthedocs.io/en/latest/)

### Available databases

The databases used by Taxadb are lengthy to build, therefore we provide pre-built sqlite databases. They are available for download below.

#### Sqlite

| Name | Size | Size (gzipped) | download link
| --- | --- | --- | ---
| full | 40G | 8.1G | [link](http://139.162.178.46/files/taxadb/taxadb_full.sqlite.gz)
| nucl | 25G | 5.0G | [link](http://139.162.178.46/files/taxadb/taxadb_nucl.sqlite.gz)
| prot | 15G | 3.2G | [link](http://139.162.178.46/files/taxadb/taxadb_prot.sqlite.gz)
| gb | 4.4G | 962M | [link](http://139.162.178.46/files/taxadb/taxadb_gb.sqlite.gz)
| wgs | 17G | 3.2G | [link](http://139.162.178.46/files/taxadb/taxadb_wgs.sqlite.gz)
| gss | 1.6M | 316M | [link](http://139.162.178.46/files/taxadb/taxadb_gss.sqlite.gz)
| est | 2.9G | 599M | [link](http://139.162.178.46/files/taxadb/taxadb_est.sqlite.gz)

Build date: April 2017

## Usage

### Querying the Database

Firstly, make sure you have [downloaded](#available-databases) or [built](#creating-the-database) the database

Below you can find basic examples. For more complete examples, please refer to the complete [API documentation](http://taxadb.readthedocs.io/en/latest/)

```python
    >>> from taxadb.taxid import TaxID

    >>> taxid = TaxID(dbtype='sqlite', dbname='mydb.sqlite')
    >>> name = taxid.sci_name(33208)
    >>> print(name)
    Metazoa

    >>> lineage = taxid.lineage_name(33208)
    >>> print(lineage)
    ['Metazoa', 'Opisthokonta', 'Eukaryota', 'cellular organisms']
    >>> lineage = taxid.lineage_name(33208, reverse=True)
    >>> print(lineage)
    ['cellular organism', 'Eukaryota', 'Opisthokonta', 'Metazoa']
```

Get the taxonomic information for accession number(s).

```python
    >>> from taxadb.accessionid import AccessionID

    >>> my_accessions = ['X17276', 'Z12029']
    >>> accession = AccessionID(dbtype='sqlite', dbname='mydb.sqlite')
    >>> taxids = accession.taxid(my_accessions)
    >>> taxids
    <generator object taxid at 0x1051b0830>

    >>> for tax in taxids:
        print(tax)
    ('X17276', 9646)
    ('Z12029', 9915)
```

You can also use a configuration file in order to automatically set database
connection parameters at object build. Either set `config` parameter to `__init__`
 object method:
 ```python
    >>> from taxadb.accessionid import AccessionID

    >>> my_accessions = ['X17276', 'Z12029']
    >>> accession = AccessionID(config='/path/to/taxadb.cfg')
    >>> taxids = accession.taxid(my_accessions)
    >>> ...
 ```

 or set environment variable `TAXADB_CONFIG` which point to configuration file:
 ```bash
    $ export TAXADB_CONFIG='/path/to/taxadb.cfg'
 ```
 then
 ```python
    >>> from taxadb.accessionid import AccessionID

    >>> my_accessions = ['X17276', 'Z12029']
    >>> accession = AccessionID()
    >>> taxids = accession.taxid(my_accessions)
    >>> ...
 ```

Check documentation for more information.

### Creating the Database

#### Download data

The following commands will download the necessary files from the ncbi ftp into the directory `taxadb`.
```
$ taxadb download -o taxadb
```

#### Insert data

##### SQLite


```
$ taxadb create -i taxadb --dbname taxadb
```
You can then safely remove the downloaded files
```
$ rm -r taxadb
```

##### MySQL

Creating databases is a very vendor specific task. Peewee, as most ORMs, can create tables but not databases.
In order to use taxadb with MySQL, you'll have to create the database yourself.

Connect to your mysql server
```
$ mysql -u $user -p
$ mysql> CREATE DATABASE taxadb;

```

Load data
```
$ taxadb create -i taxadb --dbname taxadb --dbtype mysql --username <user> --password <pwd> ...
```

##### PostgreSQL

Creating databases is a very vendor specific task. Peewee, as most ORMs, can create tables but not databases.
In order to use taxadb with PosgreSQL, you'll have to create the database yourself.

Connect to your postgresql server
```
$ psql -U $user -d postgres
$ psql> CREATE DATABASE taxadb;
```

Load data
```
$ taxadb create -i taxadb --dbname taxadb --dbtype postgres --username <user> --password <pwd> ...
```

You can easily rerun the same command, `taxadb` is able to skip already inserted `taxid` as well as `accession`.

## Tests

You can easily run some tests. Go to the root directory of this projects `cd /path/to/taxadb` and run
`nosetests`.

This simple command will run tests against an `SQLite` test database called `test_db.sqlite` located in `taxadb/test`
directory.

It is also possible to only run tests related to accessionid or taxid as follow
```
$ nosetests -a 'taxid'
$ nosetests -a 'accessionid'
```

You can also use the configuration file located in root distribution `taxadb.ini` as follow. This file should contains
database connection settings:
```
$ nosetests --tc-file taxadb.ini
```

You can easily override configuration file settings using command line options `--tc` such as:
```
$ nosetest --tc-file taxadb.ini --tc=sql.dbname:another_dbname
```

More info at [nose-testconfig](https://pypi.python.org/pypi/nose-testconfig)

### Running tests against PostgreSQL or MySQL

#### First create a test database to insert test data

* PostgreSQL

```
$ createdb <test_db>
```
or
```
$ psql -U postgres
psql> CREATE DATABASE <test_db>;
```

* MySQL

```
$ mysql -u root
mysql> CREATE DATABASE <test_db>;
```

#### Load test data

* PostgreSQL
```
$ gunzip -c /path/to/taxadb/taxadb/test/test_mypg_db.sql.gz | psql -d <test_db> -U <user>
```

* MySQL
```
$ gunzip -c /path/to/taxadb/taxadb/test/test_mypg_db.sql.gz | mysql -D <test_db> -u <user> -p
```

#### Run tests

Either edit `taxadb.ini` to fit database configuration or use `--tc` command line option and set appropriate values like
`username, password, port, hostname, dbtype(postgres or mysql), dbname`.

1) PostgreSQL
```
$ nosetests --tc-file taxadb.ini
OR
$ nosetests -tc-file taxadb.ini --tc=sql.dbtype:postgres --tc=sql.username:postgres --tc=sql.dbname:test_db2
```

2) MySQL
```
$ nosetests --tc-file taxadb.ini
OR
$ nosetests -tc-file taxadb.ini --tc=sql.dbtype:mysql --tc=sql.username:root --tc=sql.dbname:newdbname
```

## License

Code is under the [MIT](LICENSE) license.

## Issues

Found a bug or have a question? Please open an [issue](https://github.com/HadrienG/taxadb/issues)

## Contributing

Thought about a new feature that you'd like us to implement? Open an [issue](https://github.com/HadrienG/taxadb/issues) or fork the repository and submit a [pull request](https://github.com/HadrienG/taxadb/pulls)
