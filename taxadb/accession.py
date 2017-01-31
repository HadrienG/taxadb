#!/usr/bin/env python
# -*- coding: utf-8 -*-

from taxadb.schema import *
import sys


def taxid(acc_number_list, db_name, table):
    """given a list of accession numbers, yield
    the accession number and their associated taxids as tuples

    Arguments:
    acc_number_list -- a list of accession numbers
    db_name -- the path to the database to query
    table -- the table containing the accession numbers
    """
    database = pw.SqliteDatabase(db_name)
    db.initialize(database)
    db.connect()
    _check_table_exists(table)
    with db.atomic():
        query = table.select().where(table.accession << acc_number_list)
        for i in query:
            try:
                yield (i.accession, i.taxid.ncbi_taxid)
            except Taxa.DoesNotExist:
                _unmapped_taxid(i.accession)
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
    _check_table_exists(table)
    with db.atomic():
        query = table.select().where(table.accession << acc_number_list)
        for i in query:
            try:
                yield (i.accession, i.taxid.tax_name)
            except Taxa.DoesNotExist:
                _unmapped_taxid(i.accession)
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
    _check_table_exists(table)
    with db.atomic():
        query = table.select().where(table.accession << acc_number_list)
        for i in query:
            try:
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
            except Taxa.DoesNotExist:
                _unmapped_taxid(i.accession)
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
    _check_table_exists(table)
    with db.atomic():
        query = table.select().where(table.accession << acc_number_list)
        for i in query:
            try:
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
            except Taxa.DoesNotExist:
                _unmapped_taxid(i.accession)
    db.close()


def _check_table_exists(table):
    """Check a table exists in the database

    Arguments:
    table -- table name
    Throws `SystemExit` if table does not exist
    """
    if not table.table_exists():
        print("Table %s does not exist" % (
            str(table._meta.db_table)), file=sys.stderr)
        sys.exit(1)
    return True


def _unmapped_taxid(acc, exit=False):
    """Prints an error message on stderr an accession number is not mapped
    with a taxid

    Source ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/README
    >> If for some reason the source organism cannot be mapped to the taxonomy
    database,
    the column will contain 0.<<

    Arguments:
    acc -- Accession number not mapped with taxid
    exit -- Exit with code 1, default False
    """
    print("No taxid mapped for accession %s" % str(acc), file=sys.stderr)
    if exit:
        sys.exit(1)
    return True
