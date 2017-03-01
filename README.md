# Taxadb

[![Build Status](https://travis-ci.org/HadrienG/taxadb.svg?branch=master)](https://travis-ci.org/HadrienG/taxadb)
[![PyPI](https://img.shields.io/badge/python-3.5-blue.svg)]()
[![LICENSE](https://img.shields.io/badge/license-MIT-lightgrey.svg)]()

Taxadb is a application to locally query the ncbi taxonomy. Taxadb is written in python, and access its database using the [peewee](http://peewee.readthedocs.io) library.

Taxadb is very much a work in progress, the following are still not implemented:  
- [x] taxadb download: download all the required files from the ncbi ftp  
- [x] taxadb create: build the sqlite database  
- [ ] API: python library to query the database


## Installation

Taxadb requires python 3.5 to work. To install, simply type the following in your terminal:

    pip install taxadb

### Available databases

The databases used by Taxadb are lengthy to build, therefore we provide pre-built databases. They are available for download below.

#### Sqlite

| Name | Size | Size (gzipped) | download link
| --- | --- | --- | ---
| full | 21G | 4.4G | [link](http://139.162.178.46/files/taxadb/taxadb_full.sqlite.gz)
| nucl | 14G | 2.9G | [link](http://139.162.178.46/files/taxadb/taxadb_nucl.sqlite.gz)
| prot | 7.1G | 1.6G | [link](http://139.162.178.46/files/taxadb/taxadb_prot.sqlite.gz)
| gb | 2.5G | 576M | [link](http://139.162.178.46/files/taxadb/taxadb_gb.sqlite.gz)
| wgs | 8.5G | 1.9G | [link](http://139.162.178.46/files/taxadb/taxadb_wgs.sqlite.gz)
| gss | 880M | 172M | [link](http://139.162.178.46/files/taxadb/taxadb_gss.sqlite.gz)
| est | 1.6G | 320M | [link](http://139.162.178.46/files/taxadb/taxadb_est.sqlite.gz)

Build date: December 2016

## Usage

### Querying the Database

Firstly, make sure you have [downloaded](#available-databases) or [built](#creating-the-database) the database

Below you can find basic examples. For more complete examples, please refer to the complete documentation (Available soon!)

```python
    >>> from taxadb.taxadb import TaxID

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

To get the taxonomic information for accession numbers, you need to know from which ncbi division it originated. Example with accession numbers from the gb division:

```python
    >>> from taxadb.taxadb import AccessionID

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

### Creating the Database

#### Sqlite

The following commands will download the necessary files from the ncbi ftp and build a database called taxadb.sqlite in the current directory

    taxadb download -o taxadb
    taxadb create -i taxadb --dbname taxadb

You can then safely remove the downloaded files

    rm -r taxadb

#### MySQL / PostgreSQL

Creating databases is a very vendor specific task. Peewee, as most ORMs, can create tables but not databases.
In order to use taxadb with MySQL or PostgreSQL, you'll have to create the database yourself.

Connect to your mysql server

    mysql -u $user -p
    mysql> create database taxadb;

Connect to your postgresql server

    psql -u $user -d postgres
    psql> create database taxadb;

then run taxadb

    taxadb download -o taxadb
    taxadb create -i taxadb -d taxadb -t mysql -u $user -p $password --port <port> --hostname <hostname>
    or
    taxadb download -o taxadb
    taxadb create -i taxadb -d taxadb -t postgres -u $user -p $password --port <port> --hostname <hostname>

You can easily rerun the same command, `taxadb` is able to skip already inserted `taxid` as well as `accession`.

## Tests

You can easily run some tests. Go to the root directory of this projects `$ cd /path/to/taxadb` and run
`$ nosetests`.

This simple command will run tests against an `SQLite` test database called `test_db.sqlite` located in `taxadb/test`
directory.

It is also possible to only run tests related to accession or taxid as follow
```
$ nosetests -a 'taxid'
$ nosetests -a 'accessionid'
```

You can also use the configuration file located in root distribution `taxadb.ini` as follow:
```
$ nosetests --tc-file taxadb.ini
```

You can easily override configuration file settings using command line options `--tc` such as:
```
$ nosetest --tc-file taxadb.ini --tc:sql.dbname:my_new_dbname
```
More info at [nose-testconfig](https://pypi.python.org/pypi/nose-testconfig)

#### Running tets against PostgreSQL or MySQL

1. **First create a test database to insert test data**

  * PostgreSQL
```
$ createdb <dbname>
```

  * MySQL
```
$ mysql -u root
mysql> CREATE DATABASE <dbname>;
Query OK, 1 row affected (0.01 sec)
```

2. **Load test data**

* PostgreSQL
```
$ gunzip -c /path/to/taxadb/taxadb/test/test_mypg_db.sql.gz | psql -d <dbname> -U <user>
```

* MySQL
```
$ gunzip -c /path/to/taxadb/taxadb/test/test_mypg_db.sql.gz | mysql -D <dbname> -u <user> -p
```

3. **Then run tests**

Either edit `taxadb.ini` to fit database configuration or use `--tc` commandline option and set appropriate values like
`username, password, port, hostname, dbtype(postgres or mysql), dbname`.

* PostgreSQL
```
$ nosetests --tc-file taxadb.ini
OR
$ nosetests -tc-file taxadb.ini --tc=sql.dbtype:postgres --tc=sql.username:postgres --tc=sql.dbname:newdbname
```

* MySQL
```commandline
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
