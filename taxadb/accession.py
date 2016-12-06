#!/usr/bin/env python
# -*- coding: utf-8 -*-

from taxadb.schema import *


def taxid(acc_number_list, db_name, table):
    """given a list of acession numbers, yield
    the accession number and their associated taxids as tuples

    Arguments:
    acc_number_list -- a list of accession numbers
    db_name -- the path to the database to query
    table -- the table containing the accession numbers
    """
    database = pw.SqliteDatabase(db_name)
    db.initialize(database)
    db.connect()
    with db.atomic():
        query = table.select().where(table.accession << acc_number_list)
        # taxid = table.get(table.accession == acc_number)
        for i in query:
            yield (i.accession, i.taxid.ncbi_taxid)
    db.close()


def sci_name(acc_number_list, db_name, table):
    """given a list of acession numbers, yield
    the accession number and their associated scientific name as tuples

    Arguments:
    acc_number_list -- a list of accession numbers
    db_name -- the path to the database to query
    table -- the table containing the accession numbers
    """
    database = pw.SqliteDatabase(db_name)
    db.initialize(database)
    db.connect()
    with db.atomic():
        query = table.select().where(table.accession << acc_number_list)
        # taxid = table.get(table.accession == acc_number)
        for i in query:
            yield (i.accession, i.taxid.tax_name)
    db.close()


def lineage_id(acc_number_list, db_name, table):
    """given a list of acession numbers, yield the accession number and their
    associated lineage (in the form of taxids) as tuples

    Arguments:
    acc_number_list -- a list of accession numbers
    db_name -- the path to the database to query
    table -- the table containing the accession numbers
    """
    database = pw.SqliteDatabase(db_name)
    db.initialize(database)
    db.connect()
    with db.atomic():
        query = table.select().where(table.accession << acc_number_list)
        for i in query:
            lineage_list = []
            current_lineage = i.taxid.tax_name
            current_lineage_id = i.taxid.ncbi_taxid
            parent = i.taxid.parent_taxid
            while current_lineage != 'root':
                lineage_list.append(current_lineage_id)
                new_query = Taxa.get(Taxa.ncbi_taxid == parent)

                current_lineage = new_query.tax_name
                current_lineage_id = new_query.ncbi_taxid
                parent = new_query.parent_taxid
            yield (i.accession, lineage_list)
    db.close()


def lineage_name(acc_number_list, db_name, table):
    """given a list of acession numbers, yield the accession number and their
    associated lineage as tuples

    Arguments:
    acc_number_list -- a list of accession numbers
    db_name -- the path to the database to query
    table -- the table containing the accession numbers
    """
    database = pw.SqliteDatabase(db_name)
    db.initialize(database)
    db.connect()
    with db.atomic():
        query = table.select().where(table.accession << acc_number_list)
        for i in query:
            lineage_list = []
            current_lineage = i.taxid.tax_name
            parent = i.taxid.parent_taxid
            while current_lineage != 'root':
                print(current_lineage)
                lineage_list.append(current_lineage)
                new_query = Taxa.get(Taxa.ncbi_taxid == parent)
                current_lineage = new_query.tax_name
                parent = new_query.parent_taxid
            yield (i.accession, lineage_list)
    db.close()
