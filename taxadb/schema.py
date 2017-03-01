#!/usr/bin/env python
# -*- coding: utf-8 -*-

import peewee as pw

db = pw.Proxy()


class BaseModel(pw.Model):
    class Meta:
        database = db


class Taxa(BaseModel):
    """table Taxa. Each row is a taxon.

    Fields:
    ncbi_taxid -- the TaxID of the taxon (from nodes.dmp)
    parent_taxid -- the TaxID of the parent taxon (from nodes.dmp)
    tax_name -- the scientific name of the taxon (from names.dmp)
    lineage_level -- the level of lineage of the taxon (from nodes.dmp)
    """
    ncbi_taxid = pw.IntegerField(null=False, primary_key=True, unique=True)
    parent_taxid = pw.IntegerField(null=False)
    tax_name = pw.CharField()
    lineage_level = pw.CharField()


class Accession(BaseModel):
    """table Accession. Each row is a sequence from nucl_*.accession2taxid.gz. Each sequence has a taxid.

    Fields:
    primary -- the primary key
    taxid -- reference to a taxon in the table Taxa.
    accession -- the accession number of the sequence.
    """
    id = pw.PrimaryKeyField()
    taxid = pw.ForeignKeyField(Taxa, related_name='accession')
    accession = pw.CharField(null=False, unique=True)


class DatabaseFactory(object):
    """Databas factory to support multiple database type"""

    SUPPORTED_DBS = ['sqlite', 'postgres', 'mysql']

    def __init__(self, dbname=None, dbtype='sqlite', **kwargs):
        """

        :param dbname: Database name
        :type dbname: str
        :param dbtype: Database type, default 'sqlite'
        :type dbtype: str
        :param kwargs: Keyword arguments
        :type kwargs: dict
        """
        if dbtype not in DatabaseFactory.SUPPORTED_DBS:
            raise AttributeError("Database type '%s' not supported" % str(dbtype))
        if not dbname:
            raise AttributeError("A database name is required")
        self.dbtype = dbtype
        self.dbname = dbname
        self.args = kwargs

    def get_database(self):
        """
        Returns the correct database driver

        :return:
        """
        if self.dbtype == 'sqlite':
            return pw.SqliteDatabase(self.dbname)
        else:
            if 'username' not in self.args or 'password' not in self.args:
                raise AttributeError('[ERROR] --dbtype %s requires --username and --password.\n' % str(self.dbtype))
            if self.args['username'] is None or self.args['password'] is None:
                raise AttributeError('[ERROR] --dbtype %s requires --username and --password.\n' % str(self.dbtype))
            if 'hostname' not in self.args:
                self.args['hostname'] = 'localhost'
            if self.dbtype == 'mysql':
                if 'port' not in self.args:
                    self.args['port'] = 3306
                return pw.MySQLDatabase(self.dbname, user=self.args['username'], password=self.args['password'],
                                        host=self.args['hostname'], port=int(self.args['port']))
            elif self.dbtype == 'postgres':
                if 'port' not in self.args:
                    self.args['port'] = 5432
                return pw.PostgresqlDatabase(self.dbname, user=self.args['username'], password=self.args['password'],
                                             host=self.args['hostname'], port=int(self.args['port']))
