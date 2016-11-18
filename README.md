# Taxadb

[![Build Status](https://travis-ci.org/HadrienG/taxadb.svg?branch=master)](https://travis-ci.org/HadrienG/taxadb)
[![PyPI](https://img.shields.io/badge/python-3.5-blue.svg)]()
<!-- [![PyPI](https://img.shields.io/badge/license-GPLv3-blue.svg)]() -->

Taxadb is a application to locally query the ncbi taxonomy. Taxadb is written in python, and access its database using the [peewee](http://peewee.readthedocs.io) library.

Taxadb is very much a work in progress, the following are still not implemented:  
- [x] taxadb download: download all the required files from the ncbi ftp  
- [x] taxadb create: build the sqlite database  
- [ ] API: python library to query the database

The sqlite database is 21G large and takes about 60h to build. However, you can download it from [here](http://139.162.178.46/files/taxadb/taxadb.sqlite.gz) (gzipped, 4.6G)


## Installation

Taxadb requires python 3.5 to work. To install, type the following in your terminal:

    pip install git+https://github.com/HadrienG/taxadb.git

or if you have different python versions installed (i.e using Homebrew)

    pip3 install git+https://github.com/HadrienG/taxadb.git


## Usage

### Querying the Database

Coming soon!

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


## Contributing

Do you need help, found a bug or thought about a new feature that you'd like us to implement? Open an [issue](https://github.com/HadrienG/taxadb/issues) or fork the repository and submit a [pull request](https://github.com/HadrienG/taxadb/pulls)!
