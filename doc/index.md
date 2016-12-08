# Taxadb

Taxadb is a application to locally query the ncbi taxonomy. Taxadb is written in python, and access its database using the [peewee](http://peewee.readthedocs.io) library.

## Installation

Taxadb requires python 3.5 to work. To install, simply type the following in your terminal:

    pip install taxadb

### Available databases

The databases used by Taxadb are lengthy to build, therefore we provide pre-built databases. They are available for download below.

#### Sqlite

<table border=1 style="border-collapse:collapse; margin: 0 auto;">
    <thead>
        <tr>
            <th>Name</th><th>Size</th><th>Size (gzipped)</th><th>download link</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>full</td><td>21G</td><td>4.4G</td><td><a href="http://139.162.178.46/files/taxadb/taxadb_full.sqlite.gz">link</a></td>
        </tr>
        <tr>
            <td>nucl</td><td>14G</td><td>2.9G</td><td><a href="http://139.162.178.46/files/taxadb/taxadb_nucl.sqlite.gz">link</a></td>
        </tr>
        <tr>
            <td>prot</td><td>7.1G</td><td>1.6G</td><td><a href="http://139.162.178.46/files/taxadb/taxadb_prot.sqlite.gz">link</a></td>
        </tr>
        <tr>
            <td>gb</td><td>2.5G</td><td>576M</td><td><a href="http://139.162.178.46/files/taxadb/taxadb_gb.sqlite.gz">link</a></td>
        </tr>
        <tr>
            <td>wgs</td><td>8.5G</td><td>1.9G</td><td><a href="http://139.162.178.46/files/taxadb/taxadb_wgs.sqlite.gz">link</a></td>
        </tr>
        <tr>
            <td>gss</td><td>880M</td><td>172M</td><td><a href="http://139.162.178.46/files/taxadb/taxadb_gss.sqlite.gz">link</a></td>
        </tr>
        <tr>
            <td>est</td><td>1.6G</td><td>320M</td><td><a href="http://139.162.178.46/files/taxadb/taxadb_est.sqlite.gz">link</a></td>
        </tr>
    </tbody>
</table>

Build date: December 2016

## Usage

### Querying the Database

Firstly, make sure you have [downloaded](#available-databases) or [built](#creating-the-database) the database

Below you can find basic examples. For more complete examples, please refer to the complete documentation (Available soon!)

```python
    >>> from taxadb import taxid

    >>> name = taxid.sci_name(33208, 'mydb.sqlite')
    >>> print(name)
    Metazoa

    >>> lineage = taxid.lineage_name(33208, 'mydb.sqlite')
    >>> print(lineage)
    ['Metazoa', 'Opisthokonta', 'Eukaryota', 'cellular organisms']
```

To get the taxonomic information for accession numbers, you need to know from which ncbi division it originated. Example with accession numbers from the gb division:

```python
    >>> from taxadb.schema import *
    >>> from taxadb import accession

    >>> my_accessions = ['X17276', 'Z12029']
    >>> taxids = accession.taxid(my_accessions, 'mydb.sqlite', Gb)
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

#### MySQL

*Due to a problem with Foreign Keys, MySQL support has been put on hold for the time being*

Creating databases is a very vendor specific task. Peewee, as most ORMs, can create tables but not databases.
In order to use taxadb with MySQL, you'll have to create the database yourself.

Connect to your mysql server

    mysql -u $user -p
    mysql> create database taxadb;

then run taxadb

    taxadb download -o taxadb
    taxadb create -i taxadb -d taxadb -t mysql -u $user -p $password

## License

Code is under the [MIT](LICENSE) license.

## Issues

Found a bug or have a question? Please open an [issue](https://github.com/HadrienG/taxadb/issues)

## Contributing

Thought about a new feature that you'd like us to implement? Open an [issue](https://github.com/HadrienG/taxadb/issues) or fork the repository and submit a [pull request](https://github.com/HadrienG/taxadb/pulls)
