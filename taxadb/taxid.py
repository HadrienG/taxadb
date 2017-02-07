#!/usr/bin/env python
# -*- coding: utf-8 -*-

from taxadb.schema import *


def sci_name(taxid, db_name, **kwargs):
    """given a taxid, return its associated scientific name

    You can access data from several database type (sqlite3/mysql/postgresql)
    To do so, call the method as follow:
    sqlite3:    sci_name = taxid.sci_name(3309, '/path/to/db.sqlite')
    mysql:      sci_name = taxid.sci_name(3309, 'dbname', dbtype='mysql', user='user', password='secret')
    postgresql: sci_name = taxid.sci_name(3309, 'dbname', dbtype='postgres', user='user', password='secret')

    Arguments:
    taxid -- a taxid (int)
    db_name -- the path to the database to query
    kwargs -- Extra options for non sqlite database type (e.g.: dbtype/username/password)
    """
    database = DatabaseFactory(dbname=db_name, **kwargs).get_database()
    db.initialize(database)
    db.connect()
    name = Taxa.get(Taxa.ncbi_taxid == taxid).tax_name
    db.close()
    return name


def lineage_id(taxid, db_name, **kwargs):
    """given a taxid, return its associated lineage (in the form of a list
    of taxids, each parents of each others)

    You can access data from several database type (sqlite3/mysql/postgresql)
    To do so, call the method as follow:
    sqlite3:    lineage_id = taxid.lineage_name(3309, '/path/to/db.sqlite')
    mysql:      lineage_id = taxid.lineage_name(3309, 'dbname', dbtype='mysql', user='user', password='secret')
    postgresql: lineage_id = taxid.lineage_name(3309, 'dbname', dbtype='postgres', user='user', password='secret')

    Arguments:
    taxid -- a taxid (int)
    db_name -- the path to the database to query
    kwargs -- Extra options for non sqlite database type (e.g.: dbtype/username/password)
    """
    database = DatabaseFactory(dbname=db_name, **kwargs).get_database()
    db.initialize(database)
    db.connect()
    lineage_list = []
    current_lineage = Taxa.get(Taxa.ncbi_taxid == taxid).tax_name
    current_lineage_id = Taxa.get(Taxa.ncbi_taxid == taxid).ncbi_taxid
    parent = Taxa.get(Taxa.ncbi_taxid == taxid).parent_taxid
    while current_lineage != 'root':
        lineage_list.append(current_lineage_id)
        new_query = Taxa.get(Taxa.ncbi_taxid == parent)

        current_lineage = new_query.tax_name
        current_lineage_id = new_query.ncbi_taxid
        parent = new_query.parent_taxid
    return lineage_list
    db.close()


def lineage_name(taxid, db_name, **kwargs):
    """given a taxid, return its associated lineage

    You can access data from several database type (sqlite3/mysql/postgresql)
    To do so, call the method as follow:
    sqlite3:    lineage = taxid.lineage_name(3309, '/path/to/db.sqlite')
    mysql:      lineage = taxid.lineage_name(3309, 'dbname', dbtype='mysql', user='user', password='secret')
    postgresql: lineage = taxid.lineage_name(3309, 'dbname', dbtype='postgres', user='user', password='secret')

    Arguments:
    taxid -- a taxid (int)
    db_name -- the path to the database to query
    kwargs -- Extra options for non sqlite database type (e.g.: dbtype/user/password)
    """
    database = DatabaseFactory(dbname=db_name, **kwargs).get_database()
    db.initialize(database)
    db.connect()
    lineage_list = []
    current_lineage = Taxa.get(Taxa.ncbi_taxid == taxid).tax_name
    parent = Taxa.get(Taxa.ncbi_taxid == taxid).parent_taxid
    while current_lineage != 'root':
        lineage_list.append(current_lineage)
        new_query = Taxa.get(Taxa.ncbi_taxid == parent)

        current_lineage = new_query.tax_name
        parent = new_query.parent_taxid
    return lineage_list
    db.close()
