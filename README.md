# Taxadb

[![Build Status](https://travis-ci.org/HadrienG/taxa_db.svg?branch=master)](https://travis-ci.org/HadrienG/taxa_db)
[![PyPI](https://img.shields.io/badge/python-3.5-blue.svg)]()
<!-- [![PyPI](https://img.shields.io/badge/license-GPLv3-blue.svg)]() -->

Taxadb is a application to locally query the ncbi taxaonomy. Taxadb is written in python, and access its database using the peewee library. At the moment only sqlite is supported but support for MySQL and Postgres are on their way.

Taxadb is very much a work in progress, the following are still not implemented:  
- [x] taxadb download: download all the required files from the ncbi ftp  
- [x] taxadb create: build the sqlite database  
- [ ] API: python library to query the database

The sqlite database is 21G large and takes about 60h to build. However, you can download it from here (gzipped, 4.4G)


### Installation

Taxadb requires python 3.5 to work. To install, type the following in your terminal:

    git clone https://github.com/HadrienG/taxadb.git
    cd taxadb
    pip install .  # or pip3 install . if you have different python versions


### Usage

The following commands will download the necessary files from the ncbi ftp and build a database called taxadb.sqlite in the current directory

    taxadb download -o taxadb
    taxadb create -i taxadb --dbname taxadb

You can then safely remove the downloaded files

    rm -r taxadb

### Contributing

Need help? Found a bug? Thought about a new feature that you'd like us to implement? Open an issue or fork the repository and submit a pull request!
