#!/usr/bin/env python
# -*- coding: utf-8 -*-

from taxadb.schema import Taxa, DatabaseFactory, db


class Taxid(object):
    """Main class for querying taxid"""

    def __init__(self, dbtype=None, dbname=None, **kwargs):
        self.db = db
        self.dbname = dbname
        self.database = DatabaseFactory(dbname=dbname, dbtype=dbtype, **kwargs).get_database()
        self.db.initialize(self.database)
        self.db.connect()

    def __del__(self):
        self.db.close()

    def sci_name(self, taxid):
        """given a taxid, return its associated scientific name

        You can access data from several database type (sqlite3/mysql/postgresql)
        Arguments:
        taxid -- a taxid (int)
        Returns:
        name -- scientific name (str) or None if taxid not found
        """
        try:
            name = Taxa.get(Taxa.ncbi_taxid == taxid).tax_name
            return name
        except Taxa.DoesNotExist as err:
            return None

    def lineage_id(self, taxid, reverse=False):
        """given a taxid, return its associated lineage (in the form of a list
        of taxids, each parents of each others)

        Arguments:
        taxid -- a taxid (int)
        reverse -- Inverted lineage, from top to bottom taxonomy hierarchy
        Returns:
        lineage_list -- associated lineage id with taxid (list) or None if taxid not found
        """
        try:
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
            if reverse is True:
                lineage_list.reverse()
            return lineage_list
        except Taxa.DoesNotExist as err:
            return None

    def lineage_name(slef, taxid, reverse=False):
        """given a taxid, return its associated lineage

        Arguments:
        taxid -- a taxid (int)
        reverse -- Inverted lineage, from top to bottom taxonomy hierarchy
        Returns:
        lineage_name -- associated lineage name with taxid (list) or None if taxid not found
        """
        try:
            lineage_list = []
            current_lineage = Taxa.get(Taxa.ncbi_taxid == taxid).tax_name
            parent = Taxa.get(Taxa.ncbi_taxid == taxid).parent_taxid
            while current_lineage != 'root':
                lineage_list.append(current_lineage)
                new_query = Taxa.get(Taxa.ncbi_taxid == parent)

                current_lineage = new_query.tax_name
                parent = new_query.parent_taxid
            if reverse is True:
                lineage_list.reverse()
            return lineage_list
        except Taxa.DoesNotExist as err:
            return None
