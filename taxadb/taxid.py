#!/usr/bin/env python
# -*- coding: utf-8 -*-

from taxadb.schema import *


def sci_name(taxid, db_name):
    """given a taxid, return its associated scientific name

    Arguments:
    taxid -- a taxid (int)
    db_name -- the path to the database to query
    """
    database = pw.SqliteDatabase(db_name)
    db.initialize(database)
    db.connect()
    name = Taxa.get(Taxa.ncbi_taxid == taxid).tax_name
    db.close()
    return name


def lineage_id(taxid, db_name):
    """given a taxid, return its associated lineage (in the form of a list
    of taxids, each parents of each others)

    Arguments:
    taxid -- a taxid (int)
    db_name -- the path to the database to query
    """
    database = pw.SqliteDatabase(db_name)
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


def lineage_name(taxid, db_name):
    """given a taxid, return its associated lineage

    Arguments:
    taxid -- a taxid (int)
    db_name -- the path to the database to query
    """
    database = pw.SqliteDatabase(db_name)
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
